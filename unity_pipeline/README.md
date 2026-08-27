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
run_lingbot_map.py            LingBot-Map 推理：帧 -> pose/depth npz
align_lingbot_map_cameras.py  LingBot npz -> Unity 相机 JSON（含 depth 回退）
vggt_vs_gt.py                 位姿对齐辅助函数（fit floor / umeyama）
examples/gt_polygons.json     scene0353_00 的房间多边形示例
Unity/CogMapSceneBuilder.cs   Unity 场景构建组件
Unity/Editor/CogMapBatchBuilder.cs
Unity/Editor/CogMapVGGTRenderer.cs
Unity/Editor/CogMapSceneWithCameras.cs
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

### LingBot-Map 相机（替代 VGGT）

先 clone [robbyant/lingbot-map](https://github.com/robbyant/lingbot-map)，下载 `lingbot-map.pt`（约 4.6GB），然后：

```bash
python unity_pipeline/run_lingbot_map.py \
  --model_path lingbot-map.pt \
  --image_folder frames_dir \
  --out lingbot_out \
  --lingbot_root /path/to/lingbot-map \
  --num_scale_frames 2 --camera_num_iterations 1
```

对齐到 cogmap 网格，并用 `--width/--height` 输出与原视频同尺寸的相机：

```bash
python unity_pipeline/align_lingbot_map_cameras.py \
  lingbot_out/predictions.npz scene0353_00 lingbot_cameras.json \
  --width 640 --height 480
```

若原视频存在回环同视角帧，可加 `--loop-pairs 0=7,1=4` 把对应相机中心取平均、朝向保持不变。

若 depth 点云对齐明显不对（相机贴地、朝向偏 90°），可先用 VGGT 生成一版已验证的 transform，再让 LingBot 复用：

```bash
python unity_pipeline/align_lingbot_map_cameras.py \
  lingbot_out/predictions.npz scene0353_00 lingbot_cameras.json \
  --transform-json vggt_cameras.transform.json --fixed-k --width 640 --height 480
```

`--fixed-k` 配合 `--width/--height` 时会在目标分辨率直接取 `fy=1.1*H`，避免 FOV 被缩放两次。

之后 Unity 渲染 V' 的步骤与 VGGT 相同，把 `camerasJson` 换成 `lingbot_cameras.json`。

注意：官方 `lingbot-map.pt` 不含 `point_head` 权重，对齐脚本默认用 depth 反投影，不要依赖 `world_points`。

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


## 口径说明

- 当前模型场景默认使用**带 yaw 的三视图**。
- cogmap 的 `front/side z` 是物体中心高度，fusion 使用 `z_anchor=center`。
- Unity 场景中落地类物体贴地，window/mirror 等挂墙类保持高度。
- VGGT 相机验证仍在进行中，V' 暂时适合流程联调和人工对比，不适合作为最终像素级评测指标。
