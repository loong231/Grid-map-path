"""
A*（A星）算法实现
特点：使用启发式函数引导搜索，高效找到最短路径
"""

import heapq
from typing import List, Tuple, Set, Optional, Dict

def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    """
    启发式函数：曼哈顿距离（适用于4方向移动）
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> Tuple[Optional[List[Tuple[int, int]]], Set[Tuple[int, int]]]:
    """
    使用A*算法在栅格地图上寻路
    
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
    
    # 初始化优先队列 (f, g, node)
    # f = g + h, 其中g是从起点到当前节点的实际代价，h是启发式估计
    open_list = []
    heapq.heappush(open_list, (0 + heuristic(start, goal), 0, start))
    
    # 记录每个节点的父节点和g值
    came_from: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
    g_values = {start: 0}
    
    explored = set([start])
    
    while open_list:
        _, g, current = heapq.heappop(open_list)
        
        # 如果找到目标
        if current == goal:
            # 回溯构建路径
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path, explored
        
        # 探索当前节点的邻居
        for dr, dc in directions:
            nr, nc = current[0] + dr, current[1] + dc
            
            # 检查边界和障碍
            if (0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and 
                grid[nr][nc] == 0):
                
                # 计算新的g值（每步代价为1）
                new_g = g + 1
                
                # 如果这是一个新节点，或者找到了更短的路径
                if (nr, nc) not in g_values or new_g < g_values[(nr, nc)]:
                    g_values[(nr, nc)] = new_g
                    f = new_g + heuristic((nr, nc), goal)
                    heapq.heappush(open_list, (f, new_g, (nr, nc)))
                    came_from[(nr, nc)] = current
                    explored.add((nr, nc))
    
    # 没有找到路径
    return None, explored