from pydantic import BaseModel

class Topic(BaseModel):
    topic_name: str
    resolution_statement: str