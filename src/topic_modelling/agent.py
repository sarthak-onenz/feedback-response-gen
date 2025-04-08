import json
import pandas as pd
from typing import List, Dict
from utils.llm import llm_call_anthropic
from utils.models import Topic
from topic_modelling.prompts import TopicExtraction

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
        extracted_topics = json.loads(llm_response)
        return extracted_topics
    except Exception as e:
        print("ERROR", e, llm_response)
        if retries > 0:
            return extract_topics_from_user_message(user_message=user_message, topics=topics, retries=retries-1)
        else:
            return {
                        "detected_topics" : [],
                        "suggested_topics" : []
                    }
        

def create_topic_objects_from_extracted_topics(
    extracted_topics: Dict[str, List[str]],
    topic_resolution_file_path: str
) -> List[Topic]:
    """
    Create Topic objects from extracted topic names by looking up their resolution statements in an Excel file.

    Args:
        extracted_topics: A dict with keys 'detected_topics' and 'suggested_topics' containing topic names.
        topic_resolution_file_path: Path to the Excel file containing 'Topic' and 'Resolution_or_comment' columns.

    Returns:
        A list of Topic objects.
    """
    # Load the resolution file
    df = pd.read_excel(topic_resolution_file_path)
    
    # Normalize topic column to enable fuzzy matching (if needed)
    df["Topic"] = df["Topic"].str.lower().str.strip()

    topic_objects = []
    for topic in extracted_topics["detected_topics"] + extracted_topics["suggested_topics"]:
        normalized_topic = topic.lower().strip()
        row = df[df["Topic"].str.contains(normalized_topic, na=False)]

        resolution_statement = row["Resolution_or_comment"].values[0] if not row.empty else "No resolution found."
        topic_objects.append(Topic(topic_name=topic, resolution_statement=str(resolution_statement)))
    
    return topic_objects
