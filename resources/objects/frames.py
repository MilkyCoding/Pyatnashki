from typing import Any, Union

import customtkinter as ctk


class PuzzleFrame(ctk.CTkFrame):
    def __init__(self, master: Any, puzzle_number: Union[int, str],
                 row: int, column: int,
                 **kwargs):
        super().__init__(master, **kwargs)

        # Configure grid
        self.grid_rowconfigure(row, weight=1)
        self.grid_columnconfigure(column, weight=1)

        # Create additionally widgets
        self.label = ctk.CTkLabel(self,
                                  text=str(puzzle_number))
        self.label.grid(row=row, column=column)