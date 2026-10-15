"""Depth-first search for four-direction grid pathfinding."""

from typing import List, Optional, Set, Tuple

from ._validation import is_valid_problem

Coordinate = Tuple[int, int]


def dfs_search(
    grid: List[List[int]], start: Coordinate, goal: Coordinate
) -> Tuple[Optional[List[Coordinate]], Set[Coordinate]]:
    """Return a path if one exists and the set of expanded nodes."""
    if not is_valid_problem(grid, start, goal):
        return None, set()

    stack = [(start, None)]
    parents = {start: None}
    explored: Set[Coordinate] = set()
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))

    while stack:
        current, parent = stack.pop()
        if current in explored:
            continue
        if parent is not None:
            parents[current] = parent
        explored.add(current)

        if current == goal:
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = parents[node]
            return list(reversed(path)), explored

        for row_delta, col_delta in directions:
            neighbor = (current[0] + row_delta, current[1] + col_delta)
            row, col = neighbor
            if (
                0 <= row < len(grid)
                and 0 <= col < len(grid[0])
                and grid[row][col] == 0
                and neighbor not in parents
                and neighbor not in explored
            ):
                parents[neighbor] = current
                stack.append((neighbor, current))

    return None, explored
