from typing import List
from pydantic import BaseModel

class TopicExtraction(BaseModel):
    topics: List[str]
    escalation_topics: List[str]

    @property
    def system_prompt(self):
        return f"""You are part of an AI agent flow.

# Given Data
1. You are given two customer comments to a telecom company:
- Improvement needed
- Reason for given NPS

2. You are also given a dataset of topics:
- Topics/issues mentioned by the 

# Tasks
You have two tasks:
1. Find the relevant topics mentioned in the user's question among the give list of topics. This will go in the `detected_topics` list. Only put topics out of the given topics dataset in this list.
2. If the user's comment has any topics which are not included in this list, put them in the `suggested_topics` list. Only put new topics in this list.
3. If the user's comment mentions any of the "escalation topics", put them in the `escalation_topics` list.

# Instructions
- *Only need negative topics:* You must only extract negative feedback/topics, or things that need improvement. If the customer has not given any negative feedback, both lists should be empty.
- *Mutually exclusive topics only:* All the topics must be completely mutually exclusive of each other. Each topic must be distinct.
- *How to name topics:* Each topic you create must be 4-5 words. Make sure that the topic name is descriptive enough yet succint.
- *When to create topics:* ONLY create a new topic if a similar topic doesn't exist in the given topics dataset already.

# Given Topics Dataset
`{str(self.topics)}`

# Escalation Topics Dataset
`{str(self.escalation_topics)}`

# Response format
""" + """
{
    "detected_topics" : ["topic_1", "topic_2"],
    "suggested_topics" : ["topic_3", "topic_4"],
    "escalation_topics: : ["topic_5"]
}""" + """

Respond with only a JSON of topics and nothing else.
"""