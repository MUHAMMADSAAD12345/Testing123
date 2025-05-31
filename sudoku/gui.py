import tkinter as tk
from tkinter import font
from sudoku.game import Sudoku
# Using the same default puzzle as the CLI for consistency
from sudoku.cli import DEFAULT_PUZZLE

class SudokuGUI(tk.Tk):
    def __init__(self, initial_board_data):
        super().__init__()
        self.title("Sudoku Game")
        # Increased height to accommodate buttons and status label
        self.geometry("550x650")
        self.resizable(False, False)

        self.game = Sudoku(board=[row[:] for row in initial_board_data])
        self.initial_board_setup = [row[:] for row in initial_board_data]

        self.cells_vars = [[tk.StringVar() for _ in range(9)] for _ in range(9)]
        self.cells_entries = [[None for _ in range(9)] for _ in range(9)]

        self.default_font = font.Font(family="Helvetica", size=16)
        self.prefilled_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.user_valid_font = font.Font(family="Helvetica", size=16)

        self._create_grid_widgets()
        self._create_control_widgets()
        self.draw_board_from_game_state()
        self.update_status("Game started. Enter numbers (1-9).")


    def _create_grid_widgets(self):
        # Renamed from _create_grid to be more specific
        grid_frame = tk.Frame(self, bd=2, relief=tk.SOLID)
        grid_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Create 3x3 subgrids (frames) for visual separation
        subgrid_frames = [[None for _ in range(3)] for _ in range(3)]
        for r_idx in range(3):
            for c_idx in range(3):
                frame = tk.Frame(main_frame, borderwidth=1, relief=tk.SOLID, bg="lightgrey" if (r_idx + c_idx) % 2 == 0 else "white")
                frame.grid(row=r_idx, column=c_idx, sticky="nsew", padx=1, pady=1) # Use padx/pady on frames
                grid_frame.grid_rowconfigure(r_idx, weight=1, minsize=150)
                grid_frame.grid_columnconfigure(c_idx, weight=1, minsize=150)
                subgrid_frames[r_idx][c_idx] = frame

        # Create cells within subgrid frames
        for r in range(9):
            for c in range(9):
                subgrid_r, subgrid_c = r // 3, c // 3
                cell_r, cell_c = r % 3, c % 3

                parent_frame = subgrid_frames[subgrid_r][subgrid_c] # This is the 3x3 subgrid frame
                cell_var = self.cells_vars[r][c]
                # Initial values for StringVars are set by draw_board_from_game_state or _on_cell_change

                validate_cmd = self.register(self._validate_char_input)
                entry = tk.Entry(
                    parent_frame, # Parent is the specific 3x3 subgrid frame
                    textvariable=cell_var,
                    width=2,
                    font=self.default_font,
                    justify='center',
                    borderwidth=1, relief=tk.SOLID,
                    validate="key", validatecommand=(validate_cmd, '%P')
                )
                cell_var.trace_add("write", lambda name, index, mode, r=r, c=c: self._on_cell_change(r, c))
                entry.grid(row=cell_r, column=cell_c, sticky="nsew", padx=1, pady=1)
                parent_frame.grid_rowconfigure(cell_r, weight=1)
                parent_frame.grid_columnconfigure(cell_c, weight=1)
                self.cells_entries[r][c] = entry

    def _create_control_widgets(self):
        control_frame = tk.Frame(self)
        control_frame.pack(pady=5)

        new_game_btn = tk.Button(control_frame, text="New Game", command=self._new_game_action)
        new_game_btn.pack(side=tk.LEFT, padx=5)

        solve_btn = tk.Button(control_frame, text="Solve", command=self._solve_action)
        solve_btn.pack(side=tk.LEFT, padx=5)

        check_btn = tk.Button(control_frame, text="Check Solution", command=self._check_solution_action)
        check_btn.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(self, text="", font=("Helvetica", 12))
        self.status_label.pack(pady=5)

    def _validate_char_input(self, proposed_value):
        """Low-level validation for Entry: Allows only single digits 1-9 or an empty string."""
        if proposed_value == "":
            return True
        if len(proposed_value) == 1 and proposed_value.isdigit() and '1' <= proposed_value <= '9':
            return True
        return False

    def _on_cell_change(self, r, c):
        if self.initial_board_setup[r][c] != 0:
            return # Pre-filled, should not change (readonly state handles this)

        entry = self.cells_entries[r][c]
        new_value_str = self.cells_vars[r][c].get()
        self.update_status("") # Clear status on new input

        if not new_value_str: # Cell cleared
            if self.game.board[r][c] != 0:
                self.game.board[r][c] = 0
                entry.config(fg='black', bg='white')
            return

        if len(new_value_str) == 1 and new_value_str.isdigit():
            num = int(new_value_str)
            original_game_board_val = self.game.board[r][c] # Store value before pretending cell is empty
            self.game.board[r][c] = 0 # Make cell empty for is_valid_move check

            if self.game.is_valid_move(r, c, num):
                self.game.board[r][c] = num # Update game board
                entry.config(fg='green', bg='white')
            else:
                self.game.board[r][c] = original_game_board_val # Revert to original value in game logic

                entry.config(fg='red', bg='pink')
                def revert_style_after_error():
                    # Only clear if the invalid value is still present
                    if self.cells_vars[r][c].get() == new_value_str:
                        self.cells_vars[r][c].set(str(original_game_board_val) if original_game_board_val != 0 else "")
                    # Ensure correct color, even if value was reverted by another action
                    current_val_in_var = self.cells_vars[r][c].get()
                    if not current_val_in_var: # Empty
                        entry.config(fg='black', bg='white')
                    elif self.game.is_valid_move(r,c,int(current_val_in_var)): # Check if current val is valid
                         entry.config(fg='green', bg='white')
                    # else it might have been set by another error, leave it red/pink or handle complex state
                    # For simplicity, if it's not empty and not the errorneous new_value_str, assume it's ok or handled by another event.
                    # This part can get complex with rapid inputs. The main goal is to remove the *current* error.
                    elif self.cells_vars[r][c].get() != new_value_str : # If different value, assume it's handled. Resetting might be bad.
                        pass # Do not change style, it might be a new valid/invalid entry
                    else: # Fallback to black/white if still the error value somehow (should be cleared by set(""))
                        entry.config(fg='black', bg='white')


                self.after(800, revert_style_after_error)
        # No specific action if not a single digit or empty, as _validate_char_input should prevent this.

    def draw_board_from_game_state(self):
        """Draws/Refreshes the board based on self.game.board and self.initial_board_setup."""
        for r in range(9):
            for c in range(9):
                entry = self.cells_entries[r][c]
                cell_var = self.cells_vars[r][c]
                game_value = self.game.board[r][c]
                initial_puzzle_value = self.initial_board_setup[r][c]

                # Manage trace to prevent self-triggering during programmatic set
                trace_info = cell_var.trace_info()
                trace_name = None
                if trace_info:
                    trace_name = trace_info[0][0] # Usually ('write', callback_name_string)
                    cell_var.trace_vdelete("w", trace_name)

                current_display_val = cell_var.get()
                new_display_val = str(game_value) if game_value != 0 else ""

                if current_display_val != new_display_val: # Only set if different
                    cell_var.set(new_display_val)

                if initial_puzzle_value != 0: # Pre-filled from original puzzle
                    entry.config(font=self.prefilled_font, fg='blue', state='readonly', readonlybackground='lightyellow')
                else: # User-editable cell
                    entry.config(state='normal') # Ensure it's normal before styling
                    if game_value != 0: # User-filled or solver-filled
                        # To color correctly, we need to know if it's valid.
                        # We assume if it's in self.game.board and not initial, it was placed there validly
                        # or by the solver.
                        # A more robust way would be to re-check self.game.is_valid_move(r,c,game_value)
                        # but that requires care if the cell itself contains game_value.
                        # For now, color user input green.
                        entry.config(font=self.user_valid_font, fg='green', bg='white')
                    else: # Empty user-editable cell
                        entry.config(font=self.default_font, fg='black', bg='white')

                if trace_name: # Re-add trace if it was removed
                    cell_var.trace_add("write", lambda name, index, mode, r_param=r, c_param=c: self._on_cell_change(r_param, c_param))


    def get_board_data_from_gui(self):
        """Retrieves board state from GUI StringVars and updates self.game.board."""
        board = [[0 for _ in range(9)] for _ in range(9)]
        for r in range(9):
            for c in range(9):
                try:
                    val_str = self.cells_vars[r][c].get().strip()
                    if val_str and val_str.isdigit():
                        board[r][c] = int(val_str)
                    else:
                        board[r][c] = 0
                except ValueError: # Should not happen with validation
                    board[r][c] = 0
        self.game.board = board # Update game state directly
        return board # Also return for convenience if needed

    def update_status(self, message):
        self.status_label.config(text=message)

    def _new_game_action(self):
        self.update_status("Starting new game...")
        # For now, re-uses DEFAULT_PUZZLE. Could be extended for difficulty.
        new_board_data = [row[:] for row in DEFAULT_PUZZLE]
        self.game = Sudoku(board=new_board_data)
        self.initial_board_setup = [row[:] for row in new_board_data]
        self.draw_board_from_game_state() # This will also reset StringVars
        self.update_status("New game started. Good luck!")

    def _solve_action(self):
        self.update_status("Attempting to solve...")
        # Ensure current GUI state is in self.game.board before solving
        # This is important if user made changes not yet reflected due to focus lost etc.
        # However, our StringVars should keep self.game.board fairly up-to-date.
        # For safety, one might call self.get_board_data_from_gui() here.

        # If any cell is invalid (red), solver might behave unexpectedly or fail.
        # It's better to solve from a valid (even if incomplete) state.
        # The current _on_cell_change tries to revert invalid entries to 0 in game.board.

        if self.game.solve():
            self.draw_board_from_game_state() # Display solution
            self.update_status("Puzzle Solved!")
        else:
            # game.solve() might leave the board partially modified.
            # Redraw to show the state after the solve attempt.
            self.draw_board_from_game_state()
            self.update_status("Could not find a solution from the current state.")

    def _check_solution_action(self):
        self.get_board_data_from_gui() # Ensure self.game.board has latest from GUI

        is_board_full = all(self.game.board[r][c] != 0 for r in range(9) for c in range(9))

        if not is_board_full:
            self.update_status("Please fill all cells before checking.")
            return

        if self.game.is_solved():
            self.update_status("Congratulations! Puzzle solved correctly!")
            # Optionally, make all cells readonly or give some other final indication.
        else:
            self.update_status("Solution is incorrect. Keep trying!")
            # Could add more specific error highlighting here if desired in future.


if __name__ == "__main__":
    initial_puzzle_data = DEFAULT_PUZZLE
    app = SudokuGUI(initial_board_data=initial_puzzle_data)
    app.mainloop()
