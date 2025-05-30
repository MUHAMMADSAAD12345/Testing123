import unittest
from sudoku.game import Sudoku

# Sample boards for testing
EMPTY_BOARD = [[0 for _ in range(9)] for _ in range(9)]

PARTIALLY_FILLED_VALID = [
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

SOLVED_BOARD = [
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

# Full board but with errors (violates Sudoku rules)
INCORRECTLY_FILLED_BOARD = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2], # Row 0 is ok
    [6, 7, 2, 1, 9, 5, 3, 4, 8], # Row 1 is ok
    [1, 9, 8, 3, 4, 2, 5, 6, 7], # Row 2 is ok
    [8, 5, 9, 7, 6, 1, 4, 2, 3], # Row 3 is ok
    [4, 2, 6, 8, 5, 3, 7, 9, 1], # Row 4 is ok
    [7, 1, 3, 9, 2, 4, 8, 5, 6], # Row 5 is ok
    [9, 6, 1, 5, 3, 7, 2, 8, 4], # Row 6 is ok
    [2, 8, 7, 4, 1, 9, 6, 3, 5], # Row 7 is ok
    [3, 4, 5, 2, 8, 6, 1, 7, 3]  # Last element is 3, should be 9 (duplicate 3 in row/col/box)
]

# A simple unsolvable puzzle (e.g. two 5s in a row required for solution)
UNSOLVABLE_BOARD_SIMPLE = [
    [5, 5, 0, 0, 0, 0, 0, 0, 0], # Two 5s in first row
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]


class TestSudoku(unittest.TestCase):

    def test_initialization(self):
        game_default = Sudoku() # Uses the default solved board
        self.assertEqual(game_default.board, SOLVED_BOARD, "Default board should be the pre-solved one.")

        game_empty = Sudoku(board=EMPTY_BOARD)
        self.assertEqual(game_empty.board, EMPTY_BOARD, "Board should be initialized as empty.")

        # Ensure deep copy
        custom_board_original = [[1,0,0,0,0,0,0,0,0]] + [[0]*9 for _ in range(8)]
        game_custom = Sudoku(board=custom_board_original)
        self.assertEqual(game_custom.board, custom_board_original)
        custom_board_original[0][0] = 9 # Modify original
        self.assertEqual(game_custom.board[0][0], 1, "Sudoku should use a deep copy of the initial board.")


    def test_is_valid_move(self):
        game = Sudoku(board=PARTIALLY_FILLED_VALID)
        # Valid moves
        self.assertTrue(game.is_valid_move(0, 2, 4), "Should be valid to place 4 at (0,2)") # Original is 0
        self.assertTrue(game.is_valid_move(2, 0, 2), "Should be valid to place 2 at (2,0)") # Original is 0

        # Invalid due to row conflict
        self.assertFalse(game.is_valid_move(0, 2, 5), "Invalid: 5 already in row 0")

        # Invalid due to column conflict
        self.assertFalse(game.is_valid_move(1, 0, 5), "Invalid: 5 already in col 0")

        # Invalid due to 3x3 subgrid conflict
        # PARTIALLY_FILLED_VALID has 5 at (0,0), 3 at (0,1)
        self.assertFalse(game.is_valid_move(1, 1, 5), "Invalid: 5 already in top-left 3x3 subgrid")

        # Test placing in an already occupied cell (is_valid_move should allow if the number itself is valid for the spot)
        # For example, PARTIALLY_FILLED_VALID has 5 at (0,0). If we check (0,0) for 5, it's a conflict.
        # If we check (0,0) for, say, 1 (assuming 1 is not in row/col/box), it should be true.
        # The current is_valid_move checks the number against existing numbers.
        # If cell (r,c) contains X, and we check is_valid_move(r,c,X), it will return False.
        # This is correct behavior for the solver (can't place a number if it's already "there" causing a conflict).
        self.assertFalse(game.is_valid_move(0, 0, 5), "Invalid: 5 is at (0,0), so placing 5 there creates conflict with itself.")
        # A different number, not violating rules for that spot (e.g. if (0,0) was empty)
        game_temp_empty_first_cell = Sudoku(board=[[0] + row[1:] for row in PARTIALLY_FILLED_VALID])
        self.assertTrue(game_temp_empty_first_cell.is_valid_move(0,0,1), "Should be valid to place 1 at (0,0) if it was empty and 1 is valid.")


    def test_is_solved(self):
        game_solved = Sudoku(board=SOLVED_BOARD)
        self.assertTrue(game_solved.is_solved(), "Board should be marked as solved.")

        game_empty = Sudoku(board=EMPTY_BOARD)
        self.assertFalse(game_empty.is_solved(), "Empty board should not be marked as solved.")

        game_partial = Sudoku(board=PARTIALLY_FILLED_VALID)
        self.assertFalse(game_partial.is_solved(), "Partially filled board should not be marked as solved.")

        game_incorrect = Sudoku(board=INCORRECTLY_FILLED_BOARD)
        self.assertFalse(game_incorrect.is_solved(), "Incorrectly filled board should not be marked as solved.")

    def test_solve_already_solved(self):
        game = Sudoku(board=SOLVED_BOARD)
        self.assertTrue(game.solve(), "Solve method should return True for an already solved board.")
        self.assertEqual(game.board, SOLVED_BOARD, "Board should remain unchanged if already solved.")
        self.assertTrue(game.is_solved(), "Board should still be solved.")

    def test_solve_empty_board(self):
        game = Sudoku(board=EMPTY_BOARD)
        self.assertTrue(game.solve(), "Solve method should be able to solve an empty board.")
        self.assertTrue(game.is_solved(), "Board should be solved after calling solve() on empty board.")

    def test_solve_standard_puzzle(self):
        game = Sudoku(board=PARTIALLY_FILLED_VALID)
        self.assertFalse(game.is_solved(), "Puzzle should initially be unsolved.")
        self.assertTrue(game.solve(), "Solve method should solve the puzzle.")
        self.assertTrue(game.is_solved(), "Board should be solved after calling solve().")
        # Check if it matches the known solution for this puzzle
        # The default SOLVED_BOARD is the solution for PARTIALLY_FILLED_VALID
        self.assertEqual(game.board, SOLVED_BOARD, "Solved puzzle should match the known solution.")

    def test_solve_unsolvable_puzzle(self):
        # This test depends on the solver being robust enough to correctly identify unsolvable.
        # The basic backtracking solver should return False.
        game_unsolvable = Sudoku(board=UNSOLVABLE_BOARD_SIMPLE)
        # The current `solve` might fill some cells before realizing it's unsolvable.
        # It should return False, and the board state might be modified.
        # A truly robust solver might leave the board as it was if no solution is found.
        # The current one will backtrack to 0s.

        # Create a copy of the board to check if it changes back to original state (or similar)
        original_unsolvable_board = [row[:] for row in UNSOLVABLE_BOARD_SIMPLE]

        self.assertFalse(game_unsolvable.solve(), "Solve method should return False for an unsolvable puzzle.")

        # After a failed solve, the board should ideally be reset to its original state before the solve attempt,
        # or at least not be marked as "solved". The current solver backtracks, so cells it tried will be 0.
        # If the original unsolvable board had 0s, it should revert to that.
        # UNSOLVABLE_BOARD_SIMPLE has non-zero values that make it unsolvable.
        # The solver will try to fill 0s. If it fails, those 0s it touched should be reset to 0.
        # The non-zero values that made it unsolvable will remain.
        # So, it should be equal to the original unsolvable board.

        # Let's verify the board is back to its original unsolvable state (or at least not solved)
        # The current solver backtracks to 0s. If the unsolvable part was due to initial non-zero numbers,
        # those numbers will persist.
        # For UNSOLVABLE_BOARD_SIMPLE, the two 5s will remain. The rest it tried will go back to 0.
        self.assertEqual(game_unsolvable.board, original_unsolvable_board,
                         "Board should be in its original unsolvable state (or equivalent) after failed solve.")
        self.assertFalse(game_unsolvable.is_solved(), "Unsolvable board should not be marked as solved after attempt.")


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
