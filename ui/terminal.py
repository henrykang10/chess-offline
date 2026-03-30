def print_board(board_obj):
    """
    Translates the 2D array into a human-readable chess board.
    """
    # The Unicode dictionary mapping pieces to symbols
    symbols = {
        'white': {'Pawn': '♙', 'Rook': '♖', 'Knight': '♘', 'Bishop': '♗', 'Queen': '♕', 'King': '♔'},
        'black': {'Pawn': '♟', 'Rook': '♜', 'Knight': '♞', 'Bishop': '♝', 'Queen': '♛', 'King': '♚'}
    }

    print("\n    a b c d e f g h")
    print("  -------------------")

    for r in range(8):
        # Start each row with its rank number (8 down to 1)
        row_display = f"{8 - r} | "
        
        for c in range(8):
            piece = board_obj.board[r][c]
            
            if piece is None:
                # The dot and space we discussed for empty squares
                row_display += "· "
            else:
                # Look up the symbol based on color and name
                symbol = symbols[piece.color][piece.name]
                row_display += f"{symbol} "
        
        # End the row with the rank number again for symmetry
        print(f"{row_display}| {8 - r}")

    print("  -------------------")
    print("    a b c d e f g h\n")