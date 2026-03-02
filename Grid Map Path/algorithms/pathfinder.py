"""
路径规划的统一接口
提供三种算法的统一调用方式
"""

import time
from typing import List, Tuple, Optional, Dict, Any
from .bfs import bfs_search
from .dfs import dfs_search
from .a_star import a_star_search

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
    
    def get_comparison_table(self) -> List[List[str]]:
        """
        生成算法对比表格
        
        返回:
            表格数据，可用于显示
        """
        if not self.results:
            return []
        
        table = [
            ["算法", "是否找到路径", "路径长度", "探索节点数", "运行时间(秒)", "特点"],
        ]
        
        for algo, result in self.results.items():
            found_path = "是" if result['path'] else "否"
            path_len = str(result['path_length'])
            nodes_exp = str(result['nodes_explored'])
            time_str = f"{result['time']:.6f}"
            
            # 算法特点描述
            if algo == 'BFS':
                feature = "保证最短路径，但搜索范围大"
            elif algo == 'DFS':
                feature = "可能快速找到路径，但不保证最短"
            else:  # A*
                feature = "智能引导，高效找到最短路径"
            
            table.append([algo, found_path, path_len, nodes_exp, time_str, feature])
        
        return table
    
    def get_algorithm_result(self, algorithm: str, start: Tuple[int, int], goal: Tuple[int, int]) -> Dict[str, Any]:
        """
        运行单个算法
        
        参数:
            algorithm: 算法名称 ('BFS', 'DFS', 或 'A*')
            start: 起点坐标
            goal: 终点坐标
        
        返回:
            算法结果
        """
        algorithm = algorithm.upper()
        
        if algorithm == 'BFS':
            path, explored = bfs_search(self.grid, start, goal)
        elif algorithm == 'DFS':
            path, explored = dfs_search(self.grid, start, goal)
        elif algorithm == 'A*' or algorithm == 'ASTAR':
            path, explored = a_star_search(self.grid, start, goal)
        else:
            raise ValueError(f"未知算法: {algorithm}")
        
        return {
            'path': path,
            'explored': explored,
            'path_length': len(path) if path else 0,
            'nodes_explored': len(explored)
        }