import random
from typing import List, Union

import customtkinter as ctk
import tkinter.messagebox as messagebox

from objects.data import PuzzleData
from objects.frames import PuzzleFrame


class App(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title("Пятнашки")
        self.geometry("256x256")
        self.resizable(False, False)  # Disable resizing

        # Generate puzzles matrix

        self.puzzles: List[List[Union[PuzzleData, None]]] = []

        for _ in range(4):
            self.puzzles.append([None, None, None, None])

        # Configure grid
        for i in range(4):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)

        # Generating puzzles
        self._filling_puzzles_matrix()

    def _filling_puzzles_matrix(self):

        alphabet: List[int] = random.sample(range(1, 16), 15)

        for row_index, row in enumerate(self.puzzles):
            for column_index, col in enumerate(row):

                # Пропускаем первый пазл
                if row_index == 0 and column_index == 0:
                    continue

                digit = random.choice(alphabet)
                alphabet.remove(digit)

                # Render puzzle
                puzzle = PuzzleFrame(self,
                                     puzzle_number=digit,
                                     row=row_index,
                                     column=column_index,
                                     fg_color="gray60",
                                     width=64,
                                     height=64,
                                     corner_radius=18)
                puzzle.grid(row=row_index,
                            column=column_index,
                            sticky="nsew")

                # Create puzzle data
                puzzle_data = PuzzleData(puzzle,
                                         digit,
                                         row_index,
                                         column_index)

                # Bind puzzle moving
                puzzle.bind("<Button-1>", lambda _, pd=puzzle_data: self._handle_puzzle_click(pd))
                puzzle.label.bind("<Button-1>", lambda _, pd=puzzle_data: self._handle_puzzle_click(pd))

                self.puzzles[row_index][column_index] = puzzle_data

        print(f"[!] Сгенерирована матрица пазлов")

    def _handle_puzzle_click(self, puzzle_data: PuzzleData):
        # Check if move is available
        is_puzzle_move_available: Union[bool, tuple] = self._is_puzzle_move_available(puzzle_data.row,
                                                                                      puzzle_data.column)

        if not is_puzzle_move_available:
            messagebox.showerror("Ошибка!", "Нет возможных ходов.")
            return

        # Move puzzle

        self.puzzles[puzzle_data.row][puzzle_data.column] = None

        puzzle_data.row = is_puzzle_move_available[0]
        puzzle_data.column = is_puzzle_move_available[1]

        puzzle_data.puzzle_frame.grid(row=puzzle_data.row,
                                      column=puzzle_data.column,
                                      sticky="nsew")

        # Update new puzzle in puzzles matrix

        self.puzzles[puzzle_data.row][puzzle_data.column] = puzzle_data

        # Check if player is won
        is_won: bool = self._is_puzzle_is_correct_order()

        if is_won:
            messagebox.showinfo("Пятнашки", "Вы выиграли! Поздравляем.")

    def _is_puzzle_is_correct_order(self) -> bool:

        correct_subsequence = [i for i in range(1, 16)] + [None]
        player_subsequence = []

        for row in self.puzzles:
            for column in row:

                if column is None:
                    player_subsequence.append(None)
                    continue

                player_subsequence.append(column.digit)

        if correct_subsequence == player_subsequence:
            return True

        return False

    def _is_puzzle_move_available(self, row: int, column: int) -> Union[bool, tuple]:
        """
        :param row:
        :param column:
        :return: False or tuple with row, column
        """

        # Check available moving to top
        puzzle_top = self._get_puzzle_by_row_column(row - 1, column)

        if puzzle_top is None:
            return row - 1, column

        # Check available moving to bottom
        puzzle_bottom = self._get_puzzle_by_row_column(row + 1, column)

        if puzzle_bottom is None:
            return row + 1, column

        # ======== CHECK AVAILABLE MOVING TO LEFT/RIGHT

        # Check available moving to left
        puzzle_left = self._get_puzzle_by_row_column(row, column - 1)

        if puzzle_left is None:
            return row, column - 1

        # Check available moving to right
        puzzle_right = self._get_puzzle_by_row_column(row, column + 1)

        if puzzle_right is None:
            return row, column + 1

        return False

    def _get_puzzle_by_row_column(self, row: int, column: int) -> Union[None, bool, PuzzleData]:

        # Check attempt to get puzzle off the map
        if row > 3 or column > 3:
            return False

        return self.puzzles[row][column]


def main():
    app = App()

    app.mainloop()


if __name__ == '__main__':
    main()
