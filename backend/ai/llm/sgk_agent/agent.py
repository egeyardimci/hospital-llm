from backend.ai.llm.prompts import SGK_AGENT_SYSTEM_PROMPT
from backend.ai.testing.models import RagResponse
from backend.common.config import SKG_AGENT_SIMILAR_VECTOR_K
from backend.ai.vectordb.main import GLOBAL_VECTOR_DB
from backend.ai.llm.rag import rag_invoke
from backend.common.constants import VECTOR_DB_OPTION

def sgk_agent(llm_name, query, options):
    """
    Run a single test with the given parameters and save the results to a JSON file.
    """
    vector_db = GLOBAL_VECTOR_DB.get_db()
    response: RagResponse = rag_invoke(llm_name, SGK_AGENT_SYSTEM_PROMPT, vector_db, SKG_AGENT_SIMILAR_VECTOR_K, query, options, VECTOR_DB_OPTION)

    return response