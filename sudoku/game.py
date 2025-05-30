class Sudoku:
    def __init__(self, board=None):
        if board:
            self.board = [row[:] for row in board]
        else:
            # A simple solved Sudoku puzzle
            self.board = [
                [5, 3, 4, 6, 7, 8, 9, 1, 2],
                [6, 7, 2, 1, 9, 5, 3, 4, 8],
                [1, 9, 8, 3, 4, 2, 5, 6, 7],
                [8, 5, 9, 7, 6, 1, 4, 2, 3],
                [4, 2, 6, 8, 5, 3, 7, 9, 1],
                [7, 1, 3, 9, 2, 4, 8, 5, 6],
                [9, 6, 1, 5, 3, 7, 2, 8, 4],
                [2, 8, 7, 4, 1, 9, 6, 3, 5],
                [3, 4, 5, 2, 8, 6, 1, 7, 9]
            ]

    def print_board(self):
        """Prints the Sudoku board in a readable format."""
        for i, row in enumerate(self.board):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            for j, num in enumerate(row):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                print(num if num != 0 else ".", end=" ")
            print()

    def is_valid_move(self, row, col, num):
        """Checks if placing num at (row, col) is a valid move."""
        # Check row
        if num in self.board[row]:
            return False

        # Check column
        if num in [self.board[i][col] for i in range(9)]:
            return False

        # Check 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False

        return True

    def is_solved(self):
        """Checks if the current board configuration is a valid and complete Sudoku solution."""
        # Check if all cells are filled
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    return False # Not completely filled

        # Check rows and columns
        for i in range(9):
            row_nums = set()
            col_nums = set()
            for j in range(9):
                # Check row duplicates
                if self.board[i][j] in row_nums:
                    return False
                row_nums.add(self.board[i][j])

                # Check col duplicates
                if self.board[j][i] in col_nums:
                    return False
                col_nums.add(self.board[j][i])

        # Check 3x3 subgrids
        for box_row_start in range(0, 9, 3):
            for box_col_start in range(0, 9, 3):
                box_nums = set()
                for r in range(box_row_start, box_row_start + 3):
                    for c in range(box_col_start, box_col_start + 3):
                        num = self.board[r][c]
                        if num in box_nums:
                            return False
                        box_nums.add(num)
        return True

    def solve(self):
        """
        Solves the Sudoku puzzle.
        Placeholder for now.
        """
        # For now, if the board is already solved (e.g. the default one),
        # we can say it's "solved".
        if self.is_solved():
            print("Board is already solved or pre-filled and solved.")
            return True

        # Basic backtracking solver can be added here.
        # Find empty cell
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    for num_to_try in range(1, 10):
                        if self.is_valid_move(r, c, num_to_try):
                            self.board[r][c] = num_to_try
                            if self.solve(): # Recursive call
                                return True
                            self.board[r][c] = 0 # Backtrack
                    return False # No valid number found for this cell
        return True # Should be reached if board is full and valid


if __name__ == '__main__':
    # Example Usage
    print("Initial (Solved) Board:")
    solved_game = Sudoku()
    solved_game.print_board()
    print(f"Is solved? {solved_game.is_solved()}")

    print("\nEmpty Board:")
    empty_board_data = [[0 for _ in range(9)] for _ in range(9)]
    empty_game = Sudoku(board=empty_board_data)
    empty_game.print_board()
    print(f"Is solved? {empty_game.is_solved()}")
    print(f"Is 5 valid at (0,0)? {empty_game.is_valid_move(0, 0, 5)}")
    empty_game.board[0][0] = 5
    print("Board after placing 5 at (0,0):")
    empty_game.print_board()
    print(f"Is 5 valid at (0,1)? {empty_game.is_valid_move(0, 1, 5)}") # Should be False
    print(f"Is 2 valid at (0,1)? {empty_game.is_valid_move(0, 1, 2)}") # Should be True

    print("\nTrying to solve the empty board (will take time if not optimized):")
    # Be cautious with solving a completely empty board with a simple
    # recursive solver as it might be very slow.
    # For now, the solve method is very basic.
    # empty_game.solve()
    # empty_game.print_board()
    # print(f"Is solved after attempt? {empty_game.is_solved()}")

    print("\nPartially Filled Board (from a known puzzle):")
    puzzle = [
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
    game_to_solve = Sudoku(board=puzzle)
    game_to_solve.print_board()
    print(f"Is solved initially? {game_to_solve.is_solved()}") # Should be False
    # print("\nAttempting to solve the puzzle...")
    # game_to_solve.solve() # This will use the basic solver.
    # game_to_solve.print_board()
    # print(f"Is solved after attempt? {game_to_solve.is_solved()}")
