import os
import time

def clear_console() -> None:
    """Clears the console screen based on the operating system."""
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def animate(animation : str, duration: float, frameDelay: float) -> None:
    for i in range(duration * round(60.0 * frameDelay)):
        for frame in open(f"animations/{animation}.txt", "r").readlines():
            frame = open(f"images/ascii/{frame.strip()}", "r").read()
            clear_console()
            print(frame, end='', flush=True)
            time.sleep(frameDelay)

animations = {
    "idle-Speak": lambda: animate("idle-Speak", 2, 0.1),
    "angry-Speak": lambda: animate("angry-Speak", 5, 0.1),
    "idle-nod": lambda: animate("idle-nod", 2, 0.1),
    "idle-shake": lambda: animate("idle-shake", 2, 0.05),
}

faceFrames = {"idle": open("images/ascii/face-idle-1.txt", "r").read(),
        "mouth-open-1": open("images/ascii/face-idle-mouth-open-1.txt", "r").read(), 
        "idle-angry-1": open("images/ascii/face-angry-1.txt", "r").read(),
        }


testSpeak = "Hello, this is a test of the face animation system. It should display a simple animation of a face opening its mouth."

running = True

while running:
    clear_console()
    print("Select an option:")
    print("stills:")
    for i in range(0, len(faceFrames)):
        print(f"{i + 1}: {list(faceFrames.keys())[i]}")
    print("animations:")
    for i in range(0, len(animations)):
        print(f"{len(faceFrames) + i + 1}: {list(animations.keys())[i]}")
        
    user_input = input()
    if user_input.lower() in ["exit", "quit", "q"]:
        running = False
    else:
        match user_input:
            case "1":
                print(faceFrames["idle"])
            case "2":
                print(faceFrames["mouth-open-1"])
            case "3":
                print(faceFrames["idle-angry-1"])
            case "4":
                animations["idle-Speak"]()
            case "5":
                animations["angry-Speak"]()
            case "6":
                animations["idle-nod"]()
            case "7":
                animations["idle-shake"]()
            case _:
                print("Something's wrong")
        time.sleep(3)