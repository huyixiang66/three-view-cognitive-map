# Three-View Cognitive Map — 文件管理结构 (File Management Structure)

> 最后更新：2026-07-21

## 项目类型 (Project Type)
AI Research — VSI-Bench spatial reasoning with multi-view cognitive maps

## 排除规则 (Exclusion Rules)
以下目录/文件不参与整理：
- .git/
- __pycache__/
- .venv/
- .claude/
- docs/
- log/

## 目录规则 (Directory Rules)

| 路径 | 用途 | 匹配条件 | 命名规范 | 优先级 |
|------|------|----------|----------|--------|
| src/ | Python 源代码 | *.py, *.json | snake_case | 1 |
| viz/ | 可视化工具 | *visualizer*.py, *.png | snake_case | 2 |
| scripts/ | 辅助工具脚本 | *.py | snake_case | 3 |
| docs/ | 文档输出 | *.md, *.pdf | 中英均可 | 4 |
| root 结果文件 | 实验结果 JSON | results_*.json | results_{model}_{n}.json | 5 |

## 待分类 (Unclassified)
- （暂无）

## 整理历史 (Organization History)
| 日期 | 操作 | 文件数 |
|------|------|--------|
| 2026-07-21 | 初始化结构 | 0 |
