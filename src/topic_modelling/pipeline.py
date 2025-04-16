import pandas as pd
from tqdm.notebook import tqdm
import json
from typing import Dict

from utils.models import Topic, EscalationTopic
from utils.constants import CURRENT_TOPICS, N_EXAMPLES_OF_EACH_TOPIC, useful_cols_and_completed_df
from utils.llm import get_embedding
from topic_modelling.agent import extract_topics_from_user_message, format_user_message
from topic_modelling.vectordb import create_topics_vectordb
from escalation.vectordb import create_escalation_topics_vectordb

useful_cols_and_completed_df = pd.read_csv(useful_cols_and_completed_df)#[:10]

def extract_topics_from_all_survey_responses():
    print("Topic modelling on", len(useful_cols_and_completed_df), "survey responses")

    current_topics_with_count = {}
    for i, topic in enumerate(CURRENT_TOPICS):
        print(f"Extracting embedding from given topic {str(i)} / {str(len(useful_cols_and_completed_df))}")
        current_topics_with_count[topic] = Topic(topic_name=topic,
                                            resolution_statement="",
                                            examples = [],
                                            count = 0,
                                            embedding=get_embedding(topic)
                                            )
                                
    for i, row in useful_cols_and_completed_df.iterrows():
        improvement_needed = row["NZ_RELATIONSHIP_IMPORTANT_IMPROVEMENT_CMT"]
        reason_for_given_nps = row["NZ_RELATIONSHIP_NPS_REASON_CMT"]

        user_message = format_user_message(improvement_needed=improvement_needed,
                                        reason_for_given_nps=reason_for_given_nps)
        if user_message:        
            print(f"Extracting topics from response {str(i)} / {str(len(useful_cols_and_completed_df))}")
            print(user_message)
            topics_response = extract_topics_from_user_message(topics=list(current_topics_with_count.keys()),
                                                               escalation_topics=[],
                                                            user_message=user_message)
            if topics_response:
                for topic in topics_response["detected_topics"] + topics_response["suggested_topics"]:
                    if topic in current_topics_with_count:
                        current_topics_with_count[topic].count += 1
                        if len(current_topics_with_count[topic].examples) < N_EXAMPLES_OF_EACH_TOPIC:
                            current_topics_with_count[topic].examples += [user_message]
                    else:
                        current_topics_with_count[topic] = Topic(topic_name=topic,
                                                                resolution_statement="",
                                                                count=1,
                                                                examples=[user_message],
                                                                embedding=get_embedding(topic)
                                                                )
                print("\n\n----------------------------------------------------------\n\n")

    print("Extracted", len(current_topics_with_count), "topics")
    return current_topics_with_count        


def export_topics_data(current_topics_with_count: Dict[str, Topic]):
    # Extract data into rows
    rows = [{
        "Topic": topic.topic_name,
        "Count": topic.count,
        "Resolution": topic.resolution_statement,
        "Examples" : topic.examples,
        "Embedding" : topic.embedding,
        "Importance_score" : topic.importance_score
    } for topic in current_topics_with_count.values()]

    with open("output_topics_data/topics_by_count.json", "w+") as f:
        json.dump(rows, f)

    # Convert to DataFrame and sort
    df = pd.DataFrame(rows)
    df_sorted = df.sort_values(by="Count", ascending=False)

    # Export to Excel
    excel_path = "output_topics_data/topics_by_count.xlsx"
    df_sorted.to_excel(excel_path, index=False)

    # Export to CSV
    csv_path = "output_topics_data/topics_by_count.csv"
    df_sorted.to_csv(csv_path, index=False)

    print(f"Topics exported to: {excel_path} and {csv_path}")


def run_topic_modelling_pipeline():
    # For topics
    try:        
        with open("output_topics_data/topics_by_count.json", "r") as f:
            topics_by_count = json.load(f)
            current_topics_with_count = {topic["Topic"] : Topic(
                                                                topic_name=topic["Topic"],
                                                                count=topic["Count"],
                                                                resolution_statement=topic["Resolution"],
                                                                examples=topic["Examples"],
                                                                embedding=topic["Embedding"],
                                                                importance_score=topic["Importance_score"]
                                                            ) for topic in topics_by_count}

    except Exception as e:
        print("ERROR in run_topic_modelling_pipeline", e)    
        current_topics_with_count = extract_topics_from_all_survey_responses()
        export_topics_data(current_topics_with_count)

    create_topics_vectordb(topics=list(current_topics_with_count.values()))

    # For escalation topics
    escalation_topics = ["my house burned down in a fire"]
    escalation_topics = [EscalationTopic(statement=topic) for topic in escalation_topics]
    create_escalation_topics_vectordb(escalation_topics=escalation_topics)

