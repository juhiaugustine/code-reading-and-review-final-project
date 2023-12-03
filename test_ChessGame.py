import unittest
from ChessGame import ChessGame

class TestChessGame(unittest.TestCase):
    def setUp(self):
        self.chess_game = ChessGame()

    def test_initial_values(self):
        self.assertEqual(self.chess_game.width, 512)
        self.assertEqual(self.chess_game.height, 512)
        self.assertEqual(self.chess_game.dimensions, 8)
        self.assertEqual(self.chess_game.sq_size, 64)
        self.assertEqual(self.chess_game.max_fps, 15)
        self.assertEqual(len(self.chess_game.images), 0)
        self.assertEqual(len(self.chess_game.colors), 2)

    def test_load_images(self):
        self.chess_game.load_images()
        self.assertTrue(len(self.chess_game.images) > 0)
        self.assertEqual(len(self.chess_game.images), 12)

if __name__ == "__main__":
    unittest.main()