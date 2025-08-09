import os
import time

def clear_console():
    """Clears the console screen based on the operating system."""
    if os.name == 'nt':  # For Windows
        _ = os.system('cls')
    else:  # For macOS and Linux
        _ = os.system('clear')

faceFrames = {"idle": open("images/ascii/face-idle-1.txt", "r").read(),
        "mouth-open-1": open("images/ascii/face-mouth-open-1.txt", "r").read(), 
        "idle-angry-1": open("images/ascii/face-idle-angry-1.txt", "r").read()}


testSpeak = "Hello, this is a test of the face animation system. It should display a simple animation of a face opening its mouth."

running = True

while running:
    user_input = input()
    if user_input.lower() in ["exit", "quit", "q"]:
        running = False
    else:
        print(faceFrames["idle"])
        print("Select an option:")
        for i in range(0, len(faceFrames)):
            print(f"{i + 1}: {list(faceFrames.keys())[i]}")
        
        match user_input:
            case "idle":
                print(faceFrames["idle"])
            case "mouth-open-1":
                print(faceFrames["mouth-open-1"])
            case "idle-angry-1":
                print(faceFrames["idle-angry-1"])

        print("Select an option:")
        for i in range(0, len(faceFrames)):
            print(f"{i + 1}: {list(faceFrames.keys())[i]}")

        

        clear_console()