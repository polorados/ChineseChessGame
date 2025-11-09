from model.board import Board
from model.player import Player
from model.piece import Piece, Position
from model.game_rules import GameRules
from view.userinterface import UserInterface
from model.save_game import SaveGame
from typing import Tuple
from model.rank import Rank


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
        self.board = None
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
                    cell = ("trap",owner)
                elif chr == 'd':
                    owner = self.players[0] if i < 3 else self.players[1]
                    cell = ("den",owner)
                elif chr == '~':
                    cell = ("river",None)
                ret.append((i,j,cell))
        return ret
    
    def initial_board_setup(self):
        pieces = self.initialize_piece()
        cells = self.initialize_cell()
        self.board = Board(pieces, cells)

    def move_piece(self, from_pos, to_pos):
        mover = self.board.piece_at(from_pos)
        if mover is None:
            return False, "No piece at source."
        if mover.owner is not self.players[self.whose_turn]: #check whether mover's turn
            return False, "Not your turn."
        
        # if is_valid == true: result = captured_piece, else result = msg
        is_valid, result = self.rules.validate_move(mover, from_pos, to_pos, self.board) #no valid move
        if not is_valid:
            return False,result
        
        undo_object = {
            "piece": mover,
            "from_pos": from_pos,
            "to_pos": to_pos,
            "captured": result,
            "prev_turn": self.whose_turn
        }
        self.move_stack.append(undo_object) #record move for undo

        # remove dead piece from board
        # result = captured_piece
        if result is not None:
            result.is_alive = False
            self.board.remove_piece_at(to_pos)
            result.owner.remove_piece(result)

        self.board.move_piece(mover, to_pos)
        self.record_move(mover, from_pos, to_pos, result)
        self.switch_turn()
        return True,"ok"

    #보류
    def record_move(self,piece_id,from_pos,to_pos, captured_piece):
        self.move_history.append((piece_id,from_pos,to_pos,captured_piece))

    def undo_move(self): 
        #undo move from top of the stack

        if not self.move_stack:
            return False, "You just started the game."
        
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

        return True,"ok"

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

            
