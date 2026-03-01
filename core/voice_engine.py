import threading
import os
import time


_stop_speaking = threading.Event()
_is_speaking = False


def _is_hindi(text):
    hindi_words = ["kya", "hai", "mera", "tera", "aur", "main", "tum",
                   "haan", "nahi", "karo", "bolo", "batao", "ek", "baar",
                   "gaya", "aadmi", "bola", "ne", "ko", "se", "ka", "ki",
                   "ke", "jo", "to", "bhi", "ab", "yeh", "jahaan", "taara",
                   "hoon", "aapka", "theek", "dhanyavad", "taiyaar"]
    text_lower = text.lower()
    count = sum(1 for word in hindi_words if f" {word} " in f" {text_lower} ")
    return count >= 2


def speak(text):
    global _is_speaking
    print(f"Jarvis: {text}")
    _stop_speaking.clear()

    def _speak():
        global _is_speaking
        _is_speaking = True
        temp_file = "temp_audio.mp3"
        try:
            from gtts import gTTS
            import pygame

            lang = 'hi' if _is_hindi(text) else 'en'
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(temp_file)

            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()

            # Check interrupt every 100ms
            while pygame.mixer.music.get_busy():
                if _stop_speaking.is_set():
                    pygame.mixer.music.stop()
                    break
                time.sleep(0.1)

            pygame.mixer.quit()

        except Exception as e:
            print(f"[Voice Error] {e}")
            # try:
            #     import pyttsx3
            #     engine = pyttsx3.init()
            #     engine.setProperty("rate", 180)
            #     engine.say(text)
            #     engine.runAndWait()
            #     engine.stop()
            # except:
            #     pass
        finally:
            _is_speaking = False
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass

    thread = threading.Thread(target=_speak)
    thread.daemon = True
    thread.start()
    return thread

def stop_speaking():
    _stop_speaking.set()

def is_speaking():
    return _is_speaking