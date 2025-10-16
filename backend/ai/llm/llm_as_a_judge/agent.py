from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from backend.ai.llm.llm_as_a_judge.models import JudgeOutput
from backend.ai.llm.prompts import EVALUATION_PROMPT, CHUNK_EVALUATION_PROMPT
from backend.common.constants import OPENAI_GPT_OSS_120B

def llm_as_a_judge(query: str, response: str, expected_answer: str,chunks) -> str:
    """
    Turkish-specific LLM judge with language-aware evaluation.
    """

    llm = ChatGroq(model=OPENAI_GPT_OSS_120B)

    messages = [
        SystemMessage(content="You are an LLM as a judge being used in a RAG system."),
        HumanMessage(content=EVALUATION_PROMPT.format(
            instruction=query,
            expected_answer=expected_answer,
            response=response
        ))
    ]
    
    llm = llm.with_structured_output(JudgeOutput)
    evaluation = llm.invoke(messages)

    chunk_evaluation_messages=[
        SystemMessage(content="You are an LLM as a judge being used in a RAG system."),
        HumanMessage(content=CHUNK_EVALUATION_PROMPT.format(
            query=query,
            chunks=chunks
        ))
    ]
    
    chunk_evaluation = llm.invoke(chunk_evaluation_messages)

    return evaluation, chunk_evaluation
