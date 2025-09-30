from neo4j import GraphDatabase
from backend.common.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE
from backend.utils.logger import get_logger

logger = get_logger()

class Neo4jConnection:
    """Singleton class for Neo4j database connection management"""
    _instance = None
    _driver = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Neo4jConnection, cls).__new__(cls)
        return cls._instance

    def get_driver(self):
        """Get or create Neo4j driver"""
        if self._driver is None:
            try:
                self._driver = GraphDatabase.driver(
                    NEO4J_URI,
                    auth=(NEO4J_USER, NEO4J_PASSWORD)
                )
                logger.info(f"Connected to Neo4j at {NEO4J_URI}")
            except Exception as e:
                logger.error(f"Failed to connect to Neo4j: {e}")
                raise
        return self._driver

    def close(self):
        """Close Neo4j driver connection"""
        if self._driver is not None:
            self._driver.close()
            self._driver = None
            logger.info("Neo4j connection closed")


def get_neo4j_driver():
    """Get Neo4j driver instance"""
    connection = Neo4jConnection()
    return connection.get_driver()


def neo4j_graph_search(search_query: str, limit: int = 10):
    """
    Search Neo4j graph database and return nodes with relationships.

    Args:
        search_query: The search query
        limit: Maximum number of results to return

    Returns:
        List of dictionaries containing nodes and their relationships
    """
    driver = get_neo4j_driver()

    # Cypher query to retrieve nodes and relationships
    # TEMPORARY: Just return any nodes to test the pipeline
    cypher_query = """
    MATCH (n)
    OPTIONAL MATCH (n)-[r]->(m)
    RETURN n, collect({rel: r, node: m}) as relationships
    LIMIT $limit
    """

    try:
        logger.info(f"Searching Neo4j for...")
        with driver.session(database=NEO4J_DATABASE) as session:
            result = session.run(cypher_query, search_text=search_query, limit=limit)
            records = []

            for record in result:
                node = dict(record["n"])
                relationships = record["relationships"]

                records.append({
                    "node": node,
                    "relationships": relationships
                })

            logger.info(f"Retrieved {len(records)} nodes from Neo4j")
            return records

    except Exception as e:
        logger.error(f"Error querying Neo4j: {e}")
        raise


def format_graph_to_context(graph_results: list) -> str:
    """
    Format graph database results into context string for LLM.

    Args:
        graph_results: List of graph records from neo4j_graph_search

    Returns:
        Formatted context string
    """
    if not graph_results:
        return "No relevant information found."

    context_parts = []

    for idx, record in enumerate(graph_results, 1):
        node = record["node"]
        relationships = record["relationships"]

        # Format node information
        node_info = f"### Result {idx}\n"

        # Add node name (primary property)
        if "name" in node:
            node_info += f"Name: {node['name']}\n"

        # Add content if available
        if "content" in node:
            node_info += f"Content: {node['content']}\n"

        # Add page if available
        if "page" in node:
            node_info += f"Page Number: {node['page']}\n"

        # Add any other node properties (excluding embedding)
        for key, value in node.items():
            if key not in ["content", "name", "page", "embedding"]:
                node_info += f"{key.title()}: {value}\n"

        # Format relationships
        if relationships and len(relationships) > 0:
            node_info += "\nRelationships:\n"
            for rel_data in relationships:
                if rel_data["rel"] is not None:
                    rel = rel_data["rel"]
                    related_node = rel_data["node"]
                    rel_type = rel.type if hasattr(rel, 'type') else "RELATED_TO"
                    related_name = related_node.get("name", related_node.get("content", "Unknown"))[:50]
                    node_info += f"  - {rel_type} -> {related_name}\n"

        context_parts.append(node_info)

    return "\n".join(context_parts)