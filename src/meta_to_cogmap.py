import json
import os

META_INFO_DIR = r'C:\Users\贝贝\Documents\Thinking in Space复现\thinking-in-space\data\meta_info'

DATASET_META_MAP = {
    'arkitscenes': 'arkitscenes_meta_info_val.json',
    'scannet': 'scannet_meta_info_val.json',
    'scannetpp': 'scannetpp_meta_info_val.json',
}

def load_meta(dataset_name):
    prefix = DATASET_META_MAP.get(dataset_name, dataset_name)
    meta_path = os.path.join(META_INFO_DIR, prefix)
    if not os.path.exists(meta_path):
        return None
    with open(meta_path, 'r') as f:
        return json.load(f)

def scene_to_cogmap(scene_name, dataset_name, grid_size=10):
    meta = load_meta(dataset_name)
    if meta is None or scene_name not in meta:
        return None
    
    scene_data = meta[scene_name]
    object_bbox = scene_data['object_bbox']
    
    all_min = [float('inf')] * 3
    all_max = [float('-inf')] * 3
    
    for obj_name, bboxes in object_bbox.items():
        for bbox in bboxes:
            for i in range(3):
                all_min[i] = min(all_min[i], bbox['min'][i])
                all_max[i] = max(all_max[i], bbox['max'][i])
    
    margin = [0.1 * max(0.01, all_max[i] - all_min[i]) for i in range(3)]
    for i in range(3):
        all_min[i] -= margin[i]
        all_max[i] += margin[i]
    
    range_x = all_max[0] - all_min[0]
    range_y = all_max[1] - all_min[1]
    range_z = all_max[2] - all_min[2]
    
    def to_grid(val, idx):
        rmin = all_min[idx]
        rmax = all_max[idx]
        if rmax == rmin:
            return grid_size // 2
        return int(((val - rmin) / (rmax - rmin)) * (grid_size - 1))
    
    objects = []
    for obj_name, bboxes in object_bbox.items():
        for bbox in bboxes:
            c = bbox['centroid']
            a = bbox['axesLengths']
            
            gx = to_grid(c[0], 0)
            gy = to_grid(c[1], 1)
            gz = to_grid(c[2], 2)
            
            gw = max(1, int((a[0] / range_x) * (grid_size - 1) + 0.5))
            gd = max(1, int((a[1] / range_y) * (grid_size - 1) + 0.5))
            gh = max(1, int((a[2] / range_z) * (grid_size - 1) + 0.5))
            
            objects.append({
                'name': obj_name,
                'top': {'x': gx, 'y': gy, 'size': [gw, gd]},
                'front': {'x': gx, 'z': gz, 'size': [gw, gh]},
                'side': {'y': gy, 'z': gz, 'size': [gd, gh]}
            })
    
    return {
        'gridSize': grid_size,
        'objects': objects,
        'scene_name': scene_name,
        'dataset': dataset_name,
        '_meta': scene_data,  # Include raw meta for scale info
    }


def cogmap_to_grid_text(cogmap):
    """Generate a compact grid-based representation optimized for VLM reasoning."""
    if not cogmap:
        return 'No scene data.'
    
    gs = cogmap['gridSize']
    lines = []
    
    top_grid = [['.'] for _ in range(gs)]
    front_grid = [['.'] for _ in range(gs)]
    side_grid = [['.'] for _ in range(gs)]
    
    for col in range(gs):
        top_grid[col] = ['.'] * gs
        front_grid[col] = ['.'] * gs
        side_grid[col] = ['.'] * gs
    
    for obj in cogmap['objects']:
        name = obj['name'][0].upper()
        t = obj['top']
        f = obj['front']
        s = obj['side']
        for dx in range(min(t['size'][0], gs - t['x'])):
            for dy in range(min(t['size'][1], gs - t['y'])):
                tx = t['x'] + dx
                ty = t['y'] + dy
                if 0 <= tx < gs and 0 <= ty < gs:
                    top_grid[ty][tx] = name
        for dx in range(min(f['size'][0], gs - f['x'])):
            for dz in range(min(f['size'][1], gs - f['z'])):
                fx = f['x'] + dx
                fz = f['z'] + dz
                if 0 <= fx < gs and 0 <= fz < gs:
                    front_grid[fz][fx] = name
        for dy in range(min(s['size'][0], gs - s['y'])):
            for dz in range(min(s['size'][1], gs - s['z'])):
                sy = s['y'] + dy
                sz = s['z'] + dz
                if 0 <= sy < gs and 0 <= sz < gs:
                    side_grid[sz][sy] = name
    
    lines.append('TOP VIEW (x-y plane, bird-eye):')
    for row in top_grid:
        lines.append(' ' + ' '.join(row))
    lines.append('')
    lines.append('FRONT VIEW (x-z plane, elevation):')
    for row in front_grid:
        lines.append(' ' + ' '.join(row))
    lines.append('')
    lines.append('SIDE VIEW (y-z plane, profile):')
    for row in side_grid:
        lines.append(' ' + ' '.join(row))
    
    return chr(10).join(lines)


def cogmap_to_text(cogmap, meta_data=None):
    if not cogmap:
        return 'No scene data available.'
    
    lines = []
    lines.append('Scene: %s (dataset: %s)' % (cogmap['scene_name'], cogmap.get('dataset', 'unknown')))
    lines.append('Grid: %dx%d' % (cogmap['gridSize'], cogmap['gridSize']))
    
    # Include raw 3D coordinates for accurate distance computation
    if meta_data:
        lines.append('')
        lines.append('RAW 3D COORDINATES (in meters):')
        object_bbox = meta_data.get('object_bbox', {})
        for obj_name, bboxes in object_bbox.items():
            for bbox in bboxes:
                c = bbox['centroid']
                a = bbox['axesLengths']
                lines.append('  %s: centroid=(%.2f, %.2f, %.2f), extents=(%.2f, %.2f, %.2f)' % (
                    obj_name, c[0], c[1], c[2], a[0], a[1], a[2]))
    
    lines.append('')
    lines.append('GRID COORDINATES (normalized to 10x10x10):')
    lines.append('')
    lines.append('TOP VIEW (x-y plane, bird\'s-eye):')
    for obj in cogmap['objects']:
        t = obj['top']
        lines.append('  %s: pos=(%d,%d), size=%s' % (obj['name'], t['x'], t['y'], str(t['size'])))
    lines.append('')
    lines.append('FRONT VIEW (x-z plane, elevation):')
    for obj in cogmap['objects']:
        f = obj['front']
        lines.append('  %s: pos=(%d,%d), size=%s' % (obj['name'], f['x'], f['z'], str(f['size'])))
    lines.append('')
    lines.append('SIDE VIEW (y-z plane, profile):')
    for obj in cogmap['objects']:
        s = obj['side']
        lines.append('  %s: pos=(%d,%d), size=%s' % (obj['name'], s['y'], s['z'], str(s['size'])))
    
    return '\n'.join(lines)

if __name__ == '__main__':
    result = scene_to_cogmap('41069025', 'arkitscenes')
    if result:
        print(cogmap_to_text(result))
    else:
        print('Failed')
