"""
Knowledge Graph Builder using NER Extraction Results
Builds Neo4j knowledge graph from dynamically extracted entities
"""

import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
from neo4j import GraphDatabase
import logging
from ner import TurkishNERExtractor

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


class Neo4jKnowledgeGraph:
    """Manages Neo4j knowledge graph operations with dynamic entity types"""
    
    def __init__(self):
        self.uri = os.getenv('NEO4J_URI')
        self.username = os.getenv('NEO4J_USERNAME')
        self.password = os.getenv('NEO4J_PASSWORD')
        self.database = os.getenv('NEO4J_DATABASE', 'neo4j')
        self.driver = None
        
    def connect(self):
        """Connect to Neo4j database"""
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password)
            )
            self.driver.verify_connectivity()
            logger.info("Successfully connected to Neo4j")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")
    
    def clear_database(self):
        """Clear all nodes and relationships"""
        with self.driver.session(database=self.database) as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.info("Database cleared")
    
    def create_indexes(self):
        """Create indexes for better query performance"""
        with self.driver.session(database=self.database) as session:
            # Create index on text for full-text search
            session.run("CREATE INDEX entity_text IF NOT EXISTS FOR (n:Entity) ON (n.text)")
            session.run("CREATE INDEX entity_type IF NOT EXISTS FOR (n:Entity) ON (n.type)")
            logger.info("Indexes created")
    
    def sanitize_label(self, label: str) -> str:
        """Sanitize label for Neo4j (remove special characters)"""
        # Remove or replace characters that aren't allowed in Neo4j labels
        sanitized = label.replace(' ', '_').replace('-', '_').replace('/', '_')
        # Remove any other special characters
        sanitized = ''.join(c for c in sanitized if c.isalnum() or c == '_')
        # Ensure it starts with a letter
        if sanitized and not sanitized[0].isalpha():
            sanitized = 'T_' + sanitized
        return sanitized or 'Entity'
    
    def sanitize_relationship_type(self, rel_type: str) -> str:
        """Sanitize relationship type for Neo4j"""
        # Convert to uppercase and replace spaces with underscores
        sanitized = rel_type.upper().replace(' ', '_').replace('-', '_')
        # Remove special characters except underscore
        sanitized = ''.join(c for c in sanitized if c.isalnum() or c == '_')
        return sanitized or 'RELATED_TO'
    
    def insert_entities_from_ner(self, entities: List[Dict[str, Any]]):
        """Insert entities from NER extraction results"""
        with self.driver.session(database=self.database) as session:
            for entity in entities:
                # Create sanitized label for Neo4j
                entity_label = self.sanitize_label(entity['type'])
                
                # Generate unique ID from text and type
                entity_id = f"{entity['text'].lower().replace(' ', '_')}_{entity_label.lower()}"
                
                query = f"""
                MERGE (n:Entity:{entity_label} {{id: $id}})
                SET n.text = $text,
                    n.type = $type,
                    n.original_type = $original_type,
                    n.context = $context,
                    n.confidence = $confidence,
                    n.start_pos = $start_pos,
                    n.end_pos = $end_pos,
                    n += $properties
                RETURN n
                """
                
                session.run(query,
                           id=entity_id,
                           text=entity['text'],
                           type=entity_label,
                           original_type=entity['type'],
                           context=entity.get('context', ''),
                           confidence=entity.get('confidence', 0.8),
                           start_pos=entity.get('start_pos', 0),
                           end_pos=entity.get('end_pos', 0),
                           properties=entity.get('properties', {}))
        
        logger.info(f"Inserted {len(entities)} entities into Neo4j")
    
    def insert_relations_from_ner(self, relations: List[Dict[str, Any]]):
        """Insert relationships from NER extraction results"""
        successful = 0
        failed = 0
        
        with self.driver.session(database=self.database) as session:
            for relation in relations:
                # Sanitize relationship type
                rel_type = self.sanitize_relationship_type(relation['relation_type'])
                
                query = f"""
                MATCH (source:Entity)
                WHERE toLower(source.text) = toLower($entity1)
                MATCH (target:Entity)
                WHERE toLower(target.text) = toLower($entity2)
                MERGE (source)-[r:{rel_type}]->(target)
                SET r.original_type = $original_type,
                    r.context = $context,
                    r.confidence = $confidence,
                    r += $properties
                RETURN r
                """
                
                try:
                    result = session.run(query,
                                       entity1=relation['entity1'],
                                       entity2=relation['entity2'],
                                       original_type=relation['relation_type'],
                                       context=relation.get('context', ''),
                                       confidence=relation.get('confidence', 0.8),
                                       properties=relation.get('properties', {}))
                    
                    if result.single():
                        successful += 1
                    else:
                        failed += 1
                        
                except Exception as e:
                    logger.warning(f"Failed to create relationship {relation['entity1']}->{relation['entity2']}: {e}")
                    failed += 1
        
        logger.info(f"Inserted {successful} relationships ({failed} failed)")
    
    def build_from_ner_results(self, ner_results: Dict[str, Any]):
        """Build complete knowledge graph from NER extraction results"""
        logger.info("Building knowledge graph from NER results...")
        
        # Insert entities
        self.insert_entities_from_ner(ner_results['entities'])
        
        # Insert relations
        self.insert_relations_from_ner(ner_results['relations'])
        
        logger.info("Knowledge graph built successfully!")
    
    # ========== QUERY METHODS ==========
    
    def search_entities(self, search_term: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search entities by text (case-insensitive)"""
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (n:Entity)
                WHERE toLower(n.text) CONTAINS toLower($search_term)
                RETURN n.id as id, 
                       n.text as text,
                       n.original_type as type,
                       n.context as context,
                       n.confidence as confidence,
                       properties(n) as properties
                ORDER BY n.confidence DESC
                LIMIT $limit
            """, search_term=search_term, limit=limit)
            
            return [dict(record) for record in result]
    
    def get_entity_details(self, entity_text: str) -> Dict[str, Any]:
        """Get full details of an entity and its relationships"""
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (n:Entity)
                WHERE toLower(n.text) = toLower($entity_text)
                OPTIONAL MATCH (n)-[r_out]->(m:Entity)
                OPTIONAL MATCH (n)<-[r_in]-(p:Entity)
                RETURN n.id as id,
                       n.text as text,
                       n.original_type as type,
                       n.context as context,
                       n.confidence as confidence,
                       properties(n) as properties,
                       collect(DISTINCT {
                           direction: 'outgoing',
                           relationship: r_out.original_type,
                           target_text: m.text,
                           target_type: m.original_type,
                           confidence: r_out.confidence
                       }) as outgoing,
                       collect(DISTINCT {
                           direction: 'incoming',
                           relationship: r_in.original_type,
                           source_text: p.text,
                           source_type: p.original_type,
                           confidence: r_in.confidence
                       }) as incoming
            """, entity_text=entity_text)
            
            record = result.single()
            if not record:
                return None
            
            return dict(record)
    
    def get_entities_by_type(self, entity_type: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get all entities of a specific type"""
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (n:Entity)
                WHERE toLower(n.original_type) = toLower($entity_type)
                RETURN n.id as id,
                       n.text as text,
                       n.original_type as type,
                       n.context as context,
                       n.confidence as confidence
                ORDER BY n.confidence DESC
                LIMIT $limit
            """, entity_type=entity_type, limit=limit)
            
            return [dict(record) for record in result]
    
    def get_path_between_entities(self, entity1_text: str, entity2_text: str, max_depth: int = 5) -> List[Dict[str, Any]]:
        """Find shortest paths between two entities"""
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (a:Entity), (b:Entity)
                WHERE toLower(a.text) = toLower($entity1) 
                  AND toLower(b.text) = toLower($entity2)
                MATCH path = shortestPath((a)-[*..%d]-(b))
                RETURN [node in nodes(path) | {text: node.text, type: node.original_type}] as nodes,
                       [rel in relationships(path) | rel.original_type] as relationships,
                       length(path) as path_length
                LIMIT 5
            """ % max_depth, entity1=entity1_text, entity2=entity2_text)
            
            return [dict(record) for record in result]
    
    def get_entity_neighbors(self, entity_text: str, depth: int = 2, limit: int = 50) -> List[Dict[str, Any]]:
        """Get neighboring entities up to specified depth"""
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (n:Entity)
                WHERE toLower(n.text) = toLower($entity_text)
                MATCH path = (n)-[*1..%d]-(m:Entity)
                RETURN n.text as start_entity,
                       n.original_type as start_type,
                       [rel in relationships(path) | rel.original_type] as relationships,
                       m.text as end_entity,
                       m.original_type as end_type,
                       length(path) as depth
                ORDER BY depth
                LIMIT $limit
            """ % depth, entity_text=entity_text, limit=limit)
            
            return [dict(record) for record in result]
    
    def get_graph_statistics(self) -> Dict[str, Any]:
        """Get overall statistics about the knowledge graph"""
        with self.driver.session(database=self.database) as session:
            # Count nodes by type
            node_counts = session.run("""
                MATCH (n:Entity)
                RETURN n.original_type as type, count(n) as count
                ORDER BY count DESC
            """)
            
            # Count relationships by type
            rel_counts = session.run("""
                MATCH ()-[r]->()
                RETURN r.original_type as type, count(r) as count
                ORDER BY count DESC
            """)
            
            # Total counts
            totals = session.run("""
                MATCH (n:Entity)
                OPTIONAL MATCH ()-[r]->()
                RETURN count(DISTINCT n) as total_nodes,
                       count(r) as total_relationships
            """).single()
            
            # Average confidence
            avg_conf = session.run("""
                MATCH (n:Entity)
                RETURN avg(n.confidence) as avg_confidence
            """).single()
            
            return {
                'total_nodes': totals['total_nodes'],
                'total_relationships': totals['total_relationships'],
                'average_confidence': avg_conf['avg_confidence'],
                'nodes_by_type': [dict(record) for record in node_counts],
                'relationships_by_type': [dict(record) for record in rel_counts]
            }
    
    def find_central_entities(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Find most connected entities (highest degree centrality)"""
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (n:Entity)
                OPTIONAL MATCH (n)-[r]-()
                WITH n, count(r) as connections
                WHERE connections > 0
                RETURN n.text as text,
                       n.original_type as type,
                       n.confidence as confidence,
                       connections
                ORDER BY connections DESC, n.confidence DESC
                LIMIT $limit
            """, limit=limit)
            
            return [dict(record) for record in result]
    
    def get_all_entity_types(self) -> List[str]:
        """Get list of all discovered entity types"""
        with self.driver.session(database=self.database) as session:
            result = session.run("""
                MATCH (n:Entity)
                RETURN DISTINCT n.original_type as type
                ORDER BY type
            """)
            
            return [record['type'] for record in result]


def print_results(title: str, results: List[Dict], max_items: int = 10):
    """Pretty print query results"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}")
    
    if not results:
        print("  No results found.")
        return
    
    for i, result in enumerate(results[:max_items], 1):
        print(f"\n{i}. ", end="")
        for key, value in result.items():
            if key == 'properties' and isinstance(value, dict):
                if value:
                    print(f"\n   {key}: {json.dumps(value, ensure_ascii=False, indent=6)}")
            elif isinstance(value, list) and len(value) > 0:
                print(f"\n   {key}:")
                for item in value[:3]:
                    if isinstance(item, dict):
                        print(f"     - {json.dumps(item, ensure_ascii=False)}")
                    else:
                        print(f"     - {item}")
                if len(value) > 3:
                    print(f"     ... and {len(value) - 3} more")
            else:
                print(f"{key}: {value}", end=" | ")
        print()
    
    if len(results) > max_items:
        print(f"\n  ... and {len(results) - max_items} more results")


def main():
    """Main execution with example queries"""
    
    # Option 1: Load from existing NER extraction file
    try:
        with open('ner_extraction.json', 'r', encoding='utf-8') as f:
            ner_results = json.load(f)
        logger.info("Loaded NER results from ner_extraction.json")
    except FileNotFoundError:
        # Option 2: Run NER extraction if file doesn't exist
        logger.info("ner_extraction.json not found. Running NER extraction...")
        
        with open('sgk_document.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        
        ner_extractor = TurkishNERExtractor()
        ner_results = ner_extractor.extract_from_document(text)
        ner_extractor.save_extraction_results(ner_results)
    
    # Initialize Knowledge Graph
    kg = Neo4jKnowledgeGraph()
    
    try:
        # Connect to Neo4j
        kg.connect()
        
        # Clear and prepare database
        print("\n🗑️  Clearing database...")
        kg.clear_database()
        kg.create_indexes()
        
        # Build knowledge graph from NER results
        print("\n🏗️  Building knowledge graph from NER results...")
        kg.build_from_ner_results(ner_results)
        
        # Get statistics
        stats = kg.get_graph_statistics()
        print(f"\n✅ Knowledge graph created successfully!")
        print(f"\n📈 Graph Statistics:")
        print(f"   Total Nodes: {stats['total_nodes']}")
        print(f"   Total Relationships: {stats['total_relationships']}")
        print(f"   Average Confidence: {stats['average_confidence']:.3f}")
        print(f"\n   Nodes by Type:")
        for item in stats['nodes_by_type'][:10]:
            print(f"     - {item['type']}: {item['count']}")
        print(f"\n   Relationships by Type:")
        for item in stats['relationships_by_type'][:10]:
            print(f"     - {item['type']}: {item['count']}")
        
        # Example Queries
        print("\n" + "="*80)
        print("  RUNNING EXAMPLE QUERIES")
        print("="*80)
        
        # Query 1: Get all entity types
        types = kg.get_all_entity_types()
        print(f"\n🏷️  Discovered Entity Types ({len(types)} total):")
        for t in types:
            print(f"   • {t}")
        
        # Query 2: Search for entities
        search_term = "MEDULA"
        results = kg.search_entities(search_term, limit=5)
        print_results(f"🔎 Search Results for '{search_term}'", results)
        
        # Query 3: Get entity details
        if results:
            entity_text = results[0]['text']
            details = kg.get_entity_details(entity_text)
            if details:
                print_results(f"📋 Details for '{entity_text}'", [details])
        
        # Query 4: Find central entities
        central = kg.find_central_entities(limit=5)
        print_results("⭐ Most Connected Entities", central)
        
        # Query 5: Get neighbors
        if results:
            neighbors = kg.get_entity_neighbors(results[0]['text'], depth=2, limit=10)
            print_results(f"🌐 Neighbors of '{results[0]['text']}'", neighbors)
        
        # Query 6: Get entities by type
        if types:
            type_entities = kg.get_entities_by_type(types[0], limit=5)
            print_results(f"📑 Entities of type '{types[0]}'", type_entities)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
    finally:
        kg.close()


if __name__ == "__main__":
    main()