# Topic modelling

1. Access feedback survey responses data from Snowflake.
2. Parse into a standard structure.
3. Use topic modelling to find the topic(s) of the survey response by following these steps:
    - Search the user message against existing vectordb of topics.
    - Give the retrieved topics and user message to an LLM, asking it to give the topics which exist in the list and suggest new topics.
    - Increment the count of all topics found in the user message.


# Response generation

1. All topics are stored in an Excel sheet, along with a count of how often they are mentioned by users. The brand team can fill out the resolutions/comments we want to send to customers for each topic.
2. Retrieve the resolution for all topics mentioned by a customer at runtime.
3. Give the user's original message, and the resolution for each topic, to an LLM, and ask it to generate a personalised email to them.
4. Have a human at the brand team review the email and send it to the customer.
