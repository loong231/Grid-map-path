"""
DFS（深度优先搜索）算法实现
特点：可能快速找到路径，但不一定是最短路径
"""

from typing import List, Tuple, Set, Optional

def dfs_search(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[Optional[List[Tuple[int, int]]], Set[Tuple[int, int]]]:
    """
    使用DFS算法在栅格地图上寻路
    
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
    
    # 使用栈实现DFS
    stack = [(start, [start])]  # (当前节点, 当前路径)
    visited = set([start])
    explored = set([start])
    
    while stack:
        current, path = stack.pop()
        
        # 如果找到目标
        if current == goal:
            return path, explored
        
        # 探索当前节点的邻居
        for dr, dc in directions:
            nr, nc = current[0] + dr, current[1] + dc
            
            # 检查边界和障碍
            if (0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and 
                grid[nr][nc] == 0 and (nr, nc) not in visited):
                
                visited.add((nr, nc))
                explored.add((nr, nc))
                stack.append(((nr, nc), path + [(nr, nc)]))
    
    # 没有找到路径
    return None, explored