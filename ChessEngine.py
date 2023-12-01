import numpy as np

class GameState:
        """
        Constructor for GameState class. This comprises of the different moves of different 
        pieces and also the board is initiazed to the initial state while having the white
        side to move first.
        
        Attributes:
        - board: A 2D numpy array representing the chess board.
        - moveFunctions: A dictionary mapping piece types to their corresponding move functions.
        - whiteToMove: A boolean indicating whether it is currently white's turn to move.
        - moveLog: A list of moves made in the game.
        - whiteKingLocation: A tuple representing the location of the white king on the board.
        - blackKingLocation: A tuple representing the location of the black king on the board.
        - checkMate: A boolean indicating whether the game is in a checkmate state.
        - staleMate: A boolean indicating whether the game is in a stalemate state.
        """


        def __init__(self):
                """
                Initializes a new instance of the GameState class.
                """
                self.board = np.array([
                        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["--", "--", "--", "--", "--", "--", "--", "--"],
                        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
                ])

                self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                                                          'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
                self.whiteToMove = True
                self.moveLog = []
                self.whiteKingLocation = (7, 4)
                self.blackKingLocation = (0, 4)
                self.checkMate = False
                self.staleMate = False

        def makeMove(self, move):
                """
                Moves a piece from the start position to the end position on the chess board.

                Args:
                - move: A Move object representing the move to be made.
                """
                self.board[move.startRow][move.startCol] = "--"
                self.board[move.endRow][move.endCol] = move.pieceMoved
                self.moveLog.append(move)
                self.whiteToMove = not self.whiteToMove
                if move.pieceMoved == "wK":
                        self.whiteKingLocation = (move.endRow, move.endCol)
                elif move.pieceMoved == "bK":
                        self.blackKingLocation = (move.endRow, move.endCol)

                if move.isPawnPromotion:
                        self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"

        def undoMove(self):
                """
                Undoes the last move made in the game.
                """
                if len(self.moveLog) != 0:
                        move = self.moveLog.pop()
                        self.board[move.startRow][move.startCol] = move.pieceMoved
                        self.board[move.endRow][move.endCol] = move.pieceCaptured
                        self.whiteToMove = not self.whiteToMove
                        if move.pieceMoved == "wK":
                                self.whiteKingLocation = (move.startRow, move.startCol)
                        if move.pieceMoved == "bK":
                                self.blackKingLocation = (move.startRow, move.startCol)

        def getValidMoves(self):
                """
                Gets all valid moves for the current player and checks if the game is in a checkmate or stalemate state.

                Returns:
                - A list of Move objects representing the valid moves.
                """
                moves = self.getAllPossibleMoves()
                for i in range(len(moves)-1, -1, -1):
                        self.makeMove(moves[i])
                        self.whiteToMove = not self.whiteToMove
                        if self.inCheck():
                                moves.remove(moves[i])
                        self.whiteToMove = not self.whiteToMove
                        self.undoMove()
                if len(moves) == 0:
                        if self.inCheck():
                                self.checkMate = True
                        else:
                                self.staleMate = True
                else:
                        self.checkMate = False
                        self.staleMate = False

                return moves

        def inCheck(self):
                """
                Checks if the current player is in check.

                Returns:
                - A boolean indicating whether the current player is in check.
                """
                if self.whiteToMove:
                        return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
                else:
                        return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

        def squareUnderAttack(self, r, c):
                """
                Checks if a square on the chess board is under attack by the opponent.

                Args:
                - r: An integer representing the row of the square.
                - c: An integer representing the column of the square.

                Returns:
                - A boolean indicating whether the square is under attack.
                """
                self.whiteToMove = not self.whiteToMove
                oppMoves = self.getAllPossibleMoves()
                self.whiteToMove = not self.whiteToMove
                return any(np.all([move.endRow == r, move.endCol == c]) for move in oppMoves)

        def getAllPossibleMoves(self):
                """
                Gets all possible moves for the current player.

                Returns:
                - A list of Move objects representing all possible moves.
                """
                moves = []
                for r in range(len(self.board)):
                        for c in range(len(self.board[r])):
                                turn = self.board[r][c][0]  # b or w based on turn
                                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                                        piece = self.board[r][c][1]
                                        self.moveFunctions[piece](r, c, moves)
                return moves

        def getPawnMoves(self, r, c, moves):
                """
                Gets all possible moves for a pawn.

                Args:
                - r: An integer representing the row of the pawn.
                - c: An integer representing the column of the pawn.
                - moves: A list to store the possible moves.
                """
                if self.whiteToMove:
                        if self.board[r-1][c] == "--":
                                moves.append(Move((r, c), (r-1, c), self.board))
                                if r == 6 and self.board[r-2][c] == "--":
                                        moves.append(Move((r, c), (r-2, c), self.board))
                        if c-1 >= 0:
                                if self.board[r-1][c-1][0] == 'b':
                                        moves.append(Move((r, c), (r-1, c-1), self.board))
                        if c+1 <= 7:
                                if self.board[r-1][c+1][0] == 'b':
                                        moves.append(Move((r, c), (r-1, c+1), self.board))

                else:
                        if self.board[r+1][c] == "--":
                                moves.append(Move((r, c), (r+1, c), self.board))
                                if r == 1 and self.board[r+2][c] == "--":
                                        moves.append(Move((r, c), (r+2, c), self.board))
                        if c-1 >= 0:
                                if self.board[r+1][c-1][0] == 'w':
                                        moves.append(Move((r, c), (r+1, c-1), self.board))
                        if c+1 <= 7:
                                if self.board[r+1][c+1][0] == 'w':
                                        moves.append(Move((r, c), (r+1, c+1), self.board))

        def getRookMoves(self, r, c, moves):
                """
                Gets all possible moves for a rook.

                Args:
                - r: An integer representing the row of the rook.
                - c: An integer representing the column of the rook.
                - moves: A list to store the possible moves.
                """
                directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
                enemyColor = "b" if self.whiteToMove else "w"
                for d in directions:
                        for i in range(1, 8):
                                endRow = r + d[0] * i
                                endCol = c + d[1] * i
                                if 0 <= endRow < 8 and 0 <= endCol < 8:
                                        endPiece = self.board[endRow][endCol]
                                        if endPiece == "--":
                                                moves.append(Move((r, c), (endRow, endCol), self.board))
                                        elif endPiece[0] == enemyColor:
                                                moves.append(Move((r, c), (endRow, endCol), self.board))
                                                break
                                        else:
                                                break
                                else:
                                        break

        def getKnightMoves(self, r, c, moves):
                """
                Gets all possible moves for a knight.

                Args:
                - r: An integer representing the row of the knight.
                - c: An integer representing the column of the knight.
                - moves: A list to store the possible moves.
                """
                knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
                allyColor = "w" if self.whiteToMove else "b"
                for m in knightMoves:
                        endRow = r + m[0]
                        endCol = c + m[1]
                        if 0 <= endRow < 8 and 0 <= endCol < 8:
                                endPiece = self.board[endRow][endCol]
                                if endPiece[0] != allyColor:
                                        moves.append(Move((r, c), (endRow, endCol), self.board))

        def getBishopMoves(self, r, c, moves):
                """
                Gets all possible moves for a bishop.

                Args:
                - r: An integer representing the row of the bishop.
                - c: An integer representing the column of the bishop.
                - moves: A list to store the possible moves.
                """
                directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
                enemyColor = "b" if self.whiteToMove else "w"
                for d in directions:
                        for i in range(1, 8):
                                endRow = r + d[0] * i
                                endCol = c + d[1] * i
                                if 0 <= endRow < 8 and 0 <= endCol < 8:
                                        endPiece = self.board[endRow][endCol]
                                        if endPiece == "--":
                                                moves.append(Move((r, c), (endRow, endCol), self.board))
                                        elif endPiece[0] == enemyColor:
                                                moves.append(Move((r, c), (endRow, endCol), self.board))
                                                break
                                        else:
                                                break
                                else:
                                        break

        def getQueenMoves(self, r, c, moves):
                """
                Gets all possible moves for a queen.

                Args:
                - r: An integer representing the row of the queen.
                - c: An integer representing the column of the queen.
                - moves: A list to store the possible moves.
                """
                self.getRookMoves(r, c, moves)
                self.getBishopMoves(r, c, moves)

        def getKingMoves(self, r, c, moves):
                """
                Gets all possible moves for a king.

                Args:
                - r: An integer representing the row of the king.
                - c: An integer representing the column of the king.
                - moves: A list to store the possible moves.
                """
                kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
                allyColor = "w" if self.whiteToMove else "b"
                for i in range(8):
                        endRow = r + kingMoves[i][0]
                        endCol = c + kingMoves[i][1]
                        if 0 <= endRow < 8 and 0 <= endCol < 8:
                                endPiece = self.board[endRow][endCol]
                                if endPiece[0] != allyColor:
                                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        if 0 <= endRow < 8 and 0 <= endCol < 8:
                                endPiece = self.board[endRow][endCol]
                                if endPiece[0] != allyColor:
                                        moves.append(Move((r,c), (endRow, endCol), self.board))
class Move():

        ranksToRow = {"1": 7, "2": 6, "3": 5, "4": 4,
                      "5": 3, "6": 2, "7": 1, "8": 0}
        rowsToRanks = {v: k for k, v in ranksToRow.items()}
        filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                      "e": 4, "f": 5, "g": 6, "h": 7}
        colsToFiles = {v: k for k, v in filesToCols.items()}

        def __init__(self, startSq, endSq, board):
                self.startRow, self.startCol = startSq
                self.endRow, self.endCol = endSq
                self.pieceMoved = board[self.startRow][self.startCol]
                self.pieceCaptured = board[self.endRow][self.endCol]
                self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)
                self.moveID = (self.startRow, self.startCol, self.endRow, self.endCol)

        def __eq__(self, other):
                if isinstance(other, Move):
                        return self.moveID  == other.moveID
                return False


        def getChessNotation(self):
                return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

        def getRankFile(self, r, c):
                return  self.colsToFiles[c] + self.rowsToRanks[r]
