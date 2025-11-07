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
    all_retrieved_chunks = []
    chunk_ids_seen = set()
    n = int(option.data) if option and option.data.isdigit() else SELF_RAG_N   # Default to SELF_RAG_N if not specified

    logger.info(f"Starting Self-RAG with {n} retrievals, {k_per_retrieval} chunks per retrieval, selecting top {final_k}")

    for i in range(n):
        # Vary the retrieval by using different k values or fetch offsets
        # We'll retrieve different amounts to get diverse results
        retrieval_k = k_per_retrieval + (i * 2)  # Gradually increase k for diversity
        chunks = db.similarity_search(query, k=retrieval_k)

        # Add only unique chunks (avoid duplicates across retrievals)
        for chunk in chunks:
            # Create a simple hash of chunk content to detect duplicates
            chunk_id = hash(chunk.page_content)
            if chunk_id not in chunk_ids_seen:
                chunk_ids_seen.add(chunk_id)
                all_retrieved_chunks.append(chunk)

    logger.info(f"Total unique chunks retrieved across {n} iterations: {len(all_retrieved_chunks)}")

    if len(all_retrieved_chunks) == 0:
        logger.warning("No chunks retrieved, returning empty list")
        return []

    selected_chunks = self_rag_agent(query, all_retrieved_chunks, final_k)

    logger.info(f"Self-RAG selected {len(selected_chunks)} final chunks")
    return selected_chunks
