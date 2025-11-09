import unittest
from model.game_rules import GameRules
from model.piece import Piece, Position, Rank
from model.player import Player
from model.game import Game

class TestGameRules(unittest.TestCase):
    def setUp(self):
        # Create two players and a new game instance
        self.player1 = Player("P1")
        self.player2 = Player("P2")
        self.game = Game(self.player1, self.player2)
        
        # Clear the board to land cells only for controlled testing
        for row in range(self.game.board.rows):
            for col in range(self.game.board.cols):
                self.game.board.grid[row][col] = (None, ("land", None))

    def test_rat_can_capture_elephant(self):
        rat = Piece('R', Rank.RAT, self.player1, Position(4, 3))
        elephant = Piece('E', Rank.ELEPHANT, self.player2, Position(4, 4))
        
        self.game.board.place(rat, rat.position)
        self.game.board.place(elephant, elephant.position)
        
        valid, result = self.game.rules.validate_move(rat, rat.position, elephant.position, self.game.board)
        
        self.assertTrue(valid, "Rat should be able to capture Elephant")
        self.assertIsInstance(result, Piece, "Result should be the captured piece")

    def test_elephant_cannot_capture_rat(self):
        elephant = Piece('E', Rank.ELEPHANT, self.player1, Position(2, 2))
        rat = Piece('R', Rank.RAT, self.player2, Position(2, 3))
        
        self.game.board.place(elephant, elephant.position)
        self.game.board.place(rat, rat.position)
        
        valid, result = self.game.rules.validate_move(elephant, elephant.position, rat.position, self.game.board)
        
        self.assertFalse(valid, "Elephant cannot capture Rat")
        self.assertIn("Elephant cannot capture Rat", result)

    def test_lion_tiger_jump_blocked_by_rat(self):
        """Lion/Tiger jump over river is blocked if any Rat is on intervening water squares."""
        
        # Set the river cells in the middle column (col=3)
        for r in range(self.game.board.rows):
            for c in range(self.game.board.cols):
                self.game.board.grid[r][c] = (None, ("land", None))
        for r in range(1, 8):
            self.game.board.grid[r][3] = (None, ("river", None))
        
        lion = Piece('L', Rank.LION, self.player1, Position(0, 3))
        target = Piece('D', Rank.DOG, self.player2, Position(8, 3))
        blocking_rat = Piece('R', Rank.RAT, self.player2, Position(3, 3))
        
        self.game.board.place(lion, lion.position)
        self.game.board.place(target, target.position)
        self.game.board.place(blocking_rat, blocking_rat.position)
        
        valid, _ = self.game.rules.validate_move(lion, lion.position, target.position, self.game.board)
        
        self.assertFalse(valid, "Lion jump should be blocked by rat in river")

    def test_trap_allows_capture(self):
        """Piece in opponent's trap can be captured by weaker pieces."""
        
        # Set a trap cell owned by player2 at (4,4)
        for r in range(self.game.board.rows):
            for c in range(self.game.board.cols):
                self.game.board.grid[r][c] = (None, ("land", None))
        self.game.board.grid[4][4] = (None, ("trap", self.player2))
        
        weak_rat = Piece('R', Rank.RAT, self.player1, Position(4, 3))
        strong_elephant = Piece('E', Rank.ELEPHANT, self.player2, Position(4, 4))
        
        self.game.board.place(weak_rat, weak_rat.position)
        self.game.board.place(strong_elephant, strong_elephant.position)
        
        valid, _ = self.game.rules.validate_move(weak_rat, weak_rat.position, strong_elephant.position, self.game.board)
        
        self.assertTrue(valid, "Trap allows weaker piece to capture stronger piece")

    def test_den_capture_results_in_victory(self):
        """Capturing opponent's den results in victory."""
        
        # Set a den cell owned by player2 at (2, 2)
        for r in range(self.game.board.rows):
            for c in range(self.game.board.cols):
                self.game.board.grid[r][c] = (None, ("land", None))
        self.game.board.grid[2][2] = (None, ("den", self.player2))
        
        mover = Piece('R', Rank.RAT, self.player1, Position(2, 1))
        self.game.board.place(mover, mover.position)
        
        # Validate move into den
        valid, _ = self.game.rules.validate_move(mover, mover.position, Position(2, 2), self.game.board)
        self.assertTrue(valid, "Move into opponent's den should be valid")
        
        # Make the move
        success = self.game.move_piece(mover.position, Position(2, 2))
        self.assertTrue(success, "Move into den should succeed")
        
        # Check victory condition
        finished, winner = self.game.check_victory(mover, Position(2, 2))
        self.assertTrue(finished, "Game should be finished when den is captured")
        self.assertEqual(winner, 0, "Player 1 should be the winner")
