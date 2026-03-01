import schedule
import time
import threading
from core.voice_engine import speak

reminders = []

def set_reminder(command):
    """
    Detects: 'remind me in 5 minutes to drink water'
    """
    command = command.lower()
    
    if "remind me in" not in command:
        return None
    
    try:
        # Extract time and task
        # "remind me in 5 minutes to drink water"
        part = command.replace("remind me in", "").strip()
        
        if "minute" in part:
            minutes = int(''.join(filter(str.isdigit, part.split("minute")[0])))
            task = part.split("to", 1)[-1].strip() if "to" in part else "your reminder"
            
            def reminder_job():
                speak(f"Shaif, reminder: {task}")
            
            # Run reminder in background thread
            def delayed():
                time.sleep(minutes * 60)
                reminder_job()
            
            thread = threading.Thread(target=delayed, daemon=True)
            thread.start()
            
            return f"Okay! I'll remind you to {task} in {minutes} minutes."
        
        elif "hour" in part:
            hours = int(''.join(filter(str.isdigit, part.split("hour")[0])))
            task = part.split("to", 1)[-1].strip() if "to" in part else "your reminder"
            
            def delayed():
                time.sleep(hours * 3600)
                speak(f"Shaif, reminder: {task}")
            
            thread = threading.Thread(target=delayed, daemon=True)
            thread.start()
            return f"Got it! Reminding you to {task} in {hours} hours."
    
    except Exception as e:
        print(f"[Reminder Error] {e}")
    
    return None