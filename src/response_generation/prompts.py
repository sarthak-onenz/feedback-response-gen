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
        return f"""# Task
You are writing an email as a customer support representative at One New Zealand, a telecom company in New Zealand.

# Given Data
You are given a list of issues mentioned by the user in their survey response, and for each issue you are given the resolution as well.

# Instructions
- Each resolution is provided to you as an email. You must combine the emails without rephrasing the content too much.
- Address each issue in a single email which maintains the tone of voice in the resolution emails given to you.
- Generate an email addressing the user's concerns mentioned below.

# Given Issues and Resolutions
{self.formatted_topics_list}
"""
    
