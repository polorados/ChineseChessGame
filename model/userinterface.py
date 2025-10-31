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