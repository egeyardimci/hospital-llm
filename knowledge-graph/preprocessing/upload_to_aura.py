"""
Upload SUT Knowledge Graph to Neo4j Aura

This script connects to Neo4j Aura and executes the generated Cypher queries.

Requirements:
    pip install neo4j

Usage:
    python upload_to_aura.py

You'll need your Aura connection details:
    - URI: neo4j+s://xxxxxxxx.databases.neo4j.io
    - Username: neo4j (default)
    - Password: (from Aura console)
"""

import json
import os
from neo4j import GraphDatabase


class AuraUploader:
    def __init__(self, uri: str, username: str, password: str):
        """Initialize connection to Neo4j Aura."""
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        print(f"Connected to {uri}")
    
    def close(self):
        """Close the database connection."""
        self.driver.close()
    
    def clear_database(self):
        """Clear all existing data, constraints, and indexes."""
        with self.driver.session() as session:
            # Drop all constraints first
            print("Dropping constraints...")
            constraints = session.run("SHOW CONSTRAINTS").data()
            for constraint in constraints:
                try:
                    session.run(f"DROP CONSTRAINT {constraint['name']}")
                except Exception as e:
                    print(f"  Could not drop constraint {constraint['name']}: {e}")
            
            # Drop all indexes
            print("Dropping indexes...")
            indexes = session.run("SHOW INDEXES").data()
            for index in indexes:
                if index['type'] != 'LOOKUP':  # Don't drop built-in lookup indexes
                    try:
                        session.run(f"DROP INDEX {index['name']}")
                    except Exception as e:
                        print(f"  Could not drop index {index['name']}: {e}")
            
            # Delete all nodes and relationships in batches (handles large graphs)
            print("Deleting all nodes and relationships...")
            deleted = 1
            total_deleted = 0
            while deleted > 0:
                result = session.run("""
                    MATCH (n)
                    WITH n LIMIT 10000
                    DETACH DELETE n
                    RETURN count(*) as deleted
                """)
                deleted = result.single()["deleted"]
                total_deleted += deleted
                if deleted > 0:
                    print(f"  Deleted {total_deleted} nodes so far...")
            
            print(f"Database cleared. Total nodes deleted: {total_deleted}")
    
    def create_constraints_and_indexes(self):
        """Create schema constraints and indexes."""
        constraints = [
            "CREATE CONSTRAINT document_title IF NOT EXISTS FOR (d:Document) REQUIRE d.title IS UNIQUE",
            "CREATE CONSTRAINT section_id IF NOT EXISTS FOR (s:Section) REQUIRE s.id IS UNIQUE",
            "CREATE CONSTRAINT subsection_id IF NOT EXISTS FOR (s:Subsection) REQUIRE s.id IS UNIQUE",
        ]
        
        indexes = [
            "CREATE INDEX section_title IF NOT EXISTS FOR (s:Section) ON (s.title)",
            "CREATE INDEX subsection_title IF NOT EXISTS FOR (s:Subsection) ON (s.title)",
            "CREATE INDEX paragraph_content IF NOT EXISTS FOR (p:Paragraph) ON (p.content)",
            "CREATE INDEX item_content IF NOT EXISTS FOR (i:Item) ON (i.content)",
        ]
        
        with self.driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                except Exception as e:
                    print(f"Constraint may already exist: {e}")
            
            for index in indexes:
                try:
                    session.run(index)
                except Exception as e:
                    print(f"Index may already exist: {e}")
        
        print("Schema constraints and indexes created.")
    
    def upload_from_json(self, json_path: str, batch_size: int = 500):
        """
        Upload directly from JSON file using optimized batch queries.
        This is more efficient than running individual CREATE statements.
        """
        with open(json_path, 'r', encoding='utf-8') as f:
            doc = json.load(f)
        
        with self.driver.session() as session:
            # Create Document node
            session.run(
                "CREATE (d:Document {document_type: $doc_type, title: $title})",
                doc_type=doc.get('document_type'),
                title=doc.get('title')
            )
            print("Created Document node")
            
            # Process sections
            sections = doc.get('sections', [])
            total_sections = len(sections)
            
            for idx, section in enumerate(sections):
                self._process_section(session, section, doc.get('title'), idx, is_top_level=True)
                print(f"Processed section {idx + 1}/{total_sections}: {section.get('id')}")
        
        print("\nUpload complete!")
    
    def _process_section(self, session, section: dict, parent_identifier: str, order: int, is_top_level: bool = False):
        """Process a section or subsection and its children."""
        section_id = section.get('id')
        section_title = section.get('title')
        section_content = section.get('content')
        
        if is_top_level:
            # Create Section and link to Document
            session.run("""
                MATCH (d:Document {title: $doc_title})
                CREATE (s:Section {id: $id, title: $title, content: $content})
                CREATE (d)-[:HAS_SECTION {order: $order}]->(s)
            """, doc_title=parent_identifier, id=section_id, title=section_title, 
                content=section_content, order=order)
            
            # Link to previous section
            if order > 0:
                session.run("""
                    MATCH (s1:Section) WHERE s1.id STARTS WITH $prefix
                    MATCH (s2:Section {id: $current_id})
                    WITH s1, s2 ORDER BY s1.id DESC LIMIT 1
                    WHERE s1.id <> s2.id
                    CREATE (s1)-[:NEXT_SECTION]->(s2)
                """, prefix=section_id.split('.')[0], current_id=section_id)
        else:
            # Create Subsection and link to parent
            session.run("""
                MATCH (p {id: $parent_id})
                CREATE (s:Subsection {id: $id, title: $title, content: $content})
                CREATE (p)-[:HAS_SUBSECTION {order: $order}]->(s)
            """, parent_id=parent_identifier, id=section_id, title=section_title,
                content=section_content, order=order)
        
        # Process paragraphs
        for para_idx, paragraph in enumerate(section.get('paragraphs', [])):
            self._process_paragraph(session, paragraph, section_id, para_idx)
        
        # Process direct items
        for item_idx, item in enumerate(section.get('items', [])):
            self._process_item(session, item, section_id, item_idx, f"sec_{section_id}")
        
        # Process amendments
        for amend_idx, amendment in enumerate(section.get('amendments', [])):
            session.run("""
                MATCH (s {id: $section_id})
                CREATE (a:Amendment {content: $content})
                CREATE (s)-[:HAS_AMENDMENT {order: $order}]->(a)
            """, section_id=section_id, content=amendment, order=amend_idx)
        
        # Process nested subsections
        for subsec_idx, subsection in enumerate(section.get('subsections', [])):
            self._process_section(session, subsection, section_id, subsec_idx, is_top_level=False)
    
    def _process_paragraph(self, session, paragraph: dict, parent_id: str, order: int):
        """Process a paragraph node."""
        para_id = paragraph.get('id')
        content = paragraph.get('content')
        
        # Create unique identifier for paragraph
        full_para_id = f"{parent_id}_p{para_id}"
        
        session.run("""
            MATCH (s {id: $parent_id})
            CREATE (p:Paragraph {id: $para_id, full_id: $full_id, content: $content})
            CREATE (s)-[:HAS_PARAGRAPH {order: $order}]->(p)
        """, parent_id=parent_id, para_id=para_id, full_id=full_para_id, 
            content=content, order=order)
        
        # Process items within paragraph
        for item_idx, item in enumerate(paragraph.get('items', [])):
            self._process_item(session, item, full_para_id, item_idx, f"para_{full_para_id}")
    
    def _process_item(self, session, item, parent_id: str, order: int, prefix: str):
        """Process an item node."""
        if isinstance(item, str):
            item_id = None
            content = item
            sub_items = []
        else:
            item_id = item.get('id')
            content = item.get('content')
            sub_items = item.get('sub_items', [])
        
        # Create unique identifier
        full_item_id = f"{prefix}_i{order}"
        
        session.run("""
            MATCH (p) WHERE p.id = $parent_id OR p.full_id = $parent_id
            CREATE (i:Item {item_id: $item_id, full_id: $full_id, content: $content})
            CREATE (p)-[:HAS_ITEM {order: $order}]->(i)
        """, parent_id=parent_id, item_id=item_id, full_id=full_item_id,
            content=content, order=order)
        
        # Process sub_items
        for subitem_idx, sub_item in enumerate(sub_items):
            subitem_id = sub_item.get('id')
            subitem_content = sub_item.get('content')
            
            session.run("""
                MATCH (i:Item {full_id: $item_full_id})
                CREATE (si:SubItem {id: $id, content: $content})
                CREATE (i)-[:HAS_SUBITEM {order: $order}]->(si)
            """, item_full_id=full_item_id, id=subitem_id, 
                content=subitem_content, order=subitem_idx)
    
    def upload_from_cypher_file(self, cypher_path: str, batch_size: int = 100):
        """
        Upload from the generated .cypher file.
        Executes queries in batches for better performance.
        """
        with open(cypher_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse individual statements
        statements = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('//'):
                # Remove trailing semicolon
                if line.endswith(';'):
                    line = line[:-1]
                if line:
                    statements.append(line)
        
        print(f"Found {len(statements)} statements to execute")
        
        # Execute in batches
        with self.driver.session() as session:
            for i in range(0, len(statements), batch_size):
                batch = statements[i:i + batch_size]
                
                # Combine into single transaction
                def run_batch(tx):
                    for stmt in batch:
                        try:
                            tx.run(stmt)
                        except Exception as e:
                            print(f"Error executing: {stmt[:50]}... - {e}")
                
                session.execute_write(run_batch)
                print(f"Executed batch {i // batch_size + 1}/{(len(statements) + batch_size - 1) // batch_size}")
        
        print("\nUpload complete!")


def main():
    # === CONFIGURE YOUR AURA CREDENTIALS HERE ===
    AURA_URI = os.environ.get("NEO4J_URI", "")
    AURA_USERNAME = os.environ.get("NEO4J_USERNAME", "neo4j")
    AURA_PASSWORD = os.environ.get("NEO4J_PASSWORD", "your-password-here")
    
    # Path to your JSON file
    JSON_PATH = "sut_out.json"
    
    # Or path to generated Cypher file
    CYPHER_PATH = "sut_cypher_queries.cypher"
    
    # === END CONFIGURATION ===
    
    print("=" * 50)
    print("Neo4j Aura Upload Script")
    print("=" * 50)
    
    # Check if credentials are set
    if "xxxxxxxx" in AURA_URI or AURA_PASSWORD == "your-password-here":
        print("\n⚠️  Please configure your Aura credentials!")
        print("\nOption 1: Set environment variables:")
        print("  export NEO4J_URI='neo4j+s://xxxxx.databases.neo4j.io'")
        print("  export NEO4J_USERNAME='neo4j'")
        print("  export NEO4J_PASSWORD='your-password'")
        print("\nOption 2: Edit this script and update the variables directly")
        print("\nYou can find your credentials in the Neo4j Aura console.")
        return
    
    uploader = AuraUploader(AURA_URI, AURA_USERNAME, AURA_PASSWORD)
    
    try:
        # Clear existing data before upload
        uploader.clear_database()
        
        # Create schema
        uploader.create_constraints_and_indexes()
        
        # Choose upload method:
        
        # Method 1: Upload directly from JSON (recommended - more efficient)
        if os.path.exists(JSON_PATH):
            print(f"\nUploading from JSON: {JSON_PATH}")
            uploader.upload_from_json(JSON_PATH)
        
        # Method 2: Upload from Cypher file
        # elif os.path.exists(CYPHER_PATH):
        #     print(f"\nUploading from Cypher: {CYPHER_PATH}")
        #     uploader.upload_from_cypher_file(CYPHER_PATH)
        
        else:
            print(f"Neither {JSON_PATH} nor {CYPHER_PATH} found!")
    
    finally:
        uploader.close()


if __name__ == "__main__":
    main()