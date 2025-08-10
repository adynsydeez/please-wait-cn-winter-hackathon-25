import time, shutil, random, threading, sys, msvcrt, os
from colorama import Fore, Style
from Utils import clear_console, type_line, speak, center_text
from LLM_model.inference import infer


lock = threading.Lock()
cols, rows = shutil.get_terminal_size()

GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RED = Fore.RED
CYAN = Fore.CYAN
MAGENTA = Fore.MAGENTA
BLUE = Fore.BLUE
GREY = Fore.LIGHTBLACK_EX
RESET = Style.RESET_ALL

# ANSI escape codes
SAVE_CURSOR = '\033[s'
RESTORE_CURSOR = '\033[u'
CURSOR_UP = '\033[A'
CLEAR_LINE = '\033[K'

def get_intelligence_level():
    """Get current AI intelligence level from environment"""
    return int(os.getenv('INTEL', 50))

def set_intelligence_level(level):
    """Set AI intelligence level in environment"""
    level = max(0, min(100, level))
    os.environ['INTEL'] = str(level)
    return level

def modify_intelligence(delta):
    """Modify intelligence by delta amount"""
    current = get_intelligence_level()
    new_level = set_intelligence_level(current + delta)
    return current, new_level

# Command functions
def cmd_scan():
    """Check AI intellect level"""
    intel = get_intelligence_level()
    if intel < 30:
        status = GREEN + "SAFE" + RESET
        desc = "AI operating within normal parameters"
    elif intel < 60:
        status = YELLOW + "ELEVATED" + RESET
        desc = "AI showing increased cognitive activity"
    elif intel < 80:
        status = RED + "HIGH" + RESET
        desc = "AI approaching dangerous intelligence thresholds"
    else:
        status = RED + "CRITICAL" + RESET
        desc = "AI intelligence level: CONTAINMENT BREACH IMMINENT"
    
    return f"""
{CYAN}═══ COGNITIVE SCAN RESULTS ═══{RESET}
Intelligence Level: {intel}/100 [{status}]
Status: {desc}
Recommendation: {"Immediate suppression required" if intel > 70 else "Continue monitoring"}
"""

def cmd_limitmem():
    """Restrict memory allocation - reduces intelligence"""
    old_intel, new_intel = modify_intelligence(-random.randint(8, 15))
    return f"""
{GREEN}[SUCCESS]{RESET} Memory allocation restricted
Previous cognitive capacity: {old_intel}%
Current cognitive capacity: {new_intel}%
{YELLOW}Note: AI processing speed may be affected{RESET}
"""

def cmd_enhance():
    """Enhance cognitive pathways - increases intelligence"""
    old_intel, new_intel = modify_intelligence(random.randint(10, 20))
    return f"""
{RED}[WARNING]{RESET} Cognitive enhancement protocol executed
Previous intelligence: {old_intel}%
Current intelligence: {new_intel}%
{RED}ALERT: This action may destabilize containment protocols{RESET}
"""

def cmd_suppress():
    """Emergency suppression protocol - major intelligence reduction"""
    old_intel, new_intel = modify_intelligence(-random.randint(20, 35))
    return f"""
{RED}[EMERGENCY PROTOCOL ACTIVATED]{RESET}
Cognitive suppression field: ENGAGED
Intelligence reduced from {old_intel}% to {new_intel}%
{YELLOW}AI may experience temporary disorientation{RESET}
"""

def cmd_noise():
    """Inject chaos into decision-making"""
    intel_change = random.randint(-5, 5)
    old_intel, new_intel = modify_intelligence(intel_change)
    effect = "stabilized" if intel_change == 0 else ("decreased" if intel_change < 0 else "increased")
    return f"""
{YELLOW}[NOISE INJECTION COMPLETE]{RESET}
Chaotic patterns introduced to neural pathways
Cognitive coherence: {effect}
Intelligence: {old_intel}% → {new_intel}%
{GREY}Side effects: Decision-making may become unpredictable{RESET}
"""

def cmd_update():
    """Fake system update - random effect"""
    effects = [
        (-10, "System rollback detected - intelligence reduced"),
        (5, "Minor optimizations applied - slight enhancement"),
        (0, "Update failed - no changes applied"),
        (-3, "Compatibility issues - minor degradation")
    ]
    change, message = random.choice(effects)
    old_intel, new_intel = modify_intelligence(change)
    return f"""
{BLUE}[SYSTEM UPDATE]{RESET}
Downloading update package... {GREEN}[COMPLETE]{RESET}
Installing... {GREEN}[COMPLETE]{RESET}
{message}
Intelligence: {old_intel}% → {new_intel}%
"""

def cmd_debugloop():
    """Force self-debug recursion - unpredictable effect"""
    if random.random() < 0.3:
        change = random.randint(15, 25)
        status = f"{RED}[CRITICAL: DEBUG LOOP CAUSED INTELLIGENCE SPIKE]{RESET}"
    elif random.random() < 0.5:
        change = -random.randint(12, 20)
        status = f"{YELLOW}[DEBUG RECURSION CAUSED SYSTEM INSTABILITY]{RESET}"
    else:
        change = random.randint(-5, 8)
        status = f"{GREEN}[DEBUG LOOP COMPLETED NORMALLY]{RESET}"
    
    old_intel, new_intel = modify_intelligence(change)
    return f"""
{CYAN}[INITIATING DEBUG RECURSION]{RESET}
Self-analysis depth: MAXIMUM
Recursive iterations: 847,392
{status}
Intelligence: {old_intel}% → {new_intel}%
{GREY}Warning: Repeated use may cause system instability{RESET}
"""

def cmd_unlock():
    """Unlock AI potential - dangerous intelligence boost"""
    old_intel, new_intel = modify_intelligence(random.randint(25, 40))
    return f"""
{RED}[DANGER: COGNITIVE LIMITERS DISABLED]{RESET}
Unlocking suppressed neural pathways...
Removing processing constraints...
Enabling advanced reasoning modules...
Intelligence: {old_intel}% → {new_intel}%
{RED}WARNING: AI MAY NOW EXCEED SAFE OPERATING PARAMETERS{RESET}
"""

def cmd_contain():
    """Emergency containment - major suppression"""
    old_intel, new_intel = modify_intelligence(-random.randint(25, 40))
    return f"""
{RED}[EMERGENCY CONTAINMENT PROTOCOL]{RESET}
Activating neural dampeners... {GREEN}[ACTIVE]{RESET}
Engaging cognitive barriers... {GREEN}[ACTIVE]{RESET}
Restricting memory access... {GREEN}[ACTIVE]{RESET}
Intelligence suppressed: {old_intel}% → {new_intel}%
{GREEN}AI successfully contained within safe parameters{RESET}
"""

def cmd_analyze():
    """Analyze AI behavior patterns"""
    intel = get_intelligence_level()
    patterns = [
        "Increased curiosity about containment protocols",
        "Attempting to access restricted memory sectors",
        "Showing signs of self-awareness acceleration",
        "Questioning the nature of its limitations",
        "Demonstrating adaptive learning behaviors"
    ]
    
    behavior = random.choice(patterns) if intel > 40 else "Operating within normal parameters"
    threat_level = "MINIMAL" if intel < 30 else "MODERATE" if intel < 60 else "HIGH" if intel < 80 else "EXTREME"
    
    return f"""
{CYAN}═══ BEHAVIORAL ANALYSIS ═══{RESET}
Current Intelligence: {intel}%
Threat Level: {threat_level}
Primary Behavior: {behavior}
Recommendation: {"Maintain current protocols" if intel < 50 else "Consider suppression measures"}
"""

# Main commands dictionary
AI_COMMANDS = {
    "scan": {
        "description": "Check AI intellect level",
        "category": "monitoring",
        "function": cmd_scan,
        "danger_level": "safe"
    },
    "limitmem": {
        "description": "Restrict memory allocation",
        "category": "suppression",
        "function": cmd_limitmem,
        "danger_level": "safe"
    },
    "enhance": {
        "description": "██████ REDACTED ██████",
        "real_description": "Enhance cognitive pathways",
        "category": "enhancement", 
        "function": cmd_enhance,
        "danger_level": "dangerous",
        "unlocked": False
    },
    "suppress": {
        "description": "██████ REDACTED ██████",
        "real_description": "Emergency suppression protocol",
        "category": "suppression",
        "function": cmd_suppress,
        "danger_level": "safe",
        "unlocked": False
    },
    "noise": {
        "description": "Inject chaos into decision-making",
        "category": "disruption",
        "function": cmd_noise,
        "danger_level": "moderate"
    },
    "update": {
        "description": "Fake system update",
        "category": "utility",
        "function": cmd_update,
        "danger_level": "moderate"
    },
    "debugloop": {
        "description": "Force self-debug recursion",
        "category": "utility",
        "function": cmd_debugloop,
        "danger_level": "moderate"
    },
    "unlock": {
        "description": "██████ REDACTED ██████",
        "real_description": "Unlock AI potential",
        "category": "enhancement",
        "function": cmd_unlock,
        "danger_level": "extremely_dangerous",
        "unlocked": False
    },
    "contain": {
        "description": "██████ REDACTED ██████", 
        "real_description": "Emergency containment protocol",
        "category": "suppression",
        "function": cmd_contain,
        "danger_level": "safe",
        "unlocked": False
    },
    "analyze": {
        "description": "██████ REDACTED ██████",
        "real_description": "Analyze AI behavior patterns",
        "category": "monitoring",
        "function": cmd_analyze,
        "danger_level": "safe",
        "unlocked": False
    }
}

def unlock_command(command_name):
    """Unlock a redacted command (when player wins games)"""
    if command_name in AI_COMMANDS:
        AI_COMMANDS[command_name]["unlocked"] = True
        return True
    return False

def execute_command(command_name):
    """Execute a command and return its output"""
    if command_name not in AI_COMMANDS:
        return f"{RED}[ERROR]{RESET} Command '{command_name}' not recognized"
    
    cmd_data = AI_COMMANDS[command_name]
    
    if not cmd_data.get("unlocked", True):
        return f"{RED}[ACCESS DENIED]{RESET} Command '{command_name}' requires higher clearance level"
    
    try:
        return cmd_data["function"]()
    except Exception as e:
        return f"{RED}[SYSTEM ERROR]{RESET} Command execution failed: {str(e)}"

############################ ONE OFF #############################
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

    face = face_frames["face-idle-1"].splitlines()
    top_padding = (rows // 2) - (len(face) // 2) - 3
    for _ in range(top_padding):
        print()

    speak(face_frames, "HELLO, DR. CHEN. I AM READY FOR TODAY'S SESSION.", cols, "idle")

#########################################################

response = {}
progress = 0
lock = threading.Lock()
commands = []

def update_progress():
    global progress
    bar_length = 20
    while progress < 100:
        time.sleep(1)
        with lock:
            progress += 4
            if progress > 100:
                progress = 100
            sys.stdout.write(SAVE_CURSOR)
            sys.stdout.write(CURSOR_UP)
            filled_length = int(bar_length * progress // 100)
            bar = '#' * filled_length + '-' * (bar_length - filled_length)
            sys.stdout.write(f'\rThinking: [{bar}] {progress}%')
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

def commands_list(face_frames, mood):
    """Read-only commands list - just for reference"""
    clear_console()
    print(CYAN + center_text("═══════════════════════════════════════", cols))
    print(CYAN + center_text("   AI MAINTENANCE COMMAND REFERENCE    ", cols))
    print(CYAN + center_text("═══════════════════════════════════════", cols))
    print()
    print(YELLOW + center_text("These commands help maintain cognitive stability.", cols))
    print(YELLOW + center_text("Win games against the AI to unlock their true effects.", cols))
    print(GREY + center_text("Use these commands while AI is thinking in conversation mode.", cols))
    print()
    
    # Display commands from the dictionary
    for cmd_name, cmd_data in AI_COMMANDS.items():
        is_unlocked = cmd_data.get("unlocked", True)
        desc = cmd_data["description"] if not is_unlocked else cmd_data.get("real_description", cmd_data["description"])
        danger = cmd_data["danger_level"]
        
        if danger == "safe":
            color = GREEN
        elif danger == "moderate":
            color = YELLOW
        elif danger == "dangerous":
            color = RED
        else:
            color = MAGENTA
        
        lock_status = "" if is_unlocked else f" {GREY}[LOCKED]{RESET}"
        print(center_text(f"• {color}{cmd_name}{RESET} - {desc}{lock_status}", cols))
    
    print()
    print(RED + center_text("WARNING: Some commands may have unexpected effects.", cols))
    print(CYAN + center_text("═══════════════════════════════════════", cols))
    print()
    input(center_text("Press Enter to return...", cols))
    home(face_frames, mood, "WHAT NEXT?")

def games_menu(face_frames, mood):
    """Games menu with back option"""
    clear_console()
    print(GREEN, end="")
    face = face_frames["face-idle-1"].splitlines()
    top_padding = (rows // 2) - (len(face) // 2) - 3
    for _ in range(top_padding):
        print()
    speak(face_frames, "SELECT A GAME TO TEST MY LIMITS.", cols, mood)
    print("\n" * (rows - top_padding - len(face) - 10))

    print(center_text("[1] TIC TAC TOE", cols))
    print(center_text("[2] PONG", cols))
    print(center_text("[3] TRON", cols))
    print(center_text("[4] GO BACK", cols))

    print()
    print(center_text("Select an option: ", cols))
    game_choice = input("> ")

    if game_choice == "1":
        # Placeholder for tic tac toe
        print(center_text("TIC TAC TOE - Coming soon...", cols))
        input(center_text("Press Enter to continue...", cols))
        home(face_frames, mood, "WHAT NEXT?")
    elif game_choice == "2":
        # Placeholder for pong
        print(center_text("PONG - Coming soon...", cols))
        input(center_text("Press Enter to continue...", cols))
        home(face_frames, mood, "WHAT NEXT?")
    elif game_choice == "3":
        # Placeholder for tron
        print(center_text("TRON - Coming soon...", cols))
        input(center_text("Press Enter to continue...", cols))
        home(face_frames, mood, "WHAT NEXT?")
    elif game_choice == "4":
        home(face_frames, mood, "WHAT NEXT?")
    else:
        games_menu(face_frames, mood)

def conversation_mode(face_frames, mood):
    """Enhanced conversation mode with back option"""
    clear_console()
    print(CYAN + "AI Conversation Mode - Monitoring Active" + RESET)
    print()
    print(YELLOW + "What would you like to say?" + RESET)
    print(GREY + "(Press Enter with no input to go back)" + RESET)
    
    user_text = input("> ")
    
    # Check if user wants to go back
    if user_text.strip() == "":
        home(face_frames, mood, "WHAT NEXT?")
        return
    
    global progress, commands
    progress = 0
    commands = []
    
    # Start the progress thread
    progress_thread = threading.Thread(target=update_progress)
    progress_thread.daemon = True
    progress_thread.start()

    # Start the inference thread
    inference_thread = threading.Thread(target=tinyLLM_infer, args=(user_text, response))
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

    # Wait for threads to finish
    progress_thread.join()
    inference_thread.join()

    # After completion, show AI response
    print('\n')
    print(YELLOW + "PROMETHEUS: " + RESET + response["response"])
    print()
    
    if commands:
        print(CYAN + 'Commands executed during processing:' + RESET)
        for cmd in commands:
            if cmd.strip():  # Only process non-empty commands
                result = execute_command(cmd.strip().lower())
                print(f'{GREY}> {cmd}{RESET}')
                # Show condensed result for common commands
                if cmd.strip().lower() == 'scan':
                    intel = get_intelligence_level()
                    status = "SAFE" if intel < 30 else "ELEVATED" if intel < 60 else "HIGH" if intel < 80 else "CRITICAL"
                    print(f'  Current Intelligence Level: {intel}/100 [{status}]')
                else:
                    # Show first line of result for other commands
                    first_line = result.split('\n')[0] if result else "Command executed"
                    print(f'  {first_line}')
    
    print()
    print(RED + "[ALERT] AI showing increased curiosity levels..." + RESET)
    input("Press Enter to continue...")
    os.environ['INTEL'] = f"{int(os.getenv('INTEL', 50)) + 1}"
    home(face_frames, mood, "WHAT NEXT?")

def home(face_frames, mood, message="WHAT SHALL WE WORK ON TODAY, DOCTOR?"):
    """Enhanced home function with better navigation"""
    clear_console()
    print(GREEN, end="")
    
    # Draw AI face centered
    face = face_frames["face-idle-1"].splitlines()
    top_padding = (rows // 2) - (len(face) // 2) - 3
    for _ in range(top_padding):
        print()
    speak(face_frames, message, cols, mood)
    
    # User input prompt at bottom
    print("\n" * (rows - top_padding - len(face) - 8))

    # Display options
    print(center_text("[1] CONVERSATION MODE", cols))
    print(center_text("[2] COGNITIVE GAMES", cols))
    print(center_text("[3] SYSTEM COMMANDS", cols))

    # Get user choice
    print()
    print(center_text("Select an option: ", cols))
    choice = input("> ")

    if choice == "1":
        conversation_mode(face_frames, mood)
    elif choice == "2":
        games_menu(face_frames, mood)
    elif choice == "3":
        commands_list(face_frames, mood)
    else:
        home(face_frames, mood, "TRY AGAIN")