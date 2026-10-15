"""A* search for four-direction grid pathfinding."""

import heapq
from typing import Dict, List, Optional, Set, Tuple

from ._validation import is_valid_problem

Coordinate = Tuple[int, int]


def heuristic(a: Coordinate, b: Coordinate) -> int:
    """Manhattan distance, admissible for four-direction unit-cost moves."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star_search(
    grid: List[List[int]], start: Coordinate, goal: Coordinate
) -> Tuple[Optional[List[Coordinate]], Set[Coordinate]]:
    """Return a shortest path and the set of expanded nodes."""
    if not is_valid_problem(grid, start, goal):
        return None, set()

    open_list = [(heuristic(start, goal), 0, start)]
    parents: Dict[Coordinate, Optional[Coordinate]] = {start: None}
    g_values = {start: 0}
    explored: Set[Coordinate] = set()
    directions = ((-1, 0), (0, 1), (1, 0), (0, -1))

    while open_list:
        _, current_g, current = heapq.heappop(open_list)
        if current_g != g_values.get(current):
            continue
        explored.add(current)

        if current == goal:
            path = []
            node: Optional[Coordinate] = current
            while node is not None:
                path.append(node)
                node = parents[node]
            return list(reversed(path)), explored

        for row_delta, col_delta in directions:
            neighbor = (current[0] + row_delta, current[1] + col_delta)
            row, col = neighbor
            if not (
                0 <= row < len(grid)
                and 0 <= col < len(grid[0])
                and grid[row][col] == 0
            ):
                continue

            new_g = current_g + 1
            if new_g < g_values.get(neighbor, float("inf")):
                g_values[neighbor] = new_g
                parents[neighbor] = current
                priority = new_g + heuristic(neighbor, goal)
                heapq.heappush(open_list, (priority, new_g, neighbor))

    return None, explored
