// Batch renderer: builds the cogmap scene, then renders V' frames from VGGT
// cameras (extrinsic/intrinsic loaded from a JSON exported from the .npz).
//
// Invoked by Unity in batch mode:
//   Unity -batchmode -quit -projectPath <proj> \
//         -executeMethod CogMapVGGTRenderer.Render \
//         -sceneJson /abs/path/scene_3d.json \
//         -camerasJson /abs/path/vggt_cameras.json \
//         -outDir /abs/path/vprime_frames
using System;
using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

public static class CogMapVGGTRenderer
{
    [Serializable]
    public class Cam
    {
        public float[] R; // 3x3, row-major
        public float[] t; // 3
        public float[] K; // 3x3, row-major
        public int width; // video frame width at which K was estimated
        public int height; // video frame height at which K was estimated
    }

    [Serializable]
    public class CamList
    {
        public Cam[] cameras;
    }

    public static void Render()
    {
        string sceneJson = GetArg("-sceneJson");
        string camerasJson = GetArg("-camerasJson");
        string outDir = GetArg("-outDir");
        if (string.IsNullOrEmpty(sceneJson) || string.IsNullOrEmpty(camerasJson) || string.IsNullOrEmpty(outDir))
        {
            Debug.LogError("[VGGTRender] missing -sceneJson / -camerasJson / -outDir");
            EditorApplication.Exit(1);
            return;
        }
        Directory.CreateDirectory(outDir);

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
        builder.cellSize = 1f; // scene JSON and camera JSON share grid world units
        builder.BuildScene();

        CamList camList = JsonUtility.FromJson<CamList>(File.ReadAllText(camerasJson));
        if (camList == null || camList.cameras == null || camList.cameras.Length == 0)
        {
            Debug.LogError("[VGGTRender] no cameras parsed");
            EditorApplication.Exit(1);
            return;
        }

        var camGo = new GameObject("VGGT Camera");
        var cam = camGo.AddComponent<Camera>();
        camGo.tag = "MainCamera";
        cam.nearClipPlane = 0.01f;
        cam.farClipPlane = 100f;
        cam.clearFlags = CameraClearFlags.SolidColor;
        cam.backgroundColor = new Color(0.9f, 0.9f, 0.9f);

        for (int i = 0; i < camList.cameras.Length; i++)
        {
            Cam c = camList.cameras[i];
            SetPose(camGo.transform, c);
            int w = c.width > 0 ? c.width : 512;
            int h = c.height > 0 ? c.height : 512;
            SetIntrinsics(cam, c.K, w, h);
            string path = Path.Combine(outDir, string.Format("frame_{0:D3}.png", i));
            RenderPng(cam, path, w, h);
            Debug.Log("[VGGTRender] saved " + path);
        }

        EditorApplication.Exit(0);
    }

    static void SetPose(Transform tf, Cam c)
    {
        Matrix4x4 R = FromRows(c.R);
        Matrix4x4 RT = R.transpose;
        Vector3 t = new Vector3(c.t[0], c.t[1], c.t[2]);
        tf.position = -RT.MultiplyPoint3x4(t);

        // OpenCV camera: x right, y down, z forward.
        // Unity camera: x right, y up, z forward, so flip camera y.
        Vector3 fwd = RT.MultiplyVector(new Vector3(0f, 0f, 1f));
        Vector3 up = RT.MultiplyVector(new Vector3(0f, -1f, 0f));
        if (fwd.sqrMagnitude < 1e-6f || up.sqrMagnitude < 1e-6f)
        {
            Debug.LogError("[VGGTRender] degenerate camera pose");
            return;
        }
        tf.rotation = Quaternion.LookRotation(fwd.normalized, up.normalized);
    }

    static void SetIntrinsics(Camera cam, float[] K, int w, int h)
    {
        float fx = K[0];
        float fy = K[4];
        float vfov = 2f * Mathf.Rad2Deg * Mathf.Atan(h / (2f * Mathf.Max(fy, 1e-6f)));
        cam.fieldOfView = vfov;
        cam.aspect = w / (float)h;
    }

    static void RenderPng(Camera cam, string path, int w, int h)
    {
        int sizeW = Mathf.Max(w, 2);
        int sizeH = Mathf.Max(h, 2);
        var rt = new RenderTexture(sizeW, sizeH, 24);
        cam.targetTexture = rt;
        cam.Render();
        RenderTexture.active = rt;
        var tex = new Texture2D(sizeW, sizeH, TextureFormat.RGB24, false);
        tex.ReadPixels(new Rect(0, 0, sizeW, sizeH), 0, 0);
        tex.Apply();
        File.WriteAllBytes(path, tex.EncodeToPNG());
        UnityEngine.Object.DestroyImmediate(tex);
        RenderTexture.active = null;
        cam.targetTexture = null;
        rt.Release();
        UnityEngine.Object.DestroyImmediate(rt);
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
