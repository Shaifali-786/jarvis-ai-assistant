import json

KNOWLEDGE_FILE = "brain/knowledge.json"

def load_knowledge():
    with open(KNOWLEDGE_FILE, "r") as f:
        return json.load(f)

def save_knowledge(data):
    with open(KNOWLEDGE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def try_learn(command):
    """
    Detects: 'remember that capital of france is paris'
    Or:      'your name is jarvis'
    """
    command = command.lower()
    
    if "remember that" in command:
        # "remember that X is Y"
        part = command.replace("remember that", "").strip()
        if " is " in part:
            key, value = part.split(" is ", 1)
            knowledge = load_knowledge()
            knowledge[key.strip()] = value.strip()
            save_knowledge(knowledge)
            return f"Got it! I'll remember that {key.strip()} is {value.strip()}."
    
    if "my name is" in command:
        name = command.replace("my name is", "").strip()
        knowledge = load_knowledge()
        knowledge["user name"] = name
        save_knowledge(knowledge)
        return f"Nice to meet you, {name}! I'll remember that."
    
    return None