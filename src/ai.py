import random
from piece import Piece
import copy 

# ChessAI class
# This class implements a simple chess AI using the Minimax algorithm.
# It evaluates the game state and selects the best move for the AI player.

class ChessAI:
    def __init__(self, board, depth = 1):
        self.depth = depth
        self.board = board
        #self.game = game
        #self.piece = Piece()

    # Evaluate the board state and assign a score based on the pieces' values.
    def evaluate(self, board, maximizing_color):
        score = 0
        for row in board.squares:
            for square in row:
                if square.has_piece():
                    piece = square.piece
                    value = piece.value

                    # add a bonus for controling the center of the board
                    if (2 <= square.row <=5) and (2 <= square.col <=5):
                        value += 0.15

                        
                    if piece.color == maximizing_color:
                        score += value
                    else:
                        score -= value
        return score

    # Minimax algorithm implementation
    # This function recursively explores the game tree to find the best move.
    # It alternates between maximizing and minimizing the score based on the current player.
    def minimax(self, board, depth, maximizing):
        if depth == 0:
            return self.evaluate(board, 'black'), None
    
        best_move = None
        if maximizing:
            max_eval = float('-inf')
            legal_moves = board.get_all_legal_moves('black' if maximizing else 'white')
            for piece, move in legal_moves:
                if board.valid_move(piece, move):
                    new_state = board.simulate_move(piece,move)
                    eval, _ = self.minimax(new_state, depth - 1, not maximizing)
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (piece, move)
            return max_eval, best_move
        else:
            min_eval = float('inf')
            legal_moves = board.get_all_legal_moves('black' if maximizing else 'white')
            for piece, move in legal_moves:
                if board.valid_move(piece, move):
                    new_state = board.simulate_move(piece,move)
                    eval, _ = self.minimax(new_state, depth - 1, not maximizing)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (piece, move)
            return min_eval, best_move


    # Get the best move for the AI player based on the current game state.
    def get_move(self, state):
        """Returns the best move from the current game state."""
        _, move = self.minimax(state, self.depth, maximizing = True)
        return move    
    

    
    """
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
    """
