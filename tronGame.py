#!/usr/bin/env python3
"""
TRON.EXE - Light Cycle Combat System v2.1
Command Line Implementation with Debug Interference
Uses only standard Python libraries
"""

import os
import sys
import time
import platform
import threading
import select
from enum import Enum
from collections import deque

# Cross-platform input handling
if os.name == 'nt':  # Windows
    import msvcrt
else:  # Unix/Linux/Mac
    import tty
    import termios

def clear_screen():
        os.system("cls" if platform.system() == "Windows" else "clear")

class DebugConsole:
    def __init__(self):
        self.active = False
        self.input_buffer = ""
        self.messages = deque(maxlen=10)
        self.command_history = deque(maxlen=20)
        self.needs_redraw = False  # NEW: Flag to track when console needs updating
        
    def toggle(self):
        self.active = not self.active
        if self.active:
            self.input_buffer = ""
        self.needs_redraw = True  # NEW: Mark for redraw when toggled
            
    def add_message(self, message):
        self.messages.append(f"[{time.strftime('%H:%M:%S')}] {message}")
        self.needs_redraw = True  # NEW: Mark for redraw when message added
        
    def update_input(self, char):
        """Handle input character and mark for redraw"""
        if ord(char) >= 32 and len(self.input_buffer) < 50:
            self.input_buffer += char
            self.needs_redraw = True
        elif char in ['\b', '\x7f']:  # Backspace
            if self.input_buffer:
                self.input_buffer = self.input_buffer[:-1]
                self.needs_redraw = True
                
    def clear_input(self):
        """Clear input buffer"""
        self.input_buffer = ""
        self.needs_redraw = True
        
    def draw(self, force=False):
        """Draw debug console in separate area"""
        if not self.active:
            return False
            
        # Only redraw if needed (unless forced)
        if not force and not self.needs_redraw:
            return False
            
        # Move cursor to debug console area (below game grid)
        print(f"\033[25;1H", end='')  # Move to row 25, column 1
        
        # Clear the debug area
        for i in range(8):  # Clear 8 lines for debug console
            print(f"\033[{25+i};1H\033[K", end='')  # Clear each line
        
        # Draw debug console
        print(f"\033[25;1H{Colors.RED}{'='*60}")
        print(f"{Colors.RED}DEBUG CONSOLE{Colors.RESET}")
        print(f"{Colors.RED}{'='*60}")
        
        # Show recent messages
        for i, msg in enumerate(list(self.messages)[-4:]):  # Show last 4 messages
            print(f"\033[{28+i};1H{Colors.DIM}{msg}{Colors.RESET}")
            
        # Input line
        print(f"\033[32;1H{Colors.WHITE}debug> {self.input_buffer}_")
        print(f"\033[33;1H{Colors.DIM}Type 'help' for commands, ESC to close{Colors.RESET}")
        
        sys.stdout.flush()
        self.needs_redraw = False
        return True
class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3
    DEBUG_MODE = 4

class Colors:
    RESET = '\033[0m'
    CYAN = '\033[96m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BLACK = '\033[30m'
    BG_BLACK = '\033[40m'
    BG_CYAN = '\033[106m'
    BG_ORANGE = '\033[103m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    BLINK = '\033[5m'

class InputHandler:
    def __init__(self):
        self.input_queue = deque()
        self.running = True
        
    def start_input_thread(self):
        """Start background input thread"""
        if os.name == 'nt':
            threading.Thread(target=self._windows_input, daemon=True).start()
        else:
            threading.Thread(target=self._unix_input, daemon=True).start()
            
    def _windows_input(self):
        """Windows input handler"""
        while self.running:
            if msvcrt.kbhit():
                char = msvcrt.getch().decode('utf-8', errors='ignore')
                self.input_queue.append(char)
            time.sleep(0.01)
            
    def _unix_input(self):
        """Unix/Linux input handler"""
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(sys.stdin.fileno())
            while self.running:
                if select.select([sys.stdin], [], [], 0.01)[0]:
                    char = sys.stdin.read(1)
                    self.input_queue.append(char)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            
    def get_input(self):
        """Get next input character if available"""
        if self.input_queue:
            return self.input_queue.popleft()
        return None
        
    def stop(self):
        """Stop input handler"""
        self.running = False

class TronGame:
    def __init__(self, width=40, height=20):
        self.width = width
        self.height = height
        self.grid = [[' ' for _ in range(width)] for _ in range(height)]
        self.state = GameState.MENU
        
        # Player setup
        self.player_pos = [height//2, width//4]
        self.player_dir = Direction.RIGHT
        self.player_trail = deque()
        
        # AI setup  
        self.ai_pos = [height//2, 3*width//4]
        self.ai_dir = Direction.LEFT
        self.ai_trail = deque()
        
        # Game state
        self.running = True
        self.game_speed = 0.35
        self.score = {"player": 0, "ai": 0}
        
        # Input system
        self.input_handler = InputHandler()
        
        self.init_display()
        self.render_offset = 0
        
    def init_display(self):
        """Initialize display settings"""
        if os.name == 'nt':  # Windows
            os.system('mode con: cols=100 lines=35')
        
        # Hide cursor
        print('\033[?25l', end='')
        sys.stdout.flush()
    
    def clear_screen(self):
        """Move cursor to top-left without clearing the screen buffer."""
        print("\033[H", end='') 
        
    def draw_border(self, char='█', color=Colors.CYAN):
        """Draw a border around the game area"""
        border = color + char * (self.width + 2) + Colors.RESET
        return border
        
    def draw_menu(self):
        """Draw the main menu"""
        self.clear_screen()
        
        title = f"""
{Colors.CYAN}{Colors.BOLD}
    ████████ ██████   ██████  ███    ██     ███████ ██   ██ ███████ 
       ██    ██   ██ ██    ██ ████   ██     ██       ██ ██  ██      
       ██    ██████  ██    ██ ██ ██  ██     █████     ███   █████   
       ██    ██   ██ ██    ██ ██  ██ ██     ██       ██ ██  ██      
       ██    ██   ██  ██████  ██   ████ ██  ███████ ██   ██ ███████ 
                                                                     
{Colors.ORANGE}              Light Cycle Combat System v2.1{Colors.RESET}
        """
        
        menu = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════╗
║                    SYSTEM COMMANDS                       ║
╠══════════════════════════════════════════════════════════╣
║  {Colors.WHITE}[ENTER]{Colors.CYAN} - Initialize Combat Grid                        ║
║  {Colors.WHITE}[Q]{Colors.CYAN}     - Quit to DOS                                   ║
║                                                          ║
║  {Colors.ORANGE}CONTROLS:{Colors.CYAN}                                               ║
║  {Colors.WHITE}WASD{Colors.CYAN}   - Navigate Light Cycle                           ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

{Colors.DIM}Status: Waiting for user input... (Press keys as shown above){Colors.RESET}
        """
        
        print(title + menu)
        sys.stdout.flush()
        
    def draw_game(self):
        """Draw the game grid and UI"""
        self.clear_screen()
        print("\033[H", end='')  # Move to top
        print("\n" * self.render_offset, end='')
        # Header
        print(f"{Colors.CYAN}{Colors.BOLD}TRON.EXE - Combat Grid Active{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        
        # Status bar
        status = f"Player: {Colors.CYAN}■{Colors.RESET} [{self.score['player']}]  |  "
        status += f"AI: {Colors.ORANGE}■{Colors.RESET} [{self.score['ai']}]"
            
        print(status)
        print()
        
        # Game grid
        print(self.draw_border())
        for row in range(self.height):
            line = Colors.CYAN + '█'
            for col in range(self.width):
                cell = self.grid[row][col]
                if [row, col] == self.player_pos:
                    line += Colors.CYAN + Colors.BG_CYAN + '●' + Colors.RESET
                elif [row, col] == self.ai_pos:
                    line += Colors.ORANGE + Colors.BG_ORANGE + '●' + Colors.RESET
                elif cell == 'P':
                    line += Colors.CYAN + '▒'
                elif cell == 'A':
                    line += Colors.ORANGE + '▒'
                else:
                    line += Colors.BLACK + '.'
            line += Colors.CYAN + '█' + Colors.RESET
            print(line)
        print(self.draw_border())
        
        # Controls reminder
        print(f"\n{Colors.DIM}Controls: WASD=Move{Colors.RESET}")
        
        sys.stdout.flush()

        
    def handle_input(self):
        """Handle keyboard input"""
        char = self.input_handler.get_input()
        if not char:
            return
            
        # Handle special keys
        if char in ['\r', '\n']:  # Enter
            if self.state == GameState.MENU:
                self.start_game()
            elif self.state == GameState.GAME_OVER:
                self.start_game()   #restart immediately 
                
        elif char.lower() == 'q':
            if self.state == GameState.MENU:
                self.running = False
            elif self.state == GameState.GAME_OVER:
                if char.lower() == 'q':
                    clear_screen()
                    self.state = GameState.MENU #return to menu when quit after game over
                elif char == '\n':
                    clear_screen()
                    self.start_game #restart game when enter is pressed after game over
                
        # Game controls
        elif self.state == GameState.PLAYING:
            char = char.lower()
            if char == 'w' and self.player_dir != Direction.DOWN:
                self.player_dir = Direction.UP
            elif char == 's' and self.player_dir != Direction.UP:
                self.player_dir = Direction.DOWN
            elif char == 'a' and self.player_dir != Direction.RIGHT:
                self.player_dir = Direction.LEFT
            elif char == 'd' and self.player_dir != Direction.LEFT:
                self.player_dir = Direction.RIGHT
                            
    def start_game(self):
        """Start a new game"""
        clear_screen()
        self.state = GameState.PLAYING
        self.render_offset = 5
        self.reset_game()
        
    def reset_game(self):
        """Reset game state"""
        self.grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.player_pos = [self.height//2, self.width//4]
        self.player_dir = Direction.RIGHT
        self.player_trail.clear()
        
        self.ai_pos = [self.height//2, 3*self.width//4]
        self.ai_dir = Direction.LEFT
        self.ai_trail.clear()
        self.render_offset = 5
        
    def move_player(self):
        """Move player light cycle"""
        # Add current position to trail
        row, col = self.player_pos
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row][col] = 'P'
            self.player_trail.append([row, col])
            
        # Calculate new position
        dr, dc = self.player_dir.value
        new_row = self.player_pos[0] + dr
        new_col = self.player_pos[1] + dc
        
        # Check collision
        if self.check_collision(new_row, new_col):
            self.game_over("AI")
            return
            
        self.player_pos = [new_row, new_col]
        
    def move_ai(self):
        """Move AI light cycle"""
        # Add current position to trail
        row, col = self.ai_pos
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row][col] = 'A'
            self.ai_trail.append([row, col])
            
        # Smart AI movement
        self.ai_dir = self.get_ai_direction()
            
        # Calculate new position
        dr, dc = self.ai_dir.value
        new_row = self.ai_pos[0] + dr
        new_col = self.ai_pos[1] + dc
        
        # Check collision
        if self.check_collision(new_row, new_col):
            self.game_over("Player")
            return
            
        self.ai_pos = [new_row, new_col]
        
    def get_ai_direction(self):
        """Calculate best AI direction"""
        current_dir = self.ai_dir
        possible_dirs = []
        
        for direction in Direction:
            # Don't reverse direction
            if direction == Direction.UP and current_dir == Direction.DOWN:
                continue
            if direction == Direction.DOWN and current_dir == Direction.UP:
                continue
            if direction == Direction.LEFT and current_dir == Direction.RIGHT:
                continue
            if direction == Direction.RIGHT and current_dir == Direction.LEFT:
                continue
                
            dr, dc = direction.value
            new_row = self.ai_pos[0] + dr
            new_col = self.ai_pos[1] + dc
            
            if not self.check_collision(new_row, new_col):
                # Simple scoring: prefer moves away from walls and trails
                score = 0
                score += min(new_row, self.height - new_row - 1)
                score += min(new_col, self.width - new_col - 1)
                
                # Avoid getting too close to player
                player_dist = abs(new_row - self.player_pos[0]) + abs(new_col - self.player_pos[1])
                if player_dist < 3:
                    score -= 5
                    
                possible_dirs.append((direction, score))
                
        if possible_dirs:
            possible_dirs.sort(key=lambda x: x[1], reverse=True)
            return possible_dirs[0][0]
        else:
            return current_dir
            
    def check_collision(self, row, col):
        """Check if position causes collision"""
        # Wall collision
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            return True
            
        # Trail collision
        if self.grid[row][col] in ['P', 'A']:
            return True
            
        return False
        
    def game_over(self, winner):
        """Handle game over"""
        clear_screen()
        self.state = GameState.GAME_OVER
        self.score[winner.lower()] += 1
        
        self.clear_screen()
        
        if winner == "Player":
            print(f"""
{Colors.CYAN}{Colors.BOLD}
     _   _ _____ _____ _____ _____________   __
    | | | |_   _/  __ \_   _|  _  | ___ \ \ / /
    | | | | | | | /  \/ | | | | | | |_/ /\ V / 
    | | | | | | | |     | | | | | |    /  \ /  
    \ \_/ /_| |_| \__/\ | | \ \_/ / |\ \  | |  
     \___/ \___/ \____/ \_/  \___/\_| \_| \_/ 
{Colors.RESET}
            {Colors.GREEN}Light Cycle Combat Won!{Colors.RESET}
            """)
        else:
            print(f"""
{Colors.RED}{Colors.BOLD}
    ______ ___________ _____  ___ _____ ___________ 
    |  _  \  ___|  ___|  ___|/ _ \_   _|  ___|     |
    | | | | |__ | |_  | |__ / /_\ \| | | |__ | | | |
    | | | |  __||  _| |  __||  _  || | |  __|| | | |
    | |/ /| |___| |   | |___| | | || | | |___| |/ / 
    |___/ \____/\_|   \____/\_| |_/\_/ \____/|___/  
{Colors.RESET}
              {Colors.RED}System Deresolution{Colors.RESET}
            """)
            
        print(f"\n{Colors.CYAN}Final Score: Player {self.score['player']} - {self.score['ai']} AI{Colors.RESET}")
        print(f"{Colors.WHITE}Press [ENTER] for new game or [Q] to quit{Colors.RESET}")
        sys.stdout.flush()
            
    def run(self):
        """Main game loop"""
        try:
            # Start input handler
            self.input_handler.start_input_thread()
            
            while self.running:
                if self.state == GameState.MENU:
                    self.draw_menu()
                    
                elif self.state == GameState.PLAYING:
                    self.move_player()
                    if self.state == GameState.PLAYING:  # Check if still playing
                        self.move_ai()
                    if self.state == GameState.PLAYING:  # Check again
                        self.draw_game()
                        
                elif self.state == GameState.GAME_OVER:
                    pass  # Handled in game_over method
                        
                self.handle_input()
                time.sleep(self.game_speed)
                
        except KeyboardInterrupt:
            pass
        finally:
            # Cleanup
            self.input_handler.stop()
            # Restore cursor and clear screen
            print('\033[?25h', end='')
            self.clear_screen()
            print(f"{Colors.CYAN}Thanks for playing TRON.EXE!{Colors.RESET}")
            sys.stdout.flush()

if __name__ == "__main__":
    print("Initializing TRON Light Cycle Combat System...")
    print("Loading combat protocols...")
    time.sleep(2)
    
    try:
        game = TronGame()
        game.run()
    except Exception as e:
        print(f"System Error: {e}")
        print("Game requires a terminal with ANSI color support.")
    