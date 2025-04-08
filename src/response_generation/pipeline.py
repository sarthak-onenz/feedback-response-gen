from typing import List

from response_generation.prompts import ResponseGen
from utils.models import Topic
from utils.llm import llm_call_anthropic

def generate_email(user_message: str, topics: List[Topic]):
    response_generation_system_prompt = ResponseGen(topics=topics).system_prompt
    llm_response = llm_call_anthropic(user_message=user_message, system_prompt=response_generation_system_prompt)
    return llm_response
