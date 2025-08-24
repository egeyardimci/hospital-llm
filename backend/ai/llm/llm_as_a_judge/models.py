
from pydantic import BaseModel, Field

class JudgeOutput(BaseModel):
    """
    The output of the LLM judge.
    """
    score: int = Field(
        description="Score determined by the LLM judge"
    )
    output: str = Field(
        description="The output of the LLM judge. It should be a string that all the output of the LLM judge"
    )
