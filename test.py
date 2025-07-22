from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

# Load your Hugging Face token from .env file (if using)
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Initialize the inference client
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    token=HF_TOKEN
)

# Basic system prompt + user prompt
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]

# Make the request
response = client.chat.completions.create(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    messages=messages,
    max_tokens=100,
)

# Print the response
print("Mistral response:", response.choices[0].message.content)
