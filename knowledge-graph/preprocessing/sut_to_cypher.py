"""
SUT JSON to Neo4j Cypher Generator

This script parses the SUT (Sağlık Uygulama Tebliği) JSON document
and generates Cypher queries to create a knowledge graph in Neo4j.

Node Types:
- Document: Root document node
- Section: Top-level sections (1.1, 1.2, etc.)
- Subsection: Nested sections (can be multiple levels deep)
- Paragraph: Text paragraphs within sections
- Item: List items (can be strings or structured objects)
- SubItem: Nested items within items
- Amendment: Legal amendments/changes to sections

Relationships:
- HAS_SECTION: Document -> Section
- HAS_SUBSECTION: Section/Subsection -> Subsection
- HAS_PARAGRAPH: Section/Subsection -> Paragraph
- HAS_ITEM: Section/Subsection/Paragraph -> Item
- HAS_SUBITEM: Item -> SubItem
- HAS_AMENDMENT: Section/Subsection -> Amendment
- NEXT_SECTION: Section -> Section (ordering)
- NEXT_PARAGRAPH: Paragraph -> Paragraph (ordering)
- NEXT_ITEM: Item -> Item (ordering)
"""

import json
from typing import Any
from pathlib import Path


class CypherGenerator:
    def __init__(self):
        self.queries = []
        self.node_counter = 0
        
    def _get_unique_id(self, prefix: str = "node") -> str:
        """Generate a unique node identifier."""
        self.node_counter += 1
        return f"{prefix}_{self.node_counter}"
    
    def _escape_string(self, text: str) -> str:
        """Escape special characters for Cypher strings."""
        if text is None:
            return ""
        # Escape backslashes first, then quotes, then newlines
        text = text.replace("\\", "\\\\")
        text = text.replace("'", "\\'")
        text = text.replace('"', '\\"')
        text = text.replace("\n", "\\n")
        text = text.replace("\r", "\\r")
        return text
    
    def _create_node(self, label: str, properties: dict, var_name: str) -> str:
        """Generate a CREATE statement for a node."""
        props = []
        for key, value in properties.items():
            if value is not None:
                if isinstance(value, str):
                    props.append(f"{key}: '{self._escape_string(value)}'")
                elif isinstance(value, (int, float)):
                    props.append(f"{key}: {value}")
                elif isinstance(value, bool):
                    props.append(f"{key}: {'true' if value else 'false'}")
        
        props_str = ", ".join(props)
        return f"CREATE ({var_name}:{label} {{{props_str}}})"
    
    def _create_relationship(self, from_var: str, to_var: str, rel_type: str, properties: dict = None) -> str:
        """Generate a CREATE statement for a relationship."""
        if properties:
            props = []
            for key, value in properties.items():
                if value is not None:
                    if isinstance(value, str):
                        props.append(f"{key}: '{self._escape_string(value)}'")
                    else:
                        props.append(f"{key}: {value}")
            props_str = " {" + ", ".join(props) + "}"
        else:
            props_str = ""
        
        return f"CREATE ({from_var})-[:{rel_type}{props_str}]->({to_var})"
    
    def process_document(self, doc: dict) -> list[str]:
        """Process the entire document and generate Cypher queries."""
        self.queries = []
        self.node_counter = 0
        
        # Create document node
        doc_var = self._get_unique_id("doc")
        doc_node = self._create_node("Document", {
            "document_type": doc.get("document_type"),
            "title": doc.get("title")
        }, doc_var)
        self.queries.append(doc_node)
        
        # Process sections
        sections = doc.get("sections", [])
        prev_section_var = None
        
        for idx, section in enumerate(sections):
            section_var = self._process_section(section, doc_var, "HAS_SECTION", idx)
            
            # Create ordering relationship between sections
            if prev_section_var:
                self.queries.append(
                    self._create_relationship(prev_section_var, section_var, "NEXT_SECTION")
                )
            prev_section_var = section_var
        
        return self.queries
    
    def _process_section(self, section: dict, parent_var: str, rel_type: str, order: int) -> str:
        """Process a section or subsection node."""
        section_var = self._get_unique_id("sec")
        
        # Determine if this is a top-level section or subsection
        label = "Section" if rel_type == "HAS_SECTION" else "Subsection"
        
        # Create section node
        section_node = self._create_node(label, {
            "id": section.get("id"),
            "title": section.get("title"),
            "content": section.get("content")  # Some sections have direct content
        }, section_var)
        self.queries.append(section_node)
        
        # Create relationship to parent
        self.queries.append(
            self._create_relationship(parent_var, section_var, rel_type, {"order": order})
        )
        
        # Process paragraphs
        paragraphs = section.get("paragraphs", [])
        prev_para_var = None
        for para_idx, paragraph in enumerate(paragraphs):
            para_var = self._process_paragraph(paragraph, section_var, para_idx)
            if prev_para_var:
                self.queries.append(
                    self._create_relationship(prev_para_var, para_var, "NEXT_PARAGRAPH")
                )
            prev_para_var = para_var
        
        # Process direct items (items directly under section, not under paragraph)
        items = section.get("items", [])
        prev_item_var = None
        for item_idx, item in enumerate(items):
            item_var = self._process_item(item, section_var, "HAS_ITEM", item_idx)
            if prev_item_var:
                self.queries.append(
                    self._create_relationship(prev_item_var, item_var, "NEXT_ITEM")
                )
            prev_item_var = item_var
        
        # Process amendments
        amendments = section.get("amendments", [])
        for amend_idx, amendment in enumerate(amendments):
            self._process_amendment(amendment, section_var, amend_idx)
        
        # Process nested subsections
        subsections = section.get("subsections", [])
        prev_subsec_var = None
        for subsec_idx, subsection in enumerate(subsections):
            subsec_var = self._process_section(subsection, section_var, "HAS_SUBSECTION", subsec_idx)
            if prev_subsec_var:
                self.queries.append(
                    self._create_relationship(prev_subsec_var, subsec_var, "NEXT_SUBSECTION")
                )
            prev_subsec_var = subsec_var
        
        return section_var
    
    def _process_paragraph(self, paragraph: dict, parent_var: str, order: int) -> str:
        """Process a paragraph node."""
        para_var = self._get_unique_id("para")
        
        para_node = self._create_node("Paragraph", {
            "id": paragraph.get("id"),
            "content": paragraph.get("content")
        }, para_var)
        self.queries.append(para_node)
        
        # Create relationship to parent
        self.queries.append(
            self._create_relationship(parent_var, para_var, "HAS_PARAGRAPH", {"order": order})
        )
        
        # Process items within paragraph
        items = paragraph.get("items", [])
        prev_item_var = None
        for item_idx, item in enumerate(items):
            item_var = self._process_item(item, para_var, "HAS_ITEM", item_idx)
            if prev_item_var:
                self.queries.append(
                    self._create_relationship(prev_item_var, item_var, "NEXT_ITEM")
                )
            prev_item_var = item_var
        
        return para_var
    
    def _process_item(self, item: Any, parent_var: str, rel_type: str, order: int) -> str:
        """Process an item node. Items can be strings or structured objects."""
        item_var = self._get_unique_id("item")
        
        if isinstance(item, str):
            # Simple string item
            item_node = self._create_node("Item", {
                "content": item
            }, item_var)
        else:
            # Structured item with id and content
            item_node = self._create_node("Item", {
                "id": item.get("id"),
                "content": item.get("content")
            }, item_var)
        
        self.queries.append(item_node)
        
        # Create relationship to parent
        self.queries.append(
            self._create_relationship(parent_var, item_var, rel_type, {"order": order})
        )
        
        # Process sub_items if present
        if isinstance(item, dict):
            sub_items = item.get("sub_items", [])
            prev_subitem_var = None
            for subitem_idx, sub_item in enumerate(sub_items):
                subitem_var = self._process_subitem(sub_item, item_var, subitem_idx)
                if prev_subitem_var:
                    self.queries.append(
                        self._create_relationship(prev_subitem_var, subitem_var, "NEXT_SUBITEM")
                    )
                prev_subitem_var = subitem_var
        
        return item_var
    
    def _process_subitem(self, sub_item: dict, parent_var: str, order: int) -> str:
        """Process a sub-item node."""
        subitem_var = self._get_unique_id("subitem")
        
        subitem_node = self._create_node("SubItem", {
            "id": sub_item.get("id"),
            "content": sub_item.get("content")
        }, subitem_var)
        self.queries.append(subitem_node)
        
        # Create relationship to parent
        self.queries.append(
            self._create_relationship(parent_var, subitem_var, "HAS_SUBITEM", {"order": order})
        )
        
        return subitem_var
    
    def _process_amendment(self, amendment: str, parent_var: str, order: int) -> str:
        """Process an amendment node."""
        amend_var = self._get_unique_id("amend")
        
        amend_node = self._create_node("Amendment", {
            "content": amendment
        }, amend_var)
        self.queries.append(amend_node)
        
        # Create relationship to parent
        self.queries.append(
            self._create_relationship(parent_var, amend_var, "HAS_AMENDMENT", {"order": order})
        )
        
        return amend_var


def generate_cypher_from_file(input_path: str, output_path: str = None, batch_size: int = 100):
    """
    Generate Cypher queries from a SUT JSON file.
    
    Args:
        input_path: Path to the input JSON file
        output_path: Path to save the Cypher queries (optional)
        batch_size: Number of queries per batch/transaction (for better performance)
    
    Returns:
        List of Cypher queries
    """
    # Load JSON
    with open(input_path, 'r', encoding='utf-8') as f:
        doc = json.load(f)
    
    # Generate queries
    generator = CypherGenerator()
    queries = generator.process_document(doc)
    
    # Save to file if output path provided
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write schema constraints first
            f.write("// ============================================\n")
            f.write("// Schema Constraints and Indexes\n")
            f.write("// ============================================\n\n")
            f.write("// Create constraints for unique identifiers\n")
            f.write("CREATE CONSTRAINT document_title IF NOT EXISTS FOR (d:Document) REQUIRE d.title IS UNIQUE;\n")
            f.write("CREATE CONSTRAINT section_id IF NOT EXISTS FOR (s:Section) REQUIRE s.id IS UNIQUE;\n")
            f.write("CREATE CONSTRAINT subsection_id IF NOT EXISTS FOR (s:Subsection) REQUIRE s.id IS UNIQUE;\n")
            f.write("\n// Create indexes for faster lookups\n")
            f.write("CREATE INDEX section_title IF NOT EXISTS FOR (s:Section) ON (s.title);\n")
            f.write("CREATE INDEX subsection_title IF NOT EXISTS FOR (s:Subsection) ON (s.title);\n")
            f.write("CREATE INDEX paragraph_content IF NOT EXISTS FOR (p:Paragraph) ON (p.content);\n")
            f.write("CREATE INDEX item_content IF NOT EXISTS FOR (i:Item) ON (i.content);\n")
            f.write("\n")
            
            # Write queries in batches for better transaction management
            f.write("// ============================================\n")
            f.write("// Data Creation Queries\n")
            f.write("// ============================================\n\n")
            
            for i in range(0, len(queries), batch_size):
                batch = queries[i:i + batch_size]
                f.write(f"// Batch {i // batch_size + 1}\n")
                for query in batch:
                    f.write(query + ";\n")
                f.write("\n")
    
    return queries


def generate_single_transaction_cypher(input_path: str, output_path: str = None):
    """
    Generate a single large Cypher transaction (useful for smaller documents).
    Uses WITH clauses to chain operations.
    """
    # Load JSON
    with open(input_path, 'r', encoding='utf-8') as f:
        doc = json.load(f)
    
    generator = CypherGenerator()
    queries = generator.process_document(doc)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("// Single transaction Cypher script\n")
            f.write("// Run all queries in a single transaction\n\n")
            
            # Join all queries
            full_query = "\n".join(queries)
            f.write(full_query)
            f.write(";\n")
    
    return queries


if __name__ == "__main__":
    import sys
    
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./sut_out.json"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "./sut_cypher_queries.cypher"
    
    print(f"Processing: {input_file}")
    queries = generate_cypher_from_file(input_file, output_file)
    print(f"Generated {len(queries)} Cypher queries")
    print(f"Output saved to: {output_file}")
    
    # Also generate statistics
    print("\n--- Statistics ---")
    node_types = {}
    rel_types = {}
    for q in queries:
        if q.startswith("CREATE ("):
            # Extract node type
            label = q.split(":")[1].split(" ")[0]
            node_types[label] = node_types.get(label, 0) + 1
        elif "]->" in q:
            # Extract relationship type
            rel = q.split("[:")[-1].split("]")[0].split(" ")[0]
            rel_types[rel] = rel_types.get(rel, 0) + 1
    
    print("\nNode counts:")
    for label, count in sorted(node_types.items()):
        print(f"  {label}: {count}")
    
    print("\nRelationship counts:")
    for rel, count in sorted(rel_types.items()):
        print(f"  {rel}: {count}")
