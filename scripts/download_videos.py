"""Download VSI-Bench videos needed for the 50-sample subset."""
import json
import os
import subprocess
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES_PATH = os.path.join(PROJECT_ROOT, 'src', 'vsi_subset_50.json')
CACHE_DIR = os.path.join(os.path.expanduser('~'), '.cache', 'huggingface', 'vsibench')

# Base URL for VSI-Bench videos on HuggingFace
HF_BASE = 'https://huggingface.co/datasets/nyu-visionx/VSI-Bench/resolve/main'


def main():
    with open(SAMPLES_PATH, 'r', encoding='utf-8') as f:
        samples = json.load(f)

    needed = set()
    for s in samples:
        dataset = s['dataset']
        scene = s['scene_name']
        needed.add((dataset, scene))

    print(f'Total samples: {len(samples)}, unique videos: {len(needed)}')
    print(f'Output dir: {CACHE_DIR}')
    os.makedirs(CACHE_DIR, exist_ok=True)

    downloaded = 0
    skipped = 0
    failed = []

    for dataset, scene in sorted(needed):
        dest_dir = os.path.join(CACHE_DIR, dataset)
        dest = os.path.join(dest_dir, scene + '.mp4')
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            print(f'[skip] {dataset}/{scene}.mp4 (exists)')
            skipped += 1
            continue

        os.makedirs(dest_dir, exist_ok=True)
        url = f'{HF_BASE}/{dataset}/{scene}.mp4'
        print(f'[download] {url}')

        try:
            subprocess.run(
                ['curl', '-L', '-o', dest, url],
                check=True,
                timeout=600,
            )
            downloaded += 1
        except Exception as e:
            failed.append(f'{dataset}/{scene}')
            print(f'[FAIL] {e}')

    print(f'\nDone. Downloaded: {downloaded}, skipped: {skipped}, failed: {len(failed)}')
    if failed:
        print('Failed videos:')
        for f in failed:
            print(f'  {f}')


if __name__ == '__main__':
    main()
