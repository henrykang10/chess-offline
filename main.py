from controller.game import Game
from ui.gui import ChessGUI

def main():
    # 1. Initialize the Engine (Model & Controller)
    chess_game = Game()
    
    # 2. Initialize the Graphical Interface (View)
    # We pass the 'chess_game' object so the UI can "read" the board
    gui = ChessGUI(chess_game)
    
    # 3. Launch the Window
    print("Launching Graphical Interface...")
    gui.run()

if __name__ == "__main__":
    main()