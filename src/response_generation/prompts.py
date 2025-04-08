from pydantic import BaseModel
from typing import List

from utils.models import Topic

class ResponseGen(BaseModel):
    topics: List[Topic]

    @property
    def formatted_topics_list(self):
        formatted_topics = ""
        for topic in self.topics:
            formatted_topics += f"""*Topic:* {topic.topic_name}

*Resolution:* {topic.resolution_statement}
"""
        return formatted_topics


    @property
    def system_prompt(self):
        return f"""Generate an email addressing the user's concerns mentioned below.

# Topics
{self.formatted_topics_list}
"""
    
