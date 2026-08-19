# Three-View Cognitive Map — 项目指令

> 本文件由 AI 自动加载，定义项目协作规则。

## 项目概况 (Project Overview)
- **产品：** Extends Thinking-in-Space 1D CogMap to orthogonal three views (Top/Front/Side) with object size output. Built for the VSI-Bench spatial reasoning benchmark.
- **当前阶段：** 实验阶段 (Research Experiment)
- **GitHub：** https://github.com/your-org/three-view-cogmap（待确认）

## Language / 语言
- **Language:** bilingual

## 项目管理系统 (Project Management System)

日常只需要记住三个动作：

- `end session` — 保存进度和下一步
- `continue` — 下次接着干
- `status` — 查看项目现状

- **Log Compaction Threshold:** 10

### 主要触发词 (Primary Triggers)

| Intent | AI Action |
|--------|-----------|
| End session / wrap up — any expression of "we're done for now" | Save progress, refresh next steps, and record important changes |
| Continue — any expression of "pick up where we left off" | Read session-handoff.md + PROJECT.md + TODO.md + logs to recover context |
| Check status — any expression of "what's the current state" | Show compact dashboard: Project, Active Work, Recent Change, Next Best Step |

### 高级触发词 (Advanced Triggers)

| Intent | AI Action |
|--------|-----------|
| Review constitution — any expression of "check/update rules" | Show .claude/candidates.md for confirmation |
| Sync wiki — any expression of "update project overview" | Force rescan and update PROJECT.md |
| Organize files — any expression of "clean up files" | Scan and reorganize per STRUCTURE.md rules |
| Change language — any expression of "switch language" | Update language, rewrite management files |
| Continue full context — any expression of "full project review" | Full trajectory recovery across all sessions |

### 内部机制：文件职责 (File Roles)

| File | Who writes | When |
|------|-----------|------|
| CLAUDE.md | Human-confirmed | review claude trigger |
| PROJECT.md | AI auto | end session + structure changes |
| session-handoff.md | AI auto | end session |
| TODO.md | AI + Human | anytime |
| log/session-*.md | AI | end session |
| .claude/candidates.md | AI auto | when stable rules identified |
| STRUCTURE.md | AI auto | end session + file changes |
| .claude/.file-snapshot.json | AI auto | end session |
| UPDATE_LOG.md | AI auto | end session + significant updates |
| DOCS.md | AI auto | end session + document archiving |
| .claude/project-profile.json | AI auto | Foundation Setup + confirmed changes |
| .claude/profile-pending.json | AI auto | Normal Close / Full Close pending queue |

### Session Start Protocol

1. Read PROJECT.md, session-handoff.md, TODO.md, UPDATE_LOG.md, and DOCS.md if present.
2. Read .claude/project-profile.json and .claude/profile-pending.json if present.
3. Read logs (bounded): highest-level summaries + all unarchived raw logs in log/.

### Session Log Format

```
# Session YYYY-MM-DD — {topic}
## 本次目标 (Session Goal)
## 关键操作 (Key Actions)
## 决策与理由 (Decisions & Rationale)
## 产出文件 (Output Files)
## 未完事项 (Unfinished Items)
```

### TODO Format
每条任务必须包含：
```
- [ ] {task description}
  Owner: {name} | Deadline: {date} | Dependencies: {prerequisite}
```

## Coding Guidelines

### 1. Think Before Coding
State assumptions explicitly. Present multiple interpretations when ambiguous. Push back when a simpler approach exists.

### 2. Simplicity First
No features beyond what was asked. No abstractions for single-use code. Minimum code that solves the problem.

### 3. Surgical Changes
Touch only what you must. Match existing style. Remove imports/variables YOUR changes made unused.

### 4. Goal-Driven Execution
Define success criteria. Loop until verified. For multi-step tasks, state a brief plan.

## Project-Specific Rules

- VSI-Bench 实验数据在 `src/` 下，实验结果 JSON 文件命名按 `results_{model}_{n}.json` 格式
- 3-pass prompt 模板在 `prompts_3pass.py`，主 pipeline 在 `run_vsibench.py`
- Visualizer 在 `viz/` 目录下
- 这是一个研究项目，优先实验可重复性，文档用中英双语

## 核心宗旨
- 目标是地图建得好、QA 好；复杂度只是手段，不为复杂而复杂。
- 每次跑实验前必须编译 + dry-run 确认无 bug，避免重复跑。
