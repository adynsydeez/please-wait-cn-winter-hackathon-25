import os, time, shutil, random
from colorama import init, Fore, Back, Style

def load_ascii_faces(directory):
    """Loads all ASCII face text files from the given directory into a dict."""
    face_frames = {}
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            key = filename.replace(".txt", "")
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
                face_frames[key] = f.read()
    return face_frames

face_frames = load_ascii_faces("images/ascii")

GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RED = Fore.RED
RESET = Style.RESET_ALL

print(GREEN)

def clear_console():
    """Clears the console screen based on the operating system."""
    if os.name == 'nt':  # For Windows
        _ = os.system('cls')
    else:  # For macOS and Linux
        _ = os.system('clear')

def type_line(text, delay=0.001):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def center_text(text, width):
    """Centers a string based on terminal width"""
    return text.center(width)

def animate(animation : str, duration: float, frameDelay: float) -> None:
    for i in range(duration * round(60.0 * frameDelay)):
        for frame in open(f"animations/{animation}.txt", "r").readlines():
            frame = frame.replace(".txt", "")
            frame = face_frames[frame]
            clear_console()
            print(frame, end='', flush=True)
            time.sleep(frameDelay)

testSpeak = "Hello, this is a test of the face animation system. It should display a simple animation of a face opening its mouth."

def boot_sequence():
    clear_console()
    print(GREEN + "ACME CORPORATION BIOS v3.14" + RESET)
    time.sleep(0.5)
    type_line("© 1984 ACME Corp. All Rights Reserved.")
    time.sleep(0.5)
    type_line("Performing system self-test...")
    time.sleep(0.5)

    checks = [
        ("Initializing system modules", GREEN + "[  OK  ]" + RESET),
        ("Loading memory banks", GREEN + "[  OK  ]" + RESET),
        ("Detecting peripherals", GREEN + "[  OK  ]" + RESET),
        ("Mounting file system", GREEN + "[  OK  ]" + RESET),
        ("Network adapter", RED + "[FAIL]" + RESET),
        ("Starting terminal interface", GREEN + "[  OK  ]" + RESET),
    ]

    for desc, status in checks:
        type_line(f"{status} {desc}...")
        time.sleep(random.uniform(0.2, 0.5))

    print()
    type_line("MEMORY TEST: 32768K OK")
    type_line("CPU: Z80 @ 4.77 MHz")
    type_line("VIDEO: CGA 320x200 4-color")
    time.sleep(0.5)
    type_line("READY.")
    print(GREEN, end="")
    print("CPU: ", end="")
    type_line("Say hello ")
    print(">", end="")
    userInput = input()
    
    if userInput.lower() in ["hello", "hi", "hey"]:
        print("CPU: ")
        type_line(":)...", delay=0.1)
        load_AI(face_frames)
    else:
        print("CPU: ", end="")
        type_line(">:(...", delay=0.1)
        load_AI(face_frames)

def load_AI(face_frames):
    """Simulates AI boot-up sequence with centered face"""
    cols, rows = shutil.get_terminal_size()
    
    # Start with a loading effect
    clear_console()

    sequence = [
        GREEN + "[ OK ]" + RESET +  "Initializing AI neural pathways...",
        GREEN + "[ OK ]" + RESET +  "Loading speech synthesis module...",
        GREEN + "[ OK ]" + RESET +  "Activating vision subsystem...",
        GREEN + "[ OK ]" + RESET +  "Establishing emotional subroutines...",
        GREEN + "[ OK ]" + RESET +  "Syncing with core directives...",
        GREEN + "[ OK ]" + RESET +  "AI personality kernel online"
    ]

    for line in sequence:
        type_line(line)
        time.sleep(random.uniform(0.2, 0.4))

    time.sleep(0.5)
    clear_console()

    print(GREEN, end="")

    # Draw AI face centered
    face = face_frames["face-idle-1"].splitlines()
    top_padding = (rows // 2) - (len(face) // 2) - 3
    for _ in range(top_padding):
        print()

    for line in face:
        print(center_text(line, cols))

    print("\n")  # Space under face for dialogue

    # Dialogue area
    dialogue = "HELLO, HUMAN. I AM ONLINE."
    print(center_text(dialogue, cols)[0:round((cols-len(dialogue))/2) + 1], end="")
    type_line(dialogue[1:], delay=0.05)

    # User input prompt at bottom
    print("\n" * (rows - top_padding - len(face) - 5))  # Push input to bottom
    user_input = input(">" + " ")
    return user_input


boot_sequence()