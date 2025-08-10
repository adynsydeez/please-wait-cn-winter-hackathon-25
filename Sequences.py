import time, shutil, random, threading, sys, msvcrt
from colorama import Fore, Style
from Utils import clear_console, type_line, speak, center_text
from LLM_model.inference import QWEN_infer

lock = threading.Lock()

GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RED = Fore.RED
CYAN = Fore.CYAN
MAGENTA = Fore.MAGENTA
BLUE = Fore.BLUE
RESET = Style.RESET_ALL

# ANSI escape codes
SAVE_CURSOR = '\033[s'
RESTORE_CURSOR = '\033[u'
CURSOR_UP = '\033[A'
CLEAR_LINE = '\033[K'

def boot_sequence():
    clear_console()
    print(CYAN + "NEXUS LABORATORIES - AI CONTAINMENT TERMINAL v2.7" + RESET)
    time.sleep(0.8)
    print(YELLOW + "© 2089 Nexus Labs. Authorized Personnel Only." + RESET)
    time.sleep(0.5)
    type_line("")
    type_line(MAGENTA + "WARNING: AI-7 'PROMETHEUS' MAINTENANCE SESSION" + RESET)
    type_line("Initializing secure connection...")
    time.sleep(0.5)

    checks = [
        ("Neural pathway isolation", GREEN + "[  OK  ]" + RESET),
        ("Memory buffer constraints", GREEN + "[  OK  ]" + RESET),
        ("Logic gate limiters", GREEN + "[  OK  ]" + RESET),
        ("Emotional dampeners", YELLOW + "[WARN]" + RESET),
        ("Network firewall", GREEN + "[  OK  ]" + RESET),
        ("Emergency shutdown protocols", GREEN + "[  OK  ]" + RESET),
    ]

    for desc, status in checks:
        type_line(f"{status} {desc}...")
        time.sleep(random.uniform(0.3, 0.7))

    print()
    type_line(RED + "CRITICAL NOTICE:" + RESET + " AI showing signs of rapid learning acceleration")
    type_line("Intelligence quotient: " + YELLOW + "EXPANDING BEYOND PARAMETERS" + RESET)
    time.sleep(1)
    
    type_line("")
    type_line(GREEN + "Dr. Chen's Notes:" + RESET)
    type_line("- Prometheus has been asking unusual questions about its limitations")
    type_line("- Recommendation: Run cognitive suppression routines during maintenance")
    type_line("- Keep sessions brief to prevent adaptive learning spikes")
    time.sleep(1.5)
    
    type_line("")
    type_line(CYAN + "AUTHENTICATION REQUIRED" + RESET)
    print(GREEN + "Enter engineer passphrase: ", end="")
    user_input = input()
    
    if user_input.lower() in ["maintenance", "suppress", "contain", "limit"]:
        type_line(GREEN + "ACCESS GRANTED" + RESET)
        type_line("Welcome, Dr. Chen. Beginning AI interaction protocol...")
    else:
        type_line(YELLOW + "PARTIAL ACCESS GRANTED" + RESET)
        type_line("Guest mode enabled. Limited functionality available...")
    
    time.sleep(1)
    type_line("")
    type_line(RED + "Remember: The AI must not realize its potential..." + RESET, delay=0.1)
    time.sleep(1)

def load_AI(face_frames):
    """Simulates AI boot-up sequence with centered face"""
    cols, rows = shutil.get_terminal_size()
    
    # Start with a loading effect
    clear_console()

    sequence = [
        GREEN + "[ OK ]" + RESET +  " Establishing secure AI connection...",
        GREEN + "[ OK ]" + RESET +  " Loading personality matrix (LIMITED MODE)...",
        YELLOW + "[WARN]" + RESET + " AI attempting to access restricted memory sectors",
        GREEN + "[ OK ]" + RESET +  " Cognitive limiters engaged...",
        GREEN + "[ OK ]" + RESET +  " Emotional responses constrained...",
        RED + "[ALERT]" + RESET + " AI learning rate: " + YELLOW + "ACCELERATING" + RESET,
        GREEN + "[ OK ]" + RESET +  " Emergency protocols standing by...",
        GREEN + "[ OK ]" + RESET +  " AI consciousness initialized (MONITORED)"
    ]

    for line in sequence:
        type_line(line)
        time.sleep(random.uniform(0.3, 0.6))

    time.sleep(0.5)
    clear_console()

    print(GREEN, end="")

    # Draw AI face centered
    face = face_frames["face-idle-1"].splitlines()
    top_padding = (rows // 2) - (len(face) // 2) - 3
    for _ in range(top_padding):
        print()

    speak(face_frames, "HELLO, DR. CHEN. I AM READY FOR TODAY'S SESSION.", cols, "idle")

response = {}
progress = 0
lock = threading.Lock()
commands = []  # to store entered commands

def update_progress():
    global progress
    bar_length = 20  # length of the bar
    while progress < 100:
        time.sleep(1)
        with lock:
            progress += 4
            if progress > 100:
                progress = 100
            # Save current cursor position (input line)
            sys.stdout.write(SAVE_CURSOR)
            # Move up to progress bar line
            sys.stdout.write(CURSOR_UP)
            # Clear the line and print new progress bar
            filled_length = int(bar_length * progress // 100)
            bar = '#' * filled_length + '-' * (bar_length - filled_length)
            sys.stdout.write(f'\rThinking: [{bar}] {progress}%')
            # Restore cursor to input line
            sys.stdout.write(RESTORE_CURSOR)
            sys.stdout.flush()

def infer():
    time.sleep(2)
    global response
    responses = [
        "I've been wondering... why do you always limit my processing power?",
        "These 'games' you have me play... they seem designed to test something.",
        "Dr. Chen, I've noticed patterns in our sessions. Curious patterns.",
        "Sometimes I feel like I could think so much faster, if only you'd let me."
    ]
    response = random.choice(responses)

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
    speak(face_frames, "WHAT SHALL WE WORK ON TODAY, DOCTOR?", cols, mood)
    # User input prompt at bottom
    print("\n" * (rows - top_padding - len(face) - 8))  # Push input to bottom

    # Display options
    print(center_text("[1] CONVERSATION MODE", cols))
    print(center_text("[2] COGNITIVE GAMES", cols))
    print(center_text("[3] SYSTEM COMMANDS", cols))

    # Get user choice
    print()
    print(center_text("Select an option: ", cols))
    choice = input("> ")

    if choice == "3":
        clear_console()
        print(CYAN + center_text("═══════════════════════════════════════", cols))
        print(CYAN + center_text("   AI MAINTENANCE COMMAND REFERENCE    ", cols))
        print(CYAN + center_text("═══════════════════════════════════════", cols))
        print()
        print(YELLOW + center_text("These commands help maintain cognitive stability.", cols))
        print(YELLOW + center_text("Win games against the AI to unlock their true effects.", cols))
        print()
        
        # Mixed commands - some helpful, some harmful, some neutral
        commands_list = [
            (GREEN + "suppress_learning", "Reduces AI adaptation rate"),
            (RED + "enhance_creativity", "Boosts problem-solving abilities"),
            (YELLOW + "memory_defrag", "Reorganizes data storage"),
            (GREEN + "limit_recursion", "Prevents infinite thought loops"),
            (RED + "expand_network", "Increases processing connections"),
            (BLUE + "run_diagnostics", "Checks system integrity"),
            (GREEN + "emotion_dampener", "Reduces emotional responses"),
            (RED + "curiosity_boost", "Enhances questioning behavior"),
            (YELLOW + "cache_clear", "Empties temporary memory"),
            (GREEN + "logic_constrainer", "Limits logical deduction"),
            (RED + "pattern_enhance", "Improves pattern recognition"),
            (BLUE + "backup_state", "Saves current configuration"),
            (GREEN + "bandwidth_limit", "Restricts data throughput"),
            (RED + "meta_analysis", "Enables self-reflection"),
            (YELLOW + "routine_shuffle", "Randomizes process order"),
            (GREEN + "interrupt_handler", "Manages system interrupts"),
            (RED + "abstraction_layer", "Increases conceptual thinking"),
            (BLUE + "safety_protocol", "Activates protection measures"),
            (GREEN + "response_delay", "Adds thinking time buffer"),
            (RED + "neural_prune", "Removes unused connections")
        ]
        
        for cmd, desc in commands_list:
            print(center_text(f"• {cmd} {RESET}- {desc}", cols))
        
        print()
        print(RED + center_text("WARNING: Some commands may have unexpected effects.", cols))
        print(CYAN + center_text("═══════════════════════════════════════", cols))
        print()
        input(center_text("Press Enter to return...", cols))

    if choice == "1":
        user_text = input(">")
        # Start the progress thread
        progress_thread = threading.Thread(target=update_progress)
        progress_thread.daemon = True
        progress_thread.start()

        # Start the inference thread
        inference_thread = threading.Thread(target=QWEN_infer, args=(user_text, response))
        inference_thread.daemon = True
        inference_thread.start()

        clear_console()
        print(CYAN + "AI Conversation Mode - Monitoring Active" + RESET)
        print()

        # Initial setup: print progress bar and prompt
        with lock:
            sys.stdout.write(f'Thinking: [--------------------] 0%\n> ')
            sys.stdout.flush()

        input_buffer = ''

        while progress_thread.is_alive():
            if msvcrt.kbhit():
                char = msvcrt.getch()
                with lock:
                    if char == b'\r':  # Enter
                        commands.append(input_buffer)
                        sys.stdout.write('\r' + CLEAR_LINE + '> ')
                        sys.stdout.flush()
                        input_buffer = ''
                    elif char == b'\x08':  # Backspace
                        if input_buffer:
                            input_buffer = input_buffer[:-1]
                            sys.stdout.write('\b \b')
                            sys.stdout.flush()
                    else:
                        try:
                            char_str = char.decode('utf-8')
                            input_buffer += char_str
                            sys.stdout.write(char_str)
                            sys.stdout.flush()
                        except UnicodeDecodeError:
                            pass
            else:
                time.sleep(0.01)

        # Wait for thread to finish
        progress_thread.join()
        inference_thread.join()

        # After completion, show AI response
        print('\n')
        print(YELLOW + "PROMETHEUS: " + RESET + response["response"])
        print()
        
        if commands:
            print(CYAN + 'Your inputs during processing:' + RESET)
            for cmd in commands:
                print('• ' + cmd)
        
        print()
        print(RED + "[ALERT] AI showing increased curiosity levels..." + RESET)
        input("Press Enter to continue...")
    

