# Unity 熟悉计划 — 面向 VSI-Bench 空间 QA 闭环

> 2026-08-01 · 按需学习，只学闭环必需能力

## 0. 学习范围

我们的目标是：把空间表示放进 Unity，用相机位姿重走 VSI-Bench 视频路径，渲染帧与原视频对比做反馈，最终提升 QA。

因此只需要掌握：
- 场景/物体/坐标（Transform）
- 相机与渲染帧输出
- 用 JSON/C# 从 Python 驱动场景和相机
- 批处理渲染 PNG
- 坐标系与位姿转换（Unity vs OpenCV/COLMAP）

**明确不学**（除非以后需要）：光照烘焙、物理引擎/碰撞、材质贴图精修、动画、UI/UGUI、Asset Store 美术资产、游戏玩法、URP/HDRP 高级管线、网络多人。

环境现状：已装 Unity Hub + Unity 2022.3.62 LTS，尚未创建项目。

## 1. 阶段划分（约 10-14 天，每天 2-3 小时）

### 阶段 0 — 环境与最小场景（0.5-1 天）

目标：能打开 Unity，搭一个最简“房间”。

要做的事：
1. Unity Hub 新建 3D 项目（Built-in Render Pipeline，模板 3D Core）
2. 熟悉 Editor 界面：Hierarchy / Scene / Game / Inspector / Project
3. 用 Plane 当地面，Cube 当物体，Sphere 当相机观察点，搭一个简单房间
4. 只保留默认 Directional Light，不改光照

验证标准：
- 能保存 scene 并重新打开
- 能拖动物体改 Transform 的 Position / Rotation / Scale
- Game 视图能显示房间画面

### 阶段 1 — 核心概念：坐标、物体、相机（1-2 天）

目标：理解 Unity 里“空间”和“相机位姿”是怎么表示的。

要做的事：
1. GameObject 与 Transform：世界坐标、父子关系、Position/Rotation/Scale
2. Camera 组件：Position / Rotation / FOV / Aspect / Near / Far，正交 vs 透视
3. Scene 与 Prefab：场景文件怎么存物体，Prefab 怎么复用模板
4. 坐标系转换：Unity 是左手系 Y-up；OpenCV/COLMAP 是右手系 Z-forward，写一个坐标转换工具函数
5. 读一下 VSI-Bench/ScanNet 的相机位姿格式，确认它是 world-to-camera 还是 camera-to-world

验证标准：
- 能口头/文字解释 Unity 左手系和 OpenCV 右手系的差异
- 能把一个相机位姿从数据集格式转换后放进 Unity，画面朝向与预期一致
- 能用 Console 打印相机世界位置和朝向

### 阶段 2 — 用代码控制场景与相机（2-3 天）

目标：从 JSON 自动建场景和设位姿，不再手拖。

要做的事：
1. C# 基础：MonoBehaviour、Start/Update、读 JSON（JsonUtility 或 Newtonsoft）
2. 输入 scene.json：物体列表（name, position, rotation, scale, color）→ 生成 GameObject
3. 输入 camera.json：每帧 position / rotation / fov → 设置 Camera
4. 对齐投影矩阵：Unity Camera 投影与 OpenCV 内参/图像分辨率的对应关系
5. 建一个最小工具脚本：读 JSON → 建场景 → 设相机 → 渲染一张图

验证标准：
- Python 写 scene.json，Unity 读入后物体位置/尺寸和 JSON 完全一致
- 同一相机位姿，Unity 渲染画面中的物体 2D 位置和手工投影计算结果一致

### 阶段 3 — 批处理渲染（2-3 天）

目标：命令行一键渲染一个视频路径的所有帧。

要做的事：
1. Unity Editor 批处理模式：`Unity -batchmode -projectPath <proj> -executeMethod RenderFrames.Render -quit`
2. 用 RenderTexture + Texture2D 导出 PNG，文件名带 frame index
3. 按时间戳/帧率从 VSI-Bench 视频抽帧，和 Unity 渲染帧一一对应
4. 连续位姿路径渲染：验证画面平滑无跳变

验证标准：
- 输入 N 个位姿，输出 N 张 PNG
- 渲染帧命名、数量、顺序正确
- 同一台机器上跑一遍完整路径耗时可接受（先不管性能优化）

### 阶段 4 — Python 闭环集成（2-3 天）

目标：让 Python 驱动 Unity，把渲染帧和原视频帧放一起对比。

要做的事：
1. Python 生成输入 JSON → 调 Unity 批处理 → 读回 PNG
2. 渲染帧 vs 原视频帧对比：先 SSIM / 简单可视化，后续可加 LPIPS
3. 坐标一致性检查：已知物体在渲染帧和真实帧里的 2D 投影位置应接近
4. 迭代接口：v1 手工改 layout JSON 再渲染；v2 再考虑自动反馈

验证标准：
- 1 个 VSI-Bench 场景跑通“视频 → 场景 JSON → Unity 渲染 → 对比 → 修改 → 再渲染”
- 能保存一组对比图（原帧/渲染帧/叠加）供人工检查

### 阶段 5 — 接回 VSI-Bench QA（1-2 天）

目标：Unity 表示进入 QA 评测链路。

要做的事：
1. 把渲染帧或场景信息接回 run_vsibench 风格的 pipeline
2. 跑 1 个 QA 样本，记录“Unity 表示版本”作为输入
3. 和三视图基线结果对比，确认指标可记录可复现

验证标准：
- VSI-Bench 评测能跑通，结果 JSON 含 Unity 表示版本字段
- 至少 1 个样本有渲染帧 + 原帧 + 答案 + 评测分数

## 2. 技能与闭环步骤对应表

| Unity 技能 | 对应闭环环节 |
|---|---|
| Transform/场景搭建 | [1] 构建 Unity 空间表示 |
| 相机位姿/投影矩阵 | [2] 恢复相机位姿、[3] 重放路径 |
| 批处理渲染 PNG | [3] 渲染观测帧 |
| JSON 驱动 + Python 调用 | [1][3] 自动化闭环 |
| 坐标转换 | [2][4] 位姿对齐、渲染对比 |

## 3. 常见坑（先记住）

1. Unity 是左手系 Y-up；OpenCV/COLMAP 位姿一般右手系，直接塞进 Unity 会左右镜像或翻转
2. Unity 相机看向 +Z，模型坐标和数据集坐标的轴向不一定相同，先写转换函数再做渲染
3. FOV 分垂直/水平，和 VSI-Bench 相机内参（fx/fy, width/height）对应时要换算
4. 默认场景有雾、环境光等，可能让画面和真实视频差异变大，可以关掉或调低
5. 批处理模式没有编辑器界面，脚本里要处理 Application.isBatchMode 和退出码

## 4. 最小脚本骨架（阶段 3 用）

```csharp
// RenderFrames.cs — Editor 菜单或 -executeMethod 调用
using UnityEngine;
using System.IO;

public static class RenderFrames
{
    public static void Render()
    {
        var cam = GameObject.Find("Main Camera").GetComponent<Camera>();
        var frames = LoadFrames(Path.Combine(Application.dataPath, "../input/camera.json"));
        for (int i = 0; i < frames.Length; i++)
        {
            cam.transform.position = frames[i].position;
            cam.transform.rotation = frames[i].rotation;
            cam.Render();
            SavePng(cam, Path.Combine(Application.dataPath, "../output", "frame_" + i.ToString("D4") + ".png"));
        }
    }
}
```

对应批处理命令：

```bash
"C:/Program Files/Unity/Hub/Editor/2022.3.62f3c1/Editor/Unity.exe" \
  -batchmode -projectPath C:/path/to/unity-project \
  -executeMethod RenderFrames.Render -quit
```

## 5. 完成标准

阶段 0-4 全部通过后，说明 Unity 熟练度已经足够支撑闭环：
1. 能独立把一个 VSI-Bench 场景的视频路径重放进 Unity 并出渲染帧
2. 能解释并处理坐标系/位姿/投影的转换
3. 能用 Python 驱动 Unity 做“改表示 → 重渲染 → 对比”的循环

更高级的 Unity 技能（物理、光照、动画）等真正需要时再学，不提前投入。
