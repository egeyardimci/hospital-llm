from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class SelfRAGOutput(BaseModel):
    """
    The output of the Self-RAG agent for chunk selection.

    Attributes:
        selected_indices: List of chunk indices ordered by relevance (most relevant first)
        reasoning: Optional explanation of why these chunks were selected
        relevance_scores: Optional relevance scores for each selected chunk (1-5 scale)
    """

    selected_indices: List[int] = Field(
        ...,  # Required field
        min_length=1,
        description="List of chunk indices ordered by relevance (most relevant first)"
    )

    reasoning: Optional[str] = Field(
        None,
        max_length=1000,
        description="Brief explanation of why these chunks were selected"
    )

    relevance_scores: Optional[List[int]] = Field(
        None,
        description="Relevance scores (1-5) for each selected chunk, in same order as selected_indices"
    )

    @field_validator('selected_indices')
    @classmethod
    def validate_indices(cls, v):
        """Ensure indices are valid and unique."""
        if not v:
            raise ValueError('At least one chunk index must be selected')

        # Check for duplicates
        if len(v) != len(set(v)):
            raise ValueError('Chunk indices must be unique')

        # Ensure all values are non-negative integers
        for idx in v:
            if not isinstance(idx, int) or idx < 0:
                raise ValueError('All indices must be non-negative integers')

        return v

    @field_validator('relevance_scores')
    @classmethod
    def validate_scores(cls, v, info):
        """Ensure relevance scores match selected indices if provided."""
        if v is None:
            return None

        # Check that all scores are between 1 and 5
        for score in v:
            if not isinstance(score, int) or score < 1 or score > 5:
                raise ValueError('Relevance scores must be integers between 1 and 5')

        # If selected_indices is available in values, check length matches
        if 'selected_indices' in info.data:
            selected_indices = info.data['selected_indices']
            if len(v) != len(selected_indices):
                raise ValueError(
                    f'Number of relevance scores ({len(v)}) must match '
                    f'number of selected indices ({len(selected_indices)})'
                )

        return v

    class Config:
        """Pydantic configuration."""
        # Validate assignment to catch errors early
        validate_assignment = True

        # Forbid extra fields to ensure strict schema compliance
        extra = "forbid"

        # Example for JSON schema generation
        json_schema_extra = {
            "example": {
                "selected_indices": [3, 7, 1, 5, 2],
                "reasoning": "Selected chunks 3 and 7 as they directly address the query topic. Chunks 1, 5, and 2 provide supporting context.",
                "relevance_scores": [5, 5, 4, 4, 3]
            }
        }
