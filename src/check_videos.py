"""Check video specs and estimate time/cost for the pipeline."""
import json, os, cv2, base64

samples = json.load(open(os.path.join(os.path.dirname(__file__), 'vsi_subset_50.json')))

total_size = 0
max_size = 0
total_frames = 0
for i, s in enumerate(samples):
    path = os.path.join(os.path.expanduser('~'), '.cache', 'huggingface', 'vsibench',
                        s['dataset'], s['scene_name'] + '.mp4')
    if not os.path.exists(path):
        print(f'{i}: {s["scene_name"]} MISSING')
        continue
    
    size_mb = os.path.getsize(path) / (1024 * 1024)
    total_size += size_mb
    max_size = max(max_size, size_mb)
    
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    dur = total / fps if fps > 0 else 0
    cap.release()
    total_frames += total
    
    b64_size_mb = os.path.getsize(path) * 4 / 3 / (1024 * 1024)
    
    if i < 3 or size_mb > 15:
        print(f'{i}: {s["dataset"]:12s} {s["scene_name"]:15s} '
              f'{size_mb:.0f}MB  base64≈{b64_size_mb:.0f}MB  '
              f'{total}帧  {dur:.0f}s  {fps:.0f}fps')

avg_size = total_size / len(samples)
print(f'\n--- Summary (all {len(samples)} samples) ---')
print(f'Average: {avg_size:.0f}MB per video')
print(f'Max:     {max_size:.0f}MB')
print(f'Total:   {total_size:.0f}MB')
print(f'Avg base64 req body: {avg_size * 4/3:.0f}MB')
print(f'Total frames: {total_frames}')

# Estimate time
print(f'\n--- Time estimate ---')
print(f'Single pass (upload + process): ~10-30s per video-dependent call')
print(f'3 passes + answer = 4 calls per sample')
print(f'50 samples ≈ 200 API calls')
print(f'@ ~15s/call ≈ 3000s ≈ 50 minutes (if no parallelism)')
print(f'@ ~30s/call ≈ 6000s ≈ 100 minutes')
print(f'With --sleep 3: +150s overhead')
