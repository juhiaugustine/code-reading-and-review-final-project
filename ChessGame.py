import pygame as p
import ChessEngine


class ChessGame:
    def __init__(self):
        """
        Initializes the ChessGame object.

        Attributes:
        - width: The width of the chessboard window.
        - height: The height of the chessboard window.
        - dimensions: The number of squares in each row and column of the chessboard.
        - sq_size: The size of each square on the chessboard.
        - max_fps: The maximum frames per second for the chessboard window.
        - images: A dictionary containing chess piece images.
        - colors: A list of colors used for the chessboard.

        Returns:
        None
        """
        self.width = self.height = 512
        self.dimensions = 8
        self.sq_size = self.height // self.dimensions
        self.max_fps = 15
        self.images = {}
        self.colors = [p.Color("white"), p.Color("grey")]

    def load_images(self):
        """
        Loads the chess piece images into the images dictionary.

        Returns:
        None
        """
        pieces = [
            "wp",
            "wR",
            "wN",
            "wB",
            "wQ",
            "wK",
            "bp",
            "bR",
            "bN",
            "bB",
            "bQ",
            "bK",
        ]
        for piece in pieces:
            self.images[piece] = p.transform.scale(
                p.image.load("images/" + piece +
                             ".png"), (self.sq_size, self.sq_size)
            )

    def draw_chessboard(self, screen):
        """
        Draws the chessboard on the screen.

        Parameters:
        - screen: The Pygame screen object.

        Returns:
        None
        """
        for row in range(self.dimensions):
            for column in range(self.dimensions):
                color = self.colors[(row + column) % 2]
                p.draw.rect(
                    screen,
                    color,
                    p.Rect(
                        column * self.sq_size,
                        row * self.sq_size,
                        self.sq_size,
                        self.sq_size,
                    ),
                )

    def draw_chess_pieces(self, screen, board):
        """
        Draws the chess pieces on the screen.

        Parameters:
        - screen: The Pygame screen object.
        - board: The current state of the chessboard.

        Returns:
        None
        """
        for row in range(self.dimensions):
            for column in range(self.dimensions):
                piece = board[row][column]
                if piece != "--":
                    screen.blit(
                        self.images[piece],
                        p.Rect(
                            column * self.sq_size,
                            row * self.sq_size,
                            self.sq_size,
                            self.sq_size,
                        ),
                    )

    def highlight_squares(self, screen, gs, valid_moves, selected_square):
        """
        Highlights the selected square and valid move squares on the screen.

        Parameters:
        - screen: The Pygame screen object.
        - gs: The current game state.
        - valid_moves: A list of valid moves.
        - selected_square: The selected square.

        Returns:
        None
        """
        if selected_square != ():
            row, column = selected_square
            if gs.board[row][column][0] == ("w" if gs.white_to_move else "b"):
                s = p.Surface((self.sq_size, self.sq_size))
                s.set_alpha(100)
                s.fill(p.Color("blue"))
                screen.blit(s, (column * self.sq_size, row * self.sq_size))
                s.fill(p.Color("yellow"))
                for moves in valid_moves:
                    if moves.start_row == row and moves.start_col == column:
                        screen.blit(
                            s,
                            (self.sq_size * moves.end_col,
                             self.sq_size * moves.end_row),
                        )

    def draw_game_state(self, screen, gs, valid_moves, selected_square):
        """
        Draws the current game state on the screen.

        Parameters:
        - screen: The Pygame screen object.
        - gs: The current game state.
        - valid_moves: A list of valid moves.
        - selected_square: The selected square.

        Returns:
        None
        """
        self.draw_chessboard(screen)
        self.highlight_squares(screen, gs, valid_moves, selected_square)
        self.draw_chess_pieces(screen, gs.board)

    def animate_moves(self, move, screen, board, clock):
        """
        Animates the chess piece moves on the screen.

        Parameters:
        - move: The move to be animated.
        - screen: The Pygame screen object.
        - board: The current state of the chessboard.
        - clock: The Pygame clock object.

        Returns:
        None
        """
        destination_row = move.end_row - move.start_row
        destination_col = move.end_col - move.start_col
        frames_per_square = 5
        frame_count = (abs(destination_row) +
                       abs(destination_col)) * frames_per_square
        for frame in range(frame_count + 1):
            row, column = (
                move.start_row + destination_row * frame / frame_count,
                move.start_col + destination_col * frame / frame_count,
            )
            self.draw_chessboard(screen)
            self.draw_chess_pieces(screen, board)
            color = self.colors[(move.end_row + move.end_col) % 2]
            end_square = p.Rect(
                move.end_col * self.sq_size,
                move.end_row * self.sq_size,
                self.sq_size,
                self.sq_size,
            )
            p.draw.rect(screen, color, end_square)
            if move.piece_captured != "--":
                screen.blit(self.images[move.piece_captured], end_square)
            screen.blit(
                self.images[move.piece_moved],
                p.Rect(
                    column * self.sq_size,
                    row * self.sq_size,
                    self.sq_size,
                    self.sq_size,
                ),
            )
            p.display.flip()
            clock.tick(60)

    def draw_text(self, screen, text):
        """
        Draws the text on the screen.

        Parameters:
        - screen: The Pygame screen object.
        - text: The text to be displayed.

        Returns:
        None
        """
        font = p.font.SysFont("Helvetica", 32, True, False)
        text_object = font.render(text, True, p.Color("Gray"))
        text_location = p.Rect(0, 0, self.width, self.height).move(
            self.width / 2 - text_object.get_width() / 2,
            self.height / 2 - text_object.get_height() / 2,
        )
        screen.blit(text_object, text_location)
        text_object = font.render(text, True, p.Color("Black"))
        screen.blit(text_object, text_location.move(2, 2))

    def main(self):
        """
        The main function that runs the chess game.

        Returns:
        None
        """
        p.init()
        screen = p.display.set_mode((self.width, self.height))
        clock = p.time.Clock()
        screen.fill(p.Color("white"))
        gs = ChessEngine.GameState()
        valid_moves = gs.get_valid_moves()
        is_move_made = False
        should_animate = False
        self.load_images()
        running = True
        selected_square = ()
        clicked_positions = []
        game_over = False
        while running:
            for event in p.event.get():
                if event.type == p.QUIT:
                    running = False
                elif event.type == p.MOUSEBUTTONDOWN:
                    if not game_over:
                        location = p.mouse.get_pos()
                        col = location[0] // self.sq_size
                        row = location[1] // self.sq_size
                        if selected_square == (row, col):
                            selected_square = ()
                            clicked_positions = []
                        else:
                            selected_square = (row, col)
                            clicked_positions.append(selected_square)
                        if len(clicked_positions) == 1 and (gs.board[row][col] == "--"):
                            selected_square = ()
                            clicked_positions = []
                        if len(clicked_positions) == 2:
                            move = ChessEngine.Move(
                                clicked_positions[0], clicked_positions[1], gs.board
                            )
                            for i in range(len(valid_moves)):
                                if move == valid_moves[i]:
                                    gs.make_move(move)
                                    is_move_made = True
                                    should_animate = True
                                    selected_square = ()
                                    clicked_positions = []
                            if not is_move_made:
                                clicked_positions = [selected_square]
                elif event.type == p.KEYDOWN:
                    if event.key == p.K_z:
                        gs.undo_move()
                        is_move_made = True
                        should_animate = False
                    if event.key == p.K_r:
                        gs = ChessEngine.GameState()
                        valid_moves = gs.get_valid_moves()
                        selected_square = ()
                        clicked_positions = []
                        is_move_made = False
                        should_animate = False
            if is_move_made:
                if should_animate:
                    self.animate_moves(
                        gs.move_log[-1], screen, gs.board, clock)
                valid_moves = gs.get_valid_moves()
                is_move_made = False
                should_animate = False
            self.draw_game_state(screen, gs, valid_moves, selected_square)
            if gs.check_mate:
                game_over = True
                if gs.white_to_move:
                    self.draw_text(screen, "Black wins by checkmate")
                else:
                    self.draw_text(screen, "White wins by checkmate")
            elif gs.stale_mate:
                game_over = True
                self.draw_text(screen, "Stalemate")
            clock.tick(self.max_fps)
            p.display.flip()


if __name__ == "__main__":
    chess_game = ChessGame()
    chess_game.main()
