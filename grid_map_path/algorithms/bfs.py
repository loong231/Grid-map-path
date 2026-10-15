"""Breadth-first search for four-direction grid pathfinding."""

from collections import deque
from typing import List, Optional, Set, Tuple

from ._validation import is_valid_problem

Coordinate = Tuple[int, int]


def bfs_search(
    grid: List[List[int]], start: Coordinate, goal: Coordinate
) -> Tuple[Optional[List[Coordinate]], Set[Coordinate]]:
    """Return a shortest path and the set of expanded nodes."""
    if not is_valid_problem(grid, start, goal):
        return None, set()

    queue = deque([start])
    parents = {start: None}
    explored: Set[Coordinate] = set()
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))

    while queue:
        current = queue.popleft()
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
            ):
                parents[neighbor] = current
                queue.append(neighbor)

    return None, explored
