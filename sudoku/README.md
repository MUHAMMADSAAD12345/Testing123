# Python Sudoku Game

## Description

This project is a simple command-line Sudoku game implemented in Python. It allows users to play Sudoku by entering numbers into a 9x9 grid. The game can validate moves, check if the puzzle is solved, and provide a solution if the user requests it.

## How to Play

To run the Sudoku game, navigate to the parent directory containing the `sudoku` package and use the following command:

```bash
python -m sudoku.cli
```

This will start the command-line interface where you can interact with the game.

### Gameplay Instructions:

-   The board will be displayed with empty cells represented by a `.` (period).
-   To place a number, enter the row, column, and the number you wish to place, separated by spaces (e.g., `3 4 5` to place the number `5` in the 3rd row and 4th column). Rows and columns are 1-indexed.
-   The game will validate your move. If it's invalid, you'll be prompted to try again.
-   Cells that are part of the initial puzzle cannot be overwritten.
-   To ask the game to solve the puzzle, type `solve`.
-   To quit the game at any time, type `quit`.

## Project Structure

The project consists of the following main files:

-   **`sudoku/game.py`**: Contains the core `Sudoku` class, which manages the game logic, including the board state, move validation (`is_valid_move`), checking for a solved state (`is_solved`), and the solving algorithm (`solve`).
-   **`sudoku/cli.py`**: Implements the command-line interface for the game. It handles user input, displays the board, and interacts with the `Sudoku` class to manage the game flow.
-   **`sudoku/tests/test_game.py`**: Includes unit tests for the `Sudoku` class in `game.py`, ensuring its methods function correctly under various conditions. These tests use Python's `unittest` module.
-   **`sudoku/README.md`**: This file, providing information about the project.

## Future Enhancements (Optional)

-   Different difficulty levels for puzzles.
-   A graphical user interface (GUI).
-   Ability to save and load game progress.
-   More advanced solver algorithms.
-   Hints for the user.
