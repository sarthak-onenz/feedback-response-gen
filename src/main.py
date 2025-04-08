from typing import List

from utils.constants import CURRENT_TOPICS, topic_resolution_file_path
from utils.models import Topic

from topic_modelling.agent import format_user_message, extract_topics_from_user_message, create_topic_objects_from_extracted_topics
from response_generation.pipeline import generate_email


def main(improvement_needed: str, reason_for_given_nps: str):
    user_message = format_user_message(improvement_needed=improvement_needed,
                                       reason_for_given_nps=reason_for_given_nps)
    if user_message:
        extracted_topics = extract_topics_from_user_message(topics=CURRENT_TOPICS,
                                                           user_message=user_message)
        
        topics: List[Topic] = create_topic_objects_from_extracted_topics(extracted_topics=extracted_topics,
                                                   topic_resolution_file_path=topic_resolution_file_path)
        
        generated_email = generate_email(user_message=user_message, topics=topics)
        return generated_email