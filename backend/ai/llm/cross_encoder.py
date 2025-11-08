
from sentence_transformers import CrossEncoder
from backend.common.config import CROSS_ENCODER_K
from backend.utils.logger import get_logger
from backend.ai.testing.models import TestOption
logger = get_logger()

def use_cross_encoder(cross_encoder_option:TestOption, query, retrieved_chunks):
    cross_encoder_model_name = cross_encoder_option.data
    top_k = CROSS_ENCODER_K

    retrieved_chunks_cross_encoded = rerank_with_cross_encoder(
        query,
        retrieved_chunks,
        cross_encoder_model_name,
        top_k
    )

    return retrieved_chunks_cross_encoded

def rerank_with_cross_encoder(query, retrieved_chunks, cross_encoder_model_name, top_k=None):
    """
    Improved re-ranking with robust error handling and fallback mechanisms.
    """
  
    cross_encoder = CrossEncoder(cross_encoder_model_name, trust_remote_code=True)
    try:
        # Prepare pairs of (query, chunk) for the cross-encoder
        pairs = [(query, chunk.page_content) for chunk in retrieved_chunks]
        
        # Get relevance scores with error handling
        scores = cross_encoder.predict(pairs)
        
        # Create list of (chunk, score) tuples
        chunk_score_pairs = list(zip(retrieved_chunks, scores))
        
        # Sort by score in descending order
        reranked_chunks = sorted(chunk_score_pairs, key=lambda x: x[1], reverse=True)
        
        # Return top_k chunks if specified, otherwise return all
        if top_k is not None:
            reranked_chunks = reranked_chunks[:top_k]
        
        # Add logging for re-ranking details
        logger.info(f"Re-ranking results: Original chunks={len(retrieved_chunks)}, Reranked chunks={len(reranked_chunks)}")
        
        return [chunk for chunk, _ in reranked_chunks]
    
    except Exception as e:
        logger.error(f"Cross-encoder re-ranking error: {e}")
        return retrieved_chunks