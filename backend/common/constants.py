SGK_DOCUMENT_FILE_NAME = "doc.pdf"
TEST_RESULTS_FILE_NAME = "results.json"
TEST_CASES_FILE_NAME = "test_cases.json"
TEST_QUERIES_AND_EXPECTED_ANSWERS_FILE_NAME = "queries_expected_answers.json"

AI = "ai"
WEB = "web"
TESTING = "testing"
DOCUMENTS = "documents"
CONFIG = "config"
REACT_BUILD = "react_build"
CHROMA_DB = "chroma_db"

ALLOWED_CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:5173"
]

DEEPSEEK_R1_DISTILL_LLAMA_70B = "deepseek-r1-distill-llama-70b"
LLAMA_3_2_90B_VISION_PREVIEW = "llama-3.2-90b-vision-preview"
LLAMA_3_3_70B_VERSATILE = "llama-3.3-70b-versatile"
META_LLAMA_LLAMA_4_MAVERICK_17B_128E_INSTRUCT = "meta-llama/llama-4-maverick-17b-128e-instruct"
MISTRAL_SABA_24B = "mistral-saba-24b"

BAAI_BGE_M3 = "BAAI/bge-m3"
LABSE = "LaBSE"
SNOWFLAKE_SNOWFLAKE_ARCTIC_EMBED_L_V2_0 = "Snowflake/snowflake-arctic-embed-l-v2.0"
EMRECAN_BERT_BASE_TURKISH_CASED_MEAN_NLI_STSB_TR = "emrecan/bert-base-turkish-cased-mean-nli-stsb-tr"
SENTENCE_TRANSFORMERS_ALL_MPNET_BASE_V2 = "sentence-transformers/all-mpnet-base-v2"

CROSS_ENCODER_MS_MARCO_MINILM_L6_V2 = "cross-encoder/ms-marco-MiniLM-L6-v2"

CROSS_ENCODER_K = 7
SKG_AGENT_SIMILAR_VECTOR_K = 10

GLOBAL_VECTOR_DB_INITIAL_EMBEDDING_MODEL = LABSE
GLOBAL_VECTOR_DB_INITIAL_CHUNK_SIZE = 500
GLOBAL_VECTOR_DB_INITIAL_CHUNK_OVERLAP = 50