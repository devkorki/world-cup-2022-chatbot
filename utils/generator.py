# File: utils/generator.py
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    token=HF_TOKEN
)

class Generator:
    def __init__(self):
        self.client = client
        self.model_name = "mistralai/Mistral-7B-Instruct-v0.3"

    # def generate(self, prompt: str) -> str:
    #     messages = [
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": prompt},
    #     ]

    #     response = self.client.chat.completions.create(
    #         model=self.model_name,
    #         messages=messages,
    #         max_tokens=300,
    #     )
    #     return response.choices[0].message.content.strip()
    def generate(self, query: str, retrieved_docs: list, max_tokens: int = 300) -> str:
        if not retrieved_docs:
            prompt = (
                "You are a helpful assistant. The user asked a question, but there were no relevant tweets retrieved.\n\n"
                f"Question: {query}\n\n"
                "You must not make up an answer. Respond by saying that no relevant tweet-based information is available."
            )
        else:
            context = "\n".join([f"- {doc}" for doc, _ in retrieved_docs])
            prompt = (
                "You are a helpful assistant. Use ONLY the following tweets to answer the user's question.\n\n"
                f"Tweets:\n{context}\n\n"
                f"User Question: {query}\n\n"
                "Answer only based on the tweets. Do not use outside knowledge."
            )

        messages = [
            {"role": "system", "content": "You are a helpful assistant answering based only on user-provided tweets."},
            {"role": "user", "content": prompt},
        ]

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content.strip()



