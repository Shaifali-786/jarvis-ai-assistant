import os
import psutil
import subprocess

def handle_system_command(command):
    command = command.lower()
    
    # Shutdown/exit
    if any(w in command for w in ["shutdown jarvis", "goodbye", "turn off", "bye jarvis"]):
        return "EXIT"
    
    # Open apps
    apps = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": "start chrome",
    "browser": "start chrome",
    "file manager": "explorer.exe",
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
    "whatsapp": "start whatsapp:",
    "camera": "start microsoft.windows.camera:",
    "paint": "mspaint.exe",
    "task manager": "taskmgr.exe",
    "spotify": "start spotify:",
    "settings": "start ms-settings:",
    "store": "start ms-windows-store:",
}
    
    for app_name, app_cmd in apps.items():
        if app_name in command and ("open" in command or "launch" in command or "start" in command):
            os.system(app_cmd)
            return f"Opening {app_name}"
    
    # Volume control
    if "mute" in command:
        os.system("nircmd.exe mutesysvolume 1")
        return "Muted"
    
    if "unmute" in command:
        os.system("nircmd.exe mutesysvolume 0")
        return "Unmuted"
    
    # Battery status
    if "battery" in command:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = "plugged in" if battery.power_plugged else "on battery"
            return f"Battery is at {percent}% and {plugged}."
        return "Could not read battery info."
    
    # CPU/RAM usage
    if "cpu" in command or "processor" in command:
        usage = psutil.cpu_percent(interval=1)
        return f"CPU usage is {usage}%"
    
    if "ram" in command or "memory" in command:
        ram = psutil.virtual_memory()
        return f"RAM usage is {ram.percent}% with {round(ram.available / (1024**3), 1)} GB available."
    
    # Screenshot
    if "screenshot" in command:
        import pyautogui
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        return "Screenshot saved."
    
    return None