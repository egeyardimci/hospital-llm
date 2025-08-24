from backend.ai.testing.models import TestCase
from backend.utils.logger import log, log_test
from backend.ai.llm.cross_encoder import rerank_with_cross_encoder
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from backend.ai.llm.prompts import SGK_AGENT_SYSTEM_PROMPT
from backend.common.constants import SKG_AGENT_SIMILAR_VECTOR_K, CROSS_ENCODER_K
from backend.ai.vectordb.main import GLOBAL_VECTOR_DB

def sgk_agent(llm_name, query, options):
    """
    Run a single test with the given parameters and save the results to a JSON file.
    """

    vector_db = GLOBAL_VECTOR_DB.get_db()

    # Querying the document
    retrieved_chunks = vector_db.similarity_search(query, SKG_AGENT_SIMILAR_VECTOR_K)
    
    cross_encoder_option = None
    for option in options:
        if option.name == "CE" and option.is_enabled:
            cross_encoder_option = option
            break
    if cross_encoder_option:
        cross_encoder_model_name = cross_encoder_option.data
        top_k = CROSS_ENCODER_K

        if isinstance(cross_encoder_option.data, dict):
            cross_encoder_model_name = cross_encoder_option.data.get("model_name")
            top_k = cross_encoder_option.data.get("top_k", top_k)
        
        log(f"Re-ranking with cross-encoder: {cross_encoder_model_name}")
        retrieved_chunks = rerank_with_cross_encoder(
            query, 
            retrieved_chunks, 
            cross_encoder_model_name,
            top_k
        )
    
    context = "\n\n".join([f'Page Number: {chunk.metadata.get("page", "Unknown")}: {chunk.page_content}\n' for chunk in retrieved_chunks])

    
    # Use Groq API for response generation
    llm = ChatGroq(model=llm_name)
    messages = [
        SystemMessage(content=SGK_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}")
    ]
    response = llm.invoke(messages)
    
    return response.content