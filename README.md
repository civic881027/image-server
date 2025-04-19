
![](example1.png)
![](example2.png)
![](result.jpg)
### MCP工具

Tools
- image_generation


### 前置需求

:: 安裝UV套件管理器
[uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)


### 設定MCP Server
```
{
  "mcpServers":{
    "image_server": {
      "command": "uv",
      "args": [
        "--directory",
        "YourDirectory",
        "run",
        "image_server.py"
      ],
      "env": {
        "IMAGE_API_URL": "https://black-forest-labs-flux-1-schnell.hf.space/call/infer"
      }
    }
}
```


