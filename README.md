# MatrixStability Lite

> Android 整机长稳自动化压测系统 - 开源学习版

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 项目简介

MatrixStability Lite 是一款面向 Android 测试工程师的**开源学习版长稳压测系统**，采用 Agent-Server 分离架构，支持：

- ✅ 7×24h 无人值守日志采集
- ✅ ANR / Java Crash / Native Crash / Tombstone 多模态检测
- ✅ 崩溃指纹去重
- ✅ 实时可视化质量看板
- ✅ 5 分钟本地一键部署

> 💡 **Pro 企业版**：如需多租户、高级指纹去重、云端部署等企业功能，请通过 GitHub Issue 或邮件联系。
---

## 系统架构

```
┌─────────────────────────────────────────────────┐
│                                                   │
│  Agent (边缘端)        HTTPS POST        Server (云端) │
│                                                   │
│  ┌──────────────┐                    ┌──────────────┐ │
│  │ ADB 日志采集  │ ───────────────→  │ FastAPI 网关  │ │
│  │ 多模态检测    │                    │ Pydantic 校验  │ │
│  │ 定时上报      │                    │ SQLite 持久化  │ │
│  └──────────────┘                    │ 指纹去重       │ │
│                                      │ Jinja2 看板    │ │
│                                      └──────────────┘ │
│                                                   │
└─────────────────────────────────────────────────┘
```

---

## 快速开始

### 环境要求

- Python 3.9+
- （可选）Docker & Docker Compose

### 方式一：本地运行（推荐）

**启动 Server：**
\`\`\`bash
cd server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
\`\`\`

**启动 Agent（新终端）：**
\`\`\`bash
cd agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python agent_lite.py
\`\`\`

**查看报告：**
打开 http://localhost:8000/api/v1/dashboard

---

### 方式二：Docker Compose（仅 Server）

\`\`\`bash
docker-compose up -d
\`\`\`

> Docker Compose 仅启动 Server 服务。Agent 需要在本地运行。

启动 Server 后，按"方式一"的 Agent 步骤运行客户端。

---

### 方式三：接入真实 ADB 设备

**1. 连接 Android 设备**
\`\`\`bash
adb devices
# 确认设备已连接
\`\`\`

**2. 修改 Agent 采集逻辑**
编辑 `agent/agent_lite.py`，替换模拟数据为真实 ADB 采集：

\`\`\`python
def collect_real_logs():
    import subprocess
    result = subprocess.run(
        ["adb", "logcat", "-d", "-s", "AndroidRuntime:D"],
        capture_output=True, text=True
    )
    return result.stdout
\`\`\`

**3. 重新运行 Agent**
\`\`\`bash
python agent_lite.py
\`\`\`

---

## 项目结构

\`\`\`
matrix-stability-lite/
├── server/                    # FastAPI 服务端
│   ├── app/
│   │   ├── database.py        # SQLite + SQLAlchemy
│   │   ├── models.py          # 数据模型
│   │   ├── schemas.py         # Pydantic 校验
│   │   └── routers/
│   │       ├── upload.py      # 日志上传 + 指纹去重
│   │       └── dashboard.py   # 报告看板
│   ├── main.py
│   ├── templates/
│   │   └── dashboard.html     # 可视化看板
│   └── requirements.txt
│
├── agent/                     # 客户端
│   ├── agent_lite.py          # 日志采集与上传
│   └── requirements.txt
│
├── docs/
│   ├── ARCHITECTURE.md        # 架构详解 + 面试要点
│   └── RESUME.md              # 简历包装指南
│
├── docker-compose.yml
├── .env.example
└── README.md
\`\`\`

---

## 核心功能

### 1. 崩溃指纹去重

\`\`\`python
# 算法流程
原始日志 → 提取堆栈 → 取前3层 → MD5哈希 → 查重 → 新崩溃/计数+1
\`\`\`

| 指标 | 说明 |
|------|------|
| 去重维度 | 堆栈前 3 层特征 |
| 哈希算法 | MD5 |
| 计数策略 | 相同指纹 occurrence_count += 1 |

### 2. 可视化看板

- 设备总数统计
- 崩溃次数（去重前 / 去重后）
- Top 设备排行榜
- 最近崩溃列表（含类型标签）

### 3. 多模态检测

| 类型 | 说明 |
|------|------|
| ANR | 应用无响应 |
| JAVA_CRASH | Java 层异常 |
| TOMBSTONE | Native 层崩溃 |

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | FastAPI |
| 数据校验 | Pydantic |
| ORM | SQLAlchemy 2.0 |
| 数据库 | SQLite |
| 模板引擎 | Jinja2 |
| 客户端 | Python requests |

---

## 学习路径

| 阶段 | 目标 | 文档 |
|------|------|------|
| 1. 跑通部署 | 理解系统运行流程 | 本 README |
| 2. 阅读代码 | 掌握核心模块设计 | [ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| 3. 二次开发 | 增加功能（告警、多设备等） | 代码注释 |
| 4. 写进简历 | 项目包装与面试准备 | [RESUME.md](docs/RESUME.md) |

---

## 扩展方向

- [ ] 接入真实 ADB 日志（替换模拟数据）
- [ ] 钉钉 / 企业微信告警推送
- [ ] 多设备并发调度（设备池 + 队列）
- [ ] React + ECharts 前端升级
- [ ] PostgreSQL 替换 SQLite
- [ ] Redis 缓存热点指纹

---

## 截图

### 看板页面

![Dashboard](docs/screenshots/dashboard.png)

### API 文档

![API Docs](docs/screenshots/api_docs.png)

---

## 贡献

欢迎 Issue 和 PR！

\`\`\`bash
# 提交 Issue
# 提交 PR（请先 fork）
\`\`\`

---

## 许可证

[MIT](LICENSE)

> 本项目采用 MIT 协议开源，可自由学习使用。企业级功能（Pro 版）请单独联系。
---

## 关于作者

Android 测试工程师，专注自动化测试与稳定性测试。
- 博客：[CSDN](https://blog.csdn.net/m0_50486420/article/details/162976503?spm=1011.2124.3001.6209)
- 小红书：[半醒散人-测试老兵]
- 💼 **Pro 企业版咨询**：请通过 GitHub Issue 联系我

---

> 如果这个项目对你有帮助，请给个 ⭐ Star！
