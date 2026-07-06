# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此仓库中工作时提供指导。

## 构建与运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用（HTTPS 端口 8888，路径 /PythonWebServer/demo/current）
python app.py
```

## 架构

这是一个基于 **Flask 3.1.3 + Python 3.9** 的演示项目，展示使用自签名证书配置 **双向 TLS (mTLS)**。

**单文件 Flask 应用**（`app.py`）：
- 使用 `ssl.SSLContext`（`PROTOCOL_TLS_SERVER`）配置 HTTPS
- 最低 TLS 版本: 1.2
- 要求客户端证书认证（`ssl.CERT_REQUIRED`）
- 暴露 `GET /PythonWebServer/demo/current` 接口，以 JSON 格式返回当前时间（`zonedDateTime` + `timestamp`）
- 服务端证书链: `cert/server.crt` + `cert/server.key`（PEM 格式）
- CA 信任库: `cert/rootca.crt`（PEM 格式）

**依赖**: Flask 3.1.3

**证书** 复用 SpringBoot2Demo 预生成的自签名证书，存放于 `cert/`。`cert/client.p12` 为测试用客户端证书。

## 对应项目

本项目的 Java 版本位于 `../SpringBoot2Demo/`（Spring Boot 3.5.14 + JDK 21）。两个项目接口、端口、证书链完全对应。
