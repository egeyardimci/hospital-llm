from langchain_groq import ChatGroq
from backend.common.constants import CROSS_ENCODER_OPTION
from langchain.schema import SystemMessage, HumanMessage
from backend.ai.testing.models import RagResponse, TestOption
from langchain_chroma import Chroma
from backend.ai.graphdb.utils import neo4j_graph_search, format_graph_to_context
from backend.utils.logger import get_logger
from backend.common.constants import GRAPH_DB_OPTION, VECTOR_DB_OPTION, SELF_RAG_OPTION
from backend.ai.llm.self_rag.self_rag import use_self_rag
from backend.ai.llm.cross_encoder import use_cross_encoder

logger = get_logger()

def rag_invoke(llm_name: str, system_prompt: str, db: Chroma|None, similarity_vector_k: int, query: str, options: list[TestOption], rag_database: str) -> str:
    final_chunks = []


    if rag_database == GRAPH_DB_OPTION:
        # Use Neo4j graph database
        logger.info("Using Neo4j graph database for retrieval")
        graph_results = neo4j_graph_search(query, similarity_vector_k)
        context = format_graph_to_context(graph_results)

    elif rag_database == VECTOR_DB_OPTION:
        # Use traditional vector database
        logger.info("Using vector database for retrieval")
        retrieved_chunks = db.similarity_search(query, similarity_vector_k)
        logger.info(f"Retrieved {len(retrieved_chunks)} chunks from vector DB.")
        final_chunks = retrieved_chunks

        for option in options:
            if option.name == CROSS_ENCODER_OPTION and option.is_enabled:
                logger.info(f"Re-ranking with cross-encoder.")
                final_chunks = use_cross_encoder(option, query, retrieved_chunks)

            # Self-RAG will override CE if both are enabled
            elif option.name == SELF_RAG_OPTION and option.is_enabled:
                logger.info("Using Self-RAG option.")
                final_chunks = use_self_rag(option,query,db, k_per_retrieval=similarity_vector_k, final_k=similarity_vector_k)

        # Format context for vector DB
        context = "\n\n".join([f'Page Number: {chunk.metadata.get("page", "Unknown")}: {chunk.page_content}\n' for chunk in retrieved_chunks])

    # Use Groq API for response generation
    llm = ChatGroq(model=llm_name)
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}")
    ]
    response = llm.invoke(messages)

    return RagResponse(content=response.content,
                       metadata={
                           "query": query,
                           "system_prompt": system_prompt,
                           "retrieved_chunks": final_chunks
                       })