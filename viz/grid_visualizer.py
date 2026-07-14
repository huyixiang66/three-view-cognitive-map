import json

EMOJI_TABLE = chr(0x1f9fa)
EMOJI_CHAIR = chr(0x1f4ba)
EMOJI_SOFA = chr(0x1f6cb)
EMOJI_BED = chr(0x1f6cc)
EMOJI_DOOR = chr(0x1f6aa)
EMOJI_WINDOW = chr(0x1f4ff)
EMOJI_MIRROR = chr(0x1fa9e)
EMOJI_FRIDGE = chr(0x1f9c8)
EMOJI_TV = chr(0x1f4fb)
EMOJI_PLANT = chr(0x1f33f)
EMOJI_LAMP = chr(0x1f4a1)
EMOJI_PERSON = chr(0x1f9d1)
QUESTION = chr(0x2753)

EMOJI_MAP = {
    'table': EMOJI_TABLE,
    'desk': EMOJI_TABLE,
    'chair': EMOJI_CHAIR,
    'sofa': EMOJI_SOFA,
    'bed': EMOJI_BED,
    'door': EMOJI_DOOR,
    'window': EMOJI_WINDOW,
    'mirror': EMOJI_MIRROR,
    'fridge': EMOJI_FRIDGE,
    'tv': EMOJI_TV,
    'plant': EMOJI_PLANT,
    'lamp': EMOJI_LAMP,
    'person': EMOJI_PERSON,
    'unknown': QUESTION,
}


def _emoji_for(obj_name):
    key = obj_name.strip().lower()
    return EMOJI_MAP.get(key, QUESTION)


class ThreeViewGrid:
    def __init__(self, size):
        self.size = size
        self.grid = {}

    def set(self, x, y, objects):
        self.grid[(x, y)] = objects

    def get(self, x, y):
        return self.grid.get((x, y), [])

    def render_text(self, view_name):
        result = []
        sep = '=' * 40
        result.append('')
        result.append(sep)
        result.append('  ' + view_name)
        result.append(sep)
        header = '      ' + ''.join(f'{c:>3}' for c in range(self.size))
        result.append(header)
        for row in range(self.size - 1, -1, -1):
            cells = []
            for col in range(self.size):
                objs = self.get(col, row)
                if objs:
                    cells.append(f'{_emoji_for(objs[0])} ')
                else:
                    cells.append('  .  ')
            joined = '|'.join(cells)
            result.append(f'  {row:>2}  |{joined}|')
        footer = '      ' + ''.join(f'{c:>3}' for c in range(self.size))
        result.append(footer)
        return chr(10).join(result)


def normalize_view_data(view_data):
    """Convert between new format {{gridSize, objects}} and legacy format [objects]."""
    if isinstance(view_data, dict) and 'objects' in view_data:
        return view_data['objects']
    if isinstance(view_data, list):
        return view_data
    return []


def extract_gridSize(cmap):
    """Extract gridSize from the first view that has it."""
    for view_name in ['front', 'top', 'side']:
        view_data = cmap.get(view_name, {})
        if isinstance(view_data, dict) and 'gridSize' in view_data:
            return view_data['gridSize']
    return 10


def visualize_three_view(cmap_str, size=None, title='Three-View Cognitive Map'):
    """Visualize three-view cognitive map. Accepts JSON string or dict.

    Supports two input formats:
    1. Legacy: {"front": [{"x":0,"z":0,"objects":["door"]}], ...}
    2. New: {"front": {"gridSize": 10, "objects": [{"x":0,"z":0,"name":"door"}]}, ...}

    If size is None, extracts from the first view that has gridSize.
    """
    try:
        cmap = json.loads(cmap_str)
    except Exception:
        try:
            cmap = eval(cmap_str)
        except Exception:
            return f'[Parse Error]\n{cmap_str[:200]}'

    if not isinstance(cmap, dict) or 'front' not in cmap:
        return f'[Parse Error]\n{cmap_str[:200]}'

    if size is None:
        size = extract_gridSize(cmap)

    grids = {}
    for view_name in ['front', 'top', 'side']:
        g = ThreeViewGrid(size)
        view_data = cmap.get(view_name, [])
        objects_list = normalize_view_data(view_data)
        for item in objects_list:
            if isinstance(item, dict):
                x = item.get('x', 0)
                y = item.get('y', 0)
                z = item.get('z', 0)
                objs = item.get('objects', item.get('name', []))
                if isinstance(objs, str):
                    objs = [objs]
                if view_name == 'front':
                    g.set(x, z, objs)
                elif view_name == 'top':
                    g.set(x, y, objs)
                elif view_name == 'side':
                    g.set(y, z, objs)
        grids[view_name] = g

    out = []
    out.append('=' * 60)
    out.append(f'  {title}')
    out.append('=' * 60)
    vlabels = {'front': 'FRONT (x-z plane)', 'top': 'TOP   (x-y plane)', 'side': 'SIDE  (y-z plane)'}
    for vn in ['front', 'top', 'side']:
        out.append(grids[vn].render_text(vlabels[vn]))
    out.append('')
    out.append(f'Grid size: {size}x{size}')
    out.append('Legend: . = empty')
    out.append('=' * 60)
    return chr(10).join(out)


if __name__ == '__main__':
    # Test with new format (gridSize included)
    # Geometrically consistent: table at (x=3, y=2, z=1), door at (x=0, y=0, z=0)
    sample = {
        'front': {'gridSize': 10, 'objects': [{'x': 0, 'z': 0, 'name': 'door'}, {'x': 3, 'z': 1, 'name': 'table'}, {'x': 5, 'z': 1, 'name': 'chair'}, {'x': 3, 'z': 4, 'name': 'sofa'}]},
        'top': {'gridSize': 10, 'objects': [{'x': 0, 'y': 0, 'name': 'door'}, {'x': 3, 'y': 2, 'name': 'table'}, {'x': 5, 'y': 2, 'name': 'chair'}, {'x': 3, 'y': 5, 'name': 'sofa'}]},
        'side': {'gridSize': 10, 'objects': [{'y': 0, 'z': 0, 'name': 'door'}, {'y': 2, 'z': 1, 'name': 'table'}, {'y': 2, 'z': 1, 'name': 'chair'}, {'y': 5, 'z': 4, 'name': 'sofa'}]},
    }
    print(visualize_three_view(json.dumps(sample, indent=2)))

    # Also test legacy format still works
    sample_legacy = {
        'front': [{'x': 0, 'z': 0, 'objects': ['door']}, {'x': 3, 'z': 1, 'objects': ['table']}],
        'top': [{'x': 0, 'y': 0, 'objects': ['door']}, {'x': 3, 'y': 2, 'objects': ['table']}],
        'side': [{'y': 0, 'z': 0, 'objects': ['door']}, {'y': 2, 'z': 1, 'objects': ['table']}],
    }
    print('\n--- Legacy format (backward compat) ---')
    print(visualize_three_view(json.dumps(sample_legacy, indent=2)))
