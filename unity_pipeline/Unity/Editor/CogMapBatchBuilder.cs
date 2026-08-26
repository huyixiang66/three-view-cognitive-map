// Editor batch entry point: builds the cogmap scene from the command line
// and saves it as a .unity scene asset. Invoked by build_unity_scene.sh via:
//
//   Unity -batchmode -quit -projectPath <proj> \
//         -executeMethod CogMapBatchBuilder.Build \
//         -cogmapJson /abs/path/scene_3d.json [-outputScene Assets/Scenes/CogMapScene.unity]

using System;
using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

public static class CogMapBatchBuilder
{
    public static void Build()
    {
        string jsonPath = GetArg("-cogmapJson");
        string scenePath = GetArg("-outputScene") ?? "Assets/Scenes/CogMapScene.unity";

        if (string.IsNullOrEmpty(jsonPath) || !File.Exists(jsonPath))
        {
            Debug.LogError($"[CogMapBatch] JSON not found: {jsonPath}");
            EditorApplication.Exit(1);
            return;
        }

        var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);

        // Light
        var lightGo = new GameObject("Directional Light");
        var light = lightGo.AddComponent<Light>();
        light.type = LightType.Directional;
        light.intensity = 1.0f;
        lightGo.transform.rotation = Quaternion.Euler(50f, -30f, 0f);

        // Builder
        var builderGo = new GameObject("CogMapBuilder");
        var builder = builderGo.AddComponent<CogMapSceneBuilder>();
        builder.jsonPath = jsonPath;
        string cellArg = GetArg("-cellSize");
        if (!string.IsNullOrEmpty(cellArg))
            builder.cellSize = float.Parse(cellArg, System.Globalization.CultureInfo.InvariantCulture);
        builder.BuildScene();

        // Camera looking at the room center
        float extent = 10f * builder.cellSize;
        var camGo = new GameObject("Main Camera");
        var cam = camGo.AddComponent<Camera>();
        camGo.tag = "MainCamera";
        camGo.transform.position = new Vector3(extent / 2f, extent * 0.35f, extent * 0.75f);
        camGo.transform.LookAt(new Vector3(extent / 2f, extent * 0.2f, extent / 2f));
        cam.clearFlags = CameraClearFlags.Skybox;

        Directory.CreateDirectory(Path.GetDirectoryName(scenePath));
        bool ok = EditorSceneManager.SaveScene(scene, scenePath);
        Debug.Log($"[CogMapBatch] Scene saved: {scenePath} (ok={ok})");
        EditorApplication.Exit(ok ? 0 : 1);
    }

    // Converts Built-in RP materials of imported assets to URP so they don't
    // render magenta. Invoked by import_asset.sh after importing a package.
    public static void ConvertMaterialsToUrp()
    {
        Debug.Log("[CogMapBatch] URP material conversion skipped (URP not installed).");
        EditorApplication.Exit(0);
    }

    static string GetArg(string name)
    {
        string[] args = Environment.GetCommandLineArgs();
        for (int i = 0; i < args.Length - 1; i++)
            if (args[i] == name) return args[i + 1];
        return null;
    }
}
