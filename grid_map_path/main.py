"""Gradio application for comparing grid pathfinding algorithms."""

import matplotlib

matplotlib.use("Agg")  # 使用非交互式后端，避免绘图报错

import gradio as gr

from algorithms.pathfinder import PathFinder
from utils.grid_generator import create_simple_grid, create_grid, create_maze_grid
from utils.visualization import plot_grid, plot_algorithm_comparison, fig_to_pil

# 全局变量
current_grid = create_simple_grid()
current_start = (1, 1)  # 非边界坐标，避免障碍
current_goal = (8, 8)
path_finder = PathFinder(current_grid)


def update_grid(grid_type: str, rows: int, cols: int, obstacle_density: float):
    """更新网格地图"""
    global current_grid, path_finder, current_start, current_goal

    # 根据地图类型生成栅格
    if grid_type == "简单地图":
        current_grid = create_simple_grid(rows, cols)
    elif grid_type == "随机地图":
        current_grid = create_grid(rows, cols, obstacle_density)
    elif grid_type == "迷宫地图":
        current_grid = create_maze_grid(rows, cols)

    # 调整起点和终点到有效区域
    rows_actual = len(current_grid)
    cols_actual = len(current_grid[0]) if rows_actual > 0 else 0
    current_start = (1, 1) if rows_actual > 2 and cols_actual > 2 else (0, 0)
    current_goal = (rows_actual - 2, cols_actual - 2) if rows_actual > 2 and cols_actual > 2 else (rows_actual - 1, cols_actual - 1)

    # 确保起点/终点不是障碍
    if current_grid[current_start[0]][current_start[1]] == 1:
        current_grid[current_start[0]][current_start[1]] = 0
    if current_grid[current_goal[0]][current_goal[1]] == 1:
        current_grid[current_goal[0]][current_goal[1]] = 0

    path_finder = PathFinder(current_grid)

    # 绘制更新后的网格（不显示探索区域）
    fig = plot_grid(
        current_grid,
        start=current_start,
        goal=current_goal,
        title=f"当前地图 ({rows_actual}x{cols_actual}) - 障碍：深灰色 | 起点：绿色 | 终点：红色"
    )
    return (
        fig_to_pil(fig),
        current_start[0],
        current_start[1],
        current_goal[0],
        current_goal[1],
    )


def update_start(start_row: int, start_col: int):
    """更新起点坐标"""
    global current_start, current_grid
    rows_actual = len(current_grid)
    cols_actual = len(current_grid[0]) if rows_actual > 0 else 0

    # 校验坐标有效性
    current_start = (
        max(0, min(int(start_row), rows_actual - 1)),
        max(0, min(int(start_col), cols_actual - 1))
    )
    # 确保起点不是障碍
    if current_grid[current_start[0]][current_start[1]] == 1:
        current_grid[current_start[0]][current_start[1]] = 0

    # 重新绘制地图
    fig = plot_grid(
        current_grid,
        start=current_start,
        goal=current_goal,
        title=f"更新起点后的地图 - 新起点：{current_start}"
    )
    return fig_to_pil(fig)


def update_goal(goal_row: int, goal_col: int):
    """更新终点坐标"""
    global current_goal, current_grid
    rows_actual = len(current_grid)
    cols_actual = len(current_grid[0]) if rows_actual > 0 else 0

    # 校验坐标有效性
    current_goal = (
        max(0, min(int(goal_row), rows_actual - 1)),
        max(0, min(int(goal_col), cols_actual - 1))
    )
    # 确保终点不是障碍
    if current_grid[current_goal[0]][current_goal[1]] == 1:
        current_grid[current_goal[0]][current_goal[1]] = 0

    # 重新绘制地图
    fig = plot_grid(
        current_grid,
        start=current_start,
        goal=current_goal,
        title=f"更新终点后的地图 - 新终点：{current_goal}"
    )
    return fig_to_pil(fig)


def run_algorithm(algorithm: str):
    """运行单个算法并返回可视化结果（优化：传递探索区域参数）"""
    global current_grid, current_start, current_goal, path_finder

    # 只运行当前选择的算法
    result = path_finder.get_algorithm_result(algorithm, current_start, current_goal)
    path = result.get('path', [])
    explored = result.get('explored', set())  # 获取探索区域

    # 绘制算法结果（传入探索区域参数）
    fig = plot_grid(
        current_grid,
        path=path,
        explored=explored,  # 新增：显示探索区域
        start=current_start,
        goal=current_goal,
        title=f"{algorithm}算法结果 - 探索区域：浅蓝色 | 路径：红色实线"
    )

    # 优化结果文本（更清晰的格式，区分成功/失败）
    if path:
        performance_text = f"✅ {algorithm}算法运行成功！\n\n"
        performance_text += f"📊 性能指标：\n"
        performance_text += f"- 路径长度：{result['path_length']} 步\n"
        performance_text += f"- 探索节点数：{result['nodes_explored']} 个\n"
        performance_text += f"- 运行时间：{result.get('time', 0):.6f} 秒\n\n"
        performance_text += f"🗺️ 路径详情：\n起点 {current_start} → 终点 {current_goal}\n"
        performance_text += f"前5个坐标：{path[:5]}...（共{len(path) - 1}步）" if len(path) > 5 else f"完整路径：{path}（共{len(path) - 1}步）"
    else:
        performance_text = f"❌ {algorithm}算法未找到有效路径！\n\n"
        performance_text += f"📊 运行详情：\n"
        performance_text += f"- 探索节点数：{result['nodes_explored']} 个\n"
        performance_text += f"- 运行时间：{result.get('time', 0):.6f} 秒\n"
        performance_text += f"原因：起点和终点之间被障碍完全阻隔"

    return fig_to_pil(fig), performance_text


def run_all_algorithms():
    """运行所有算法并生成对比图（优化：使用优化后的对比图）"""
    global current_grid, current_start, current_goal, path_finder

    all_results = path_finder.run_all_algorithms(current_start, current_goal)
    # 绘制优化后的对比图
    compare_fig = plot_algorithm_comparison(all_results)

    # 优化汇总文本（分点清晰，突出关键信息）
    summary_text = "📋 所有算法性能汇总\n"
    summary_text += "="*50 + "\n"
    for algo, res in all_results.items():
        found = "✅ 找到路径" if res['path'] else "❌ 未找到路径"
        summary_text += f"\n{algo}算法：\n"
        summary_text += f"  - 状态：{found}\n"
        summary_text += f"  - 路径长度：{res['path_length']} 步\n"
        summary_text += f"  - 探索节点：{res['nodes_explored']} 个\n"
        summary_text += f"  - 运行耗时：{res['time']:.6f} 秒\n"
        summary_text += f"  - 算法特点：{'保证最短路径，搜索范围大' if algo == 'BFS' else '可能快速找到路径，不保证最短' if algo == 'DFS' else '智能引导，高效找到最短路径'}\n"

    # 添加最优算法推荐（增强实用性）
    valid_results = [r for r in all_results.values() if r['path']]
    if valid_results:
        best_path = min(valid_results, key=lambda x: x['path_length'])
        best_time = min(valid_results, key=lambda x: x['time'])
        best_nodes = min(valid_results, key=lambda x: x['nodes_explored'])
        summary_text += "\n" + "="*50 + "\n"
        summary_text += "🏆 最优算法推荐：\n"
        summary_text += f"  - 最短路径：{[k for k, v in all_results.items() if v == best_path][0]}（{best_path['path_length']}步）\n"
        summary_text += f"  - 最快速度：{[k for k, v in all_results.items() if v == best_time][0]}（{best_time['time']:.6f}秒）\n"
        summary_text += f"  - 最高效率：{[k for k, v in all_results.items() if v == best_nodes][0]}（探索{best_nodes['nodes_explored']}个节点）\n"

    return fig_to_pil(compare_fig), summary_text


# 构建Gradio界面（优化：放大文本框，调整布局）
with gr.Blocks(title="路径规划算法对比演示系统", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🗺️ 路径规划算法对比演示系统")
    gr.Markdown("《人工智能导论》课程设计 - BFS/DFS/A* 搜索算法可视化（优化版）")
    gr.Markdown("🔍 优化功能：探索区域显示 | 结果文本框放大 | 对比图增强")

    with gr.Row():
        # 左侧：参数设置（保持原有功能，仅调整布局文字）
        with gr.Column(scale=1):
            gr.Markdown("### 📌 地图设置")
            grid_type = gr.Radio(["简单地图", "随机地图", "迷宫地图"], label="选择地图类型", value="简单地图")
            rows = gr.Slider(5, 20, value=10, label="行数", step=1)
            cols = gr.Slider(5, 20, value=10, label="列数", step=1)
            obstacle_density = gr.Slider(0.1, 0.4, value=0.2, label="障碍物密度（仅随机地图）")
            update_grid_btn = gr.Button("更新地图", variant="primary")

            gr.Markdown("### 📍 起点/终点设置")
            start_row = gr.Number(value=1, label="起点行", precision=0)
            start_col = gr.Number(value=1, label="起点列", precision=0)
            update_start_btn = gr.Button("更新起点")

            goal_row = gr.Number(value=8, label="终点行", precision=0)
            goal_col = gr.Number(value=8, label="终点列", precision=0)
            update_goal_btn = gr.Button("更新终点")

            gr.Markdown("### ⚙️ 算法运行")
            algorithm = gr.Radio(["BFS", "DFS", "A*"], label="选择算法", value="BFS")
            run_algo_btn = gr.Button("运行单个算法", variant="primary")
            run_all_btn = gr.Button("运行所有算法", variant="secondary")

        # 右侧：可视化结果（核心优化：放大文本框）
        with gr.Column(scale=3):  # 增大右侧占比，给文本框更多空间
            gr.Markdown("### 📊 可视化结果")
            # 优化图片显示：增大高度，支持缩放
            result_img = gr.Image(label="地图/路径/探索区域", height=500, type="pil")
            # 优化文本框：放大高度（15行），支持自动换行，显示更多内容
            result_text = gr.Textbox(
                label="算法结果/性能汇总",
                lines=15,  # 关键：从默认3行改为15行，解决显示不全问题
                max_lines=30,
                interactive=False,
                placeholder="运行算法后显示结果...",
                elem_id="result-text"
            )

    # 绑定事件（保持原有逻辑不变）
    update_grid_btn.click(
        update_grid,
        inputs=[grid_type, rows, cols, obstacle_density],
        outputs=[result_img, start_row, start_col, goal_row, goal_col]
    )
    update_start_btn.click(
        update_start,
        inputs=[start_row, start_col],
        outputs=[result_img]
    )
    update_goal_btn.click(
        update_goal,
        inputs=[goal_row, goal_col],
        outputs=[result_img]
    )
    run_algo_btn.click(
        run_algorithm,
        inputs=[algorithm],
        outputs=[result_img, result_text]
    )
    run_all_btn.click(
        run_all_algorithms,
        inputs=[],
        outputs=[result_img, result_text]
    )

    # 初始化显示（适配优化后的plot_grid）
    demo.load(
        lambda: fig_to_pil(plot_grid(
            current_grid,
            start=current_start,
            goal=current_goal,
            title="初始地图 (10x10) - 障碍：深灰色 | 起点：绿色 | 终点：红色"
        )),
        inputs=[],
        outputs=[result_img]
    )


if __name__ == "__main__":
    demo.launch(server_port=7860, inbrowser=True)
