from model.piece import Piece

# Helper for the Controller to translate 'a1' -> (7, 0)
def parse_location(move_str):
    column_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    col = column_map[move_str[0].lower()]
    row = 8 - int(move_str[1])
    return (row, col)

class Board:
    def __init__(self):
        # Create an 8x8 grid filled with None (Empty Squares)
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self._setup_pieces()

    def _setup_pieces(self):
        """Places all 32 pieces in their starting positions."""
        # Setup Pawns
        for i in range(8):
            self.board[1][i] = Piece('black', 'Pawn', (1, i))
            self.board[6][i] = Piece('white', 'Pawn', (6, i))

        # Setup Rooks, Knights, Bishops
        piece_order = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook']
        for i, name in enumerate(piece_order):
            self.board[0][i] = Piece('black', name, (0, i))
            self.board[7][i] = Piece('white', name, (7, i))

    def move_piece(self, start_pos, end_pos):
        """
        The 'Update' command. This is 'God Mode'—it just moves 
        whatever is there without checking rules.
        """
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        piece = self.board[start_row][start_col]
        
        if piece:
            # Update the 2D Array (The Grid)
            self.board[end_row][end_col] = piece
            self.board[start_row][start_col] = None
            
            # Update the Object's internal state
            piece.position = (end_row, end_col)
            piece.has_moved = True
            return True
            
        return False