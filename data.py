"""
This file contains the data for the tests to be run.

llm_names: List of LLM names to be used for the tests.
embedding_model_names: List of embedding model names to be used for the tests.
system_messages: List of system messages to be used for the tests.
chunk_sizes_and_chunk_overlaps: List of tuples containing chunk sizes and chunk overlaps to be used for the tests.
similar_vector_counts: List of similar vector counts to be used for the tests.
queries: List of queries to be used for the tests.
document_name: Name of the document to be used for the tests and db creation.
"""

llm_names = [
    "llama-3.1-8b-instant",
]

embedding_model_names = [
    "sentence-transformers/all-MiniLM-L6-v2",
]

system_messages = [
    """
    You are a helpful assistant. Answer based on the provided context do NOT use any other information you have. 
    If you can not answer the question with the data provided in context say it. 
    Give the reference to where you find the relevant information!
    Your customer is talking only Turkish so give answers in Turkish.""",
]

chunk_sizes_and_chunk_overlaps = [
    (500, 50),
]

similar_vector_counts = [
    10,
]

queries= [
    "Ayakta tedavide kullanılan tıbbi malzemeler ne zaman kurum tarafından ödenir?",
]

document_name = "doc.docx"