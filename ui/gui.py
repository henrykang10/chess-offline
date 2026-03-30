import pygame
import sys
from logic.validator import is_move_legal, causes_self_check, is_checkmate

# Configuration Constants
WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 8
# Soft Wood/Green palette for a professional look
COLORS = [(235, 235, 208), (119, 149, 86)] 
HIGHLIGHT_COLOR = (186, 202, 68, 100) # Semi-transparent yellow

class ChessGUI:
    def __init__(self, game):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Systems Engineer Chess")
        self.game = game
        self.images = {}
        self.selected_sq = None # Stores (row, col) of the first click
        self.load_images()

    def load_images(self):
        """Pre-loads PNG assets into memory for high performance."""
        pieces = ['Pawn', 'Rook', 'Knight', 'Bishop', 'Queen', 'King']
        for color in ['white', 'black']:
            for p in pieces:
                filename = f"{color}_{p}.png"
                # Load from your /assets folder
                img = pygame.image.load(f"assets/{filename}")
                # Scale to fit the 75x75 pixel squares
                self.images[f"{color}_{p}"] = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))

    def draw_board(self):
        """Renders the 8x8 grid and highlights the selection."""
        for r in range(8):
            for c in range(8):
                # 1. Draw the Square
                color = COLORS[(r + c) % 2]
                pygame.draw.rect(self.screen, color, (c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
                # 2. Draw Highlight if this square is selected
                if self.selected_sq == (r, c):
                    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                    s.set_alpha(150) # Transparency
                    s.fill((255, 255, 0)) # Solid Yellow
                    self.screen.blit(s, (c*SQUARE_SIZE, r*SQUARE_SIZE))

                # 3. Draw the Piece Image
                piece = self.game.board.board[r][c]
                if piece:
                    img_key = f"{piece.color}_{piece.name}"
                    self.screen.blit(self.images[img_key], (c*SQUARE_SIZE, r*SQUARE_SIZE))

    def handle_click(self, row, col):
        """The core event logic connecting UI to Engine."""
        # Case A: Selecting a piece for the first time
        if self.selected_sq is None:
            piece = self.game.board.board[row][col]
            # Only select if it's a piece and it's that player's turn
            if piece and piece.color == self.game.current_turn:
                self.selected_sq = (row, col)
        
        # Case B: Already have a piece, now choosing a destination
        else:
            start = self.selected_sq
            end = (row, col)
            piece = self.game.board.board[start[0]][start[1]]

            # Run the Validator Logic
            if is_move_legal(self.game.board, piece, start, end):
                if not causes_self_check(self.game.board, piece, start, end):
                    # Commit the move to the Model
                    self.game.board.move_piece(start, end)
                    piece.has_moved = True
                    # Toggle Turn in the Controller
                    self.game.current_turn = 'black' if self.game.current_turn == 'white' else 'white'
            
            # Reset selection regardless of whether move was legal
            self.selected_sq = None

    def draw_game_over(self, winner):
        """Renders a semi-transparent overlay and a 'Wins' message."""
        # 1. Create a dark overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150) # Transparency (0-255)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # 2. Configure Font
        font = pygame.font.SysFont('Arial', 64, bold=True)
        text = font.render(f"CHECKMATE: {winner.upper()} WINS!", True, (255, 255, 255))
        
        # 3. Center the text
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        
        # 4. Add 'Press R to Restart' subtext
        small_font = pygame.font.SysFont('Arial', 32)
        sub_text = small_font.render("Press 'R' to Play Again", True, (200, 200, 200))
        sub_rect = sub_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        self.screen.blit(sub_text, sub_rect)

    def run(self):
        """The main loop, updated to check for game-ending states."""
        clock = pygame.time.Clock()
        game_over = False
        winner = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Only handle clicks if the game is still active
                if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    col = mouse_x // SQUARE_SIZE
                    row = mouse_y // SQUARE_SIZE
                    self.handle_click(row, col)
                    
                    # AFTER the move, check if the other player is now mated
                    if is_checkmate(self.game.board, self.game.current_turn):
                        game_over = True
                        winner = "Black" if self.game.current_turn == "white" else "White"

                # Handle Restart
                if game_over and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # You'd need a reset method in your Game class to restart
                        print("Restarting...") 

            self.draw_board()
            
            if game_over:
                self.draw_game_over(winner)

            pygame.display.flip()
            clock.tick(60)