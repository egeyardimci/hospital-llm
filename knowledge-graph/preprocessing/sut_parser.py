"""
Improved Parser for Turkish Health Regulation Documents (SUT - Sağlık Uygulama Tebliği)
Converts hierarchical regulation text into structured JSON with proper nesting.
"""

import re
import json
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SubItem:
    """Represents nested items like a), b), 1), 2)"""
    id: str  # e.g., "a", "b", "1", "2"
    content: str
    sub_items: list["SubItem"] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        result = {"id": self.id, "content": self.content}
        if self.sub_items:
            result["sub_items"] = [s.to_dict() for s in self.sub_items]
        return result


@dataclass
class Paragraph:
    """Represents a paragraph like (1), (2) with nested a), b), 1), 2)"""
    id: str  # e.g., "1", "2"
    content: Optional[str] = None
    items: list[SubItem] = field(default_factory=list)
    amendments: list[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        result = {"id": self.id}
        if self.content:
            result["content"] = self.content
        if self.items:
            result["items"] = [i.to_dict() for i in self.items]
        if self.amendments:
            result["amendments"] = self.amendments
        return result


@dataclass
class Section:
    """Represents a section/article in the regulation."""
    id: str
    title: str
    content: Optional[str] = None
    items: list[str] = field(default_factory=list)  # Direct 1) 2) 3) items
    paragraphs: list[Paragraph] = field(default_factory=list)
    amendments: list[str] = field(default_factory=list)
    subsections: list["Section"] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert to dictionary, excluding empty fields."""
        result = {"id": self.id, "title": self.title}
        if self.content:
            result["content"] = self.content
        if self.items:
            result["items"] = self.items
        if self.paragraphs:
            result["paragraphs"] = [p.to_dict() for p in self.paragraphs]
        if self.amendments:
            result["amendments"] = self.amendments
        if self.subsections:
            result["subsections"] = [s.to_dict() for s in self.subsections]
        return result


class SUTParser:
    """Improved parser for SUT regulation documents."""
    
    # Pattern for section headers - handles various formats
    # Examples: "1.1 - Amaç", "1.4.1.A - Title", "2.4.3-A - Title", "1.5.1.A-1 - Title", "4.2.27.D.1 - Title"
    # Must have at least one dot to be a section header (prevents matching 1-, 2-, 3-)
    # Requires section to be at start of line (after optional whitespace)
    SECTION_PATTERN = re.compile(
        r'^[\s]*(\d+\.\d+(?:\.\d+)*(?:[\.-][A-ZÇĞİÖŞÜ])?(?:[.-]\d+)?)[\s]*[-–][\s]*([^\n]+)',
        re.MULTILINE
    )
    
    # Pattern for numbered list items: "1) Item" or "  1) Item"
    LIST_ITEM_PATTERN = re.compile(r'^[\s]*(\d+)\)[\s]+(.+)$')
    
    # Pattern for amendment notes
    AMENDMENT_PATTERN = re.compile(
        r'\((?:Değişik|Ek|Mülga):\s*RG-\s*[\d/]+[-–]\s*\d+/?\s*\d*\s*md\.?\s*(?:Yürürlük:\s*[\d/]+)?\)',
        re.IGNORECASE
    )
    
    # Patterns for nested content
    PARAGRAPH_MARKER = re.compile(r'^\((\d+)\)\s*(.*)$')  # (1), (2)
    LETTER_ITEM = re.compile(r'^([a-zçğıöşü])\)\s*(.+)$')  # a), b), ç)
    NUMBER_ITEM = re.compile(r'^(\d+)\)\s*(.+)$')  # 1), 2)
    SUB_NUMBER_ITEM = re.compile(r'^(\d+)-\s*(.+)$')  # 1-, 2-
    
    def __init__(self, text: str):
        self.text = self._normalize_text(text)
        
    def _normalize_text(self, text: str) -> str:
        """Normalize whitespace and line endings."""
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        lines = text.split('\n')
        normalized_lines = []
        for line in lines:
            normalized_lines.append(re.sub(r'  +', ' ', line))
        return '\n'.join(normalized_lines)
    
    def parse(self) -> dict:
        """Parse the document and return structured JSON."""
        sections = self._find_all_sections()
        hierarchy = self._build_hierarchy(sections)
        
        return {
            "document_type": "SUT",
            "title": "Sağlık Uygulama Tebliği",
            "sections": [s.to_dict() for s in hierarchy]
        }
    
    def _find_all_sections(self) -> list[dict]:
        """Find all sections with their positions and content boundaries."""
        sections = []
        
        for match in self.SECTION_PATTERN.finditer(self.text):
            section_id = match.group(1).strip()
            title = match.group(2).strip()
            start_pos = match.end()
            header_start = match.start()
            
            sections.append({
                'id': section_id,
                'title': title,
                'header_start': header_start,
                'content_start': start_pos
            })
        
        for i, section in enumerate(sections):
            if i + 1 < len(sections):
                section['content_end'] = sections[i + 1]['header_start']
            else:
                section['content_end'] = len(self.text)
        
        return sections
    
    def _parse_nested_content(self, text: str) -> tuple[Optional[str], list[Paragraph], list[str], list[str]]:
        """Parse content with nested structure: (1) a) b) 1) 2) or direct 1) 2) 3) items"""
        
        # Extract amendments
        amendments = self.AMENDMENT_PATTERN.findall(text)
        clean_text = self.AMENDMENT_PATTERN.sub('', text).strip()
        
        paragraphs = []
        direct_items = []  # For standalone 1) 2) 3) without (1) wrapper
        intro_content = []
        
        lines = clean_text.split('\n')
        current_paragraph = None
        current_letter_item = None
        pending_text = []
        has_paragraph_markers = bool(self.PARAGRAPH_MARKER.search(clean_text))
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            i += 1
            
            if not line:
                continue
            
            # Check for paragraph marker (1), (2)
            para_match = self.PARAGRAPH_MARKER.match(line)
            if para_match:
                # Save previous paragraph
                if current_paragraph:
                    if pending_text and current_letter_item:
                        current_letter_item.content += ' ' + ' '.join(pending_text)
                        pending_text = []
                    paragraphs.append(current_paragraph)
                
                para_id = para_match.group(1)
                para_content = para_match.group(2).strip() if para_match.group(2) else None
                current_paragraph = Paragraph(id=para_id, content=para_content)
                current_letter_item = None
                pending_text = []
                continue
            
            # Check for letter item a), b), ç)
            letter_match = self.LETTER_ITEM.match(line)
            if letter_match and current_paragraph:
                if pending_text and current_letter_item:
                    current_letter_item.content += ' ' + ' '.join(pending_text)
                    pending_text = []
                
                letter_id = letter_match.group(1)
                letter_content = letter_match.group(2).strip()
                current_letter_item = SubItem(id=letter_id, content=letter_content)
                current_paragraph.items.append(current_letter_item)
                continue
            
            # Check for number item 1), 2)
            number_match = self.NUMBER_ITEM.match(line)
            if number_match:
                # If we have a letter item, add as sub-item
                if current_letter_item:
                    if pending_text:
                        current_letter_item.content += ' ' + ' '.join(pending_text)
                        pending_text = []
                    
                    num_id = number_match.group(1)
                    num_content = number_match.group(2).strip()
                    current_letter_item.sub_items.append(SubItem(id=num_id, content=num_content))
                # If no paragraph markers in document, treat as direct item
                elif not has_paragraph_markers:
                    num_id = number_match.group(1)
                    num_content = number_match.group(2).strip()
                    direct_items.append(f"{num_content}")
                continue
            
            # Check for sub-number item 1-, 2-
            sub_num_match = self.SUB_NUMBER_ITEM.match(line)
            if sub_num_match and current_letter_item and current_letter_item.sub_items:
                last_sub = current_letter_item.sub_items[-1]
                sub_id = sub_num_match.group(1)
                sub_content = sub_num_match.group(2).strip()
                last_sub.sub_items.append(SubItem(id=sub_id, content=sub_content))
                continue
            
            # Regular text - append to appropriate place
            if current_letter_item:
                pending_text.append(line)
            elif current_paragraph:
                if current_paragraph.content:
                    current_paragraph.content += ' ' + line
                else:
                    current_paragraph.content = line
            else:
                intro_content.append(line)
        
        # Save last paragraph
        if current_paragraph:
            if pending_text and current_letter_item:
                current_letter_item.content += ' ' + ' '.join(pending_text)
            paragraphs.append(current_paragraph)
        
        content = ' '.join(intro_content) if intro_content else None
        return content, paragraphs, amendments, direct_items
    
    def _get_parent_id(self, section_id: str, existing_ids: set[str]) -> Optional[str]:
        """Find the parent section ID."""
        # Handle "4.2.27.D.1" -> parent is "4.2.27.D"
        letter_dot_num_match = re.match(r'^(.+\.[A-ZÇĞİÖŞÜ])\.\d+$', section_id)
        if letter_dot_num_match:
            potential_parent = letter_dot_num_match.group(1)
            if potential_parent in existing_ids:
                return potential_parent
        
        # Handle "1.5.1.A-1" -> parent is "1.5.1.A"
        letter_dash_num_match = re.match(r'^(.+\.[A-ZÇĞİÖŞÜ])-\d+$', section_id)
        if letter_dash_num_match:
            potential_parent = letter_dash_num_match.group(1)
            if potential_parent in existing_ids:
                return potential_parent
        
        # Handle "2.4.3-A" -> parent is "2.4.3"
        dash_letter_match = re.match(r'^(.+)-[A-ZÇĞİÖŞÜ]$', section_id)
        if dash_letter_match:
            potential_parent = dash_letter_match.group(1)
            if potential_parent in existing_ids:
                return potential_parent
        
        parts = section_id.split('.')
        
        # Handle letter suffixes like "1.4.1.A"
        if parts and parts[-1].isalpha():
            potential_parent = '.'.join(parts[:-1])
            if potential_parent in existing_ids:
                return potential_parent
        
        # Try removing last numeric part
        for i in range(len(parts) - 1, 0, -1):
            potential_parent = '.'.join(parts[:i])
            if potential_parent in existing_ids:
                return potential_parent
        
        return None
    
    # Turkish alphabet order for sorting
    TURKISH_LETTER_ORDER = 'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ'
    
    def _sort_key(self, section_id: str) -> tuple:
        """Generate sort key for proper ordering."""
        # Handle "4.2.27.D.1" format
        letter_dot_num_match = re.match(r'^(.+)\.([A-ZÇĞİÖŞÜ])\.(\d+)$', section_id)
        if letter_dot_num_match:
            base = letter_dot_num_match.group(1)
            letter = letter_dot_num_match.group(2)
            num = int(letter_dot_num_match.group(3))
            base_key = self._sort_key(base)
            letter_idx = self.TURKISH_LETTER_ORDER.index(letter) if letter in self.TURKISH_LETTER_ORDER else 0
            return base_key + ((1, letter_idx, letter), (0, num, ''))
        
        # Handle "1.5.1.A-1" format
        letter_dash_num_match = re.match(r'^(.+)\.([A-ZÇĞİÖŞÜ])-(\d+)$', section_id)
        if letter_dash_num_match:
            base = letter_dash_num_match.group(1)
            letter = letter_dash_num_match.group(2)
            num = int(letter_dash_num_match.group(3))
            base_key = self._sort_key(base)
            letter_idx = self.TURKISH_LETTER_ORDER.index(letter) if letter in self.TURKISH_LETTER_ORDER else 0
            return base_key + ((1, letter_idx, letter), (0, num, ''))
        
        # Handle dash-letter format: "2.4.3-A"
        dash_letter_match = re.match(r'^(.+)-([A-ZÇĞİÖŞÜ])$', section_id)
        if dash_letter_match:
            base = dash_letter_match.group(1)
            letter = dash_letter_match.group(2)
            base_key = self._sort_key(base)
            letter_idx = self.TURKISH_LETTER_ORDER.index(letter) if letter in self.TURKISH_LETTER_ORDER else 0
            return base_key + ((1, letter_idx, letter),)
        
        parts = []
        for part in section_id.split('.'):
            if part.isdigit():
                parts.append((0, int(part), ''))
            elif len(part) == 1 and part.upper() in self.TURKISH_LETTER_ORDER:
                idx = self.TURKISH_LETTER_ORDER.index(part.upper())
                parts.append((1, idx, part))
            elif part.isalpha():
                parts.append((1, 0, part))
            else:
                parts.append((2, 0, part))
        return tuple(parts)
    
    def _build_hierarchy(self, flat_sections: list[dict]) -> list[Section]:
        """Build nested hierarchy from flat section list."""
        if not flat_sections:
            return []
        
        # Create Section objects with content
        section_objs = {}
        for sec in flat_sections:
            raw_content = self.text[sec['content_start']:sec['content_end']].strip()
            content, paragraphs, amendments, direct_items = self._parse_nested_content(raw_content)
            
            section_objs[sec['id']] = Section(
                id=sec['id'],
                title=sec['title'],
                content=content,
                items=direct_items,
                paragraphs=paragraphs,
                amendments=amendments
            )
        
        all_ids = set(section_objs.keys())
        root_sections = []
        
        # Build parent-child relationships
        for sid, section in section_objs.items():
            parent_id = self._get_parent_id(sid, all_ids)
            if parent_id:
                section_objs[parent_id].subsections.append(section)
            else:
                root_sections.append(section)
        
        # Sort everything
        root_sections.sort(key=lambda s: self._sort_key(s.id))
        for section in section_objs.values():
            section.subsections.sort(key=lambda s: self._sort_key(s.id))
        
        return root_sections


def parse_sut_document(text: str) -> dict:
    """Main entry point for parsing SUT documents."""
    parser = SUTParser(text)
    return parser.parse()


def read_pdf(filepath: str) -> str:
    """Extract text from a PDF file."""
    import fitz  # PyMuPDF
    
    text = ""
    with fitz.open(filepath) as doc:
        for page in doc:
            text += page.get_text()
    return text


def parse_sut_file(filepath: str, output_path: Optional[str] = None) -> dict:
    """Parse a SUT document from file (PDF or text) and optionally save JSON output."""
    
    if filepath.lower().endswith('.pdf'):
        text = read_pdf(filepath)
    else:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    
    result = parse_sut_document(text)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"JSON output saved to: {output_path}")
    
    return result


# Test with sample
if __name__ == "__main__":
    sample_text = """4.2.27 - Trombosit düşüklüğü tedavisi
4.2.27.D - Eltrombopag, romiplostim kullanım ilkeleri
4.2.27.D.1 - İmmün trombositopenik purpura endikasyonunda eltrombopag kullanım ilkeleri
(1) Diğer tedavilere dirençli hastalarda tedaviye başlanır.
(2) Başlangıç dozu günde bir kez 50 mg'dır.
(3) Trombosit sayısının 250.000 üzerine çıkması durumunda tedavi sonlandırılır.
4.2.27.D.2 - Kazanılmış ağır aplastik anemi endikasyonunda eltrombopag kullanım ilkeleri
(1) Önceki tedaviye dirençli hastalarda tedaviye başlanır.
(2) 12 hafta sonunda trombosit sayısı 20.000'in altında ise ilaç kesilir.
(3) Hematoloji uzman hekimlerince reçete edilir.
4.2.27.D.3 - İmmün trombositopenik purpura endikasyonunda romiplostim kullanım ilkeleri
(1) Diğer tedavilere dirençli hastalarda tedaviye başlanır.
(2) Başlangıç dozu 1 mcg/kg'dir.
1.4.1 - Birinci basamak sağlık hizmeti sunucuları
1.4.1.A - Birinci basamak resmi sağlık hizmeti sunucuları
1) Toplum sağlığı merkezi (TSM)
2) Aile sağlığı merkezi (ASM)"""

    result = parse_sut_document(sample_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    result = parse_sut_file("doc-new.pdf", "sut_out.json")
