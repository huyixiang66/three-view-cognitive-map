# Windows one-shot: legacy cogmap -> scene_3d.json -> Unity scene -> V' frames.
param(
    [Parameter(Mandatory=$true)][string]$CogmapJson,
    [Parameter(Mandatory=$true)][string]$CamerasJson,
    [Parameter(Mandatory=$true)][string]$OutDir,
    [string]$Scene3d = "",
    [string]$ProjectDir = "C:\UnityProjects\CogMapUnityProject"
    ,
    [string]$CopyAssetsFrom = ""
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$archive = Join-Path $root "tmp\archive_unity_2026_08"
$unityFiles = Join-Path $root "tmp\unity_cogmap"

$unity = "C:\Program Files\Unity\Hub\Editor\6000.5.10f1\Editor\Unity.exe"
if (-not (Test-Path $unity)) {
    throw "Unity not found: $unity"
}


# 1) fuse legacy cogmap into flat 3D JSON (skip when a prebuilt scene is provided)
if (-not $Scene3d) {
    $Scene3d = Join-Path (Split-Path -Parent $CogmapJson) "scene_3d.json"
    # cogmap front/side z is already the object center, not the bottom
    python (Join-Path $archive "fuse_views_to_3d.py") $CogmapJson -o $Scene3d --z-anchor center
    if ($LASTEXITCODE -ne 0) { throw "fuse_views_to_3d.py failed" }
}

# 2) create project on first run
if (-not (Test-Path (Join-Path $ProjectDir "Assets"))) {
    $sp = Start-Process -FilePath $unity -ArgumentList @("-batchmode","-quit","-createProject",('"'+$ProjectDir+'"'),"-logFile",('"'+(Join-Path $PSScriptRoot "unity_create.log")+'"')) -Wait -PassThru -WindowStyle Hidden
    if ($sp.ExitCode -ne 0) { throw "Unity createProject failed (exit $($sp.ExitCode))" }
}

# 3) sync scripts
if ($CopyAssetsFrom) {
    Get-ChildItem $CopyAssetsFrom -Directory | ForEach-Object {
        Copy-Item $_.FullName (Join-Path $ProjectDir "Assets") -Recurse -Force
    }
}
Copy-Item (Join-Path $unityFiles "CogMapSceneBuilder.cs") (Join-Path $ProjectDir "Assets")
New-Item -ItemType Directory -Force -Path (Join-Path $ProjectDir "Assets\Editor") | Out-Null
Copy-Item (Join-Path $unityFiles "Editor\CogMapBatchBuilder.cs") (Join-Path $ProjectDir "Assets\Editor")
Copy-Item (Join-Path $unityFiles "Editor\CogMapVGGTRenderer.cs") (Join-Path $ProjectDir "Assets\Editor")

# 4) build scene
$sp = Start-Process -FilePath $unity -ArgumentList @("-batchmode","-quit","-projectPath",('"'+$ProjectDir+'"'),"-executeMethod","CogMapBatchBuilder.Build","-cogmapJson",('"'+$Scene3d+'"'),"-logFile",('"'+(Join-Path $PSScriptRoot "unity_build.log")+'"')) -Wait -PassThru -WindowStyle Hidden
if ($sp.ExitCode -ne 0) { throw "Unity build failed (exit $($sp.ExitCode))" }

# 5) render V' frames at VGGT poses
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$sp = Start-Process -FilePath $unity -ArgumentList @("-batchmode","-quit","-projectPath",('"'+$ProjectDir+'"'),"-executeMethod","CogMapVGGTRenderer.Render","-sceneJson",('"'+$Scene3d+'"'),"-camerasJson",('"'+$CamerasJson+'"'),"-outDir",('"'+$OutDir+'"'),"-logFile",('"'+(Join-Path $PSScriptRoot "unity_render.log")+'"')) -Wait -PassThru -WindowStyle Hidden
if ($sp.ExitCode -ne 0) { throw "Unity render failed (exit $($sp.ExitCode))" }

Write-Host "Done. V' frames in $OutDir"
