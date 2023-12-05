import unittest
from ChessEngine import *


class TestGameState(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case by initializing the game state.
        """
        self.game_state = GameState()

    def test_initial_values(self):
        """
        Test case to check the initial values of the game state.

        This test case checks the following:
        - The board has a size of 8x8.
        - The game state starts with white to move.
        - The move log is empty.
        - The initial locations of the white and black kings.
        - The check mate and stale mate flags are set to False.
        """
        self.assertEqual(len(self.game_state.board), 8)
        self.assertEqual(len(self.game_state.board[0]), 8)
        self.assertEqual(self.game_state.white_to_move, True)
        self.assertEqual(len(self.game_state.move_log), 0)
        self.assertEqual(self.game_state.white_king_location, (7, 4))
        self.assertEqual(self.game_state.black_king_location, (0, 4))
        self.assertEqual(self.game_state.check_mate, False)
        self.assertEqual(self.game_state.stale_mate, False)

    def test_make_move(self):
        """
        Test the make_move method of the GameState class.

        This test verifies that the make_move method correctly updates the game state after a move is made.
        It checks if the piece at the source position is empty ('--'), the piece at the destination position is 'wp',
        the move log has been updated, and the turn has switched to the opponent's turn.
        """
        move = Move((6, 4), (4, 4), self.game_state.board)
        self.game_state.make_move(move)
        self.assertEqual(self.game_state.board[6][4], "--")
        self.assertEqual(self.game_state.board[4][4], "wp")
        self.assertEqual(len(self.game_state.move_log), 1)
        self.assertEqual(self.game_state.white_to_move, False)

    def test_undo_move(self):
        """
        Test the undo_move method of the GameState class.

        This test case verifies that the undo_move method correctly reverts the changes made by the make_move method.
        It checks if the board state is restored to its previous state, the move log is empty, and the turn is reverted to the previous player.
        """
        move = Move((6, 4), (4, 4), self.game_state.board)
        self.game_state.make_move(move)
        self.game_state.undo_move()
        self.assertEqual(self.game_state.board[6][4], "wp")
        self.assertEqual(self.game_state.board[4][4], "--")
        self.assertEqual(len(self.game_state.move_log), 0)
        self.assertEqual(self.game_state.white_to_move, True)

    def test_get_valid_moves(self):
        """
        Test case to verify the correctness of the get_valid_moves method.
        It checks if the number of valid moves returned by the method is equal to 20.
        """
        moves = self.game_state.get_valid_moves()
        self.assertEqual(len(moves), 20)

    def test_in_check(self):
        self.assertEqual(self.game_state.in_check(), False)

    def test_square_under_attack(self):
        """
        Test case to verify the behavior of the square_under_attack method.

        This method checks if the square at the given coordinates is under attack in the current game state.
        """
        self.assertEqual(self.game_state.square_under_attack(7, 4), False)

    def test_get_all_possible_moves(self):
        """
        Test case to verify the functionality of the get_all_possible_moves method.

        It checks if the number of moves returned by the method is equal to 20.
        """
        moves = self.game_state.get_all_possible_moves()
        self.assertEqual(len(moves), 20)

    def test_get_pawn_moves(self):
        """
        Test case for the get_pawn_moves method.

        This test verifies that the get_pawn_moves method returns the correct number of moves for a pawn at a given position.
        """
        moves = []
        self.game_state.get_pawn_moves(6, 4, moves)
        self.assertEqual(len(moves), 2)

    def test_get_rook_moves(self):
        """
        Test case for the get_rook_moves method.

        This test case verifies that the get_rook_moves method returns the correct moves for a rook piece
        on the chessboard.
        """
        moves = []
        self.game_state.get_rook_moves(7, 0, moves)
        self.assertEqual(len(moves), 0)

    def test_get_knight_moves(self):
        """
        Test case for the get_knight_moves method.

        This test verifies that the get_knight_moves method returns the correct number of moves for a knight piece
        at a specific position on the chessboard.
        """
        moves = []
        self.game_state.get_knight_moves(7, 1, moves)
        self.assertEqual(len(moves), 2)

    def test_get_bishop_moves(self):
        """
        Test case for the get_bishop_moves method.

        This test verifies that the get_bishop_moves method returns the correct moves for a bishop piece
        on the chessboard.

        It checks if the number of moves returned is 0 when the bishop is placed at position (7, 2).
        """
        moves = []
        self.game_state.get_bishop_moves(7, 2, moves)
        self.assertEqual(len(moves), 0)


if __name__ == "__main__":
    unittest.main()
