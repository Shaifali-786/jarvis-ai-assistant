import re

# Words to strip from commands
FILLER_WORDS = ["please", "can you", "could you", "jarvis", "hey", "ok", "okay", "um", "uh"]

def normalize_command(text):
    """Clean and normalize spoken command."""
    if not text:
        return ""
    
    text = text.lower().strip()
    
    # Remove filler words
    for word in FILLER_WORDS:
        text = text.replace(word, "")
    
    # Remove extra spaces and punctuation
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[^\w\s]', '', text)
    
    return text

def classify_intent(command):
    """Classify what the user wants."""
    command = command.lower()
    
    if any(w in command for w in ["open", "launch", "start", "run"]):
        return "open_app"
    elif any(w in command for w in ["close", "quit", "exit", "kill"]):
        return "close_app"
    elif any(w in command for w in ["volume", "mute", "louder", "quieter"]):
        return "volume_control"
    elif any(w in command for w in ["search", "google", "look up", "find"]):
        return "web_search"
    elif any(w in command for w in ["time", "date", "day", "today"]):
        return "datetime_query"
    elif any(w in command for w in ["weather"]):
        return "weather"
    elif any(w in command for w in ["shutdown", "restart", "sleep"]):
        return "power_control"
    else:
        return "general_query"