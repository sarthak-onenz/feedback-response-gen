# Runtime

1. Access feedback survey responses data from Snowflake.
2. Parse into a standard structure.
3. Use topic modelling to find the topic(s) of the survey response.
    - Match it against existing vectordb of topics.
    - If a new topic exists, add it to the primary vectordb.
    - If it doesn't exist, then search it against the secondary vectordb.
        - If it does exist, increment the count in the metadata.
        - If it doesn't exist, add it.
    - If it does exist, then return the entry along with the metadata.
    - Use an LLM to find, out of the search results, which are the issues actually present in the user's feedback.
4. Return the resolution for these issues.
5. If required, also send a Teams message or email to the concerned team.

# Adding knowledge

1. For all responses in the secondary vectordb, rank them by count.
2. Have a human validate them and add the resolution for them.
3. Add the validates ones the primary vectordb.