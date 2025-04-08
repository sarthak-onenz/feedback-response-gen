import snowflake.connector
import pandas as pd

# Establish connection using Azure AD SSO
conn = snowflake.connector.connect(
    user="SARTHAK.RASTOGI@ONE.NZ",
    account="vodafonenz-prod",
    authenticator="externalbrowser",
    warehouse="PROD_ENPS_WH",
    database="PROD_ENPS",
    schema="SERVING"
)

# Define the view you want to query
view_name = "V_MDL_EPISODIC_PIVOTED"


import pandas as pd

# Define the useful columns
useful_cols = [
    "NZ_USE_IMPORTANT_IMPROVEMENT_CMT", "NZ_USE_QUERY_TOPIC_ALT", "NZ_USE_QUERY_TOPIC_OTHER_TXT",
    "NZ_CHANGE_IMPORTANT_IMPROVEMENT_CMT", "NZ_CHANGE_OVERALL_SATISFACTION_REASON_CMT",
    "NZ_JOIN_GENERAL_SATISFACTION_REASON_CMT", "NZ_JOIN_IMPORTANT_IMPROVEMENT_CMT",
    "NZ_RELATIONSHIP_IMPORTANT_IMPROVEMENT_CMT", "NZ_RELATIONSHIP_NPS_REASON_CMT",
    "NZ_USE_CSAT_REASON_CMT"
]

def extract_feedback_data_from_snowflake(limit: int = 400) -> pd.DataFrame:
    """
    Extracts useful feedback data from a Snowflake view.

    Args:
        limit (int, optional): Number of rows to fetch. Defaults to 400.

    Returns:
        pd.DataFrame: A DataFrame containing only the useful feedback columns.
    """
    # Format column list for SQL
    cols_str = ", ".join(useful_cols)

    # Build query
    query = f"SELECT {cols_str} FROM {view_name} LIMIT {limit}"

    # Execute query
    df = pd.read_sql(query, conn)

    print(df.head())

    return df
