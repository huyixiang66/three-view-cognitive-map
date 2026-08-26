// Builds a Unity scene from the 3D-coordinate JSON produced by fuse_views_to_3d.py.
//
// Setup:
//   1. Copy this file into your Unity project's Assets/ folder.
//   2. Copy the fused JSON (e.g. scene_3d.json) into Assets/ as well, then drag
//      it onto the "Json File" field, OR set "Json Path" to an absolute path.
//   3. Create an empty GameObject, attach this component, and press Play
//      (or right-click the component header -> "Build Scene" in the Editor).
//
// Coordinate mapping (cogmap -> Unity):
//   cogmap x (width)  -> Unity X
//   cogmap y (depth)  -> Unity Z
//   cogmap z (height) -> Unity Y
// Each grid cell is `cellSize` meters (default 0.5m, so a 10x10 grid = 5m room).

using System;
using System.IO;
using UnityEngine;
#if UNITY_EDITOR
using UnityEditor;
#endif

public class CogMapSceneBuilder : MonoBehaviour
{
    [Serializable]
    public class CogMapObject
    {
        public string name;
        public float x, y, z;          // box center, grid units
        public float sizeX, sizeY, sizeZ; // width, depth, height, grid units
        public float yaw;               // degrees, 0 = facing +x, counter-clockwise positive
    }

    [Serializable]
    public class CogMapScene
    {
        public int gridSize = 10;
        public CogMapObject[] objects;
    }

    [Header("Input (use one of the two)")]
    public TextAsset jsonFile;
    public string jsonPath = "";

    [Header("Settings")]
    [Tooltip("Meters per grid cell")]
    public float cellSize = 0.5f;
    public bool addFloor = true;
    public bool addLabels = true;
    [Tooltip("Three walls: left, right, back. The front (camera side) stays open.")]
    public bool addWalls = true;
    [Tooltip("Replace cubes with prefabs from the asset library when a name matches (Editor only)")]
    public bool usePrefabs = true;
    [Tooltip("Folder searched for matching prefabs")]
    public string prefabSearchFolder = "Assets";
    [Tooltip("Name synonyms for prefab matching, format: cogmapName=prefabName")]
    public string[] prefabAliases = { "desk=table", "sofa=couch", "nightstand=night_stand", "wardrobe=closet" };

    void Start()
    {
        BuildScene();
    }

    [ContextMenu("Build Scene")]
    public void BuildScene()
    {
        string json = LoadJson();
        if (string.IsNullOrEmpty(json))
        {
            Debug.LogError("[CogMap] No JSON input. Assign jsonFile or jsonPath.");
            return;
        }

        CogMapScene scene = JsonUtility.FromJson<CogMapScene>(json);
        if (scene == null || scene.objects == null)
        {
            Debug.LogError("[CogMap] Failed to parse JSON.");
            return;
        }

        // Clear previous build
        Transform old = transform.Find("CogMapRoot");
        if (old != null) DestroyImmediate(old.gameObject);

        GameObject root = new GameObject("CogMapRoot");
        root.transform.SetParent(transform, false);

        if (addFloor) CreateFloor(root.transform, scene.objects, scene.gridSize);
        if (addWalls) CreateWalls(root.transform, scene.gridSize);

        foreach (CogMapObject obj in scene.objects)
            CreateBox(root.transform, obj);

        Debug.Log($"[CogMap] Built {scene.objects.Length} objects (grid {scene.gridSize}, cell {cellSize}m).");
    }

    string LoadJson()
    {
        if (jsonFile != null) return jsonFile.text;
        if (!string.IsNullOrEmpty(jsonPath) && File.Exists(jsonPath)) return File.ReadAllText(jsonPath);
        return null;
    }

    void CreateFloor(Transform parent, CogMapObject[] objects, int gridSize)
    {
        // Floor spans the full grid so it aligns with the walls.
        float extent = gridSize * cellSize;
        Vector3 center = new Vector3(extent / 2f, -0.05f, extent / 2f);
        Vector3 size = new Vector3(extent, 0.1f, extent);
        GameObject floor = GameObject.CreatePrimitive(PrimitiveType.Cube);
        floor.name = "Floor";
        floor.transform.SetParent(parent, false);
        floor.transform.localPosition = center;
        floor.transform.localScale = size;
        SetColor(floor, new Color(0.85f, 0.85f, 0.85f));
    }

    // Left (x=0), right (x=max) and back (y=max, far from camera) walls;
    // the front side is left open so the room interior stays visible.
    void CreateWalls(Transform parent, int gridSize)
    {
        float extent = gridSize * cellSize;
        float height = gridSize * cellSize;
        const float thickness = 0.1f;
        Color wallColor = new Color(0.93f, 0.91f, 0.88f);

        CreateWall(parent, "Wall_Left",
            new Vector3(-thickness / 2f, height / 2f, extent / 2f),
            new Vector3(thickness, height, extent), wallColor);
        CreateWall(parent, "Wall_Right",
            new Vector3(extent + thickness / 2f, height / 2f, extent / 2f),
            new Vector3(thickness, height, extent), wallColor);
        CreateWall(parent, "Wall_Back",
            new Vector3(extent / 2f, height / 2f, extent + thickness / 2f),
            new Vector3(extent + 2f * thickness, height, thickness), wallColor);
    }

    void CreateWall(Transform parent, string name, Vector3 position, Vector3 scale, Color color)
    {
        GameObject wall = GameObject.CreatePrimitive(PrimitiveType.Cube);
        wall.name = name;
        wall.transform.SetParent(parent, false);
        wall.transform.localPosition = position;
        wall.transform.localScale = scale;
        SetColor(wall, color);
    }

    bool IsWallMounted(string name)
    {
        string n = name.ToLowerInvariant();
        return n.Contains("window") || n.Contains("mirror") || n.Contains("whiteboard")
            || n.Contains("picture") || n.Contains("air condition");
    }

    void CreateBox(Transform parent, CogMapObject obj)
    {
        // cogmap (x, y, z) = (width, depth, height) -> Unity (X, Z, Y)
        Vector3 center = new Vector3(obj.x * cellSize, obj.z * cellSize, obj.y * cellSize);
        Vector3 targetSize = new Vector3(
            Mathf.Max(obj.sizeX, 0.1f) * cellSize,
            Mathf.Max(obj.sizeZ, 0.1f) * cellSize,
            Mathf.Max(obj.sizeY, 0.1f) * cellSize);
        if (IsWallMounted(obj.name))
            center.y = Mathf.Max(center.y, targetSize.y / 2f); // never below floor
        else
            center.y = targetSize.y / 2f; // snap floor-standing objects to the floor

        GameObject go = usePrefabs ? TryCreateFromPrefab(parent, obj.name, center, targetSize) : null;
        float labelY = center.y + targetSize.y / 2f;

        if (go == null)
        {
            go = GameObject.CreatePrimitive(PrimitiveType.Cube);
            go.name = obj.name;
            go.transform.SetParent(parent, false);
            go.transform.localPosition = center;
            go.transform.localScale = targetSize;
            SetColor(go, ColorForName(obj.name));
        }
        else
        {
            Bounds b = GetBounds(go);
            labelY = b.max.y;
        }

        if (Mathf.Abs(obj.yaw) > 0.01f)
            go.transform.localRotation = Quaternion.Euler(0f, 90f - obj.yaw, 0f);

        if (addLabels) CreateLabel(parent, obj.name, new Vector3(center.x, labelY, center.z));
    }

    // Editor-only: find a prefab in the asset library whose name matches the
    // object name, instantiate it, and scale/position it to fit the target box.
    // Returns null when no prefab matches (caller falls back to a plain cube).
    GameObject TryCreateFromPrefab(Transform parent, string objName, Vector3 center, Vector3 targetSize)
    {
#if UNITY_EDITOR
        string path = FindPrefabPath(objName);
        if (path == null)
        {
            Debug.Log($"[CogMap] '{objName}': no prefab match, using cube");
            return null;
        }

        GameObject prefab = AssetDatabase.LoadAssetAtPath<GameObject>(path);
        GameObject inst = (GameObject)PrefabUtility.InstantiatePrefab(prefab, parent);
        inst.name = $"{objName} ({prefab.name})";

        Bounds b = GetBounds(inst);
        if (b.size.x <= 0f || b.size.y <= 0f || b.size.z <= 0f)
        {
            DestroyImmediate(inst);
            return null;
        }

        // Uniform scale so the model fits inside the target box without distortion
        float scale = Mathf.Min(targetSize.x / b.size.x, targetSize.y / b.size.y, targetSize.z / b.size.z);
        inst.transform.localScale *= scale;

        // Align the model's bottom center with the bottom center of the target box
        b = GetBounds(inst);
        Vector3 targetBottom = new Vector3(center.x, center.y - targetSize.y / 2f, center.z);
        Vector3 currentBottom = new Vector3(b.center.x, b.min.y, b.center.z);
        inst.transform.position += targetBottom - currentBottom;

        Debug.Log($"[CogMap] '{objName}' -> prefab '{prefab.name}' ({path})");
        return inst;
#else
        return null;
#endif
    }

#if UNITY_EDITOR
    string FindPrefabPath(string objName)
    {
        string needle = objName.ToLowerInvariant().Trim();
        string path = FindPrefabPathExact(needle);
        if (path != null) return path;

        // Try synonyms (e.g. desk=table) when the literal name has no match
        foreach (string alias in prefabAliases)
        {
            int eq = alias.IndexOf('=');
            if (eq <= 0) continue;
            if (alias.Substring(0, eq).Trim().ToLowerInvariant() != needle) continue;
            path = FindPrefabPathExact(alias.Substring(eq + 1).Trim().ToLowerInvariant());
            if (path != null) return path;
        }
        return null;
    }

    // Match by name tokens: exact filename > first token > any token > prefix > substring
    string FindPrefabPathExact(string needle)
    {
        string[] guids = AssetDatabase.FindAssets("t:Prefab", new[] { prefabSearchFolder });

        string bestPath = null;
        float bestScore = 0f;
        foreach (string guid in guids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            string file = Path.GetFileNameWithoutExtension(path).ToLowerInvariant();
            string[] tokens = file.Split(new[] { '_', '-', ' ', '.' }, StringSplitOptions.RemoveEmptyEntries);

            float score = 0f;
            if (file == needle) score = 5f;
            else if (tokens.Length > 0 && tokens[0] == needle) score = 4f;
            else if (Array.IndexOf(tokens, needle) >= 0) score = 3f;
            else if (file.StartsWith(needle)) score = 2f;
            else if (file.Contains(needle)) score = 1f;
            if (score <= 0f) continue;

            // Prefer shorter names among equal scores (e.g. "desk" over "desk_big_old")
            score -= file.Length * 0.001f;
            if (score > bestScore)
            {
                bestScore = score;
                bestPath = path;
            }
        }
        return bestPath;
    }
#endif

    static Bounds GetBounds(GameObject go)
    {
        Renderer[] renderers = go.GetComponentsInChildren<Renderer>();
        if (renderers.Length == 0) return new Bounds(go.transform.position, Vector3.zero);
        Bounds b = renderers[0].bounds;
        for (int i = 1; i < renderers.Length; i++) b.Encapsulate(renderers[i].bounds);
        return b;
    }

    void CreateLabel(Transform parent, string name, Vector3 topPosition)
    {
        GameObject labelGo = new GameObject("Label");
        labelGo.transform.SetParent(parent, false);
        labelGo.transform.localPosition = topPosition + new Vector3(0f, 0.15f, 0f);

        TextMesh text = labelGo.AddComponent<TextMesh>();
        text.text = name;
        text.characterSize = 0.08f;
        text.fontSize = 48;
        text.anchor = TextAnchor.LowerCenter;
        text.alignment = TextAlignment.Center;
        text.color = Color.black;
    }

    // Uses sharedMaterial with a fresh material so it works in both
    // Play mode and Editor batch mode (accessing .material in edit mode leaks).
    static void SetColor(GameObject go, Color color)
    {
        // Pick the shader matching the active render pipeline (URP vs built-in)
        bool srpActive = UnityEngine.Rendering.GraphicsSettings.currentRenderPipeline != null;
        Shader shader = srpActive ? Shader.Find("Universal Render Pipeline/Lit") : Shader.Find("Standard");
        if (shader == null) shader = Shader.Find("Standard");
        Material mat = new Material(shader);
        mat.color = color;
        go.GetComponent<Renderer>().sharedMaterial = mat;
    }

    static Color ColorForName(string name)
    {
        // Deterministic pastel color per object name
        int hash = 17;
        foreach (char c in name) hash = hash * 31 + c;
        float hue = Mathf.Abs(hash % 360) / 360f;
        return Color.HSVToRGB(hue, 0.55f, 0.9f);
    }
}
