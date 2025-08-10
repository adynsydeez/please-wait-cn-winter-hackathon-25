    
def tic_tac_toe():

    start_message = "Welcome to your first Tic Tac Toe game!"

    game_board = [[' ', 'A', 'B', 'C'],
                        ['1', '_', '_', '_'],
                        ['2', '_', '_', '_'],
                        ['3', '_', '_', '_']]


    def print_game():
        print('\n')
        for row in game_board:
            for position in row:
                print(position, end = '   ')
            print('\n')
            
        
    def update_board(move, player):

        if move == "A1":
            if player == 1:
                game_board[1][1] = "X"
                print_game()

            elif player == 2:
                game_board[1][1] = "O"
                print_game()

        elif move == "A2":
            if player == 1:
                game_board[2][1] = "X"
                print_game()
            
            elif player == 2:
                game_board[2][1] = "O"
                print_game()

        elif move == "A3":
            if player == 1:
                game_board[3][1] = "X"
                print_game()
            
            elif player == 2:
                game_board[3][1] = "O"
                print_game()

        elif move == "B1":
            if player == 1:
                game_board[1][2] = "X"
                print_game()

            elif player == 2:
                game_board[1][2] = "O"
                print_game()

        elif move == "B2":
            if player == 1:
                game_board[2][2] = "X"
                print_game()

            elif player == 2:
                game_board[2][2] = "O"
                print_game()

        elif move == "B3":
            if player == 1:
                game_board[3][2] = "X"
                print_game()

            elif player == 2:
                game_board[3][2] = "O"
                print_game()

        elif move == "C1":
            if player == 1:
                game_board[1][3] = "X"
                print_game()

            elif player == 2:
                game_board[1][3] = "O"
                print_game()

        elif move == "C2":
            if player == 1:
                game_board[2][3] = "X"
                print_game()

            elif player == 2:
                game_board[2][3] = "O"
                print_game()

        elif move == "C3":
            if player == 1:
                game_board[3][3] = "X"
                print_game()

            elif player == 2:
                game_board[3][3] = "O"
                print_game()


    def someone_won(board):
        # column_A
        # game_board[1][1]
        # game_board[2][1]
        # game_board[3][1]

        if board[1][1] == board[2][1] == board[3][1]:
            if board[1][1] != '_':
                return True

        # column_B
        # game_board[1][2]
        # game_board[2][2]
        # game_board[3][2]

        elif board[1][2] == board[2][2] == board[3][2]:
            if board[1][2] != '_':
                return True

        # column_C
        # game_board[1][3]
        # game_board[2][3]
        # game_board[3][3]

        elif board[1][3] == board[2][3] == board[3][3]:
            if board[1][3] != '_':
                return True

        # row_1
        # game_board[1][1]
        # game_board[1][2]
        # game_board[1][3]

        elif board[1][1] == board[1][2] == board[1][3]:
            if board[1][1] != '_':
                return True

        # row_2
        # game_board[2][1]
        # game_board[2][2]
        # game_board[2][3]

        elif board[2][1] == board[2][2] == board[2][3]:
            if board[2][1] != '_':
                return True

        # row_3
        # game_board[3][1]
        # game_board[3][2]
        # game_board[3][3]

        elif board[3][1] == board[3][2] == board[3][3]:
            if board[3][1] != '_':
                return True

        # diagonal_1
        # game_board[1][1]
        # game_board[2][2]
        # game_board[3][3]

        elif board[1][1] == board[2][2] == board[3][3]:
            if board[1][1] != '_':
                return True

        # diagonal_2
        # game_board[1][3]
        # game_board[2][2]
        # game_board[3][1]

        elif board[1][3] == board[2][2] == board[3][1]:
            if board[1][3] != '_':
                return True
        
        else:
            return False

        # game_board = [[' ', 'A', 'B', 'C'],
        #                 ['1', '_', '_', '_'],
        #                 ['2', '_', '_', '_'],
        #                 ['3', '_', '_', '_']]
    
    

    def brain_rot_ai():
        import copy
        import random

        player_mark = 'O'  # AI is always player 2

        coord_to_move = {
            (1, 1): 'A1', (2, 1): 'A2', (3, 1): 'A3',
            (1, 2): 'B1', (2, 2): 'B2', (3, 2): 'B3',
            (1, 3): 'C1', (2, 3): 'C2', (3, 3): 'C3'
        }

        possible_moves = [(r, c) for r in range(1, 4) for c in range(1, 4)
                        if game_board[r][c] == '_']

        random.shuffle(possible_moves)

        for row, col in possible_moves:
            test_board = copy.deepcopy(game_board)
            test_board[row][col] = player_mark

            if not someone_won(test_board):
                return coord_to_move[(row, col)]

        # fallback
        if possible_moves:
            return coord_to_move[possible_moves[0]]

        return None
    
    import random

    def simple_ai():
        coord_to_move = {
            (1, 1): 'A1', (2, 1): 'A2', (3, 1): 'A3',
            (1, 2): 'B1', (2, 2): 'B2', (3, 2): 'B3',
            (1, 3): 'C1', (2, 3): 'C2', (3, 3): 'C3'
        }

        possible_moves = [(r, c) for r in range(1, 4) for c in range(1, 4)
                        if game_board[r][c] == '_']

        if not possible_moves:
            return None  # No moves left

        choice = random.choice(possible_moves)
        return coord_to_move[choice]


    

    def minimax_algo():

        import copy
        import random

        coord_to_move = {
            (1, 1): 'A1', (2, 1): 'A2', (3, 1): 'A3',
            (1, 2): 'B1', (2, 2): 'B2', (3, 2): 'B3',
            (1, 3): 'C1', (2, 3): 'C2', (3, 3): 'C3'
        }
        
        def minimax(board, is_ai_turn):
            if someone_won(board):
                # Previous player won, so if it's AI's turn now, human won (-10), else AI won (+10)
                return -10 if is_ai_turn else 10
            
            # Check for draw (no empty spaces)
            if all(board[r][c] != '_' for r in range(1, 4) for c in range(1, 4)):
                return 0
            
            if is_ai_turn:
                best_score = -float('inf')
                for r in range(1, 4):
                    for c in range(1, 4):
                        if board[r][c] == '_':
                            new_board = copy.deepcopy(board)
                            new_board[r][c] = 'O'  # AI move
                            score = minimax(new_board, False)
                            best_score = max(best_score, score)
                return best_score
            else:
                best_score = float('inf')
                for r in range(1, 4):
                    for c in range(1, 4):
                        if board[r][c] == '_':
                            new_board = copy.deepcopy(board)
                            new_board[r][c] = 'X'  # Human move
                            score = minimax(new_board, True)
                            best_score = min(best_score, score)
                return best_score

        best_score = -float('inf')
        best_moves = []

        for r in range(1, 4):
            for c in range(1, 4):
                if game_board[r][c] == '_':
                    test_board = copy.deepcopy(game_board)
                    test_board[r][c] = 'O'  # AI move
                    score = minimax(test_board, False)
                    if score > best_score:
                        best_score = score
                        best_moves = [(r, c)]
                    elif score == best_score:
                        best_moves.append((r, c))

        chosen_move = random.choice(best_moves) if best_moves else None
        return coord_to_move[chosen_move] if chosen_move else None

    # def brain_rot_ai():

        from random import randint

        import copy

        test_game_board = copy.deepcopy(game_board)
        
        possible_moves = []
    
        for row in range (1,4):
            for position in range (1,4):
                if game_board[row][position] == '_':
                    possible_moves.append([row, position])

        choice = randint(0, len(possible_moves) - 1)

        choice_position = possible_moves[choice]

        # x = ["A","B","C"]
        # y = ["1","2","3"]
        # test_game_board[choice_position[0]][choice_position[1]] = x[choice_position[0]-1] + y[choice_position[1]-1]



        if choice_position == [1,1]:
            
            if len(possible_moves) != 1:

                test_game_board[1][1] = 'A1'

                if someone_won(test_game_board) == False:
                    
                    return 'A1'
                
                else:
                    test_game_board[1][1] = '_'

                    return brain_rot_ai()
            
            else:

                return 'A1'

        
        elif choice_position == [2,1]:

            if len(possible_moves) != 1:
            
                test_game_board[2][1] = 'A2'

                if someone_won(test_game_board) == False:
                    
                    return 'A2'
                
                else:
                    test_game_board[2][1] = '_'

                    return brain_rot_ai()
            
            else:

                return 'A2'

        
        elif choice_position == [3,1]:

            if len(possible_moves) != 1:
            
                test_game_board[3][1] = 'A3'

                if someone_won(test_game_board) == False:
                    
                    return 'A3'
                
                else:
                    test_game_board[3][1] = '_'

                    return brain_rot_ai()

            else:

                return 'A3'
        
        
        elif choice_position == [1,2]:

            if len(possible_moves) != 1:
            
                test_game_board[1][2] = 'B1'

                if someone_won(test_game_board) == False:
                    
                    return 'B1'
                
                else:
                    test_game_board[1][2] = '_'

                    return brain_rot_ai()

            else:

                return 'B1'

        
        elif choice_position == [2,2]:

            if len(possible_moves) != 1:
            
                test_game_board[2][2] = 'B2'

                if someone_won(test_game_board) == False:
                    
                    return 'B2'
                
                else:
                    test_game_board[2][2] = '_'

                    return brain_rot_ai()

            else:
                
                return 'B2'


        elif choice_position == [3,2]:

            if len(possible_moves) != 1:
            
                test_game_board[3][2] = 'B3'

                if someone_won(test_game_board) == False:
                    
                    return 'B3'
                
                else:
                    test_game_board[3][2] = '_'

                    return brain_rot_ai()

            else:

                return 'B3'

        
        elif choice_position == [1,3]:

            if len(possible_moves) != 1:
            
                test_game_board[1][3] = 'C1'

                if someone_won(test_game_board) == False:
                    
                    return 'C1'
                
                else:
                    test_game_board[1][3] = '_'

                    return brain_rot_ai()

            else:

                return 'C1'

        
        elif choice_position == [2,3]:

            if len(possible_moves) != 1:
            
                test_game_board[2][3] = 'C2'

                if someone_won(test_game_board) == False:
                    
                    return 'C2'
                
                else:
                    test_game_board[2][3] = '_'

                    return brain_rot_ai()

            else:

                return 'C2'

        
        elif choice_position == [3,3]:

            if len(possible_moves) != 1:
            
                test_game_board[3][3] = 'C3'

                if someone_won(test_game_board) == False:
                    
                    return 'C3'
                
                else:
                    test_game_board[3][3] = '_'

                    return brain_rot_ai()
            
            else:

                return 'C3'
    
    


        
        



            
    def main_game():

        print()
        
        print(start_message)

        difficulty = input('''
Pick your difficulty:
                       
Enter 1 for Easy
Enter 2 for Medium
Enter 3 for Hard

''')
        while difficulty not in ['1', '2', '3']:

            difficulty = input('''
Pick your difficulty:
                       
Enter 1 for Easy
Enter 2 for Medium
Enter 3 for Hard

''')

        print_game()

        valid_moves = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']

        made_moves = []

        while made_moves != valid_moves:

            player_1_move_validity = False

            while player_1_move_validity == False:

                player_1_move = (input('Player 1 select a position- ')).upper()

                if player_1_move in valid_moves:
                    
                    if player_1_move not in made_moves:
                        made_moves.append(player_1_move)
                        made_moves.sort()
                        update_board(player_1_move, 1)
                        
                        if someone_won(game_board) == True:
                            print("Player 1 won!!!")
                            return

                        if made_moves == valid_moves:
                            print("It's a draw!")
                            return
                        
                        player_1_move_validity = True

            
            player_2_move_validity = False

            while player_2_move_validity == False:
            
                # player_2_move = (input('Player 2 select a position- ')).upper()

                if difficulty == '1':

                    player_2_move = brain_rot_ai()

                elif difficulty == '2':

                    player_2_move = simple_ai()

                elif difficulty == '3':

                    player_2_move = minimax_algo()
            
                if player_2_move in valid_moves:
                    
                    if player_2_move not in made_moves:
                        made_moves.append(player_2_move)
                        made_moves.sort()
                        update_board(player_2_move, 2)

                        if someone_won(game_board) == True:
                            print("Player 2 won!!!")
                            return

                        if made_moves == valid_moves:
                            print("It's a draw!")
                            return
                        
                        player_2_move_validity = True

    main_game()






tic_tac_toe()