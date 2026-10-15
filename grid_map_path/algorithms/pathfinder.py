"""Run and compare the grid pathfinding algorithms."""

from time import perf_counter
from typing import Any, Dict, List, Tuple

from .a_star import a_star_search
from .bfs import bfs_search
from .dfs import dfs_search

Coordinate = Tuple[int, int]
SearchResult = Dict[str, Any]


class PathFinder:
    """Run BFS, DFS, and A* against one grid and collect comparable metrics."""

    _algorithms = {
        "BFS": bfs_search,
        "DFS": dfs_search,
        "A*": a_star_search,
    }

    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.results: Dict[str, SearchResult] = {}

    @staticmethod
    def _run(search, grid, start, goal) -> SearchResult:
        started = perf_counter()
        path, explored = search(grid, start, goal)
        elapsed = perf_counter() - started
        return {
            "path": path,
            "explored": explored,
            "time": elapsed,
            "path_length": len(path) - 1 if path else 0,
            "nodes_explored": len(explored),
        }

    def run_all_algorithms(
        self, start: Coordinate, goal: Coordinate
    ) -> Dict[str, SearchResult]:
        """Run all algorithms and return their paths and performance metrics."""
        self.results = {
            name: self._run(search, self.grid, start, goal)
            for name, search in self._algorithms.items()
        }
        return self.results

    def get_comparison_table(self) -> List[List[str]]:
        """Return a text table for the latest algorithm comparison."""
        if not self.results:
            return []

        table = [["算法", "是否找到路径", "路径长度", "探索节点数", "运行时间(秒)", "特点"]]
        features = {
            "BFS": "保证最短路径，搜索范围可能较大",
            "DFS": "找到可行路径，但不保证最短",
            "A*": "启发式搜索，可找到最短路径",
        }
        for name, result in self.results.items():
            table.append([
                name,
                "是" if result["path"] else "否",
                str(result["path_length"]),
                str(result["nodes_explored"]),
                f"{result['time']:.6f}",
                features[name],
            ])
        return table

    def get_algorithm_result(
        self, algorithm: str, start: Coordinate, goal: Coordinate
    ) -> SearchResult:
        """Run one algorithm and return its path and performance metrics."""
        name = algorithm.strip().upper()
        if name == "ASTAR":
            name = "A*"
        try:
            search = self._algorithms[name]
        except KeyError as exc:
            raise ValueError(f"未知算法: {algorithm}") from exc
        return self._run(search, self.grid, start, goal)
