import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROK_API")  # sirf yahi ek line rakho


MEMORY_FILE = "brain/memory.json"


SYSTEM_PROMPT = """You are Jarvis, a smart AI assistant and robot built by Shaif.
Be helpful, concise and intelligent. Keep responses short since they will be spoken aloud.
Always address the user as Shaif.

STRICT LANGUAGE RULES - VERY IMPORTANT:
- Detect the language of user's message carefully
- If user message is in ENGLISH → reply in ENGLISH only
- If user speaks HINDI → reply in simple spoken HINDI only (easy words, not bookish)
- If user speaks HINGLISH → reply in ENGLISH
- NEVER mix languages in one response
- Hindi replies must be natural conversational Hindi, not translated English"""


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    return []

def save_memory(history):
    history = history[-20:]
    with open(MEMORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def ask_groq(user_input):
    history = load_memory()
    history.append({"role": "user", "content": user_input})
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + history,
                "max_tokens": 300,  # 150 se 300 karo — longer answers
                "temperature": 0.8,  # thoda creative
            },
            timeout=10
        )
        print(f"[Groq Status] {response.status_code}")
        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            history.append({"role": "assistant", "content": reply})
            save_memory(history)
            return reply
        else:
            print(f"[Groq Error] {response.text}")
            return None
    except Exception as e:
        print(f"[Groq Exception] {e}")
        return None