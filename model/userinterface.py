class UserInterface:
    def __init__(self):
        self.commands = {
            'help': 'Show available commands',
            'move': 'Make a move (e.g., "e2 e4")',
            'history': 'Show move history',
            'status': 'Show current game status',
            'resign': 'Resign from the game',
            'save': 'Save the current game',
            'load': 'Load a saved game',
            'quit': 'Exit the game'
        }

    def display_welcome(self):
        # Display a welcome message
        print("=" * 50)
        print("           WELCOME TO JUNGLE CHESS")
        print("=" * 50)
        print("\nCommands:")
        for cmd, desc in self.commands.items():
            print(f"  {cmd:8} - {desc}")
        print("\nEnter 'help' at any time to see available commands.")
        print("=" * 50)
        print()

    def get_user_input(self):
        # Get command input from the user
        try:
            user_input = input("\nEnter command: ").strip().lower()
            return user_input
        except (EOFError, KeyboardInterrupt):
            return "quit"

    def display_game_status(self, game):
        """Show the current game status"""
        if not game:
            print("No game in progress.")
            return

        print("\n" + "=" * 40)
        print("CURRENT GAME STATUS")
        print("=" * 40)
        
        # Display current player
        current_player = "White" if game.current_player == 'w' else "Black"
        print(f"Current turn: {current_player}")

        print("=" * 40)

    def display_move_history(self, history):
        # Display the history of moves
        if not history:
            print("No moves have been made yet.")
            return

        print("\n" + "=" * 40)
        print("MOVE HISTORY")
        print("=" * 40)
        
        # Display moves in a chess notation format
        for i, move in enumerate(history, 1):
            move_number = (i + 1) // 2
            if i % 2 == 1:  # White's move
                print(f"white move {move_number}. {move}", end="")
            else:  # Black's move
                print(f"black move {move_number}. {move}")
        
        # If last move was white and no black response yet
        if len(history) % 2 == 1:
            print()  # New line for incomplete pair
        
        print("=" * 40)


    def display_board(self, board):

        print("\n      " + "            ".join("abcdefgh"))

        for row in range(9):
            print(7*("+"+12*"-")+"+")
            print(7*("|"+12*" ")+"|")
            
            for col in range(7):
                cell = board[row][col]
                if cell[0] == None : 
                    symbol = cell[1].symbol if cell is not None else ''
                else :
                    symbol = cell[0].symbol
                print("|", end="")
                #print(symbol, end="        ")
                for i in range((12-len(symbol))//2):
                    print(end=" ")
                print(symbol, end="")
                for i in range(12-((12-len(symbol))//2)-len(symbol)):
                    print(end=" ")
            print("|")
            print(7*("|"+12*" ")+"|", end="")
            print()  # New line after each row
        print(7*("+"+12*"-")+"+")

        print("\n      " + "            ".join("abcdefgh"))


    def display_help(self):
        """Display available commands"""
        print("\n" + "=" * 50)
        print("AVAILABLE COMMANDS")
        print("=" * 50)
        for cmd, desc in self.commands.items():
            print(f"  {cmd:8} - {desc}")
        print("=" * 50)

    def display_move_prompt(self, current_player):
        """Prompt for a move from the current player"""
        player_name = "White" if current_player == 'w' else "Black"
        print(f"\n{player_name}'s turn. Enter your move (e.g., 'a1 a2') or 'help' for commands:")

    def display_invalid_move(self, message="Invalid move. Please try again."):
        """Display invalid move message"""
        print(f"\n{message}")

    def display_valid_move(self, move_from, move_to, piece_symbol):
        """Display confirmation of a valid move"""
        print(f"\nMove accepted: {piece_symbol} from {move_from} to {move_to}")

    def display_game_result(self, winner):
        """Display game result (win, draw, resignation)"""
        print("\n" + "=" * 50)
        print("GAME OVER")
        print("=" * 50)
        
        
        print(winner + " wins!")

        print("=" * 50)

    def display_save_success(self, filename):
        """Display successful save message"""
        print(f"\nGame successfully saved to '{filename}'")

    def display_load_success(self, filename):
        """Display successful load message"""
        print(f"\nGame successfully loaded from '{filename}'")

    def display_resignation(self, player):
        """Display resignation confirmation"""
        player_name = "White" if player == 'w' else "Black"
        print(f"\n⚐ {player_name} has resigned from the game.")

    def display_quit_confirmation(self):
        """Ask for confirmation before quitting"""
        response = input("\nAre you sure you want to quit? (y/n): ").strip().lower()
        return response in ['y', 'yes']
    
    def display_error(self, error_message):
        """Display general error messages"""
        print(f"\nError: {error_message}")