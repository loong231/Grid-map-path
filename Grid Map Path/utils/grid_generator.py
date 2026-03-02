"""
路径规划的统一接口
提供三种算法的统一调用方式
"""

import time
import random
from typing import List, Tuple, Optional, Dict, Any
from algorithms.bfs import bfs_search
from algorithms.dfs import dfs_search
from algorithms.a_star import a_star_search

# 新增栅格生成函数
def create_simple_grid(rows: int = 10, cols: int = 10) -> List[List[int]]:
    """创建简单栅格（仅边界为障碍）"""
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    # 边界设为障碍
    for i in range(rows):
        grid[i][0] = 1
        grid[i][cols-1] = 1
    for j in range(cols):
        grid[0][j] = 1
        grid[rows-1][j] = 1
    return grid

def create_grid(rows: int = 10, cols: int = 10, obstacle_rate: float = 0.2) -> List[List[int]]:
    """创建随机障碍栅格"""
    grid = create_simple_grid(rows, cols)
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            if random.random() < obstacle_rate:
                grid[i][j] = 1
    return grid

def create_maze_grid(rows: int = 10, cols: int = 10) -> List[List[int]]:
    """创建迷宫式栅格（示例，可根据需求修改）"""
    grid = create_simple_grid(rows, cols)
    # 中间添加随机通道和障碍
    for i in range(2, rows-2, 2):
        for j in range(2, cols-2, 2):
            grid[i][j] = 1
            grid[i+1][j] = 0
            grid[i][j+1] = 0
    return grid

class PathFinder:
    """路径规划器，整合三种算法"""
    def __init__(self, grid: List[List[int]]):
        """
        初始化路径规划器
        
        参数:
            grid: 二维栅格地图，0表示可通过，1表示障碍
        """
        self.grid = grid
        self.results = {}  # 存储算法运行结果

    def run_all_algorithms(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Dict[str, Dict[str, Any]]:
        """
        运行所有算法并比较结果
        
        参数:
            start: 起点坐标 (row, col)
            goal: 终点坐标 (row, col)
        
        返回:
            包含所有算法结果的字典
        """
        self.results = {}
        
        # 运行BFS
        start_time = time.time()
        bfs_path, bfs_explored = bfs_search(self.grid, start, goal)
        bfs_time = time.time() - start_time
        
        # 运行DFS
        start_time = time.time()
        dfs_path, dfs_explored = dfs_search(self.grid, start, goal)
        dfs_time = time.time() - start_time
        
        # 运行A*
        start_time = time.time()
        a_star_path, a_star_explored = a_star_search(self.grid, start, goal)
        a_star_time = time.time() - start_time
        
        # 存储结果
        self.results['BFS'] = {
            'path': bfs_path,
            'explored': bfs_explored,
            'time': bfs_time,
            'path_length': len(bfs_path) if bfs_path else 0,
            'nodes_explored': len(bfs_explored)
        }
        
        self.results['DFS'] = {
            'path': dfs_path,
            'explored': dfs_explored,
            'time': dfs_time,
            'path_length': len(dfs_path) if dfs_path else 0,
            'nodes_explored': len(dfs_explored)
        }
        
        self.results['A*'] = {
            'path': a_star_path,
            'explored': a_star_explored,
            'time': a_star_time,
            'path_length': len(a_star_path) if a_star_path else 0,
            'nodes_explored': len(a_star_explored)
        }
        return self.results