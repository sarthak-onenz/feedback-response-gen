from typing import List

from utils.constants import topic_resolution_file_path
from utils.models import Topic
from utils.llm import get_embedding

from topic_modelling.agent import format_user_message, extract_topics_from_user_message, create_topic_objects_from_extracted_topics, rank_and_filter_topics
from topic_modelling.vectordb import vector_search_topics
from escalation.vectordb import vector_search_escalation_topics
from response_generation.pipeline import generate_email

from sarthakai.models import VectorSearchResponse

def main(improvement_needed: str, reason_for_given_nps: str):
    """
    Runtime pipeline
    """
    user_message = format_user_message(improvement_needed=improvement_needed,
                                       reason_for_given_nps=reason_for_given_nps)
    if user_message:
        # Step 1: Vector search relevant topics
        user_message_embedding = get_embedding(user_message)
        topics_vector_search_results: List[VectorSearchResponse] = vector_search_topics(user_message=user_message,
                                                                                        embedding=user_message_embedding)
        possible_topics = [search_result.document for search_result in topics_vector_search_results]
        
        escalation_topics_vector_search_results: List[VectorSearchResponse] = vector_search_escalation_topics(user_message=user_message,
                                                                                                              embedding=user_message_embedding)
        possible_escalation_topics = [search_result.document
                                      for search_result
                                      in escalation_topics_vector_search_results]
        print("Vector search results\n Topics", possible_topics, "\n Escalation topics", possible_escalation_topics)
        
        
        # Step 2: Get LLM response
        extracted_topics = extract_topics_from_user_message(topics=possible_topics,
                                                            escalation_topics=possible_escalation_topics,
                                                            user_message=user_message)
        
        if extracted_topics["escalation_topics"]:
            return "needs_escalation", "Email not generated because escalation is required."
                        
        else:
           
            # Step 3: Create Topic objects
            topics: List[Topic] = create_topic_objects_from_extracted_topics(extracted_topics=extracted_topics,
                                                   topic_resolution_file_path=topic_resolution_file_path)                    
            topics: List[Topic] = rank_and_filter_topics(topics=topics)
            
            if topics:
                
                # Step 4: Generate email
                print("Generating email based on topics", topics)
                generated_email = generate_email(user_message=user_message, topics=topics)
                return "success", generated_email
            
    return "failure", "Email not generated because of incomplete information."