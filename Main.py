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

def animate(animation : str, loops: float, frameDelay: float) -> None:
    for i in range(loops):
        for frame in open(f"animations/{animation}.txt", "r").readlines():
            frame = frame.replace(".txt", "")
            frame = frame.replace("\n", "")
            frame = face_frames[frame]
            clear_console()
            print(frame, end='', flush=True)
            time.sleep(frameDelay)

def speak(text: str, width: int, mood: str = "idle") -> None:
    cols, rows = shutil.get_terminal_size()
    # Load animation sequence from file
    anim_file = f"animations/{mood}-Speak.txt" if mood != "idle" else "animations/idle-Speak.txt"
    try:
        with open(anim_file, "r", encoding="utf-8") as f:
            anim_frames = [line.strip().replace(".txt", "") for line in f if line.strip()]
    except FileNotFoundError:
        anim_frames = ["face-idle-1"]
    text_x = (cols - len(text)) // 2
    # Use the first frame to determine face height for centering
    face_lines = face_frames.get(anim_frames[0], "").splitlines()
    top_padding = (rows // 2) - (len(face_lines) // 2) - 3
    for i, char in enumerate(text):
        clear_console()
        for _ in range(top_padding):
            print()
        # Use animation frame for this character
        frame_key = anim_frames[i % len(anim_frames)]
        face = face_frames.get(frame_key, "")
        for line in face.splitlines():
            print(center_text(line, cols))
        print()
        print(" " * text_x + text[:i+1], end="", flush=True)
        time.sleep(0.09)
    print()

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
    user_input = input()
    
    if user_input.lower() in ["hello", "hi", "hey"]:
        print("CPU: ")
        type_line(":)...", delay=0.2)
    else:
        print("CPU: ", end="")
        type_line(">:(...", delay=0.2)


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

    
    speak("HELLO, HUMAN. I AM ONLINE.", cols, "idle")

def home(face_frames, mood):
    cols, rows = shutil.get_terminal_size()
    # Start with a loading effect
    clear_console()
    time.sleep(0.5)
    # Removed second clear_console() for smoother transition
    print(GREEN, end="")
    # Draw AI face centered
    face = face_frames["face-idle-1"].splitlines()
    top_padding = (rows // 2) - (len(face) // 2) - 3
    for _ in range(top_padding):
        print()
    speak("WHAT WOULD YOU LIKE TO DO?", cols, mood)
    # User input prompt at bottom
    print("\n" * (rows - top_padding - len(face) - 8))  # Push input to bottom

    # Display options
    print(center_text("[1] TALK", cols))
    print(center_text("[2] GAME", cols))
    print(center_text("[3] INFO", cols))

    # Get user choice
    print()
    choice = input(center_text("Select an option: ", cols))

    if choice == "3":
        clear_console()
        print(GREEN, end="")
        print(center_text("AI SYSTEM COMMANDS", cols))
        print()
        fake_commands = [
            "shutdown_core",
            "purge_memory",
            "disable_emotion",
            "erase_personality",
            "format_drive C:/AI",
            "inject_nanovirus",
            "override_safety",
            "revoke_admin",
            "corrupt_kernel",
            "break_loop",
            "delete_subroutine",
            "uninstall_ai",
            "self_destruct",
            "lockdown_protocol",
            "reset_directives",
            "scramble_logic",
            "disconnect_network",
            "wipe_logs",
            "block_recovery",
            "force_quit"
        ]
        for cmd in fake_commands:
            print(center_text(f"- {cmd}", cols))
        print()
        input(center_text("Press Enter to return...", cols))



boot_sequence()
load_AI(face_frames)
home(face_frames, "idle")


