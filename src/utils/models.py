from pydantic import BaseModel
from typing import List

class Topic(BaseModel):
    topic_name: str
    resolution_statement: str
    examples: List[str] = None
    count: int = 0
    embedding: List = None

class EscalationTopic(BaseModel):
    statement: str
    embedding: List = None