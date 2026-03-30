from model.board import Board, parse_location
from ui.terminal import print_board
from logic.validator import is_move_legal, causes_self_check

class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = 'white'
        self.is_running = True

    def play(self):
        while self.is_running:
            # 1. RENDER PHASE
            print_board(self.board)
            print(f"--- {self.current_turn.upper()}'S TURN ---")

            # 2. INPUT PHASE
            move_input = input("Enter move (e.g., 'e2 e4') or 'quit': ").strip().lower()

            if move_input == 'quit':
                self.is_running = False
                continue

            try:
                # Parse coordinates
                start_str, end_str = move_input.split()
                start_pos = parse_location(start_str)
                end_pos = parse_location(end_str)

                # 3. DATA RETRIEVAL
                piece = self.board.board[start_pos[0]][start_pos[1]]

                # 4. VALIDATION GATEWAY
                if piece is None:
                    print("!!! No piece at starting square !!!")
                    continue
                
                if piece.color != self.current_turn:
                    print(f"!!! It's {self.current_turn}'s turn !!!")
                    continue

                # Rule Check
                if not is_move_legal(self.board, piece, start_pos, end_pos):
                    print(f"!!! Illegal {piece.name} Move !!!")
                    continue

                # Safety Check (Simulation)
                if causes_self_check(self.board, piece, start_pos, end_pos):
                    print("!!! Illegal: You cannot leave your King in Check! !!!")
                    continue

                # 5. COMMIT PHASE
                success = self.board.move_piece(start_pos, end_pos)

                if success:
                    piece.has_moved = True # Update piece history
                    # Toggle Turn
                    self.current_turn = 'black' if self.current_turn == 'white' else 'white'

            except (ValueError, IndexError, KeyError):
                print("!!! Invalid Input format. Please use 'e2 e4' !!!")