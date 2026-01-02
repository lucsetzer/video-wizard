# utils/ai_client.py
import requests
from .config import DEEPSEEK_KEY

def enhance_prompt(goal: str, audience: str, prompt: str) -> str:
    system_prompt = f"""You are a prompt engineering expert..."""
    
    response = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={"Authorization": f"Bearer {DEEPSEEK_KEY}"},
        json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        }
    )
    
    return response.json()["choices"][0]["message"]["content"]
