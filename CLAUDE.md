# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此仓库中工作时提供指导。

## 构建与运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用（HTTPS 端口 8888，路径 /PythonWebServer/demo/current）
python run.py
```

## 架构

这是一个基于 **Flask 3.1.3 + Python 3.9** 的演示项目，展示使用自签名证书配置 **双向 TLS (mTLS)**。

**包结构**：
- `run.py` — 入口，加载 `.env`，创建 app，根据 `SERVER_PROTOCOL` 选择 HTTP/HTTPS 模式
- `server/__init__.py` — `create_app()` 工厂，加载配置、注册 Blueprint
- `server/config.py` — 路径常量（基于 `__file__` 解析）、Flask 配置
- `server/routes.py` — Blueprint `demo_bp`，暴露 `GET /PythonWebServer/demo/current`
- `server/ssl_context.py` — `create_ssl_context()`，配置 TLS 1.2+、服务端证书链、可选 mTLS

**TLS/mTLS**：
- 使用 `ssl.SSLContext`（`PROTOCOL_TLS_SERVER`）
- 最低 TLS 版本: 1.2
- 客户端证书认证可配置，默认开启（`VERIFY_CLIENT_CERT=true`）
- 服务端证书链: `cert/server.crt` + `cert/server.key`（PEM 格式）
- CA 信任库: `cert/rootca.crt`（PEM 格式）

**配置**: 通过 `.env` 文件设置环境变量，`python-dotenv` 自动加载。

**依赖**: Flask 3.1.3, python-dotenv 1.2.1

**证书** 复用 SpringBoot2Demo 预生成的自签名证书，存放于 `cert/`。`cert/client.p12` 为测试用客户端证书。

## 对应项目

本项目的 Java 版本位于 `../SpringBoot2Demo/`（Spring Boot 3.5.14 + JDK 21）。两个项目接口、端口、证书链完全对应。
