    
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


    def someone_won():
        # column_A
        # game_board[1][1]
        # game_board[2][1]
        # game_board[3][1]

        if game_board[1][1] == game_board[2][1] == game_board[3][1]:
            if game_board[1][1] != '_':
                return True

        # column_B
        # game_board[1][2]
        # game_board[2][2]
        # game_board[3][2]

        elif game_board[1][2] == game_board[2][2] == game_board[3][2]:
            if game_board[1][2] != '_':
                return True

        # column_C
        # game_board[1][3]
        # game_board[2][3]
        # game_board[3][3]

        elif game_board[1][3] == game_board[2][3] == game_board[3][3]:
            if game_board[1][3] != '_':
                return True

        # row_1
        # game_board[1][1]
        # game_board[1][2]
        # game_board[1][3]

        elif game_board[1][1] == game_board[1][2] == game_board[1][3]:
            if game_board[1][1] != '_':
                return True

        # row_2
        # game_board[2][1]
        # game_board[2][2]
        # game_board[2][3]

        elif game_board[2][1] == game_board[2][2] == game_board[2][3]:
            if game_board[2][1] != '_':
                return True

        # row_3
        # game_board[3][1]
        # game_board[3][2]
        # game_board[3][3]

        elif game_board[3][1] == game_board[3][2] == game_board[3][3]:
            if game_board[3][1] != '_':
                return True

        # diagonal_1
        # game_board[1][1]
        # game_board[2][2]
        # game_board[3][3]

        elif game_board[1][1] == game_board[2][2] == game_board[3][3]:
            if game_board[1][1] != '_':
                return True

        # diagonal_2
        # game_board[1][3]
        # game_board[2][2]
        # game_board[3][1]

        elif game_board[1][3] == game_board[2][2] == game_board[3][1]:
            if game_board[1][3] != '_':
                return True
        
        else:
            return False

        

            
    def main_game():
        
        print(start_message)

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
                        
                        if someone_won() == True:
                            print("Player 1 won!!!")
                            return

                        if made_moves == valid_moves:
                            print("It's a draw!")
                            return
                        
                        player_1_move_validity = True

            
            player_2_move_validity = False

            while player_2_move_validity == False:
            
                player_2_move = (input('Player 2 select a position- ')).upper()
            
                if player_2_move in valid_moves:
                    
                    if player_2_move not in made_moves:
                        made_moves.append(player_2_move)
                        made_moves.sort()
                        update_board(player_2_move, 2)

                        if made_moves == valid_moves:
                            print("It's a draw!")
                            return
                        
                        player_2_move_validity = True

    main_game()