import pandas as pd
from slugify import slugify

chromadir = "vectordb"
topics_collection_name = slugify("topics_collection")
escalation_topics_collection_name = slugify("escalation_topics_collection")

CURRENT_TOPICS =  ["customer_wants_cheaper_pricing_plans", "slow_laggy_internet_speed"]
topic_resolution_file_path = "output_topics_data/topics_by_count.xlsx"
current_topics_df = pd.read_excel(topic_resolution_file_path)
#CURRENT_TOPICS = current_topics_df["Topic"].to_list()

escalation_topic_resolution_file_path = "output_topics_data/escalation_topics_by_count.xlsx"
escalation_topics_df = pd.read_excel(escalation_topic_resolution_file_path)
ESCALATION_TOPICS = escalation_topics_df["Topic"].to_list()

N_EXAMPLES_OF_EACH_TOPIC = 5

useful_cols_and_completed_df = "input_feedback_data/snowflake_data/useful_cols_and_completed_df.csv"