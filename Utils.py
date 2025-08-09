import os, time, shutil

def load_ascii_faces(directory):
    """Loads all ASCII face text files from the given directory into a dict."""
    face_frames = {}
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            key = filename.replace(".txt", "")
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
                face_frames[key] = f.read()
    return face_frames

def clear_console():
    """Clears the console screen based on the operating system."""
    if os.name == 'nt':  # For Windows
        _ = os.system('cls')
    else:  # For macOS and Linux
        _ = os.system('clear')

def type_line(text, delay=0.01):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def center_text(text, width):
    """Centers a string based on terminal width"""
    return text.center(width)

def animate(face_frames, animation : str, loops: float, frameDelay: float) -> None:
    for i in range(loops):
        for frame in open(f"animations/{animation}.txt", "r").readlines():
            frame = frame.replace(".txt", "")
            frame = frame.replace("\n", "")
            frame = face_frames[frame]
            clear_console()
            print(frame, end='', flush=True)
            time.sleep(frameDelay)

def speak(face_frames: dict, text: str, width: int, mood: str = "idle") -> None:
    cols, rows = shutil.get_terminal_size()
    # Load animation sequence from file
    anim_file = f"animations/{mood}-Speak.txt" if mood != "idle" else "animations/idle-Speak.txt"
    try:
        with open(anim_file, "r", encoding="utf-8") as f:
            anim_frames = [line.strip().replace(".txt", "") for line in f if line.strip()]
    except FileNotFoundError:
        anim_frames = ["face-idle-1"]
    text_x = (cols - len(str(text))) // 2
    face_content = face_frames.get(anim_frames[0])
    if face_content is None:
        face_lines = []
    else:
        face_lines = face_content.splitlines()
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