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
    # Examples: "1.1 - Amaç", "1.4.1.A - Title", "1.4.1- Title"
    # Must have at least one dot to be a section header (prevents matching 1-, 2-, 3-)
    SECTION_PATTERN = re.compile(
        r'^[\s]*(\d+\.\d+(?:\.\d+)*(?:\.[A-Z])?)[\s]*[-–][\s]*([^\n]+)',
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
        parts = section_id.split('.')
        
        # Handle letter suffixes like "1.4.1.A"
        if parts and parts[-1].isalpha():
            # Parent would be "1.4.1"
            potential_parent = '.'.join(parts[:-1])
            if potential_parent in existing_ids:
                return potential_parent
        
        # Try removing last numeric part
        for i in range(len(parts) - 1, 0, -1):
            potential_parent = '.'.join(parts[:i])
            if potential_parent in existing_ids:
                return potential_parent
        
        return None
    
    def _sort_key(self, section_id: str) -> tuple:
        """Generate sort key for proper ordering."""
        parts = []
        for part in section_id.split('.'):
            if part.isdigit():
                parts.append((0, int(part), ''))
            elif part.isalpha():
                parts.append((1, 0, part))
            else:
                # Mixed like "1A" - shouldn't happen in SUT but handle it
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
    sample_text = """1.4.1 - Birinci basamak sağlık hizmeti sunucuları
1.4.1.A - Birinci basamak resmi sağlık hizmeti sunucuları
1) Bünyesinde birinci basamak sağlık kuruluşu bulunan ilçe sağlık müdürlüğü
2) Toplum sağlığı merkezi (TSM)
3) Aile sağlığı merkezi (ASM)
4) Halk sağlığı laboratuvarı (L1ve L2)
5) Kurum tabipliği
6) 112 Acil sağlık hizmeti birimleri
7) Üniversiteler bünyesindeki mediko-sosyal birimler
8) Türk Silahlı Kuvvetlerinin birinci basamak sağlık üniteleri
9) Belediyelere ait poliklinikler
10) Birinci basamak ayaktan ve yataklı teşhis, tedavi ve rehabilitasyon hizmeti sunan sağlık hizmeti sunucuları entegre ilçe devlet hastaneleridir (E2 ve E3)
1.4.1.B - Birinci basamak özel sağlık hizmeti sunucuları
1) Evde bakım merkezleri veya birimler
2) İşyeri sağlık ve güvenlik hizmeti sunulan birimler
3) Özel poliklinikler
4) Ağız ve diş sağlığı hizmeti veren özel sağlık kuruluşları
5) Eczaneler
3.3.10 - Sakral sinir stimülatörleri
(1) Sakral sinir stimülatörlerinin anal inkontinansta kullanımı:
a) Eğitim kliniği olan üçüncü basamak resmi sağlık hizmeti sunucularında bedeli karşılanır.
b) Genel endikasyonlar;
1) 75 yaşın altındaki hastalarda kullanılmalıdır,
2) Hasta cihaz hakkında bilgilendirilmelidir.
(2) Sakral sinir stimülatörlerinin üriner inkontinansta kullanımı:
a) Üroloji kliniklerince oluşturulacak konsey kararı gerekir.
b) Genel Endikasyonlar;
1) 75 yaşın altındaki hastalarda kullanılmalıdır,
2) Psikiyatri konsültasyonu gereklidir."""

    result = parse_sut_document(sample_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    result = parse_sut_file("doc.pdf", "sut_out.json")
