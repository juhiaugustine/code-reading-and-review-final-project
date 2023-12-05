import numpy as np


class GameState:
    """
    Constructor for GameState class. This comprises of the different moves of different
    pieces and also the board is initialized to the initial state while having the white
    side to move first.

    Attributes:
    - board: A 2D numpy array representing the chess board.
    - move_functions: A dictionary mapping piece types to their corresponding move functions.
    - white_to_move: A boolean indicating whether it is currently white's turn to move.
    - move_log: A list of moves made in the game.
    - white_king_location: A tuple representing the location of the white king on the board.
    - black_king_location: A tuple representing the location of the black king on the board.
    - check_mate: A boolean indicating whether the game is in a checkmate state.
    - stale_mate: A boolean indicating whether the game is in a stalemate state.
    """

    def __init__(self):
        """
        Initializes a new instance of the GameState class.
        """
        self.board = np.array(
            [
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ]
        )

        self.move_functions = {
            "p": self.get_pawn_moves,
            "R": self.get_rook_moves,
            "N": self.get_knight_moves,
            "B": self.get_bishop_moves,
            "Q": self.get_queen_moves,
            "K": self.get_king_moves,
        }
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.check_mate = False
        self.stale_mate = False

    def make_move(self, move):
        """
        Moves a piece from the start position to the end position on the chess board.

        Args:
        - move: A Move object representing the move to be made.
        """
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)

        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"

    def undo_move(self):
        """
        Undoes the last move made in the game.
        """
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)
            if move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)

    def get_valid_moves(self):
        """
        Gets all valid moves for the current player and checks
        if the game is in a checkmate or stalemate state.

        Returns:
        - A list of Move objects representing the valid moves.
        """
        moves = self.get_all_possible_moves()
        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move
            self.undo_move()
        if len(moves) == 0:
            if self.in_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = False
            self.stale_mate = False

        return moves

    def in_check(self):
        """
        Checks if the current player is in check.

        Returns:
        - A boolean indicating whether the current player is in check.
        """
        if self.white_to_move:
            return self.square_under_attack(
                self.white_king_location[0], self.white_king_location[1]
            )
        return self.square_under_attack(
            self.black_king_location[0], self.black_king_location[1]
        )

    def square_under_attack(self, row, col):
        """
        Checks if a square on the chess board is under attack by the opponent.

        Args:
        - row: An integer representing the row of the square.
        - col: An integer representing the column of the square.

        Returns:
        - A boolean indicating whether the square is under attack.
        """
        self.white_to_move = not self.white_to_move
        opp_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        return any(np.all([move.end_row == row, move.end_col == col]) for move in opp_moves)

    def get_all_possible_moves(self):
        """
        Gets all possible moves for the current player.

        Returns:
        - A list of Move objects representing all possible moves.
        """
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]  # b or w based on turn
                if (turn == "w" and self.white_to_move) or (
                    turn == "b" and not self.white_to_move
                ):
                    piece = self.board[row][col][1]
                    self.move_functions[piece](row, col, moves)
        return moves

    def get_pawn_moves(self, row, col, moves):
        """
        Gets all possible moves for a pawn.

        Args:
        - row: An integer representing the row of the pawn.
        - col: An integer representing the column of the pawn.
        - moves: A list to store the possible moves.
        """
        if self.white_to_move:
            if self.board[row - 1][col] == "--":
                moves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == "--":
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if col - 1 >= 0:
                if self.board[row - 1][col - 1][0] == "b":
                    moves.append(
                        Move((row, col), (row - 1, col - 1), self.board))
            if col + 1 <= 7:
                if self.board[row - 1][col + 1][0] == "b":
                    moves.append(
                        Move((row, col), (row - 1, col + 1), self.board))

        else:
            if self.board[row + 1][col] == "--":
                moves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == "--":
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == "w":
                    moves.append(
                        Move((row, col), (row + 1, col - 1), self.board))
            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == "w":
                    moves.append(
                        Move((row, col), (row + 1, col + 1), self.board))

    def get_rook_moves(self, row, col, moves):
        """
        Gets all possible moves for a rook.

        Args:
        - row: An integer representing the row of the rook.
        - col: An integer representing the column of the rook.
        - moves: A list to store the possible moves.
        """
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(
                            Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(
                            Move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_knight_moves(self, row, col, moves):
        """
        Gets all possible moves for a knight.

        Args:
        - row: An integer representing the row of the knight.
        - col: An integer representing the column of the knight.
        - moves: A list to store the possible moves.
        """
        knight_moves = (
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        )
        ally_color = "w" if self.white_to_move else "b"
        for m in knight_moves:
            end_row = row + m[0]
            end_col = col + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(
                        Move((row, col), (end_row, end_col), self.board))

    def get_bishop_moves(self, row, col, moves):
        """
        Gets all possible moves for a bishop.

        Args:
        - row: An integer representing the row of the bishop.
        - col: An integer representing the column of the bishop.
        - moves: A list to store the possible moves.
        """
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = "b" if self.white_to_move else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(
                            Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(
                            Move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_queen_moves(self, row, col, moves):
        """
        Gets all possible moves for a queen.

        Args:
        - row: An integer representing the row of the queen.
        - col: An integer representing the column of the queen.
        - moves: A list to store the possible moves.
        """
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)

    def get_king_moves(self, row, col, moves):
        """
        Gets all possible moves for a king.

        Args:
        - row: An integer representing the row of the king.
        - col: An integer representing the column of the king.
        - moves: A list to store the possible moves.
        """
        king_moves = (
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        )
        ally_color = "w" if self.white_to_move else "b"
        for i in range(8):
            end_row = row + king_moves[i][0]
            end_col = col + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(
                        Move((row, col), (end_row, end_col), self.board))
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(
                        Move((row, col), (end_row, end_col), self.board))


class Move:
    """
    Represents a move in a chess game.

    Attributes:
            start_row (int): The starting row of the move.
            start_col (int): The starting column of the move.
            end_row (int): The ending row of the move.
            end_col (int): The ending column of the move.
            piece_moved (str): The piece that is being moved.
            piece_captured (str): The piece that is being captured.
            is_pawn_promotion (bool): Indicates if the move is a pawn promotion.
            move_id (tuple): The unique identifier of the move.
    """
    ranks_to_row = {"1": 7, "2": 6, "3": 5,
                    "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_row.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2,
                     "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board):
        """
        Initializes a Move object.

        Args:
                start_sq (tuple): The starting square of the move.
                end_sq (tuple): The ending square of the move.
                board (list): The chess board.

        Returns:
                None
        """
        self.start_row, self.start_col = start_sq
        self.end_row, self.end_col = end_sq
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.is_pawn_promotion = (self.piece_moved == "wp" and self.end_row == 0) or (
            self.piece_moved == "bp" and self.end_row == 7
        )
        self.move_id = (self.start_row, self.start_col,
                        self.end_row, self.end_col)

    def __eq__(self, other):
        """
        Checks if two Move objects are equal.

        Args:
                other (Move): The other Move object to compare.

        Returns:
                bool: True if the moves are equal, False otherwise.
        """
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        """
        Returns the chess notation of the move.

        Returns:
                str: The chess notation of the move.
        """
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(
            self.end_row, self.end_col
        )

    def get_rank_file(self, row, col):
        """
        Returns the rank and file notation of a given position.

        Args:
                row (int): The row of the position.
                col (int): The column of the position.

        Returns:
                str: The rank and file notation of the position.
        """
        return self.cols_to_files[col] + self.rows_to_ranks[row]
