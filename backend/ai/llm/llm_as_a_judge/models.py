
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Union
class JudgeOutput(BaseModel):
    """
    The output of the LLM judge evaluation.
    
    Attributes:
        score: Numerical score from the judge (typically 1-5)
        feedback: Detailed explanation and reasoning from the judge
        reasoning: Optional step-by-step reasoning breakdown
    """
    
    score: int = Field(
        ...,  # Required field
        ge=1,  # Greater than or equal to 1
        le=5,  # Less than or equal to 5
        description="Numerical score determined by the LLM judge (1-5 scale)"
    )
    
    feedback: str = Field(
        ...,  # Required field
        min_length=10,  # Minimum 10 characters
        max_length=2000,  # Maximum 2000 characters
        description="Detailed explanation and reasoning from the LLM judge"
    )
    
    reasoning: Optional[Union[str, List[str]]] = Field(
        None,
        description="Step-by-step reasoning breakdown of how the score was determined"
    )

    criteria_met: Optional[List[str]] = Field(
        None,
        description="List of evaluation criteria that were met in the response"
    )
    
    
    @field_validator('score')
    @classmethod
    def validate_score(cls, v):
        """Ensure score is within valid range."""
        if not isinstance(v, int):
            raise ValueError('Score must be an integer')
        if v < 1 or v > 5:
            raise ValueError('Score must be between 1 and 5')
        return v
    
    @field_validator('feedback')
    @classmethod
    def validate_feedback(cls, v):
        """Ensure feedback is meaningful and not empty."""
        if not v or v.strip() == "":
            raise ValueError('Feedback cannot be empty or whitespace only')
        return v.strip()
    
    @field_validator('reasoning', mode='before')
    @classmethod
    def normalize_reasoning(cls, v):
        """Normalize reasoning to always be a string."""
        if v is None:
            return None
        if isinstance(v, list):
            # Join list items with newlines for better readability
            return "\n".join(str(item) for item in v)
        return str(v)
    
    class Config:
        """Pydantic configuration."""
        # Validate assignment to catch errors early
        validate_assignment = True
        
        # Allow extra fields in case you need flexibility
        extra = "forbid"  # Change to "allow" if you want to accept extra fields
        
        # Example for JSON schema generation
        json_schema_extra = {
            "example": {
                "score": 2,
                "feedback": "The response adequately addresses most key points about medical participation fees, including specific information about different branches and relevant regulations. However, it could provide more detail about hospital-specific variations.",
                "reasoning": "Response covered 4 out of 5 required criteria with good detail level",
            }
        }
