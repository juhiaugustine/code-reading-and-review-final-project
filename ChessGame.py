import pygame as p
import ChessEngine

class ChessGame:
    def __init__(self):
        """
        Initializes the ChessGame object.

        Attributes:
        - WIDTH: The width of the chessboard window.
        - HEIGHT: The height of the chessboard window.
        - DIMENSIONS: The number of squares in each row and column of the chessboard.
        - SQ_SIZE: The size of each square on the chessboard.
        - MAX_FPS: The maximum frames per second for the chessboard window.
        - IMAGES: A dictionary containing chess piece images.
        - colors: A list of colors used for the chessboard.

        Returns:
        None
        """
        self.WIDTH = self.HEIGHT = 512
        self.DIMENSIONS = 8
        self.SQ_SIZE = self.HEIGHT // self.DIMENSIONS
        self.MAX_FPS = 15
        self.IMAGES = {}
        self.colors = [p.Color("white"), p.Color("grey")]
    
    def loadImages(self):
        """
        Loads the chess piece images into the IMAGES dictionary.

        Returns:
        None
        """
        pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
        for piece in pieces:
            self.IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (self.SQ_SIZE, self.SQ_SIZE))

    def drawChessboard(self, screen):
        """
        Draws the chessboard on the screen.

        Parameters:
        - screen: The Pygame screen object.

        Returns:
        None
        """
        for r in range(self.DIMENSIONS):
            for c in range(self.DIMENSIONS):
                color = self.colors[(r + c) % 2]
                p.draw.rect(screen, color, p.Rect(c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def drawChessPieces(self, screen, board):
        """
        Draws the chess pieces on the screen.

        Parameters:
        - screen: The Pygame screen object.
        - board: The current state of the chessboard.

        Returns:
        None
        """
        for r in range(self.DIMENSIONS):
            for c in range(self.DIMENSIONS):
                piece = board[r][c]
                if piece != "--":
                    screen.blit(self.IMAGES[piece], p.Rect(c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def highlightSquares(self, screen, gs, validMoves, selectedSquare):
        """
        Highlights the selected square and valid move squares on the screen.

        Parameters:
        - screen: The Pygame screen object.
        - gs: The current game state.
        - validMoves: A list of valid moves.
        - selectedSquare: The selected square.

        Returns:
        None
        """
        if selectedSquare != ():
            r, c = selectedSquare
            if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
                s = p.Surface((self.SQ_SIZE, self.SQ_SIZE))
                s.set_alpha(100)
                s.fill(p.Color('blue'))
                screen.blit(s, (c * self.SQ_SIZE, r * self.SQ_SIZE))
                s.fill(p.Color("yellow"))
                for moves in validMoves:
                    if moves.startRow == r and moves.startCol == c:
                        screen.blit(s, (self.SQ_SIZE * moves.endCol, self.SQ_SIZE * moves.endRow))

    def drawGameState(self, screen, gs, validMoves, selectedSquare):
        """
        Draws the current game state on the screen.

        Parameters:
        - screen: The Pygame screen object.
        - gs: The current game state.
        - validMoves: A list of valid moves.
        - selectedSquare: The selected square.

        Returns:
        None
        """
        self.drawChessboard(screen)
        self.highlightSquares(screen, gs, validMoves, selectedSquare)
        self.drawChessPieces(screen, gs.board)

    def animateMoves(self, move, screen, board, clock):
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
        dR = move.endRow - move.startRow
        dC = move.endCol - move.startCol
        framesPerSquare = 5
        frameCount = (abs(dR) + abs(dC)) * framesPerSquare
        for frame in range(frameCount + 1):
            r, c = ((move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount))
            self.drawChessboard(screen)
            self.drawChessPieces(screen, board)
            color = self.colors[(move.endRow + move.endCol) % 2]
            endSquare = p.Rect(move.endCol * self.SQ_SIZE, move.endRow * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE)
            p.draw.rect(screen, color, endSquare)
            if move.pieceCaptured != "--":
                screen.blit(self.IMAGES[move.pieceCaptured], endSquare)

            screen.blit(self.IMAGES[move.pieceMoved], p.Rect(c * self.SQ_SIZE, r * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))
            p.display.flip()
            clock.tick(60)

    def drawText(self, screen, text):
        """
        Draws the text on the screen.

        Parameters:
        - screen: The Pygame screen object.
        - text: The text to be displayed.

        Returns:
        None
        """
        font = p.font.SysFont("Helvitca", 32, True, False)
        textObject = font.render(text, True, p.Color('Gray'))
        textLocation = p.Rect(0, 0, self.WIDTH, self.HEIGHT).move(self.WIDTH / 2 - textObject.get_width() / 2,
                                                                     self.HEIGHT / 2 - textObject.get_height() / 2)
        screen.blit(textObject, textLocation)
        textObject = font.render(text, True, p.Color("Black"))
        screen.blit(textObject, textLocation.move(2, 2))

    def main(self):
        """
        The main function that runs the chess game.

        Returns:
        None
        """
        p.init()
        screen = p.display.set_mode((self.WIDTH, self.HEIGHT))
        clock = p.time.Clock()
        screen.fill(p.Color("white"))
        gs = ChessEngine.GameState()
        validMoves = gs.getValidMoves()
        isMoveMade = False
        shouldAnimate = False
        self.loadImages()
        running = True
        selectedSquare = ()
        clickedPositions = []
        gameOver = False
        while running:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    if not gameOver:
                        location = p.mouse.get_pos()
                        col = location[0] // self.SQ_SIZE
                        row = location[1] // self.SQ_SIZE
                        if selectedSquare == (row, col):
                            selectedSquare = ()
                            clickedPositions = []
                        else:
                            selectedSquare = (row, col)
                            clickedPositions.append(selectedSquare)
                        if len(clickedPositions) == 1 and (gs.board[row][col] == "--"):
                            selectedSquare = ()
                            clickedPositions = []
                        if len(clickedPositions) == 2:
                            move = ChessEngine.Move(clickedPositions[0], clickedPositions[1], gs.board)
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(move)
                                    isMoveMade = True
                                    shouldAnimate = True
                                    selectedSquare = ()
                                    clickedPositions = []
                            if not isMoveMade:
                                clickedPositions = [selectedSquare]
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_z:
                        gs.undoMove()
                        isMoveMade = True
                        shouldAnimate = False
                    if e.key == p.K_r:
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        selectedSquare = ()
                        clickedPositions = []
                        isMoveMade = False
                        shouldAnimate = False
            if isMoveMade:
                if shouldAnimate:
                    self.animateMoves(gs.moveLog[-1], screen, gs.board, clock)
                validMoves = gs.getValidMoves()
                isMoveMade = False
                shouldAnimate = False
            self.drawGameState(screen, gs, validMoves, selectedSquare)
            if gs.checkMate:
                gameOver = True
                if gs.whiteToMove:
                    self.drawText(screen, 'Black wins by checkmate')
                else:
                    self.drawText(screen, 'White wins by checkmate')
            elif gs.staleMate:
                gameOver = True
                self.drawText(screen, 'Stalemate')
            clock.tick(self.MAX_FPS)
            p.display.flip()


if __name__ == "__main__":
    chess_game = ChessGame()
    chess_game.main()
