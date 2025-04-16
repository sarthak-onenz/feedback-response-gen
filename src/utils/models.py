from pydantic import BaseModel, validator
from typing import List

class Topic(BaseModel):
    topic_name: str
    resolution_statement: str
    examples: List[str] = None
    count: int = 0
    embedding: List = None
    importance_score: int = 1  # Default to 1 (least important)

    @validator('importance_score')
    def validate_importance_score(cls, v):
        if not (1 <= v <= 5):
            raise ValueError('importance_score must be between 1 and 5')
        return v

class EscalationTopic(BaseModel):
    statement: str
    embedding: List = None