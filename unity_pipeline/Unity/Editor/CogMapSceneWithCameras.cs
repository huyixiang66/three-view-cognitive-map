// Batch method: build the cogmap scene AND create VGGT camera GameObjects,
// then save the whole thing as a .unity scene so it can be opened in the editor.
using System;
using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

public static class CogMapSceneWithCameras
{
    [Serializable]
    public class Cam { public float[] R; public float[] t; public float[] K; public int width; public int height; }
    [Serializable]
    public class CamList { public Cam[] cameras; }

    public static void Build()
    {
        string sceneJson = GetArg("-sceneJson");
        string camerasJson = GetArg("-camerasJson");
        string outputScene = GetArg("-outputScene") ?? "Assets/Scenes/CogMapScene_VGGT.unity";
        if (string.IsNullOrEmpty(sceneJson) || string.IsNullOrEmpty(camerasJson))
        {
            Debug.LogError("[SceneWithCams] missing -sceneJson / -camerasJson");
            EditorApplication.Exit(1);
            return;
        }

        var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);

        var lightGo = new GameObject("Directional Light");
        var light = lightGo.AddComponent<Light>();
        light.type = LightType.Directional;
        light.intensity = 1.0f;
        lightGo.transform.rotation = Quaternion.Euler(50f, -30f, 0f);
        lightGo.transform.position = new Vector3(0f, 5f, 0f);

        var builderGo = new GameObject("CogMapBuilder");
        var builder = builderGo.AddComponent<CogMapSceneBuilder>();
        builder.jsonPath = sceneJson;
        builder.addLabels = false;
        builder.cellSize = 1f; // scene JSON is already in VGGT world units
        builder.BuildScene();

        CamList camList = JsonUtility.FromJson<CamList>(File.ReadAllText(camerasJson));
        if (camList != null && camList.cameras != null)
        {
            for (int i = 0; i < camList.cameras.Length; i++)
            {
                var c = camList.cameras[i];
                var camGo = new GameObject(string.Format("VGGT_Cam_{0:D2}", i));
                var cam = camGo.AddComponent<Camera>();
                if (i == 0) camGo.tag = "MainCamera";
                cam.nearClipPlane = 0.01f;
                cam.farClipPlane = 100f;
                SetPose(camGo.transform, c);
                SetIntrinsics(cam, c);
                var marker = GameObject.CreatePrimitive(PrimitiveType.Sphere);
                marker.name = "CameraMarker";
                marker.transform.SetParent(camGo.transform, false);
                marker.transform.localPosition = Vector3.zero;
                marker.transform.localScale = new Vector3(0.12f, 0.12f, 0.12f);
                var col = marker.GetComponent<Collider>();
                if (col != null) UnityEngine.Object.DestroyImmediate(col);
                Debug.Log("[SceneWithCams] created " + camGo.name);
            }
        }

        Directory.CreateDirectory(Path.GetDirectoryName(outputScene));
        bool ok = EditorSceneManager.SaveScene(scene, outputScene);
        Debug.Log("[SceneWithCams] saved: " + outputScene + " ok=" + ok);
        EditorApplication.Exit(ok ? 0 : 1);
    }

    static void SetPose(Transform tf, Cam c)
    {
        Matrix4x4 R = FromRows(c.R);
        Matrix4x4 RT = R.transpose;
        Vector3 t = new Vector3(c.t[0], c.t[1], c.t[2]);
        tf.position = -RT.MultiplyPoint3x4(t);
        Vector3 fwd = RT.MultiplyVector(new Vector3(0f, 0f, 1f));
        Vector3 up = RT.MultiplyVector(new Vector3(0f, -1f, 0f));
        if (fwd.sqrMagnitude < 1e-6f || up.sqrMagnitude < 1e-6f) return;
        tf.rotation = Quaternion.LookRotation(fwd.normalized, up.normalized);
    }

    static void SetIntrinsics(Camera cam, Cam c)
    {
        float[] K = c.K;
        float fy = K[4];
        float h = c.height > 0 ? c.height : 252f;
        float w = c.width > 0 ? c.width : 336f;
        float vfov = 2f * Mathf.Rad2Deg * Mathf.Atan(h / (2f * Mathf.Max(fy, 1e-6f)));
        cam.fieldOfView = vfov;
        cam.aspect = w / h;
    }

    static Matrix4x4 FromRows(float[] m)
    {
        var M = new Matrix4x4();
        for (int r = 0; r < 3; r++)
            for (int c = 0; c < 3; c++)
                M[r, c] = m[r * 3 + c];
        M[3, 3] = 1f;
        return M;
    }

    static string GetArg(string name)
    {
        string[] args = Environment.GetCommandLineArgs();
        for (int i = 0; i < args.Length - 1; i++)
            if (args[i] == name) return args[i + 1];
        return null;
    }
}
