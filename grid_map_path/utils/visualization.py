"""
路径规划结果可视化模块
提供栅格绘制、算法对比绘图、图片转换功能
优化：1.显示探索区域 2.优化对比图样式
"""
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from PIL import Image
from typing import List, Dict, Any, Tuple, Set, Optional

# Prefer a Chinese-capable font where one is installed, with common OS fallbacks.
plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei",
    "SimHei",
    "PingFang SC",
    "Hiragino Sans GB",
    "Noto Sans CJK SC",
    "WenQuanYi Zen Hei",
    "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False


def plot_grid(
    grid: List[List[int]],
    path: List[Tuple[int, int]] = None,
    start: Tuple[int, int] = None,
    goal: Tuple[int, int] = None,
    explored: Set[Tuple[int, int]] = None,  # 新增：探索区域参数
    title: str = "Grid Map"
) -> plt.Figure:
    """
    优化后：支持显示探索区域
    - 障碍：深灰色
    - 探索区域：浅蓝色半透明
    - 路径：红色实线
    - 起点：绿色圆点
    - 终点：红色圆点
    """
    grid_np = np.array(grid)
    fig, ax = plt.subplots(figsize=(10, 10))  # 增大画布尺寸

    # 绘制栅格背景（障碍：深灰色）
    ax.imshow(grid_np, cmap="gray_r", alpha=0.3)

    # 绘制探索区域（浅蓝色半透明）
    if explored and len(explored) > 0:
        explored_np = np.zeros_like(grid_np)
        for (r, c) in explored:
            if 0 <= r < len(grid_np) and 0 <= c < len(grid_np[0]):
                explored_np[r, c] = 1
        ax.imshow(explored_np, cmap="Blues", alpha=0.4)  # 半透明叠加，不遮挡其他元素

    # 绘制路径（红色粗线，层级最上层）
    if path and len(path) > 0:
        path_np = np.array(path)
        ax.plot(path_np[:, 1], path_np[:, 0], "r-", linewidth=3, label="Path", zorder=5)

    # 绘制起点（绿色大圆点，带边框）
    if start:
        ax.scatter(start[1], start[0], c="#2ecc71", s=150, edgecolors="black", linewidth=2, label="Start", zorder=6)

    # 绘制终点（红色大圆点，带边框）
    if goal:
        ax.scatter(goal[1], goal[0], c="#e74c3c", s=150, edgecolors="black", linewidth=2, label="Goal", zorder=6)

    # 优化标题和图例
    ax.set_title(title, fontsize=16, fontweight="bold", pad=20)
    ax.legend(loc="upper right", fontsize=14, framealpha=0.9)
    ax.axis("off")
    plt.tight_layout()
    return fig


def plot_algorithm_comparison(results: Dict[str, Dict[str, Any]]) -> plt.Figure:
    """
    优化后多算法对比图：
    1. 增加数据标签显示
    2. 优化颜色搭配和图表样式
    3. 调整布局，提升可读性
    """
    algorithms = list(results.keys())
    path_lengths = [results[algo]["path_length"] for algo in algorithms]
    nodes_explored = [results[algo]["nodes_explored"] for algo in algorithms]
    times = [results[algo]["time"] * 1000 for algo in algorithms]  # 转换为毫秒，更易读

    # 优化颜色方案（专业配色，区分度高）
    colors = ["#3498db", "#e67e22", "#27ae60"]  # 蓝（BFS）、橙（DFS）、绿（A*）
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))  # 增大图表尺寸，避免拥挤

    # 1. 路径长度对比（添加数值标签）
    bars1 = ax1.bar(algorithms, path_lengths, color=colors, alpha=0.8, edgecolor="black", linewidth=1)
    ax1.set_title("Path Length Comparison", fontsize=14, fontweight="bold")
    ax1.set_ylabel("Path Length", fontsize=12)
    ax1.grid(axis="y", alpha=0.3)  # 添加横向网格线，便于对比
    # 为每个柱子添加数值标签
    for bar, val in zip(bars1, path_lengths):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f"{val}", ha="center", va="bottom", fontsize=11, fontweight="bold")

    # 2. 探索节点数对比（添加数值标签）
    bars2 = ax2.bar(algorithms, nodes_explored, color=colors, alpha=0.8, edgecolor="black", linewidth=1)
    ax2.set_title("Nodes Explored Comparison", fontsize=14, fontweight="bold")
    ax2.set_ylabel("Number of Nodes", fontsize=12)
    ax2.grid(axis="y", alpha=0.3)
    # 为每个柱子添加数值标签
    for bar, val in zip(bars2, nodes_explored):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f"{val}", ha="center", va="bottom", fontsize=11, fontweight="bold")

    # 3. 运行时间对比（添加数值标签，保留1位小数）
    bars3 = ax3.bar(algorithms, times, color=colors, alpha=0.8, edgecolor="black", linewidth=1)
    ax3.set_title("Running Time Comparison (ms)", fontsize=14, fontweight="bold")
    ax3.set_ylabel("Time (ms)", fontsize=12)
    ax3.grid(axis="y", alpha=0.3)
    # 为每个柱子添加数值标签
    for bar, val in zip(bars3, times):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f"{val:.1f}", ha="center", va="bottom", fontsize=11, fontweight="bold")

    # 整体样式优化：添加总标题，调整布局
    plt.suptitle("Algorithm Performance Comparison", fontsize=16, fontweight="bold", y=0.98)
    plt.tight_layout()
    return fig


def fig_to_pil(fig: plt.Figure) -> Image.Image:
    """将matplotlib的Figure对象转换为PIL.Image对象（适配新版Gradio，提高清晰度）"""
    buffer = BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight", dpi=120)  # 提高DPI，图片更清晰
    buffer.seek(0)
    img = Image.open(buffer)
    plt.close(fig)  # 关闭画布释放资源，避免内存泄漏
    return img