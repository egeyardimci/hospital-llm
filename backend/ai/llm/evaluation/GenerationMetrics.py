from typing import List, Dict
import numpy as np

class GenerationMetricsLLM:
    """
    Semantic generation metrics using Sentence Transformers
    """

    def __init__(self):
        self.name = "Generation Metrics (Semantic)"

    def generation_metrics(
        self,
        query: str,
        answer: str,
        contexts: List[str],
        ground_truth: str = None
    ) -> Dict:
        """
        Generation metrics using Sentence Transformers for semantic similarity
        Requires: pip install sentence-transformers
        """
        try:
            from sentence_transformers import SentenceTransformer
            from sklearn.metrics.pairwise import cosine_similarity

            # Load a lightweight model for fast inference
            model = SentenceTransformer('all-MiniLM-L6-v2')

            # Encode texts
            query_embedding = model.encode([query])
            answer_embedding = model.encode([answer])
            context_embeddings = model.encode(contexts)

            # Faithfulness: How well is the answer grounded in contexts?
            # Higher similarity to contexts = more faithful
            answer_context_similarities = cosine_similarity(answer_embedding, context_embeddings)[0]
            faithfulness = float(np.mean(answer_context_similarities))

            # Answer Relevancy: How relevant is the answer to the query?
            answer_relevancy = float(cosine_similarity(query_embedding, answer_embedding)[0][0])

            result = {
                'faithfulness': faithfulness,
                'answer_relevancy': answer_relevancy,
            }

            # If ground truth is available, calculate correctness and similarity
            if ground_truth:
                ground_truth_embedding = model.encode([ground_truth])

                # Answer Similarity: Semantic similarity to ground truth
                answer_similarity = float(cosine_similarity(answer_embedding, ground_truth_embedding)[0][0])

                # Answer Correctness: Weighted combination of similarity and relevancy
                # This approximates the quality of the answer
                answer_correctness = float(0.7 * answer_similarity + 0.3 * answer_relevancy)

                result['answer_correctness'] = answer_correctness
                result['answer_similarity'] = answer_similarity
            else:
                result['answer_correctness'] = None
                result['answer_similarity'] = None

            return result

        except Exception as e:
            print(f"Generation metrics failed: {e}")
            return {
                'faithfulness': 0.0,
                'answer_relevancy': 0.0,
                'answer_correctness': None,
                'answer_similarity': None
            }
    
    
# ============================================================================
# TRADITIONAL GENERATION METRICS
# ============================================================================

class TraditionalGenerationMetrics:
    """
    Traditional metrics requiring reference answers
    """
    
    def __init__(self):
        self.name = "Traditional Generation Metrics"
    
    def bleu_score(self, prediction: str, reference: str) -> float:
        """
        BLEU score for n-gram overlap
        Requires: pip install nltk
        """
        try:
            import nltk
            from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

            # Download required NLTK data if not present
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                print("Downloading punkt tokenizer for BLEU score...")
                nltk.download('punkt', quiet=True)
                nltk.download('punkt_tab', quiet=True)

            # Tokenize
            reference_tokens = nltk.word_tokenize(reference.lower())
            prediction_tokens = nltk.word_tokenize(prediction.lower())

            # Use smoothing to handle cases with no n-gram overlaps
            smoothing = SmoothingFunction().method1
            score = sentence_bleu([reference_tokens], prediction_tokens, smoothing_function=smoothing)

            return score
        except Exception as e:
            print(f"BLEU failed: {e}")
            return 0.0
    
    def rouge_scores(self, prediction: str, reference: str) -> Dict:
        """
        ROUGE-1, ROUGE-2, ROUGE-L scores
        Requires: pip install rouge-score
        """
        try:
            from rouge_score import rouge_scorer
            
            scorer = rouge_scorer.RougeScorer(
                ['rouge1', 'rouge2', 'rougeL'],
                use_stemmer=True
            )
            
            scores = scorer.score(reference, prediction)
            
            return {
                'rouge1': scores['rouge1'].fmeasure,
                'rouge2': scores['rouge2'].fmeasure,
                'rougeL': scores['rougeL'].fmeasure
            }
        except Exception as e:
            print(f"ROUGE failed: {e}")
            return {}
    
    def meteor_score(self, prediction: str, reference: str) -> float:
        """
        METEOR score (better than BLEU)
        Requires: pip install nltk
        """
        try:
            import nltk
            from nltk.translate.meteor_score import meteor_score

            # Download required NLTK data if not present
            try:
                nltk.data.find('corpora/wordnet')
            except LookupError:
                print("Downloading WordNet for METEOR score...")
                nltk.download('wordnet', quiet=True)
                nltk.download('omw-1.4', quiet=True)

            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                print("Downloading punkt tokenizer for METEOR score...")
                nltk.download('punkt', quiet=True)
                nltk.download('punkt_tab', quiet=True)

            reference_tokens = nltk.word_tokenize(reference)
            prediction_tokens = nltk.word_tokenize(prediction)

            score = meteor_score([reference_tokens], prediction_tokens)
            return score
        except Exception as e:
            print(f"METEOR failed: {e}")
            return 0.0
    
    def bert_score(self, prediction: str, reference: str) -> Dict:
        """
        BERTScore for semantic similarity
        Requires: pip install bert-score
        """
        try:
            from bert_score import score
            
            P, R, F1 = score(
                [prediction],
                [reference],
                model_type="microsoft/deberta-xlarge-mnli",
                lang="en"
            )
            
            return {
                'bert_precision': P.mean().item(),
                'bert_recall': R.mean().item(),
                'bert_f1': F1.mean().item()
            }
        except Exception as e:
            print(f"BERTScore failed: {e}")
            return {}
    