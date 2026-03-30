# Chess-Offline: Modular Python Engine

A high-fidelity chess engine built in **Python 3.12**, focusing on the **Model-View-Controller (MVC)** architectural pattern. This version is designed for local execution, providing a robust logic layer that serves as the "brain" for the extended web-based application.

# System Architecture

The project is strictly modularized to ensure high maintainability and clear separation of concerns:

* `logic/` (The Controller): Contains the `Validator` gateway. It acts as the "referee," ensuring all moves follow official FIDE rules.
* `model/` (The Data Layer): Defines the `Board` and `Piece` objects. It manages the internal state and handles FEN (Forsyth-Edwards Notation) parsing.
* `ui/` (The View): Manages the terminal-based rendering, providing a clean CLI (Command Line Interface) for player interaction.



# Key Technical Features

* OOP Design: Extensive use of Classes and Inheritance to represent chess pieces and board states.
* Extensible Validator: Built with a "plug-and-play" logic gateway, allowing for easy addition of complex rules like En Passant or Castling.
* Dependency-Light: Optimized for performance with minimal external dependencies, ensuring a fast and portable execution environment.

# How to Run

1.  Clone the Repo:
    ```zsh
    git clone [https://github.com/henrykang10/chess-offline.git](https://github.com/henrykang10/chess-offline.git)
    cd chess-offline
    ```
2.  Install Requirements:
    ```zsh
    pip install -r requirements.txt
    ```
3.  Start Game:
    ```zsh
    python main.py
    ```

# Future Roadmap
- Implementation of a Minimax-based AI opponent.
- Integration of a Move-Undo stack (Command Pattern).
- Transition from Terminal UI to a local Pygame Graphical Interface.
