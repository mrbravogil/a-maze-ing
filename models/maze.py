"""Maze class for the A-Maze-ing project."""

from typing import Optional
from .cell import Cell


class Maze:
    """Represents the base structure of a maze.

    Holds the maze dimensions, the entrance and exit cells, and the grid
    of cells that makes up the full maze layout.
    """
    def __init__(
            self,
            width: int,
            height: int,
            entry: Optional[Cell] = None,
            exit: Optional[Cell] = None) -> None:
        self.width = width
        self.height = height
        self.entry: Optional[Cell] = entry
        self.exit: Optional[Cell] = exit
        self.grid: list[list[Cell]] = []
