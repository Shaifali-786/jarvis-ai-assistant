from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("GROK_API")

from core.voice_engine import speak, stop_speaking, is_speaking
from core.wake_listener import listen_once
from core.router import route_command
from core.command_processor import normalize_command
from modules.learning import try_learn
from modules.reminder import set_reminder
from modules.web_control import handle_web_command
import time

speak("Jarvis activated. All systems ready, Shaif.")
time.sleep(4)

WAKE_WORDS = ["jarvis", "hey jarvis", "ok jarvis"]
EXIT_WORDS = ["shutdown", "goodbye", "turn off", "bye jarvis"]

conversation_mode = False

def handle_command(command):
    if not command:
        return False

    if any(w in command for w in EXIT_WORDS):
        speak("Shutting down Jarvis. Goodbye Shaif.")
        time.sleep(3)
        return True

    learn_response = try_learn(command)
    if learn_response:
        speak(learn_response)
        return False

    reminder_response = set_reminder(command)
    if reminder_response:
        speak(reminder_response)
        return False

    web_response = handle_web_command(command)
    if web_response:
        speak(web_response)
        return False

    response, source = route_command(command)

    if response == "EXIT":
        speak("Shutting down. Goodbye Shaif.")
        time.sleep(3)
        return True

    speak(response)
    return False

while True:
    try:
        text = listen_once(timeout=6, phrase_limit=15)
        if not text:
            continue

        text_lower = text.lower()
        wake_detected = any(w in text_lower for w in WAKE_WORDS)

        if wake_detected:
            stop_speaking()
            time.sleep(0.2)

            command_inline = text_lower
            for w in WAKE_WORDS:
                command_inline = command_inline.replace(w, "").strip()

            if command_inline and len(command_inline) > 3:
                command = normalize_command(command_inline)
                should_exit = handle_command(command)
                if should_exit:
                    break
            else:
                speak("Yes Shaif?")
                time.sleep(0.5)
                raw_command = listen_once(timeout=8, phrase_limit=20)
                if not raw_command:
                    speak("I didn't catch that.")
                    continue
                command = normalize_command(raw_command)
                should_exit = handle_command(command)
                if should_exit:
                    break

            conversation_mode = True

        elif conversation_mode:
            command = normalize_command(text)
            should_exit = handle_command(command)
            if should_exit:
                break

    except KeyboardInterrupt:
        stop_speaking()
        speak("Jarvis shutting down.")
        time.sleep(2)
        break
    except Exception as e:
        time.sleep(1)
        continue
    