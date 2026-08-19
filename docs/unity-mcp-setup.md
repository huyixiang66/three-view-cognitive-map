# Unity MCP 安装记录（CoplayDev/unity-mcp）

> 2026-08-01 · 已安装并通过验收：Codex 通过 MCP 创建红色立方体并截图成功

## 已完成

- 安装 uv 0.12.1（经 PyPI 镜像安装，GitHub 直连太慢）
  - 路径：`C:\Users\贝贝\AppData\Roaming\Python\Python313\Scripts\uv.exe`
  - 已追加到用户 PATH
- Unity 项目 `C:\UnityProjects\My project` 的 `Packages/manifest.json` 已添加依赖：
  - `com.coplaydev.unity-mcp` = `https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#main`
  - 原始 manifest 备份在 `Packages/manifest.json.bak`
- Unity 2022.3.62 已成功拉取并编译 MCPForUnity.Runtime / MCPForUnity.Editor
- Codex 配置 `~/.codex/config.toml` 已写入（备份 `config.toml.bak`）：

```toml
[mcp_servers.unityMCP]
url = "http://localhost:8080/mcp"

[features]
rmcp_client = true
```

## 剩余步骤
1. [x] Unity 内 Start Server 已启动，127.0.0.1:8080 监听正常
2. [x] MCP initialize 握手成功，服务器返回 mcp-for-unity-server 3.4.5
3. [x] 重启 Codex 并执行验收：创建 RedCube @ (0,0.5,0) + 上色 + 截图成功

## 测试指令

> 在当前场景原点创建一个红色立方体，并把相机对准它，然后截图给我看。

## 常见问题

- 8080 被占用：停掉旧服务器或换端口，同时改 Codex config 里的 url
- Codex 连不上：确认 Unity 里服务器 Running，重启 Codex
- uv 找不到：在 MCP for Unity 窗口手动指定 uv.exe 路径
