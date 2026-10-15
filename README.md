# Grid Map Path

网格地图路径规划算法演示项目，使用 Gradio 和 Matplotlib 可视化比较 BFS、DFS 与 A*。可生成简单地图、随机障碍地图和迷宫地图，设置起点/终点，并查看路径、搜索区域和运行指标。

## 功能

- BFS、DFS、A* 三种四邻域寻路算法
- 简单、随机和迷宫地图生成
- 起点、终点和地图尺寸交互设置
- 路径、探索节点和算法指标可视化

## 环境要求

- Python 3.11 或更高版本
- Windows 可选用 `grid_map_path/start_windows.bat` 启动

## 安装与运行

在仓库根目录执行：

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r grid_map_path/requirements.txt
python grid_map_path/main.py
```

启动后访问 <http://127.0.0.1:7860>。关闭运行程序的终端即可停止服务。详细操作方法见[使用说明](docs/使用说明.md)。

Windows 用户也可以双击 `grid_map_path/start_windows.bat`；脚本使用当前 Python 环境，并从脚本所在目录启动，不依赖个人电脑上的固定路径。

## 项目结构

```text
.
├── README.md
├── .gitignore
└── grid_map_path/
    ├── main.py
    ├── requirements.txt
    ├── start_windows.bat
    ├── algorithms/
    │   ├── __init__.py
    │   ├── bfs.py
    │   ├── dfs.py
    │   ├── a_star.py
    │   └── pathfinder.py
    └── utils/
        ├── grid_generator.py
        └── visualization.py
```

## 算法说明

地图采用四方向移动，每步代价为 1。BFS 和 A* 在该设定下可找到最短路径；DFS 找到可行路径，但不保证最短。探索节点数按算法实际展开的节点计数，包含起点，不包含仅被发现而尚未展开的节点。
