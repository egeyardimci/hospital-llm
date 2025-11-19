import numpy as np
from typing import List, Dict

class RetrievalMetrics:
    """
    Implements all retrieval quality metrics
    """
    
    def __init__(self):
        self.name = "Retrieval Metrics"

    # -------- Semantic Similarity Metrics (via Sentence Transformers) --------

    def context_metrics(
        self,
        query: str,
        answer: str,
        contexts: List[str],
        ground_truth: str = None
    ) -> Dict:
        """
        Context retrieval metrics using Sentence Transformers
        Calculates semantic similarity between query, contexts, and answers
        Requires: pip install sentence-transformers
        """
        try:
            from sentence_transformers import SentenceTransformer
            from sklearn.metrics.pairwise import cosine_similarity

            # Load a lightweight model for fast inference
            model = SentenceTransformer('all-MiniLM-L6-v2')

            # Encode texts
            query_embedding = model.encode([query])
            context_embeddings = model.encode(contexts)
            answer_embedding = model.encode([answer])

            # Context Relevancy: How relevant are contexts to the query?
            query_context_similarities = cosine_similarity(query_embedding, context_embeddings)[0]
            context_relevancy = float(np.mean(query_context_similarities))

            # Context Precision: Top-k contexts that are actually relevant
            # Using answer as proxy for relevance
            answer_context_similarities = cosine_similarity(answer_embedding, context_embeddings)[0]

            # Sort by similarity and calculate precision
            sorted_indices = np.argsort(answer_context_similarities)[::-1]
            top_k = min(5, len(contexts))
            precision_scores = answer_context_similarities[sorted_indices[:top_k]]
            context_precision = float(np.mean(precision_scores))

            result = {
                'context_relevancy': context_relevancy,
                'context_precision': context_precision,
            }

            # Context Recall: If ground truth available, check coverage
            if ground_truth:
                ground_truth_embedding = model.encode([ground_truth])
                gt_context_similarities = cosine_similarity(ground_truth_embedding, context_embeddings)[0]
                # Recall: average similarity of contexts to ground truth
                context_recall = float(np.mean(gt_context_similarities))
                result['context_recall'] = context_recall
            else:
                result['context_recall'] = None

            return result

        except Exception as e:
            print(f"Context metrics failed: {e}")
            return {
                'context_relevancy': 0.0,
                'context_precision': 0.0,
                'context_recall': None
            }
