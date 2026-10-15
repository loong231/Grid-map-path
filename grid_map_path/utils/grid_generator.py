"""生成用于路径规划演示的网格地图。"""

import random
from typing import List


def _validate_dimensions(rows: int, cols: int) -> None:
    if rows < 3 or cols < 3:
        raise ValueError("地图行数和列数必须至少为 3。")


def create_simple_grid(rows: int = 10, cols: int = 10) -> List[List[int]]:
    """创建四周为障碍、内部可通行的网格。"""
    _validate_dimensions(rows, cols)
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for row in range(rows):
        grid[row][0] = grid[row][-1] = 1
    for col in range(cols):
        grid[0][col] = grid[-1][col] = 1
    return grid


def create_grid(
    rows: int = 10, cols: int = 10, obstacle_rate: float = 0.2
) -> List[List[int]]:
    """在内部区域按给定概率随机放置障碍。"""
    if not 0 <= obstacle_rate <= 1:
        raise ValueError("障碍物密度必须在 0 到 1 之间。")
    grid = create_simple_grid(rows, cols)
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            if random.random() < obstacle_rate:
                grid[row][col] = 1
    return grid


def create_maze_grid(rows: int = 10, cols: int = 10) -> List[List[int]]:
    """创建带有规则障碍的示例迷宫地图。"""
    grid = create_simple_grid(rows, cols)
    for row in range(2, rows - 2, 2):
        for col in range(2, cols - 2, 2):
            grid[row][col] = 1
            grid[row + 1][col] = 0
            grid[row][col + 1] = 0
    return grid
