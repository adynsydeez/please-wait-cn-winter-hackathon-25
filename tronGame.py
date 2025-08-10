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
import random
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
        self.difficulty = "medium" # default difficulty
        
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
        self.crashed = False
        self.crash_pos = None
        self.crash_winner = None
        
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
║  {Colors.WHITE}[1]{Colors.CYAN}     - Easy AI                                       ║
║  {Colors.WHITE}[2]{Colors.CYAN}     - Medium AI                                     ║
║  {Colors.WHITE}[3]{Colors.CYAN}     - Hard AI                                       ║
║  {Colors.WHITE}[Q]{Colors.CYAN}     - Quit to DOS                                   ║
║                                                          ║
║  {Colors.ORANGE}CONTROLS:{Colors.CYAN}                                               ║
║  {Colors.WHITE}WASD{Colors.CYAN}   - Navigate Light Cycle                           ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
{Colors.WHITE}Difficulty{Colors.CYAN} - {self.difficulty}                                  
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
        char = self.input_handler.get_input()
        if not char:
            return

        
        if self.state == GameState.MENU:
            if char in ['\r', '\n']:  # Enter
                self.start_game()
            elif char == '1':
                self.difficulty = "easy"
                self.draw_menu()
            elif char == '2':
                self.difficulty = "medium"
                self.draw_menu()
            elif char == '3':
                self.difficulty = "hard"
                self.draw_menu()
            elif self.state == GameState.GAME_OVER:
                clear_screen()
                self.start_game()

        elif self.state == GameState.GAME_OVER:
            if char in ['\r', '\n']:  # Enter in game over restarts game
                self.start_game()
            elif char.lower() == 'q':
                clear_screen()
                self.state = GameState.MENU
        
        elif char.lower() == 'q':
            if self.state == GameState.MENU:
                self.running = False
            elif self.state == GameState.GAME_OVER:
                clear_screen()
                self.state = GameState.MENU

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
        if self.check_collision(new_row, new_col) or [new_row, new_col] == self.ai_pos:
            self.crashed = True
            self.crash_pos = [new_row, new_col]
            self.crash_winner = "AI"
            return
            
        self.player_pos = [new_row, new_col]
        
    def move_ai(self):
        """Move AI light cycle"""
        # Add current position to trail
        row, col = self.ai_pos
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row][col] = 'A'
            self.ai_trail.append([row, col])
            
        # Choose ai direction based on selected difficulty
        new_direction = None
        if self.difficulty == "easy":
            new_direction = self.get_ai_direction_easy()
        elif self.difficulty == "hard":
            new_direction = self.get_ai_direction_hard()
        else:
            new_direction = self.get_ai_direction()  # medium difficulty
        
        # CRITICAL: Only update direction if we got a valid one
        if new_direction is not None:
            self.ai_dir = new_direction
            
        # Calculate new position
        dr, dc = self.ai_dir.value
        new_row = self.ai_pos[0] + dr
        new_col = self.ai_pos[1] + dc
        
        # Check collision
        if self.check_collision(new_row, new_col) or [new_row, new_col] == self.player_pos:
            self.crashed = True
            self.crash_pos = [new_row, new_col]
            self.crash_winner = "Player"  # AI crashed, player wins
            return
            
        self.ai_pos = [new_row, new_col]
    
    def check_player_collision(self, next_player_pos, next_ai_pos):
        # Check if both next positions are the same (player collision)
        if next_player_pos == next_ai_pos:
            return True
        return False
    
    def get_ai_direction_easy(self):
        directions = list(Direction)
        random.shuffle(directions)
        for direction in directions:
            dr, dc = direction.value
            nr, nc = self.ai_pos[0] + dr, self.ai_pos[1] + dc
            if not self.check_collision(nr, nc):
                return direction
        return self.ai_dir
    
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
    
    def bfs_path(self, start, goal):
        """Find shortest path from start to goal avoiding collisions using BFS.
       Returns list of positions from start to goal (including start), or [] if no path.
        """
        queue = deque([[start]])
        visited = set([tuple(start)])

        while queue:
            path = queue.popleft()
            current = path[-1]
            if current == tuple(goal):
                return path

            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = current[0] + dr, current[1] + dc

                if 0 <= nr < self.height and 0 <= nc < self.width:
                    if not self.check_collision(nr, nc) and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append(path + [(nr, nc)])

        return []
      
    def get_ai_direction_hard(self):
        px, py = self.player_pos
        pdx, pdy = self.player_dir.value

        steps_ahead = 3
        predicted = None

        while steps_ahead > 0:
            pred_x = px + pdx * steps_ahead
            pred_y = py + pdy * steps_ahead

            # Check if predicted position is within bounds BEFORE using it
            if (pred_x < 0 or pred_x >= self.height or 
                pred_y < 0 or pred_y >= self.width or 
                self.check_collision(pred_x, pred_y)):
                steps_ahead -= 1
                continue

            # Find path from AI to predicted position
            path = self.bfs_path(tuple(self.ai_pos), (pred_x, pred_y))

            # Check path validity and length
            if path is not None and len(path) >= 2:
                next_pos = path[1]
                dr = next_pos[0] - self.ai_pos[0]
                dc = next_pos[1] - self.ai_pos[1]

                # Find direction leading to next_pos
                next_dir = None
                for direction in Direction:
                    if direction.value == (dr, dc):
                        next_dir = direction
                        break

                # If no direction found, try shorter prediction
                if next_dir is None:
                    steps_ahead -= 1
                    continue

                next_r = self.ai_pos[0] + next_dir.value[0]
                next_c = self.ai_pos[1] + next_dir.value[1]

                # Check if next move is safe
                if self.check_collision(next_r, next_c):
                    steps_ahead -= 1
                    continue

                # Stronger lookahead: check reachable free space from next move
                free_space = self.count_reachable_space((next_r, next_c), max_steps=10)
                MIN_SAFE_SPACE = 7

                if free_space >= MIN_SAFE_SPACE:
                    predicted = (pred_x, pred_y)
                    break
                else:
                    steps_ahead -= 1
            else:
                steps_ahead -= 1

        # Fallback if no predicted safe position found
        if predicted is None:
            if (px >= 0 and px < self.height and py >= 0 and py < self.width and 
                not self.check_collision(px, py)):
                predicted = (px, py)
            else:
                predicted = self.find_nearest_safe(pos=self.player_pos) or tuple(self.ai_pos)

        # Find path to final predicted position
        path = self.bfs_path(tuple(self.ai_pos), predicted)

        if path is not None and len(path) >= 2:
            next_pos = path[1]
            dr = next_pos[0] - self.ai_pos[0]
            dc = next_pos[1] - self.ai_pos[1]

            for direction in Direction:
                if direction.value == (dr, dc):
                    next_r = self.ai_pos[0] + direction.value[0]
                    next_c = self.ai_pos[1] + direction.value[1]
                    if not self.check_collision(next_r, next_c):
                        return direction

        # No valid path found — pick any safe random move
        directions = list(Direction)
        best_dir = None
        max_space = -1

        for d in directions:
            nr = self.ai_pos[0] + d.value[0]
            nc = self.ai_pos[1] + d.value[1]
            if not self.check_collision(nr, nc):
                space = self.count_reachable_space((nr, nc), max_steps=10)
                if space > max_space:
                    max_space = space
                    best_dir = d

        if best_dir:
            return best_dir

        # No safe moves — try to keep current direction if safe
        next_r = self.ai_pos[0] + self.ai_dir.value[0]
        next_c = self.ai_pos[1] + self.ai_dir.value[1]
        if not self.check_collision(next_r, next_c):
            return self.ai_dir

        # CRITICAL: Always return a valid direction, never None
        return self.ai_dir
    
    def find_nearest_safe(self, pos):
        """Find nearest safe position around pos using BFS."""
        visited = set()
        queue = deque([pos])
        while queue:
            r, c = queue.popleft()
            if not self.check_collision(r, c):
                return (r, c)
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) not in visited and 0 <= nr < self.height and 0 <= nc < self.width:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        return None
    
    def is_safe(self, x, y):
        # Out of bounds?
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False
        # Check collision with trails or walls
        if (x, y) in self.trail or (x, y) in self.ai_trail:
            return False
        return True
      
    def _evaluate_move(self, row, col):
        # Basic distance from player
        dist = abs(row - self.player_pos[0]) + abs(col - self.player_pos[1])
        # Check available space by counting free cells around
        free_space = sum(
            not self.check_collision(row + dr, col + dc)
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]
        )
        return dist + free_space * 2
    
    def check_collision(self, row, col):
        """Check if position causes collision"""
        # Wall collision
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            return True
            
        # Trail collision
        if self.grid[row][col] in ['P', 'A']:
            return True
            
        return False
    
    def count_reachable_space(self, start_pos, max_steps=10):
        visited = set()
        queue = deque([(start_pos, 0)])
        count = 0
        while queue:
            (r, c), steps = queue.popleft()
            if (r, c) in visited or steps > max_steps:
                continue
            visited.add((r, c))
            count += 1
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r + dr, c + dc
                if not self.check_collision(nr, nc) and (nr, nc) not in visited:
                    queue.append(((nr, nc), steps + 1))
        return count
       
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
            self.input_handler.start_input_thread()
            self.crashed = False
            self.crash_pos = None
            self.crash_winner = None

            while self.running:
                if self.state == GameState.MENU:
                    self.draw_menu()

                elif self.state == GameState.PLAYING:
                    # Move both players first
                    self.move_player() 
                    if not self.crashed and self.state == GameState.PLAYING:
                        self.move_ai()

                    # Check if either crashed during movement
                    if self.crashed:
                        # Mark crash on grid
                        if self.crash_pos:
                            r, c = self.crash_pos
                            if 0 <= r < self.height and 0 <= c < self.width:
                                self.grid[r][c] = 'X'  # Visible crash marker

                        self.draw_game()  # Draw crash frame
                        time.sleep(1.5)   # Pause so user can see the impact
                        self.game_over(self.crash_winner)
                        self.crashed = False
                        continue

                    if self.state == GameState.PLAYING:
                        self.draw_game()

                elif self.state == GameState.GAME_OVER:
                    pass  # handled in game_over()

                self.handle_input()
                time.sleep(self.game_speed)

        except KeyboardInterrupt:
            pass
        finally:
            self.input_handler.stop()
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
    