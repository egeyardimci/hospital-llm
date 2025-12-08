#!/usr/bin/env python3
"""
Remove strikethrough (crossed out) text from a Word document.
Preserves all other formatting and document structure.
"""

import sys
import os
import zipfile
import shutil
from xml.etree import ElementTree as ET

# Word XML namespaces
NAMESPACES = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
}

# Register namespaces to preserve them in output
for prefix, uri in NAMESPACES.items():
    ET.register_namespace(prefix, uri)

# Register additional namespaces commonly found in Word docs
ADDITIONAL_NS = {
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
    'w15': 'http://schemas.microsoft.com/office/word/2012/wordml',
    'w16se': 'http://schemas.microsoft.com/office/word/2015/wordml/symex',
    'w16cid': 'http://schemas.microsoft.com/office/word/2016/wordml/cid',
    'w16': 'http://schemas.microsoft.com/office/word/2018/wordml',
    'w16cex': 'http://schemas.microsoft.com/office/word/2018/wordml/cex',
    'w16sdtdh': 'http://schemas.microsoft.com/office/word/2020/wordml/sdtdatahash',
    'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
    'wpg': 'http://schemas.microsoft.com/office/word/2010/wordprocessingGroup',
    'wpc': 'http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'v': 'urn:schemas-microsoft-com:vml',
    'o': 'urn:schemas-microsoft-com:office:office',
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'wne': 'http://schemas.microsoft.com/office/word/2006/wordml',
    'sl': 'http://schemas.openxmlformats.org/schemaLibrary/2006/main',
    'w16du': 'http://schemas.microsoft.com/office/word/2023/wordml/word16du',
}
for prefix, uri in ADDITIONAL_NS.items():
    ET.register_namespace(prefix, uri)


def has_strikethrough(element):
    """Check if a run (w:r) element has strikethrough formatting."""
    # Look for w:rPr (run properties) containing w:strike
    rPr = element.find('w:rPr', NAMESPACES)
    if rPr is not None:
        strike = rPr.find('w:strike', NAMESPACES)
        if strike is not None:
            return True
        # Also check for double strikethrough
        dstrike = rPr.find('w:dstrike', NAMESPACES)
        if dstrike is not None:
            return True
    return False


def remove_strikethrough_from_paragraph(p_element):
    """Remove all strikethrough runs from a paragraph, preserving structure."""
    runs_to_remove = []
    
    # Find all runs with strikethrough
    for run in p_element.findall('.//w:r', NAMESPACES):
        if has_strikethrough(run):
            runs_to_remove.append(run)
    
    # Remove them
    for run in runs_to_remove:
        parent = find_parent(p_element, run)
        if parent is not None:
            parent.remove(run)
    
    # Also clean strikethrough from paragraph properties (w:pPr/w:rPr)
    pPr = p_element.find('w:pPr', NAMESPACES)
    if pPr is not None:
        rPr = pPr.find('w:rPr', NAMESPACES)
        if rPr is not None:
            strike = rPr.find('w:strike', NAMESPACES)
            if strike is not None:
                rPr.remove(strike)
            dstrike = rPr.find('w:dstrike', NAMESPACES)
            if dstrike is not None:
                rPr.remove(dstrike)
    
    return len(runs_to_remove)


def find_parent(root, target):
    """Find the parent of target element within root."""
    for parent in root.iter():
        for child in parent:
            if child is target:
                return parent
    return None


def is_paragraph_empty(p_element):
    """Check if paragraph has no text content after cleanup."""
    # Check for any text in w:t elements
    for t in p_element.findall('.//w:t', NAMESPACES):
        if t.text and t.text.strip():
            return False
    return True


def process_document(input_path, output_path):
    """Process a Word document to remove all strikethrough text."""
    
    # Create temp directory
    temp_dir = 'temp_docx_processing'
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    try:
        # Extract docx
        with zipfile.ZipFile(input_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Process document.xml
        doc_xml_path = os.path.join(temp_dir, 'word', 'document.xml')
        
        # Read and preserve the original XML declaration and processing instructions
        with open(doc_xml_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Parse with ElementTree
        tree = ET.parse(doc_xml_path)
        root = tree.getroot()
        
        total_removed = 0
        empty_paragraphs = []
        
        # Find all paragraphs
        for p in root.findall('.//w:p', NAMESPACES):
            removed = remove_strikethrough_from_paragraph(p)
            total_removed += removed
            
            # Track empty paragraphs for optional removal
            if removed > 0 and is_paragraph_empty(p):
                empty_paragraphs.append(p)
        
        # Remove completely empty paragraphs that only had strikethrough content
        removed_empty = 0
        for p in empty_paragraphs:
            parent = find_parent(root, p)
            if parent is not None:
                parent.remove(p)
                removed_empty += 1
        
        print(f"Removed {removed_empty} empty paragraphs")
        
        print(f"Removed {total_removed} strikethrough runs")
        print(f"Found {len(empty_paragraphs)} paragraphs that became empty")
        
        # Write back
        tree.write(doc_xml_path, encoding='UTF-8', xml_declaration=True)
        
        # Repackage docx
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for foldername, subfolders, filenames in os.walk(temp_dir):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)
        
        print(f"Output saved to: {output_path}")
        
    finally:
        # Cleanup
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python remove_strikethrough.py input.docx output.docx")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    process_document(input_file, output_file)
