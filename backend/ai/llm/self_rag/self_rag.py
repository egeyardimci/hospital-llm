from langchain_chroma import Chroma
from backend.utils.logger import get_logger
from backend.ai.testing.models import TestOption
from backend.common.config import SELF_RAG_N
from backend.ai.llm.self_rag.agent import self_rag_agent


logger = get_logger()


def use_self_rag(option:TestOption, query: str, db: Chroma, k_per_retrieval: int, final_k: int):
    """
    Self-Reflective RAG: Performs n different retrievals and uses LLM to select the most k relevant chunks.

    Args:
        query: The user's query
        db: ChromaDB vector database instance
        n: Number of different retrieval iterations to perform
        k_per_retrieval: Number of chunks to retrieve in each iteration
        final_k: Final number of most relevant chunks to return after LLM selection

    Returns:
        List of the most relevant chunks selected by the LLM
    """

    # Step 1: Perform n different retrievals with varying parameters
    n = int(option.data) if option and option.data.isdigit() else SELF_RAG_N   # Default to SELF_RAG_N if not specified

    logger.info(f"Starting Self-RAG with {k_per_retrieval * n} retrievals, selecting top {final_k}")

    total_k = k_per_retrieval * n
    all_retrieved_chunks = db.similarity_search(query, k=total_k)
    
    logger.info(f"Retrieved {len(all_retrieved_chunks)} chunks")
    
    selected_chunks = self_rag_agent(query, all_retrieved_chunks, final_k)
    return selected_chunks
