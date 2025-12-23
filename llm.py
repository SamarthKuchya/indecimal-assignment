import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  
model = "openai/gpt-4o-mini"

def get_response(query):
    response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer " + OPENROUTER_API_KEY,
  },

  data=json.dumps({
    "model": model,
    "messages": [
      {
        "role": "user",
        "content": query
      }
    ]
  })
)
    return response.json()["choices"][0]["message"]["content"]
