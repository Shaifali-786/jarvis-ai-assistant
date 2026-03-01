import json
import os
import datetime

KNOWLEDGE_FILE = "brain/knowledge.json"

def load_knowledge():
    if os.path.exists(KNOWLEDGE_FILE):
        with open(KNOWLEDGE_FILE, "r") as f:
            return json.load(f)
    return {}

def check_local_knowledge(command):
    knowledge = load_knowledge()
    command_lower = command.lower().strip()
    
    if command_lower in knowledge:
        response = knowledge[command_lower]
        if response == "__TIME__":
            return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}"
        if response == "__DATE__":
            return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}"
        return response
    
    for key, value in knowledge.items():
        if key in command_lower or command_lower in key:
            return value
    
    return None

def route_command(command):
    from modules.system_control import handle_system_command
    from brain.ai_engine import ask_groq

    # 1. System commands
    sys_response = handle_system_command(command)
    if sys_response and sys_response != "EXIT":
        return sys_response, "system"
    if sys_response == "EXIT":
        return "EXIT", "system"

    # 2. Local knowledge
    local_response = check_local_knowledge(command)
    if local_response:
        return local_response, "local"

    # 3. Groq AI
    ai_response = ask_groq(command)
    if ai_response:
        return ai_response, "ai"

    return "I don't know that yet, but I'm learning.", "unknown"