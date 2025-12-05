# caspian-
上传个人所完成的简单项目


socket通讯项目README

# Socket Chat System

一套基于 Python asyncio 与自定义 JSON 协议的双端 Socket 聊天框架，覆盖《Socket 需求实验》中定义的消息骨架、命令集合与共享协议模块。当前仓库聚焦于“基础通信 + 会话管理 + 在线状态 + 文本消息”四大能力，并为后续文件通道、语音扩展等预留接口。

---

## 已实现的实验功能

- **统一协议栈（shared/protocol）**  
  - 采用 JSON 报文 + `\n` 分帧，提供命令枚举、状态码、模型校验、HMAC 验证等工具。  
  - 落地《protocol.md》末尾的子目录规范，支持 `commands.py / errors.py / framing.py / messages.py / validator.py / schemas/*`。
- **客户端框架**  
  - `NetworkClient` 封装连接、心跳、自动重连、消息派发、文件通道预留。  
  - `ClientSession` 负责 token/headers 注入，Auth/Refresh/Logout 流程通过 `AuthManager` 协调。  
  - `MessagingManager`、`PresenceManager`、`FileTransferManager`、`ChatCLI` 架起业务脚手架。  
  - `LocalDatabase` + `InMemoryCache` 为消息/状态提供持久化与缓存。
- **服务端框架**  
  - `SocketServer` 基于 `asyncio.start_server`，配合 `CommandRouter` 派发消息。  
  - `AuthService`、`PresenceService`、`MessageService` 对应实验中的 auth/presence/message 场景。  
  - `InMemoryRepository` 维护用户、会话、消息、在线状态；`OfflineDispatcher` 为后台任务留口。
- **测试与工具**  
  - `tests/test_protocol.py` 覆盖协议编解码回环。  
  - `shared/settings.py`、`.env` 支持 CLIENT_*/SERVER_* 前缀的配置注入。

---

## 目录结构

```
Socket/
├── client/                 # 客户端源代码
│   ├── core/               # network + session
│   ├── features/           # auth / messaging / presence / file_transfer
│   ├── storage/            # sqlite + cache
│   ├── ui/                 # CLI + GUI 界面
│   │   ├── cli.py          # 命令行界面
│   │   ├── tk_chat.py      # Tkinter图形界面（现代化深色主题）
│   │   └── modern_style.py # UI样式配置
│   ├── main.py             # CLI 客户端启动器
│   └── tk_main.py          # GUI 客户端启动器
├── server/                 # 服务器端源代码
│   ├── core/               # ConnectionContext / router / server
│   ├── services/           # AuthService / PresenceService / MessageService
│   ├── storage/            # InMemoryRepository
│   ├── workers/            # 离线调度占位
│   └── main.py             # asyncio 服务启动器
├── shared/                 # 协议、工具、配置
├── docs/                   # 架构/协议/说明文档
├── tests/                  # Pytest
├── requirements.txt
└── README.md
```

---

## 快速开始

### 1. 环境准备

```bash
python -m venv .venv
. .venv/Scripts/activate        # Windows PowerShell
pip install -r requirements.txt
```

> Python 3.10+；依赖 `pydantic`, `jsonschema`, `python-dotenv`, `pytest`。

### 2. 配置

可选创建 `.env` 放在仓库根目录，支持下列变量（部分示例）：

```ini
# 客户端
CLIENT_SERVER_HOST=127.0.0.1
CLIENT_SERVER_PORT=8080
CLIENT_LOG_LEVEL=DEBUG

# 服务端
SERVER_HOST=0.0.0.0
SERVER_PORT=8080
SERVER_LOG_LEVEL=INFO
```

### 3. 启动服务器

```bash
python -m server.main
```

服务器将监听 `SERVER_HOST:SERVER_PORT`，并注册 auth/presence/message 处理器。

### 4. 启动客户端

在另一个终端，可以选择以下两种方式之一：

#### 方式一：图形界面（GUI）- 推荐 🎨

```bash
python -m client.tk_main
```

**现代化图形界面特性：**
- 💬 深色主题设计，界面美观现代
- 🎨 支持私聊、群聊、文件传输
- 📊 实时在线用户列表
- 🏠 房间管理功能
- 📎 文件传输进度显示
- 💾 消息历史记录

> 登录窗口已默认填写 `alice` / `alice`，点击"🚀 登录系统"即可进入。

#### 方式二：命令行（CLI）

```bash
python -m client.main
```

CLI 提供以下指令：

- `login <username> <password>`（密码自动做 SHA256）
- `send <conversation_id> <target_id> <text>`
- `presence`（拉取在线列表）
- `quit`

> 默认内置 `alice` / `bob` 账户（密码同名）。登录成功后会通过 `NetworkClient` 保持心跳。

### 5. 运行测试

```bash
pytest
```

当前包含协议编解码回环示例，可按需求补充更多用例。

---

## 后续迭代建议

- **消息存储**：把 `InMemoryRepository` 替换为 SQLite / Redis，并实现离线消息推送。
- **文件/语音**：利用 `NetworkClient.open_file_channel` 与 `framing.encode_chunk` 完成二进制传输。
- **安全与观测**：接入 TLS、HMAC 签名校验、结构化日志与 metrics。
- **UI/UX**：✅ 已实现现代化深色主题 GUI，可扩展为 Web 端或移动端。

如需了解每个模块/函数的详细职责，请阅读 `docs/introduction.md`。
