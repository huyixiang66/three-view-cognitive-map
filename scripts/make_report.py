"""Generate report.ipynb with both visualizer examples."""
import json, os, sys

nb = {
    'cells': [],
    'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'}},
    'nbformat': 4,
    'nbformat_minor': 5,
}

def md(source):
    nb['cells'].append({
        'cell_type': 'markdown', 'metadata': {},
        'source': source if isinstance(source, list) else [source]
    })

def code(source):
    nb['cells'].append({
        'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [],
        'source': source if isinstance(source, list) else [source]
    })

sample_json = json.dumps({
    "front": {"gridSize": 10, "objects": [
        {"x": 0, "z": 0, "name": "door", "size": [1, 2]},
        {"x": 3, "z": 1, "name": "table", "size": [3, 1]},
        {"x": 5, "z": 1, "name": "chair", "size": [1, 1]},
        {"x": 3, "z": 4, "name": "bookshelf", "size": [1, 3]},
        {"x": 7, "z": 2, "name": "microwave", "size": [2, 1]},
    ]},
    "top": {"gridSize": 10, "objects": [
        {"x": 0, "y": 0, "name": "door", "size": [1, 1]},
        {"x": 3, "y": 2, "name": "table", "size": [3, 2]},
        {"x": 5, "y": 2, "name": "chair", "size": [1, 1]},
        {"x": 3, "y": 5, "name": "bookshelf", "size": [1, 1]},
        {"x": 7, "y": 2, "name": "microwave", "size": [2, 1]},
    ]},
    "side": {"gridSize": 10, "objects": [
        {"y": 0, "z": 0, "name": "door", "size": [1, 2]},
        {"y": 2, "z": 1, "name": "table", "size": [2, 1]},
        {"y": 2, "z": 1, "name": "chair", "size": [1, 1]},
        {"y": 5, "z": 4, "name": "bookshelf", "size": [1, 3]},
        {"y": 2, "z": 2, "name": "microwave", "size": [1, 1]},
    ]},
}, indent=2)

# === Title ===
md("# Three-View Cognitive Map — 项目进度汇报\n---")

# === Project Intro ===
md([
    "## 一、项目简介\n",
    "**目标：** 将 Thinking-in-Space 的 1D 认知图扩展到正交三视图（Top / Front / Side），并输出物体位置与尺寸，在 **VSI-Bench** 空间推理基准上评测。\n\n",
    "**VSI-Bench：** 多模态空间推理数据集，5000+ 问答对，5 种问题类型（绝对距离、相对距离、三档方向难度），场景来自 ScanNet / ScanNet++ / ARKitScenes。\n\n",
    "**核心思路：** VLM 看完视频后，通过 3-pass 逐步构建三视图认知图（俯视图→正视图→侧视图），再基于 cogmap 回答空间问题。\n",
])

# === Tech Evolution ===
md([
    "## 二、技术路线演进\n\n",
    "### Phase 1：文本模式（Wellapi）\n",
    "- 只传场景名字符串给模型，模型靠先验知识猜房间布局\n\n",
    "### Phase 2：5 帧视频帧（Wellapi）\n",
    "- opencv 均匀采样 5 帧，JPEG base64，通过 image_url 传给模型\n",
    "- 准确率 38.0%\n\n",
    "### Phase 3：完整视频（新网关 + Gemini 原生）\n",
    "- 导师搭建的统一 API 网关，video_url 直接传完整视频\n",
    "- Gemini 原生端点处理视频，保留全部时序\n",
    "- 跑通 4 组对比实验，最佳 44.9%\n",
])

# === Results ===
md([
    "## 三、实验结果\n\n",
    "| 实验 | 总准确率 | 绝对距离 | 相对距离 | 方向 Easy | 方向 Medium | 方向 Hard |\n",
    "|------|:--------:|:--------:|:--------:|:--------:|:----------:|:--------:|\n",
    "| **3-pass shared** | **44.9%** | 0% | **60%** | **86%** | **50%** | **42%** |\n",
    "| direct（无建图）| 36.0% | 0% | 50% | 43% | 45% | 42% |\n",
    "| 3-pass noshared | 22.0% | 0% | 30% | 14% | 36% | 25% |\n",
    "| 3-pass shared+viz | 26.0% | 0% | 30% | 57% | 36% | 17% |\n| **3-pass noshared_video** | **32.0%** | 0% | **70%** | 14% | 36% | 33% |\n\n",
    "**关键发现：**\n",
    "- 完整视频优于 5 帧（44.9% vs 38.0%），时序信息有帮助\n",
    "- cogmap 建图有价值（44.9% vs direct 36.0%），方向 Easy 翻倍\n",
    "- 绝对距离全线 0/10，模型无法精确估计米数\n",
    "- 可视化网格图反而有害（44.9% -> 26.0%），信息密度低、token 噪声大\n- 对话记忆贡献约 +13%（shared 44.9% vs noshared_video 32.0%），方向类问题尤其依赖对话历史\n- rel_distance 在新会话中反而提升（60% -> 70%），无历史干扰时纯计算更准\n",
])

# === My Work ===
md([
    "## 四、我的工作\n\n",
    "**1. Visualizer 开发。** 写了一个脚本，把模型输出的三视图 JSON 解析成网格坐标，用 emoji 在终端里画出三张可视化图（俯视、正视、侧视）。后来做了升级：size 字段真实占用多个格子，缺 emoji 的物体显示全称文本。\n\n",
    "**2. Prompt 设计与数据集整理。** 设计了 3-pass prompt 模板，要求输出物体的 size 信息。从 VSI-Bench 的 8 类中选了 3 类，筛选 50 条样本。\n\n",
    "**3. 三视图建图 pipeline。** 以第一帧作为 x 轴锚点，分 3 次 prompt 逐步建图，支持 shared / noshared memory 两种模式。\n\n",
    "**4. 演示终端版 visualizer 给导师。** 导师建议用 matplotlib 画图片版，emoji 按 size 调整大小，与文本版做对比。\n",
])

# === Visualizer Demo ===
md([
    "## 五、Visualizer 对比示例\n\n",
    "同一个 cogmap，分别用终端文本版和 matplotlib 图片版展示。\n",
])

code([
    'import sys, os, json\n',
    'sys.path.insert(0, os.path.abspath(".."))\n',
    'from viz.grid_visualizer import visualize_three_view\n\n',
    'sample = ' + sample_json + '\n\n',
    'print(visualize_three_view(json.dumps(sample)))\n',
])

md(["### Matplotlib 图片版"])

code([
    '%matplotlib inline\n',
    'import sys, os, json\n',
    'sys.path.insert(0, os.path.abspath(".."))\n',
    'from viz.matplotlib_visualizer import ThreeViewVisualizer\n',
    'import matplotlib.pyplot as plt\n\n',
    'sample = ' + sample_json + '\n\n',
    'viz = ThreeViewVisualizer(cmap=json.dumps(sample))\n',
    'fig, axes = viz.plot()\n',
    'plt.tight_layout()\n',
    'plt.show()\n',
])

# === Follow-up ===
md([
    "## 六、后续计划\n\n",
    "1. **Matplotlib 可视化优化** — 图片版，emoji 按 size 调整大小，与文本版对比\n",
    "2. **abs_distance 策略优化** — 网格比例推算还不够精确\n",
    "3. **noshared + viz 实验补完** — 最后一组对比数据\n",
    "4. **混合输入探索** — 文本 + 视频组合（参考 VSI-Bench 论文）\n",
    "5. **emoji 库扩展** — 补全 55 种物体中的可用 emoji\n",
    "6. **飞书文档同步** — 整理实验记录给导师\n",
    "7. **代码清理** — 清理无用结果文件\n",
])

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'report.ipynb')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print(f'Done: {out_path}')
