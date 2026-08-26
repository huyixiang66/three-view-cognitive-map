"""Fuse a three-view cognitive map JSON into a single 3D-coordinate JSON.

The input is the cogmap saved by run_vsibench.py, e.g.:
    {"top_view": {"gridSize": 10, "objects": [{"x":2,"y":7,"name":"desk","size":[3,2]}, ...]},
     "front_view": {...}, "side_view": {...}}

Views are matched by object name (multiple instances of the same name are
paired by their order of appearance). Fusion rules:
    x (width axis)  = mean(top.x,  front.x)
    y (depth axis)  = mean(top.y,  side.y)
    z (height axis) = mean(front.z, side.z)   -> treated as the object's BOTTOM
    width  = mean(top.size[0],  front.size[0])
    depth  = mean(top.size[1],  side.size[0])
    height = mean(front.size[1], side.size[1])

Output format (Unity-friendly flat fields, position is the BOX CENTER in
grid units):
    {"gridSize": 10, "objects": [
        {"name":"desk","x":2.0,"y":7.0,"z":1.5,"sizeX":3.0,"sizeY":2.0,"sizeZ":3.0}, ...]}

Usage:
    python fuse_views_to_3d.py ../scannetpp_09c1414f1b.json -o scene_3d.json
"""
import argparse
import json
from collections import defaultdict


def _view_objects(view):
    """Return the object list of a view (supports both list and dict formats)."""
    if isinstance(view, dict):
        return view.get('objects', [])
    if isinstance(view, list):
        return view
    return []


def _group_by_name(objects):
    groups = defaultdict(list)
    for obj in objects:
        name = str(obj.get('name', 'unknown')).strip().lower()
        groups[name].append(obj)
    return groups


def _mean(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else 0.0


def _get(obj, key, default=None):
    if obj is None:
        return default
    v = obj.get(key, default)
    return v if isinstance(v, (int, float)) else default


def _get_size(obj, idx, default=None):
    if obj is None:
        return default
    size = obj.get('size')
    if isinstance(size, (list, tuple)) and len(size) > idx and isinstance(size[idx], (int, float)):
        return size[idx]
    return default


def fuse(cogmap, z_anchor='bottom'):
    top = _group_by_name(_view_objects(cogmap.get('top_view')))
    front = _group_by_name(_view_objects(cogmap.get('front_view')))
    side = _group_by_name(_view_objects(cogmap.get('side_view')))

    grid_size = 10
    for view in (cogmap.get('top_view'), cogmap.get('front_view'), cogmap.get('side_view')):
        if isinstance(view, dict) and isinstance(view.get('gridSize'), int):
            grid_size = view['gridSize']
            break

    names = list(dict.fromkeys(list(top) + list(front) + list(side)))
    objects = []
    for name in names:
        count = max(len(top.get(name, [])), len(front.get(name, [])), len(side.get(name, [])))
        for i in range(count):
            t = top.get(name, [None] * count)[i] if i < len(top.get(name, [])) else None
            f = front.get(name, [None] * count)[i] if i < len(front.get(name, [])) else None
            s = side.get(name, [None] * count)[i] if i < len(side.get(name, [])) else None

            x = _mean([_get(t, 'x'), _get(f, 'x')])
            y = _mean([_get(t, 'y'), _get(s, 'y')])
            z = _mean([_get(f, 'z'), _get(s, 'z')])
            width = _mean([_get_size(t, 0), _get_size(f, 0)]) or 1.0
            depth = _mean([_get_size(t, 1), _get_size(s, 0)]) or 1.0
            height = _mean([_get_size(f, 1), _get_size(s, 1)]) or 1.0

            # Convert z to box center so Unity can place cubes directly
            z_center = z + height / 2.0 if z_anchor == 'bottom' else z

            objects.append({
                'name': name,
                'x': round(x, 3),
                'y': round(y, 3),
                'z': round(z_center, 3),
                'sizeX': round(width, 3),
                'sizeY': round(depth, 3),
                'sizeZ': round(height, 3),
            })
    return {'gridSize': grid_size, 'objects': objects}


def main():
    parser = argparse.ArgumentParser(description='Fuse three-view cogmap into 3D JSON')
    parser.add_argument('input', help='path to the three-view cogmap JSON')
    parser.add_argument('-o', '--output', default='scene_3d.json', help='output 3D JSON path')
    parser.add_argument('--z-anchor', choices=['bottom', 'center'], default='bottom',
                        help='whether the z in front/side views is the object bottom or center')
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as fp:
        cogmap = json.load(fp)

    result = fuse(cogmap, z_anchor=args.z_anchor)

    with open(args.output, 'w', encoding='utf-8') as fp:
        json.dump(result, fp, indent=2, ensure_ascii=False)

    print(f'{len(result["objects"])} objects -> {args.output}')
    for obj in result['objects']:
        print(f'  {obj["name"]:<12} center=({obj["x"]}, {obj["y"]}, {obj["z"]}) '
              f'size=({obj["sizeX"]}, {obj["sizeY"]}, {obj["sizeZ"]})')


if __name__ == '__main__':
    main()
