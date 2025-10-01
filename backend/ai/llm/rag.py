from langchain_groq import ChatGroq
from threading import Lock
from backend.ai.llm.cross_encoder import rerank_with_cross_encoder
from backend.common.config import CROSS_ENCODER_K
from backend.common.constants import CROSS_ENCODER_OPTION
from langchain.schema import SystemMessage, HumanMessage
from backend.ai.testing.models import RagResponse, TestOption
from langchain_chroma import Chroma
from backend.ai.graphdb.utils import neo4j_graph_search, format_graph_to_context
from backend.utils.logger import get_logger

logger = get_logger()

# Global lock for vector DB access (create once at module level)
_vector_db_lock = Lock()

def rag_invoke(
    llm_name: str, 
    system_prompt: str, 
    vector_db: Chroma, 
    similarity_vector_k: int, 
    query: str, 
    options: list[TestOption], 
    use_graph_db: bool = False
) -> RagResponse:

    if use_graph_db:
        # Use Neo4j graph database
        logger.info("Using Neo4j graph database for retrieval")
        graph_results = neo4j_graph_search(query, similarity_vector_k)
        context = format_graph_to_context(graph_results)
        retrieved_chunks = []  # No chunks for graph DB, context is pre-formatted
    else:
        # Use traditional vector database with thread-safe access
        logger.info("Using vector database for retrieval")
        
        # Acquire lock before accessing vector DB
        with _vector_db_lock:
            logger.debug(f"Acquired lock for query: {query[:50]}...")
            retrieved_chunks = vector_db.similarity_search(query, similarity_vector_k)
            logger.debug(f"Released lock after retrieving {len(retrieved_chunks)} chunks")
        
        logger.info(f"Retrieved {len(retrieved_chunks)} chunks from vector DB.")
    
    # Cross-encoder re-ranking (only for vector DB)
    if not use_graph_db:
        cross_encoder_option = None
        for option in options:
            if option.name == CROSS_ENCODER_OPTION and option.is_enabled:
                cross_encoder_option = option
                break
        
        if cross_encoder_option:
            cross_encoder_model_name = cross_encoder_option.data
            top_k = CROSS_ENCODER_K

            if isinstance(cross_encoder_option.data, dict):
                cross_encoder_model_name = cross_encoder_option.data.get("model_name")
                top_k = cross_encoder_option.data.get("top_k", top_k)

            logger.info(f"Re-ranking with cross-encoder: {cross_encoder_model_name}")
            retrieved_chunks = rerank_with_cross_encoder(
                query,
                retrieved_chunks,
                cross_encoder_model_name,
                top_k
            )

        # Format context for vector DB
        context = "\n\n".join([
            f'Page Number: {chunk.metadata.get("page", "Unknown")}: {chunk.page_content}\n' 
            for chunk in retrieved_chunks
        ])

    # Use Groq API for response generation
    llm = ChatGroq(model=llm_name)
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}")
    ]
    response = llm.invoke(messages)

    return RagResponse(
        content=response.content,
        metadata={
            "query": query,
            "system_prompt": system_prompt,
            "retrieved_chunks": retrieved_chunks
        }
    )