from sudoku.game import Sudoku

# Default puzzle for the CLI game (moderately difficult)
DEFAULT_PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

def display_board(board):
    """Prints the Sudoku board in a user-friendly format."""
    print("\n+" + "-------+" * 3)
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("+" + "-------+" * 3)
        print("| ", end="")
        for j, num in enumerate(row):
            print(num if num != 0 else ".", end=" ")
            if (j + 1) % 3 == 0:
                print("| ", end="")
        print()
    print("+" + "-------+" * 3)

def get_user_input(board):
    """
    Prompts the user for row, column, and number, or a command.
    Returns a tuple (row, col, num) or a command string ('solve', 'quit').
    Row and col are 0-indexed internally, but 1-indexed for user.
    """
    while True:
        try:
            user_input = input("Enter row, col, num (e.g., '1 2 3'), or command ('solve', 'quit'): ").strip().lower()

            if user_input == "solve":
                return "solve"
            if user_input == "quit":
                return "quit"

            parts = user_input.split()
            if len(parts) != 3:
                raise ValueError("Invalid input format. Please enter three numbers or a command.")

            row, col, num = map(int, parts)

            if not (1 <= row <= 9 and 1 <= col <= 9 and 1 <= num <= 9):
                raise ValueError("Row, column, and number must be between 1 and 9.")

            # Check if the cell is part of the original puzzle (non-zero)
            # We need the original puzzle state for this. For simplicity,
            # we can assume the initial DEFAULT_PUZZLE's non-zero cells are fixed.
            # A better way would be to store the initial state in the Sudoku object.
            # For now, let's allow overwriting for simplicity in this CLI,
            # or assume a Sudoku class that can differentiate fixed cells.
            # Let's adjust this to check if the cell in the *current* board is already filled.
            # The Sudoku class's is_valid_move doesn't care if we're overwriting,
            # but for user experience, we might want to warn or prevent overwriting non-empty cells.
            # However, the prompt asks for `is_valid_move` to check, which implies we can try any cell.

            return row - 1, col - 1, num  # Adjust to 0-indexed

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def main():
    """Main game loop for the Sudoku CLI."""
    game = Sudoku(board=DEFAULT_PUZZLE) # Initialize with a default puzzle
    # game = Sudoku() # To start with the solved board from game.py for testing
    # game = Sudoku(board=[[0]*9 for _ in range(9)]) # To start with an empty board

    print("Welcome to Sudoku!")
    print("Enter 'row col num' (1-9) to place a number.")
    print("Enter 'solve' to see the solution, or 'quit' to exit.")

    while True:
        display_board(game.board)

        if game.is_solved():
            print("\nCongratulations! You solved the Sudoku!")
            break

        user_action = get_user_input(game.board) # Pass board for potential future checks

        if user_action == "quit":
            print("Thanks for playing!")
            break

        if user_action == "solve":
            print("Attempting to solve the puzzle...")
            # We need to ensure the original puzzle is what's being solved,
            # not the current state if the user made mistakes.
            # For now, we'll solve the current state.
            solution_found = game.solve()
            if solution_found:
                print("Solution:")
                display_board(game.board)
                if not game.is_solved(): # Should be solved if game.solve() returned True
                     print("The solver finished, but the board isn't marked as solved. This might be a bug.")
                else:
                    print("Puzzle solved successfully!")
            else:
                print("Could not solve the puzzle from the current state.")
            break # End game after attempting solve

        if isinstance(user_action, tuple):
            row, col, num = user_action

            # Check if the cell is part of the original puzzle
            # For this version, we assume the DEFAULT_PUZZLE's initial non-zero cells are fixed.
            # A more robust way is to have the Sudoku class track fixed cells.
            # This check is for user experience to prevent accidental overwriting of clues.
            if DEFAULT_PUZZLE[row][col] != 0:
                print(f"Cell ({row+1},{col+1}) is part of the original puzzle and cannot be changed.")
                continue

            if game.is_valid_move(row, col, num):
                game.board[row][col] = num
                print(f"Placed {num} at ({row+1},{col+1}).")
            else:
                # Provide more specific feedback if possible
                print(f"Invalid move: Placing {num} at ({row+1},{col+1}) violates Sudoku rules.")
                # game.is_valid_move could be enhanced to return *why* it's invalid.

        # Small delay or press enter to continue? For now, direct loop.

if __name__ == "__main__":
    main()
