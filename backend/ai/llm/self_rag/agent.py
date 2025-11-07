from backend.utils.logger import get_logger
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from backend.common.constants import LLAMA_3_3_70B_VERSATILE
from backend.ai.llm.prompts import SELF_RAG_SYSTEM_PROMPT
from backend.ai.llm.self_rag.models import SelfRAGOutput
from langchain.schema import Document
from pydantic import ValidationError

logger = get_logger()

def self_rag_agent(query: str, chunks: list[Document], top_k: int):
    """
    Uses Llama 3.3 70b to evaluate and select the most relevant chunks.

    Args:
        query: The user's query
        chunks: List of retrieved chunks
        top_k: Number of most relevant chunks to select

    Returns:
        List of selected chunks ordered by relevance
    """
    logger.info(f"Using LLM to select top {top_k} chunks from {len(chunks)} candidates")

    # Prepare chunks for LLM evaluation with indices
    chunks_text = ""
    for idx, chunk in enumerate(chunks):
        page_num = chunk.metadata.get("page", "Unknown")
        chunks_text += f"\n[Chunk {idx}] (Page {page_num}):\n{chunk.page_content}\n"

    # Create prompt for LLM to evaluate chunks
    system_prompt = SELF_RAG_SYSTEM_PROMPT
    user_prompt = f"""Query: {query}
        Available chunks (total: {len(chunks)}):
        {chunks_text}
        Select the top {top_k} most relevant chunks. """

    # Call LLM with structured output
    llm = ChatGroq(model=LLAMA_3_3_70B_VERSATILE)
    llm = llm.with_structured_output(SelfRAGOutput)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    try:
        # Get structured response
        response: SelfRAGOutput = llm.invoke(messages)

        logger.info(f"LLM selected indices: {response.selected_indices}")
        if response.relevance_scores:
            logger.info(f"Relevance scores: {response.relevance_scores}")

        # Validate indices are within range
        valid_indices = [idx for idx in response.selected_indices if 0 <= idx < len(chunks)]

        if len(valid_indices) < len(response.selected_indices):
            logger.warning(
                f"Some indices were out of range. "
                f"Original: {response.selected_indices}, Valid: {valid_indices}"
            )

        # Return selected chunks in order of relevance, limit to top_k
        selected_chunks = [chunks[idx] for idx in valid_indices[:top_k]]

        logger.info(f"Successfully selected {len(selected_chunks)} chunks")
        return selected_chunks

    except ValidationError as e:
        logger.error(f"Pydantic validation error: {e}")
        # Fallback: return first top_k chunks
        logger.warning(f"Falling back to first {top_k} chunks")
        return chunks[:top_k]

    except Exception as e:
        logger.error(f"Error in LLM chunk selection: {e}")
        # Fallback: return first top_k chunks
        logger.warning(f"Falling back to first {top_k} chunks")
        return chunks[:top_k]
