from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from typing import Optional, List, Tuple

class Position:
    row: int
    col: int
    
class Piece:
    id: int
    name: str
    rank: Rank
    owner: Player
    position: Position
    is_alive: bool = True

    def __init__(self, name, rank: Rank, owner: Player, position: Position):
        self.id = id(self)
        self.name = name
        self.rank = rank
        self.owner = owner
        self.position = position
    
    def remove_piece(self):
        self.is_alive = False
        self.position = None
        
RANK_MAP = {
    'R': Rank.RAT,
    'C': Rank.CAT,
    'D': Rank.DOG,
    'W': Rank.WOLF,
    'P': Rank.LEOPARD,
    'T': Rank.TIGER,
    'L': Rank.LION,
    'E': Rank.ELEPHANT
}

#E = Elephant, W = wolf, p = leopard, r = rat,
#c = cat, d = dog
#t = tiger l = lion
PIECE_MAP = [
    "L.....T",
    ".D...C.",
    "R.P.W.E",
    ".......",
    ".......",
    ".......",
    "E.W.P.R",
    ".C...D.",
    "T.....L",
]
# . = land, t = trap, d = den, r = river
CELL_MAP = [
    "..tdt..",
    "...t...",
    ".......",
    ".rr.rr.",
    ".rr.rr.",
    ".rr.rr.",
    ".......",
    "...t...",
    "..tdt..",
]
class Game:
    board: Board
    rules: GameRules
    players: Tuple[Player, Player] #(playerid1, playerid2)
    whose_turn: int #0: player1 1: player2
    move_stack: dict # (piece, from, to)
    move_history: list[str] #record in human readable string

    def __init__(self, player1, player2):
        self.board = Board()
        self.rules = GameRules()
        self.players = [player1, player2]
        self.whose_turn = 0
        self.move_stack = []
        self.move_history = []
    
    def initialize_piece(self):
        ret = []
        for i, line in enumerate(PIECE_MAP):
            for j,chr in enumerate(line):
                if chr =='.':
                    continue
                rank = RANK_MAP[chr]
                owner = self.players[0] if i < 3 else self.players[1]
                pos = Position(i,j)
                piece = Piece(chr,rank,owner,pos)
                ret.append((i,j,piece))
        return ret
    
    def initialize_cell(self):
        ret = []
        for i,line in enumerate(CELL_MAP):
            for j,chr in enumerate(line):
                if chr =='.':
                    cell = ("land",None)
                if chr == 't':
                    owner = self.players[0] if i < 3 else self.players[1]
                    cell = ("trap",None)
                elif chr == 'd':
                    owner = self.players[0] if i < 3 else self.players[1]
                    cell = ("den",owner)
                elif chr == '~':
                    cell = ("river",None)
                ret.append((i,j,cell))
        return ret
    
    def initial_board_setup(self):
        self.board.setup_board(self.initialize_piece(), self.initialize_cell())

    def move_piece(self, from_pos, to_pos):
        mover = self.board.piece_at(from_pos)
        if mover is None:
            return False 
        if mover.owner is not self.players[self.whose_turn]: #check whether mover's turn
            return False
        
        is_valid, captured_piece = self.rules.validate_move(mover, from_pos, to_pos, self.board) #no valid move
        if not is_valid:
            return False
        
        undo_object = {
            "piece": mover,
            "from_pos": from_pos,
            "to_pos": to_pos,
            "captured": captured_piece,
            "prev_turn": self.whose_turn
        }
        self.move_stack.append(undo_object) #record move for undo

        # remove dead piece from board
        if captured_piece is not None:
            captured_piece.is_alive = False
            self.board.remove_piece_at(to_pos)
            captured_piece.owner.remove_piece(captured_piece)

        self.board.move_piece(mover, to_pos)
        self.record_move(mover, from_pos, to_pos, captured_piece)
        self.switch_turn()
        return True

    #보류
    def record_move(self,piece_id,from_pos,to_pos, captured_piece):
        self.move_history.append((piece_id,from_pos,to_pos,captured_piece))

    def undo_move(self): 
        #undo move from top of the stack

        if not self.move_stack:
            return False
        
        move = self.move_stack.pop()

        mover = move["piece"]
        from_pos = move["from_pos"]
        to_pos = move["to_pos"]
        captured_piece = move["captured_piece"]
        prev_turn = move["prev_turn"]

        self.board.move_piece(mover, from_pos)
        mover.position = from_pos

        if captured_piece is not None:
            captured_piece.is_alive = True
            captured_piece.position = to_pos
            self.board.place(captured_piece, to_pos)
            captured_piece.owner.add_piece(captured_piece)

        self.whose_turn = prev_turn

        return True

    def switch_turn(self):
        self.whose_turn = 1-self.whose_turn

    def get_owner_idx(self, owner):
        return 0 if owner is self.players[0] else 1

    def has_alive_pieces(self, owner_idx):
        player = self.players[owner_idx]
        
        return player.get_alive_pieces() > 0
    
    def check_victory(self,mover,to_pos):
        # return (bool,winner). winner = None if bool = False
        cell = self.board.grid[to_pos.row][to_pos.col][1]
        mover_idx = self.get_owner_idx(mover.owner)

        if cell[0] == "den":
            den_owner_idx = 0 if cell[1] == self.players[0] else 1
            if den_owner_idx != mover_idx:
                return True, mover_idx
        if not self.has_alive_pieces(1-mover_idx):
            return True, mover_idx
        
        return False, None


    def save_game(self):
        SaveGame.save_game(self)

    def load_game(self):
        SaveGame.load_game(self)

class Board:
    # piece_list : (row, col, piece object)
    # cell_list: (row,col, (cell_name,owner))
    def __init__(self, piece_list, cell_list):
        self.rows = 9
        self.cols = 7
        # Create grid where each position is a tuple (piece, cell)
        self.grid = [[(None, None) for _ in range(self.cols)] for _ in range(self.rows)]
        #self.move_history = []
        self.setup_board(piece_list, cell_list)
        

    def setup_board(self, piece_list, cell_list):
        # Initialize all positions with (None, None)
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col] = (None, None)
        
        # Set pieces
        for row, col, piece in piece_list:
            current_cell = self.grid[row][col][1]  # Preserve existing cell
            self.grid[row][col] = (piece, current_cell)
        
        # Set cells
        for row, col, cell in cell_list:
            current_piece = self.grid[row][col][0]  # Preserve existing piece
            self.grid[row][col] = (current_piece, cell)

    def place(self, piece, pos):
        # place dead piece for undo
        cell = self.grid[pos.row][pos.col][1]
        self.grid[pos.row][pos.col][0] = (piece,cell)
        piece.position = pos

    def remove_piece_at(self, pos):
        piece, cell = self.grid[pos.row][pos.col]

        if piece is not None:
            self.grid[pos.row][pos.col] = (None, cell)
        return piece

    def move_piece(self, piece, to_pos):
        #just move the cell without validation
        if piece is None:
            return
        from_pos = piece.position
        if from_pos is None:
            return
        
        from_pos_piece, from_pos_cell = self.grid[from_pos.row][from_pos.col]
        to_pos_piece, to_pos_cell = self.grid[to_pos.row][to_pos.col]

        self.grid[from_pos.row][from_pos.col] = (None, from_pos_cell)
        self.grid[to_pos.row][to_pos.col] = (piece, to_pos_cell)
        piece.position = to_pos

class Player:
    def _init_(self, name):
        self.id = id(self)
        self.name=name
        self.pieces=[]

    def add_piece(self, piece):
        if piece not in self.pieces:
            self.pieces.append(piece)

    def remove_piece(self, piece):
        if piece in self.pieces:
            self.pieces.remove(piece)

    def get_alive_pieces(self):
        return [piece for piece in self.pieces if piece.is_alive]
        
    def __str__(self):
        return f"Player({self.name}) with {len(self.get_alive_pieces())} active pieces"


class GameRules:
  def _init_(self):
    pass,

  def validate_move(self, piece, from_pos: Position, to_pos: Position, board):
    """Validate a piece's move according to Jungle Chess rules."""

    # 1. Base checks
    if piece is None:
      return False, "No piece selected."

    if not (0 <= to_pos.row < board.rows and 0 <= to_pos.col < board.cols):
      return False, "Move out of board boundaries."

    target_piece, target_cell = board.grid[to_pos.row][to_pos.col]
    _, from_cell = board.grid[from_pos.row][from_pos.col]

    dest_terrain, dest_owner = target_cell if target_cell else ("land", None)
    start_terrain, _ = from_cell if from_cell else ("land", None)

    # 2. Movement distance
    row_diff = to_pos.row - from_pos.row
    col_diff = to_pos.col - from_pos.col
    delta_row, delta_col = abs(row_diff), abs(col_diff)
    
    is_one_step = (delta_row + delta_col == 1)

    # 3. Special Jump Rule for Lion/Tiger
    if piece.rank in [Rank.LION, Rank.TIGER]:
      if not (is_one_step or self._is_river_jump(from_pos, to_pos, board)):
        return False, "Lion/Tiger must move one step or jump across the river."
    else:
      if not is_one_step:
        return False, "This animal can only move one step."

    # 4. Terrain restrictions
    if not self._can_enter_cell(piece, dest_terrain, dest_owner):
      return False, f"{piece.name} cannot enter {dest_terrain}."

    # 5. Capturing rules
    if target_piece:
      if target_piece.owner == piece.owner:
        return False, "Cannot capture your own piece."

      can_capture, reason = self._can_capture(piece, target_piece, dest_terrain)
      if not can_capture:
        return False, reason
      return True, target_piece  # valid capture

    # 6. Valid empty move
    return True, None


  #Can enter conditions
  def _can_enter_cell(self, piece, terrain, cell_owner):
    """Check whether the piece can legally enter a terrain type."""
    if terrain == "river":
       # Only Rat can enter river
      return piece.rank == Rank.RAT 
    elif terrain == "den":
      # Cannot enter own den
      return cell_owner != piece.owner
    return True  # land or trap are always allowed

  def _can_capture(self, attacker, defender, dest_terrain):
    """Check Jungle Chess capturing rules."""

    # 1. If defender is in own trap, attacker can always capture it
    if dest_terrain == "trap" and defender.owner != attacker.owner:
      return True, None

    # 2. Elephant cannot capture Rat
    if attacker.rank == Rank.ELEPHANT and defender.rank == Rank.RAT:
      return False, "Elephant cannot capture Rat."

    # 3. Rat can capture Elephant (special exception)
    if attacker.rank == Rank.RAT and defender.rank == Rank.ELEPHANT:
      return True, None

    # 4. If attacker is Rat and it's in river, cannot capture piece on land
    if attacker.rank == Rank.RAT and attacker.position:
      attacker_cell = attacker.position
      
      _, current_cell = defender.owner.game.board.grid[attacker_cell.row][attacker_cell.col]
      terrain, _ = current_cell if current_cell else ("land", None)
      
      if terrain == "river" and dest_terrain != "river":
        return False, "Rat cannot capture from river to land."
      if terrain != "river" and dest_terrain == "river":
        return False, "Rat cannot capture from land to river."

    # 5.  piece can capture if rank >= defender.rank
    if attacker.rank >= defender.rank:
      return True, None

    return False, "Cannot capture higher-ranked piece."


#Lion?Tiger Jump Rules
def _is_river_jump(self, from_pos, to_pos, board):
  """-The lion and tiger pieces may jump over a river by moving horizontally or vertically. 
  -They move from a square on one edge of the river to the next non-water square on the other side. 
  -Such a move is not allowed if there is a rat (whether friendly or enemy) on any of the intervening water squares. 
  -The lion and tiger are allowed to capture enemy pieces by such jumping moves"""
  fr, fc = from_pos.row, from_pos.col
  tr, tc = to_pos.row, to_pos.col

  # Must move in a straight line 
  if fr != tr and fc != tc:
    return False

  # Move = Direction
  row_step = 0 if fr == tr else (1 if tr > fr else -1)
  col_step = 0 if fc == tc else (1 if tc > fc else -1)

  # Move one cell at a time until reaching destination
  r, c = fr + row_step, fc + col_step

  while (r != tr or c != tc) and (0 <= r < board.rows and 0 <= c < board.cols):
    piece_in_path, cell = board.grid[r][c]
    terrain, _ = cell if cell else ("land", None)

    # Jump path must only be through river cells
    if terrain != "river":
      return False

    # Rat blocks the jump
    if piece_in_path and piece_in_path.rank == Rank.RAT:
      return False

    r += row_step
    c += col_step

  return True


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


class SaveGame:
    @staticmethod
    def save_game(game, filename: str = "game.jungle"):
        
        try:
            with open(filename, 'wb') as file:
                pickle.dump(game, file)
            print(f"Game successfully saved to '{filename}'")
        except Exception as e:
            print(f"Error saving game: {e}")

    @staticmethod
    def load_game(filename: str = "game.jungle"):
        
        try:
            with open(filename, 'rb') as file:
                game = pickle.load(file)
            print(f"Game successfully loaded from '{filename}'")
            return game
        except Exception as e:
            print(f" Error loading game: {e}")
            return None

