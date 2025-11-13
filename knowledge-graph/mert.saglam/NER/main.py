from ner import TurkishNERExtractor
from extract import Neo4jKnowledgeGraph
import json

with open('ner_extraction_test.json', 'r', encoding='utf-8') as f:
    ner_results = json.load(f)

# Build knowledge graph
kg = Neo4jKnowledgeGraph()
kg.connect()
kg.clear_database()
kg.create_indexes()
kg.build_from_ner_results(ner_results)

# Query examples
results = kg.search_entities("provizyon", limit=10)
print(f"Found {len(results)} entities matching 'provizyon'")

details = kg.get_entity_details("MEDULA")
print(f"MEDULA details: {details}")

stats = kg.get_graph_statistics()
print(f"\nGraph has {stats['total_nodes']} nodes and {stats['total_relationships']} relationships")

kg.close()