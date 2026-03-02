"""
BFS（广度优先搜索）算法实现
特点：找到的路径是最短的，但搜索范围大
"""

from collections import deque
from typing import List, Tuple, Set, Optional

def bfs_search(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[Optional[List[Tuple[int, int]]], Set[Tuple[int, int]]]:
    """
    使用BFS算法在栅格地图上寻路
    
    参数:
        grid: 二维列表，0表示可通过，1表示障碍
        start: 起点坐标 (row, col)
        goal: 终点坐标 (row, col)
    
    返回:
        (path, explored): 路径列表和探索过的节点集合
    """
    # 验证输入
    if not (0 <= start[0] < len(grid) and 0 <= start[1] < len(grid[0])):
        return None, set()
    if not (0 <= goal[0] < len(grid) and 0 <= goal[1] < len(grid[0])):
        return None, set()
    if grid[start[0]][start[1]] == 1 or grid[goal[0]][goal[1]] == 1:
        return None, set()
    
    # 方向：上、右、下、左（4邻域）
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    # 初始化队列和访问记录
    queue = deque()
    queue.append(start)
    
    visited = {start: None}  # 记录每个节点的父节点（用于回溯路径）
    explored = set()  # 记录所有探索过的节点
    
    while queue:
        current = queue.popleft()
        
        # 如果找到目标
        if current == goal:
            # 回溯构建路径
            path = []
            while current is not None:
                path.append(current)
                current = visited[current]
            path.reverse()
            return path, explored
        
        # 探索当前节点的邻居
        for dr, dc in directions:
            nr, nc = current[0] + dr, current[1] + dc
            
            # 检查边界和障碍
            if (0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and 
                grid[nr][nc] == 0 and (nr, nc) not in visited):
                
                visited[(nr, nc)] = current
                queue.append((nr, nc))
                explored.add((nr, nc))
    
    # 没有找到路径
    return None, explored