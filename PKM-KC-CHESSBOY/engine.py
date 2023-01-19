import chess as ch
import chess.svg
import random as rd
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1100, 1100)

        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(10, 10, 1080, 1080)

        self.chessboard = chess.Board()

        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)


class Engine:
    def __init__(self, board, maxDepth, color):
        self.board = board
        self.maxDepth = maxDepth
        self.color = color

    def getBestMove(self):
        return self.engine(None, 1)

    def evalFunct(self):
        compt = 0
        #Sums up the material values
        for i in range(64):
            compt+=self.squareResPoints(ch.SQUARES[i])
        compt += self.mateOpportunity() + self.openning() + 0.001*rd.random()
        return compt

    def openning(self):
        if(self.board.fullmove_number < 10):
            if(self.board.turn == self.color):
                return 1/30 * self.board.legal_moves.count()
            else:
                return -1/30 * self.board.legal_moves.count()
        else:
            return 0

    def mateOpportunity(self):
        # checkmate
        if(self.board.legal_moves.count() == 0):
            # engine checkmated
            if(self.board.turn == self.color):
                return -999
            # human checkmated
            else:
                return 999
        else:
            return 0
    
    # get square as input and return corresponding han's berliner's system value of it's resident
    def squareResPoints(self, square):
        pieceValue = 0
        if(self.board.piece_type_at(square) == ch.PAWN):
            pieceValue = 1
        elif(self.board.piece_type_at(square) == ch.ROOK):
            pieceValue = 5.1
        elif(self.board.piece_type_at(square) == ch.BISHOP):
            pieceValue = 3.33
        elif(self.board.piece_type_at(square) == ch.KNIGHT):
            pieceValue = 3.2
        elif(self.board.piece_type_at(square) == ch.QUEEN):
            pieceValue = 8.8
        
        if(self.board.color_at(square) != self.color):
            return -pieceValue
        else:
            return pieceValue

    def engine(self, candidate, depth):
        if(depth == self.maxDepth or self.board.legal_moves.count()==0):
            return self.evalFunct()
        
        else:
            # get legal moves
            moveList = list(self.board.legal_moves)

            # init newCandidate
            newCandidate = None

            if(depth % 2 != 0):
                newCandidate = float("-inf")
            else:
                newCandidate = float("inf")

            for i in moveList:
                # play the move i
                self.board.push(i)

                # get value of move i
                value = self.engine(newCandidate, depth+1)

                # basic minmax alg
                # maximizing(engine turn)
                if(value > newCandidate and depth % 2 != 0):
                    newCandidate = value
                    if(depth == 1):
                        move = i
                
                # minimizing(human turn)
                elif(value < newCandidate and depth % 2 == 0):
                    newCandidate = value

                # alpha beta pruning
                # if prev move was made by engine

                if(candidate != None and value < candidate and depth % 2 == 0):
                    self.board.pop()
                    break

                # if prev move was by human
                elif(candidate != None and value > candidate and depth % 2 != 0):
                    self.board.pop()
                    break
                # undo last move
                self.board.pop()

        if(depth > 1):
            # return node in tree
            return newCandidate
        else:
            return move