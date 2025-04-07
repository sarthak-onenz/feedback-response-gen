import os
import boto3
from botocore.exceptions import ClientError
import json
from environment import AWS_SESSION_TOKEN, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
    region_name='ap-southeast-2'
)

bedrock_client = session.client('bedrock-runtime')


# Define the model ID
# model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
model_id = "anthropic.claude-3-sonnet-20240229-v1:0"


def llm_call_anthropic(user_message, system_prompt):
    
    if system_prompt:
        # Prepare the prompt data
        prompt_data = {
            "system" : system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "max_tokens": 4096,
            "anthropic_version": "bedrock-2023-05-31"
        }
        
        # Convert prompt data to JSON string
        body = json.dumps(prompt_data)
        
        try:
            print("Sending request to LLM")
            # Invoke the model
            response = bedrock_client.invoke_model(
                modelId=model_id,
                body=body,
                contentType='application/json'
            )
            
            # Read the response body as a string
            response_body = response['body'].read().decode('utf-8')
            
            # Parse the response body as JSON
            response_json = json.loads(response_body)

            print("Received response from LLM.")
            
            # Extract the model's response
            if 'content' in response_json and response_json['content']:
                model_response = response_json['content'][0]['text']
            else:
                model_response = "Model output not found."
            
            
            return model_response
        except ClientError as e:
            print("Error invoking model:", e)
            return None
    else:
        return None
    
    
