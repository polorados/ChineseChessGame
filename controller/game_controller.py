from model.piece import Position

class GameController:

    def __init__(self,game,ui):
        self.game = game
        self.ui = ui
        self.is_running = True
        
        self.handlers = {
            "move": self.cmd_move,
            "undo": self.cmd_undo,
            "status": self.cmd_status,
            "board": self.cmd_board,
            #"history": self.cmd_history,
            "save": self.cmd_save,
            "load": self.cmd_load,
            "resign": self.cmd_resign,
            "help": self.cmd_help,
            "quit": self.cmd_quit,
            "exit": self.cmd_quit
        }

    def run(self):
        while self.is_running:
            self.ui.display_move_prompt(self.current_whose_turn_w_or_b())
            inp = self.ui.get_user_input()
            if not inp:
                continue
            cmd, args = self.parse_tokens(inp)
            self.handle(cmd,args)

    def handle(self, cmd, args):
        handler = self.handlers.get(cmd)
        if handler is None:
            self.ui.display_error("Unknown command. Type 'help' to see available commands.")
        try:
            handler(args)
        except Exception as e:
            self.ui.display_error(str(e))
    
    def parse_tokens(self, inp):
        #args can be empty or list
        parts = inp.strip().split()
        if not parts:
            return "",[]
        return parts[0], parts[1:]
    
    def current_whose_turn_w_or_b(self):
        if self.game.whose_turn == 0:
            return 'w'
        else:
            return 'b'
        
    #### cmd handler #####
    def cmd_help(self, args):
        self.ui.display_help()
    
    def cmd_move(self, args):
        """
        move src dest
        ex) move A3 A4
        """
        if len(args) != 2:
            self.ui.display_error("Right Format: move <src> <dest> (move A3 A4)")
            return
        
        arg1 = args[0]
        arg2 = args[1]
        src = self.parse_pos(arg1)
        dst = self.parse_pos(arg2)

        ok,msg = self.game.move_piece(src, dst)
        if not ok:
            self.ui.display_error(msg)
            return
        
        piece = self.game.board.piece_at(dst)
        self.ui.display_valid_move(src,dst,piece.name)

        is_over, winner_index = self.game.check_victory(piece,dst)
        if is_over:
            winner = self.players[winner_index]
            self.ui.display_game_result(winner.name)
            self.is_running = False

    def cmd_undo(self, args):
        """
        undo
        """
        ok,msg = self.game.undo_move()
        if not ok:
            self.ui.display_error(msg)

    def cmd_status(self, args):
        self.ui.display_game_status(self.game)
    
    def cmd_board(self, args):
        grid = self.game.board.grid
        if grid is None:
            self.ui.display_error("Board does not exist")
            return
        self.ui.display_board(grid)

    def cmd_resign(self, args):
        current_turn = self.game.whose_turn
        winner_index = 1-current_turn
        winner = self.game.players[winner_index]

        self.ui.display_game_result(winner.name)
    
    def cmd_save(self, args):
        path = args[0] if args else "default_save.json"
        ok, msg = self.game.save_game(path)
        if ok:
            self.ui.display_save_success(path)
        else:
            self.ui.display_error(msg)
    def cmd_load(self, args):
        path = args[0] if args else "default_save.json"
        ok, msg = self.game.load_game(path)
        if ok:
            self.ui.display_load_success(path)
        else:
            self.ui.display_error(msg)

    def cmd_quit(self, args):
        if self.ui.display_quit_confirmation():
            self.is_running = False
    def parse_pos(self, s):
        """
        s=A3 -> A=col, 3=row
        return Position
        """
        s = s.strip().lower()

        if len(s) < 2:
            return None
        
        row = s[1:]
        col = s[0]
        if col < 'a' or col > 'g':
            return None
        
        row = int(row)
        if not (1 <= row <= 9):
            return None
        col = ord(col) - ord('a')
        row = 9 - row
        return Position(row,col)