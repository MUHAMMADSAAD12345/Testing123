# Python Sudoku Game

## Description

This project is a Sudoku game implemented in Python, featuring both a command-line interface (CLI) and a graphical user interface (GUI). It allows users to play Sudoku by entering numbers into a 9x9 grid. The game can validate moves, check if the puzzle is solved, and provide a solution.

## Running the Game

This game offers two interfaces: a command-line interface and a graphical user interface built with Tkinter.

### 1. Command-Line Interface (CLI)

To run the CLI version, navigate to the parent directory containing the `sudoku` package and use the following command:

```bash
python -m sudoku.cli
```
This will start the game in your terminal.

**CLI Gameplay Instructions:**
-   The board will be displayed with empty cells represented by a `.` (period).
-   To place a number, enter the row, column, and the number you wish to place, separated by spaces (e.g., `3 4 5` to place the number `5` in the 3rd row and 4th column). Rows and columns are 1-indexed.
-   The game will validate your move. If it's invalid, you'll be prompted to try again.
-   Cells that are part of the initial puzzle cannot be overwritten.
-   To ask the game to solve the puzzle, type `solve`.
-   To quit the game at any time, type `quit`.

### 2. Graphical User Interface (GUI)

To run the GUI version, ensure you have Tkinter installed (usually included with Python). Navigate to the parent directory containing the `sudoku` package and use the following command:

```bash
python -m sudoku.gui
```
Alternatively, you can run the `gui.py` file directly if you are in the `sudoku` directory: `python gui.py`. The module approach is generally recommended.

**GUI Features & Gameplay:**
-   **Interactive Board**: A 9x9 grid of cells where you can type numbers.
-   **Visual Feedback**:
    - Pre-filled numbers are bold, blue, and read-only.
    - Valid user-entered numbers appear in green.
    - Invalid entries will temporarily turn the cell background pink and the text red, then the invalid number will be cleared.
-   **Control Buttons**:
    - **New Game**: Starts a new puzzle (currently resets to the default puzzle).
    - **Solve**: Attempts to solve the current puzzle and displays the solution if found.
    - **Check Solution**: Verifies if your current solution is correct. You must fill all cells first.
-   **Status Bar**: Displays messages about game state and actions.

## Project Structure

The project consists of the following main files:

-   **`sudoku/game.py`**: Contains the core `Sudoku` class, which manages the game logic, including the board state, move validation (`is_valid_move`), checking for a solved state (`is_solved`), and the solving algorithm (`solve`).
-   **`sudoku/cli.py`**: Implements the command-line interface for the game. It handles user input, displays the board, and interacts with the `Sudoku` class to manage the game flow.
-   **`sudoku/gui.py`**: Implements the graphical user interface using Tkinter. It provides an interactive grid, input validation with visual feedback, and game control buttons.
-   **`sudoku/tests/test_game.py`**: Includes unit tests for the `Sudoku` class in `game.py`, ensuring its methods function correctly under various conditions. These tests use Python's `unittest` module.
-   **`sudoku/README.md`**: This file, providing information about the project.

## Future Enhancements (Optional)

-   Different difficulty levels for puzzles.
-   Ability to save and load game progress.
-   More advanced solver algorithms.
-   Hints for the user during gameplay.
-   Improved visual styling for the GUI.
