def is_pawn_move_legal(board, piece, start, end):
    start_row, start_col = start
    end_row, end_col = end
    
    # Determine direction based on color
    direction = -1 if piece.color == 'white' else 1
    
    # Calculate the 'delta' (the change in coordinates)
    row_diff = end_row - start_row
    col_diff = abs(end_col - start_col)

    # --- 1. Forward Moves ---
    if col_diff == 0:
        # Check if the destination square is empty
        if board.board[end_row][end_col] is not None:
            return False
            
        # Standard 1-step move
        if row_diff == direction:
            return True
            
        # Initial 2-step move
        if not piece.has_moved: # We'll need to add this attribute to Piece
            if row_diff == 2 * direction:
                # Ensure the middle square is also empty
                mid_row = start_row + direction
                if board.board[mid_row][start_col] is None:
                    return True
                    
    # --- 2. Diagonal Captures ---
    elif col_diff == 1 and row_diff == direction:
        target = board.board[end_row][end_col]
        # Must be an enemy piece there
        if target is not None and target.color != piece.color:
            return True

    return False

def is_knight_move_legal(board, piece, start, end):
    start_row, start_col = start
    end_row, end_col = end
    
    # Get the absolute difference in coordinates
    row_diff = abs(end_row - start_row)
    col_diff = abs(end_col - start_col)
    
    # 1. The L-Shape Check
    is_l_shape = (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
    
    if is_l_shape:
        # 2. The "Friendly Fire" Check
        target = board.board[end_row][end_col]
        
        # It's legal if the square is empty, OR if the piece there is an enemy
        if target is None or target.color != piece.color:
            return True
            
    return False

def is_path_clear(board, start, end):
    start_row, start_col = start
    end_row, end_col = end
    
    # Calculate the direction of travel (-1, 0, or 1)
    def get_step(s, e):
        if s == e: return 0
        return 1 if e > s else -1

    row_step = get_step(start_row, end_row)
    col_step = get_step(start_col, end_col)
    
    # Start one step away from the beginning
    current_row = start_row + row_step
    current_col = start_col + col_step
    
    # Walk until we reach the destination square
    while (current_row, current_col) != (end_row, end_col):
        if board.board[current_row][current_col] is not None:
            return False # Path is blocked!
        current_row += row_step
        current_col += col_step
        
    return True

def is_sliding_move_legal(board, piece, start, end):
    start_row, start_col = start
    end_row, end_col = end
    
    row_diff = abs(end_row - start_row)
    col_diff = abs(end_col - start_col)
    
    # Define valid directions
    is_straight = (start_row == end_row or start_col == end_col)
    is_diagonal = (row_diff == col_diff)
    
    # Check if the piece type matches the move type
    if piece.name == 'Rook' and not is_straight: return False
    if piece.name == 'Bishop' and not is_diagonal: return False
    if piece.name == 'Queen' and not (is_straight or is_diagonal): return False
    
    # 1. Is the path clear?
    if not is_path_clear(board, start, end):
        return False
        
    # 2. Is the destination valid? (Empty or Enemy)
    target = board.board[end_row][end_col]
    if target is not None and target.color == piece.color:
        return False
        
    return True

def is_king_move_legal(board, piece, start, end):
    start_row, start_col = start
    end_row, end_col = end
    
    # Calculate the distance moved
    row_diff = abs(end_row - start_row)
    col_diff = abs(end_col - start_col)
    
    # Rule 1: King can only move 1 square in any direction
    if row_diff <= 1 and col_diff <= 1:
        target = board.board[end_row][end_col]
        
        # Rule 2: Cannot land on a square occupied by a friendly piece
        if target is None or target.color != piece.color:
            return True
            
    return False

def is_move_legal(board, piece, start, end):
    """The central hub for all move validation."""
    if piece.name == 'Pawn':
        return is_pawn_move_legal(board, piece, start, end)
    elif piece.name == 'Knight':
        return is_knight_move_legal(board, piece, start, end)
    elif piece.name in ['Rook', 'Bishop', 'Queen']:
        return is_sliding_move_legal(board, piece, start, end)
    elif piece.name == 'King':
        return is_king_move_legal(board, piece, start, end)
    return False

def is_square_under_attack(board, target_pos, attacker_color):
    """
    Scans the board to see if any piece of attacker_color 
    can legally move to target_pos.
    """
    for r in range(8):
        for c in range(8):
            piece = board.board[r][c]
            if piece and piece.color == attacker_color:
                # Reuse our existing 'is_move_legal' function!
                if is_move_legal(board, piece, (r, c), target_pos):
                    return True
    return False

def causes_self_check(board, piece, start, end):
    # 1. Save the original state
    original_target = board.board[end[0]][end[1]]
    
    # 2. Simulate the move
    board.board[end[0]][end[1]] = piece
    board.board[start[0]][start[1]] = None
    
    # 3. Find the King
    king_pos = None
    for r in range(8):
        for c in range(8):
            p = board.board[r][c]
            if p and p.name == 'King' and p.color == piece.color:
                king_pos = (r, c)
                break
    
    # 4. Check if King is now under attack
    enemy_color = 'black' if piece.color == 'white' else 'white'
    in_check = is_square_under_attack(board, king_pos, enemy_color)
    
    # 5. Undo the simulation (Very important!)
    board.board[start[0]][start[1]] = piece
    board.board[end[0]][end[1]] = original_target
    
    return in_check

def is_in_check(board, color):
    """Checks if the King of the given color is currently under attack."""
    # Find the King's current position
    king_pos = None
    for r in range(8):
        for c in range(8):
            p = board.board[r][c]
            if p and p.name == 'King' and p.color == color:
                king_pos = (r, c)
                break
    
    if not king_pos:
        return False # Should never happen in a real game!

    enemy_color = 'black' if color == 'white' else 'white'
    return is_square_under_attack(board, king_pos, enemy_color)

def is_checkmate(board, color):
    """Determines if the player of the given color has been checkmated."""
    # 1. If not in check, it's either mid-game or a stalemate (not mate)
    if not is_in_check(board, color):
        return False

    # 2. Iterate through every square on the board
    for r in range(8):
        for c in range(8):
            piece = board.board[r][c]
            
            # 3. If it's the current player's piece, try every possible move
            if piece and piece.color == color:
                for dr in range(8):
                    for dc in range(8):
                        start = (r, c)
                        end = (dr, dc)
                        
                        # 4. If a legal move exists that clears the check, it's NOT mate
                        if is_move_legal(board, piece, start, end):
                            if not causes_self_check(board, piece, start, end):
                                return False # We found a literal 'saving grace'
                                
    return True # No legal moves found; King is trapped.