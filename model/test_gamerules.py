import unittest
from gamerules import GameRules
from piece import Piece, Position, Rank
from player import Player
from game import Game

class TestGameRules(unittest.TestCase):
    def setUp(self):
        self.p1 = Player("P1")
        self.p2 = Player("P2")
        self.game = Game(self.p1, self.p2)
        for r in range(self.game.board.rows):
            for c in range(self.game.board.cols):
                self.game.board.grid[r][c] = (None, ("land", None))

    def test_rat_can_capture_elephant(self):
        rat = Piece('R', Rank.RAT, self.p1, Position(4,3))
        elephant = Piece('E', Rank.ELEPHANT, self.p2, Position(4,4))
        self.game.board.place(rat, rat.position)
        self.game.board.place(elephant, elephant.position)
        valid, result = self.game.rules.validate_move(rat, rat.position, elephant.position, self.game.board)
        self.assertTrue(valid)
        self.assertIsInstance(result, Piece)

    def test_elephant_cannot_capture_rat(self):
        elephant = Piece('E', Rank.ELEPHANT, self.p1, Position(2,2))
        rat = Piece('R', Rank.RAT, self.p2, Position(2,3))
        self.game.board.place(elephant, elephant.position)
        self.game.board.place(rat, rat.position)
        valid, result = self.game.rules.validate_move(elephant, elephant.position, rat.position, self.game.board)
        self.assertFalse(valid)
        self.assertIn("Elephant cannot capture Rat", result)

    def test_lion_tiger_jump_blocked_by_rat(self):
        for r in range(self.game.board.rows):
            for c in range(self.game.board.cols):
                self.game.board.grid[r][c] = (None, ("land", None))
        for r in range(1, 8):
            self.game.board.grid[r][3] = (None, ("river", None))
        lion = Piece('L', Rank.LION, self.p1, Position(0,3))
        target_piece = Piece('D', Rank.DOG, self.p2, Position(8,3))
        self.game.board.place(lion, lion.position)
        self.game.board.place(target_piece, target_piece.position)
        rat_block = Piece('R', Rank.RAT, self.p2, Position(3,3))
        self.game.board.place(rat_block, rat_block.position)
        valid, result = self.game.rules.validate_move(lion, lion.position, target_piece.position, self.game.board)
        self.assertFalse(valid)

    def test_trap_allows_capture(self):
        for r in range(self.game.board.rows):
            for c in range(self.game.board.cols):
                self.game.board.grid[r][c] = (None, ("land", None))
        self.game.board.grid[4][4] = (None, ("trap", self.p2))
        weak = Piece('R', Rank.RAT, self.p1, Position(4,3))
        strong = Piece('E', Rank.ELEPHANT, self.p2, Position(4,4))
        self.game.board.place(weak, weak.position)
        self.game.board.place(strong, strong.position)
        valid, result = self.game.rules.validate_move(weak, weak.position, strong.position, self.game.board)
        self.assertTrue(valid)

    def test_den_victory(self):
        for r in range(self.game.board.rows):
            for c in range(self.game.board.cols):
                self.game.board.grid[r][c] = (None, ("land", None))
        self.game.board.grid[2][2] = (None, ("den", self.p2))
        mover = Piece('R', Rank.RAT, self.p1, Position(2,1))
        self.game.board.place(mover, mover.position)
        valid, result = self.game.rules.validate_move(mover, mover.position, Position(2,2), self.game.board)
        self.assertTrue(valid)
        ok, msg = self.game.move_piece(mover.position, Position(2,2))
        self.assertTrue(ok)
        finished, winner = self.game.check_victory(mover, Position(2,2))
        self.assertTrue(finished)
        self.assertEqual(winner, 0)
