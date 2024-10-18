from dataclasses import dataclass

from objects.frames import PuzzleFrame


@dataclass
class PuzzleData:
    puzzle_frame: PuzzleFrame
    digit: int
    row: int
    column: int
