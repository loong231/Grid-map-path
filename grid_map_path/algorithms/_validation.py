"""Shared input validation for grid search algorithms."""

from typing import List, Tuple


def is_valid_problem(
    grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]
) -> bool:
    """Return whether the grid and endpoints describe a usable search problem."""
    if not grid or not grid[0]:
        return False
    width = len(grid[0])
    if any(len(row) != width for row in grid):
        return False

    for point in (start, goal):
        if (
            not isinstance(point, tuple)
            or len(point) != 2
            or not all(isinstance(value, int) for value in point)
        ):
            return False
        row, col = point
        if not (0 <= row < len(grid) and 0 <= col < width):
            return False
        if grid[row][col] != 0:
            return False
    return True
