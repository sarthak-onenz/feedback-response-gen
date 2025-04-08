import pandas as pd

topic_resolution_file_path = "output_topics_data/topics_by_count.xlsx"
chromadir = "vectordb"
topics_collection_name = "topics_collection"

# CURRENT_TOPICS =  ["customer_wants_cheaper_pricing_plans", "slow_laggy_internet_speed"]
df = pd.read_excel(topic_resolution_file_path)
CURRENT_TOPICS = df["Topic"].to_list()

N_EXAMPLES_OF_EACH_TOPIC = 5
