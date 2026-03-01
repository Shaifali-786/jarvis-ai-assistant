import webbrowser
import urllib.parse

def handle_web_command(command):
    command = command.lower()
    
    # Google search
    if "search" in command or "google" in command or "look up" in command:
        query = command.replace("search", "").replace("google", "").replace("look up", "").strip()
        if query:
            url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            webbrowser.open(url)
            return f"Searching Google for {query}"
    
    # YouTube
    if "youtube" in command:
        query = command.replace("youtube", "").replace("play", "").strip()
        if query:
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
            webbrowser.open(url)
            return f"Opening YouTube for {query}"
    
    # Open website directly
    if "open" in command and "." in command:
        words = command.split()
        for word in words:
            if "." in word and word not in ["open", "jarvis"]:
                webbrowser.open(f"https://{word}")
                return f"Opening {word}"
    
    return None