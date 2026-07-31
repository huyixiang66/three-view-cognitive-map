"""Three-View Cognitive Map -- Matplotlib Visualizer (v4)
- Center-based positioning (pos = object center)
- Size-proportional icon rendering
- PNG icons from viz/icons/ for ALL objects (no emoji)
- Clean scientific-figure layout per nature-figure principles
"""
import json, io, base64, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- Icon directory ----
_ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons')

# ---- Name aliases: map variant names to canonical icon names ----
NAME_ALIAS = {
    "stool": "chair",
    "seat": "chair",
    "television": "tv",
    "light": "lamp",
    "trash_bin": "trash_can",
    "trash": "trash_can",
    "washer": "washing_machine",
    "desk": "table",
    "coffee_cup": "cup",
    "ceiling_lamp": "ceiling_light",
    "shoe": "shoes",
    "hanger": "coat_hanger",
}


def _canonical(name):
    """Return canonical icon name (lowercase, underscores, aliased)."""
    key = name.strip().lower().replace(" ", "_")
    return NAME_ALIAS.get(key, key)


def draw_view(ax, objects, grid_size=10, title="", coord_keys=None):
    """Draw one view of the cognitive map on given axes."""
    if coord_keys is None:
        coord_keys = ('x', 'y')
    c1_key, c2_key = coord_keys

    # Grid setup
    ax.set_xlim(-0.5, grid_size - 0.5)
    ax.set_ylim(-0.5, grid_size - 0.5)
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=12, fontweight="bold", pad=8)
    ax.set_xticks(range(grid_size))
    ax.set_yticks(range(grid_size))
    ax.grid(True, alpha=0.15, linestyle="-", linewidth=0.5)
    ax.tick_params(labelsize=6, pad=2)
    ax.set_xticklabels([str(c) for c in range(grid_size)], fontsize=6)
    ax.set_yticklabels([str(r) for r in range(grid_size)], fontsize=6)
    ax.invert_yaxis()

    for obj in objects:
        if not isinstance(obj, dict):
            continue
        name = obj.get("name", "")
        c1 = obj.get(c1_key, 0)
        c2 = obj.get(c2_key, 0)
        sz = obj.get("size", [1, 1])
        w = max(1, int(sz[0])) if sz and len(sz) >= 1 else 1
        h = max(1, int(sz[1])) if sz and len(sz) >= 2 else 1

        icon_file = _canonical(name) + ".png"
        icon_path = os.path.join(_ICON_DIR, icon_file)

        if os.path.exists(icon_path):
            try:
                icon_img = plt.imread(icon_path)
                extent = (c1 - w / 2 + 0.05, c1 + w / 2 - 0.05,
                          c2 - h / 2 + 0.05, c2 + h / 2 - 0.05)
                ax.imshow(icon_img, extent=extent, zorder=10, origin='lower')
            except Exception:
                ax.text(c1, c2, name.upper()[:5], fontsize=8,
                        ha="center", va="center", fontweight="bold",
                        color="#555555", zorder=10)
        else:
            # Text fallback
            ax.text(c1, c2, name.upper()[:5], fontsize=8,
                    ha="center", va="center", fontweight="bold",
                    color="#555555", zorder=10)


def cogmap_to_viz(cmap, title="Three-View Cognitive Map"):
    """Convert pipeline cogmap dict to matplotlib figure."""
    if isinstance(cmap, str):
        cmap = json.loads(cmap)

    grid_size = 10
    pipeline_fmt = any(k in cmap for k in ('top_view', 'front_view', 'side_view'))

    if pipeline_fmt:
        key_specs = [
            ("top_view", "Top View (x-y)", ('x', 'y')),
            ("front_view", "Front View (x-z)", ('x', 'z')),
            ("side_view", "Side View (y-z)", ('y', 'z')),
        ]
    else:
        key_specs = [
            ("top", "Top View (x-y)", ('x', 'y')),
            ("front", "Front View (x-z)", ('x', 'z')),
            ("side", "Side View (y-z)", ('y', 'z')),
        ]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5), dpi=120)
    fig.suptitle(title, fontsize=14, fontweight="bold", y=0.98)

    for ax, (key, label, ckeys) in zip(axes, key_specs):
        raw = cmap.get(key, [])
        if isinstance(raw, dict):
            items = raw.get("objects", [])
        elif isinstance(raw, list):
            items = raw
        else:
            items = []
        draw_view(ax, items, grid_size, label, coord_keys=ckeys)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return fig


def visualize_three_view(cmap, title="Three-View Cognitive Map", save_path=None):
    """Main entry point: returns figure or saves to file."""
    fig = cogmap_to_viz(cmap, title)
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight", facecolor='white')
        plt.close(fig)
        return save_path
    return fig


if __name__ == "__main__":
    sample = {
        "top_view": [
            {"x": 2, "y": 1, "name": "door", "size": [1, 1]},
            {"x": 6, "y": 5, "name": "table", "size": [3, 2]},
            {"x": 8, "y": 6, "name": "chair", "size": [1, 1]},
            {"x": 1, "y": 7, "name": "bookshelf", "size": [1, 2]},
            {"x": 7, "y": 1, "name": "microwave", "size": [2, 1]},
            {"x": 3, "y": 4, "name": "sofa", "size": [3, 2]},
            {"x": 8, "y": 8, "name": "plant", "size": [1, 1]},
        ],
        "front_view": [
            {"x": 2, "z": 1, "name": "door", "size": [1, 2]},
            {"x": 6, "z": 3, "name": "table", "size": [3, 1]},
            {"x": 8, "z": 4, "name": "chair", "size": [1, 1]},
            {"x": 1, "z": 3, "name": "bookshelf", "size": [1, 2]},
            {"x": 7, "z": 0, "name": "microwave", "size": [2, 1]},
            {"x": 3, "z": 2, "name": "sofa", "size": [3, 2]},
            {"x": 8, "z": 7, "name": "plant", "size": [1, 1]},
        ],
        "side_view": [
            {"y": 1, "z": 1, "name": "door", "size": [1, 2]},
            {"y": 5, "z": 3, "name": "table", "size": [2, 1]},
            {"y": 6, "z": 4, "name": "chair", "size": [1, 1]},
            {"y": 7, "z": 3, "name": "bookshelf", "size": [1, 2]},
            {"y": 1, "z": 0, "name": "microwave", "size": [1, 1]},
            {"y": 4, "z": 2, "name": "sofa", "size": [2, 3]},
            {"y": 8, "z": 7, "name": "plant", "size": [1, 1]},
        ],
    }
    out = sys.argv[1] if len(sys.argv) > 1 else "cogmap_v4.png"
    visualize_three_view(sample, save_path=out)
    print(f"Saved to {out}")
