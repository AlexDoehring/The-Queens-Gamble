# Move class
# This class represents a move in the game of chess
# It contains the initial and final squares of the move.
# It also provides methods to compare moves for equality.
# The Move class is used to track the movement of pieces on the chessboard.
# It is initialized with the initial and final squares of the move.

class Move:

    def __init__(self, initial, final):
        # initial and final are squares
        self.initial = initial
        self.final = final

    def __str__(self):
        s = ''
        s += f'({self.initial.col}, {self.initial.row})'
        s += f' -> ({self.final.col}, {self.final.row})'
        return s

    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final