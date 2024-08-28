import json 
import os 
from openai import AzureOpenAI


os.environ["AZURE_OPENAI_API_KEY"] = "XXX"
os.environ["AZURE_OPENAI_ENDPOINT"] = "YYY"

# Retrieve the environment variables
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

deployment = 'gpt-4o-mini-ozguler'


from openai import AzureOpenAI
    
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-06-01",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

# Define a simple schema for structured output
sentiment_analysis_function = {
    "type": "function",
    "function": {
        "name": "analyze_sentiment",
        "description": "Extract the sentiment of the review",
        "parameters": {
            "type": "object",
            "properties": {
                "sentiment": {
                    "type": "string",
                    "description": "The sentiment of the review",
                    "enum": ["Positive", "Neutral", "Negative"]
                }
            },
            "required": ["sentiment"]
        }
    },
    "strict": True  # Enforce the structured output
}

# Simple test input
user_input = "I love this product, it's fantastic!"

# Function to get a response from the model
def get_response(user_input):
    response = client.chat.completions.create(
        model=deployment,
        temperature=0.7,
        messages=[
            {"role": "system", "content": "You are a sentiment analyzer."},
            {"role": "user", "content": user_input}
        ],
        tools=[sentiment_analysis_function]
    )

    # Extract the arguments from the tool call
    tool_call = response.choices[0].message.tool_calls[0]
    return tool_call.function.arguments

# Get and print the response
response = get_response(user_input)
print(json.dumps(json.loads(response), indent=2))
