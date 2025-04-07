from typing import List
from pydantic import BaseModel

class TopicExtraction(BaseModel):
    topics: List[str]

    @property
    def system_prompt(self):
        return f"""# Given Data
You are part of an AI agent flow.
- You are given two customer comments to a telecom company:
1. Improvement needed
2. Reason for given NPS

- You are also given a list of topics.

# Tasks
You have two tasks:
1. Find the relevant topics mentioned in the user's question among the give list of topics. This will go in the `detected_topics` list. Only put topics out of the given topics in this list.
2. If the user's comment has any topics which are not included in this list, put them in the `suggested_topics` list. Only put new topics in this list.

# Instructions
- You must only extract negative topics, or things that need improvement.

# Given Topics
{str(self.topics)}

# Response format
""" + """
{
    "detected_topics" : ["topic_1", "topic_2"],
    "suggested_topics" : ["topic_3", "topic_4"]
}""" + """

Respond with only a JSON of topics and nothing else.
"""