import random

class ChessAI:
    def __init__(self, board):
        self.board = board

    def get_random_move(self):
        squares = self.board.squares
        black_pieces = []

        # Collect all black pieces and their positions
        for row in range(len(squares)):
            for col in range(len(squares[row])):
                square = squares[row][col]
                if square.has_piece() and square.piece.color == 'black':
                    black_pieces.append((square.piece, row, col))

        random.shuffle(black_pieces)

        for piece, row, col in black_pieces:
            self.board.calc_moves(piece, row, col)
            legal_moves = piece.moves
            if legal_moves:
                return piece, random.choice(legal_moves)

        return None, None
