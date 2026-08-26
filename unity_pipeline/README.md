# Unity Pipeline: 视频 → 三视图 → Unity → V'

这条目录提供从模型三视图到 Unity 场景、再到 V' 帧的可复现脚本。

```text
video
  └─> VGGT poses (.npz)
  └─> model three-view (run_tis_compare.py / run_vsibench.py)
three-view JSON
  └─> scene_3d.json (fuse + yaw)
scene_3d.json + camera JSON
  └─> Unity scene / V' frames
```

## 文件

```text
fuse_views_to_3d.py          三视图 -> 扁平 3D scene JSON
extract_cogmap_from_result.py 从 result JSON 抽标准三视图（含 yaw）
build_scene_3d.py             合成 scene_3d.json 并保留 yaw
align_vggt_cameras.py         VGGT npz -> Unity 相机 JSON（正交 + upright）
vggt_vs_gt.py                 位姿对齐辅助函数（fit floor / umeyama）
examples/gt_polygons.json     scene0353_00 的房间多边形示例
Unity/CogMapSceneBuilder.cs   Unity 场景构建组件
Unity/Editor/CogMapBatchBuilder.cs
Unity/Editor/CogMapVGGTRenderer.cs
Unity/Editor/CogMapSceneWithCameras.cs
build_unity_scene_win.ps1     Windows 批量构建/渲染入口
```

## 示例：scene0353_00

### 1. 三视图

项目已有 `results_task1_3pass.json` 时直接抽取：

```bash
python unity_pipeline/extract_cogmap_from_result.py \
  results_task1_3pass.json scene0353_00 cogmap_yaw.json

python unity_pipeline/build_scene_3d.py \
  cogmap_yaw.json scene_3d.json
```

也可以先用 `src/run_tis_compare.py --arm threeview_3pass` 生成 result，再执行上面两步。

### 2. VGGT 相机

需要先准备 VGGT 源码和权重，然后运行仓库里已有的提取脚本：

```bash
python src/vggt_poses.py video.mp4 vggt.npz --frames 8
```

再把 VGGT 相机对齐到 cogmap 网格：

```bash
python unity_pipeline/align_vggt_cameras.py \
  vggt.npz scene0353_00 cameras.json --fixed-k
```

`--fixed-k` 使用 `fy=1.1*H` 的稳定近似内参，避免直接使用 VGGT 不稳定的 K。

### 3. Unity

把 `unity_pipeline/Unity/` 下文件复制到 Unity 工程：

```text
Assets/CogMapSceneBuilder.cs
Assets/Editor/CogMapBatchBuilder.cs
Assets/Editor/CogMapVGGTRenderer.cs
Assets/Editor/CogMapSceneWithCameras.cs
```

Windows 批处理：

```powershell
# 只建场景（cellSize 默认 0.5，米制场景传 -cellSize 1）
Unity.exe -batchmode -quit -projectPath YOUR_PROJECT \
  -executeMethod CogMapBatchBuilder.Build \
  -cogmapJson scene_3d.json \
  -outputScene Assets/Scenes/CogMapScene_Grid.unity \
  -logFile build.log

# 渲染 V'
Unity.exe -batchmode -quit -projectPath YOUR_PROJECT \
  -executeMethod CogMapVGGTRenderer.Render \
  -sceneJson scene_3d.json \
  -camerasJson cameras.json \
  -outDir vprime_frames \
  -logFile render.log
```

也可以直接使用 `build_unity_scene_win.ps1`，它封装了 fuse/build/render 三步。

## 口径说明

- 当前模型场景默认使用**带 yaw 的三视图**。
- cogmap 的 `front/side z` 是物体中心高度，fusion 使用 `z_anchor=center`。
- Unity 场景中落地类物体贴地，window/mirror 等挂墙类保持高度。
- VGGT 相机验证仍在进行中，V' 暂时适合流程联调和人工对比，不适合作为最终像素级评测指标。
