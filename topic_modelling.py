import json
import pandas as pd
from typing import List
from llm import llm_call_anthropic
from prompts import TopicExtraction

def format_user_message(improvement_needed: str, reason_for_given_nps: str):
    user_message = ""
    if improvement_needed and pd.notna(improvement_needed) and len(improvement_needed) > 4:
        user_message += f"""Improvement needed: {improvement_needed}\n"""
    if reason_for_given_nps and pd.notna(reason_for_given_nps) and len(reason_for_given_nps) > 4:
        user_message += f"""Reason for given NPS: {reason_for_given_nps}"""
    return user_message

def extract_topics_from_user_message(user_message: str, topics: List[str], retries: int=5):
    try:
        topic_extraction_system_prompt = TopicExtraction(topics=topics).system_prompt
        llm_response = llm_call_anthropic(system_prompt=topic_extraction_system_prompt, user_message=user_message)
        print("llm response", llm_response)
        topics_list = json.loads(llm_response)
        return topics_list
    except Exception as e:
        print("ERROR", e, llm_response)
        if retries > 0:
            return extract_topics_from_user_message(user_message=user_message, topics=topics, retries=retries-1)
        else:
            return {
                        "detected_topics" : [],
                        "suggested_topics" : []
                    }