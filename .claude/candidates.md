# CLAUDE.md 候选条目

> 以下条目由 AI 自动收集，等待人工 review。
> 触发 review：对 AI 说 "review claude" 或 "更新宪法"

## 待确认（待 review）
- Pipeline 视频帧输入依赖 opencv-python-headless, numpy, wcwidth，需在环境安装中注明
- 运行视频帧实验前需下载 VSI-Bench 视频到 ~/.cache/huggingface/vsibench/{dataset}/{scene}.mp4
- max_tokens 已提升至 4000（多模态推理），文本模式实验需注意 token 成本差异
- VSI-Bench 视频路径需确认 huggingface 下载结构（scene_name 在样本中，dataset 需从 sample['dataset'] 读取）

## 已驳回
（暂无）

## 已采纳（已写入 CLAUDE.md）
（暂无）
