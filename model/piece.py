class Piece:
    def __init__(self, color, name, position):
        # 'white' or 'black'
        self.color = color
        
        # 'Pawn', 'Rook', 'Knight', 'Bishop', 'Queen', or 'King'
        self.name = name
        
        # Tuple of (row, col), e.g., (7, 4)
        self.position = position
        
        # Boolean flags to track state changes
        self.is_captured = False
        self.has_moved = False 

    def __repr__(self):
        """
        This helps with debugging. If you ever print a piece object directly,
        it will show 'white Pawn' instead of <Piece object at 0x123...>.
        """
        return f"{self.color} {self.name}"