import os
import time

def clear_console():
    """Clears the console screen based on the operating system."""
    if os.name == 'nt':  # For Windows
        _ = os.system('cls')
    else:  # For macOS and Linux
        _ = os.system('clear')

faceFrames = {"idle": open("images/ascii/face-idle-1.txt", "r").read(),
        "mouth-open-1": open("images/ascii/face-idle-mouth-open-1.txt", "r").read(), }


testSpeak = "Hello, this is a test of the face animation system. It should display a simple animation of a face opening its mouth."


for i in range(0, len(testSpeak)):
    clear_console()
    print(faceFrames["idle"])
    print(testSpeak[0:i], end='', flush=True)
    time.sleep(0.1)
    clear_console()
    print(faceFrames["mouth-open-1"])
    print(testSpeak[0:i], end='', flush=True)
    time.sleep(0.1)