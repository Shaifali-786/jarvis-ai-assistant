import speech_recognition as sr
import time

recognizer = sr.Recognizer()
recognizer.energy_threshold = 500
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 1.5
recognizer.non_speaking_duration = 1.0

# Alag recognizer sirf interrupt ke liye
interrupt_recognizer = sr.Recognizer()
interrupt_recognizer.energy_threshold = 400
interrupt_recognizer.dynamic_energy_threshold = False

def listen_once(timeout=6, phrase_limit=15):
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_limit
            )
        text = recognizer.recognize_google(audio, language="en-IN")
        return text.lower()
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except OSError as e:
        print(f"[Mic Hardware Error] {e}")
        time.sleep(2)
        return None
    except Exception as e:
        print(f"[Listen Error] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        time.sleep(1)
        return None

def listen_for_interrupt():
    """Sirf 'Jarvis' ke liye sunta hai — fast aur lightweight"""
    try:
        with sr.Microphone() as source:
            audio = interrupt_recognizer.listen(
                source, 
                timeout=1,
                phrase_time_limit=2
            )
        text = interrupt_recognizer.recognize_google(audio, language="en-IN").lower()
        if "jarvis" in text:
            return True
    except:
        pass
    return False