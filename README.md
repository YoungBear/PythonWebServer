# Python Flask HTTPS Web Server

基于 Flask 3.1.3 + Python 3.12 的演示项目，对应 [SpringBoot2Demo](../SpringBoot2Demo) 的 Python 实现。

## 特性

- **HTTP / HTTPS 双模式** — 通过配置切换，开发调试无需证书
- **双向 TLS (mTLS)** — 自签名证书，可配置是否校验客户端证书
- **生产级 WSGI 服务器** — 使用 waitress 替代 Flask 开发服务器
- **健康检查** — `GET /health`，始终在根路径，返回 `{"status": "UP", "timestamp": "..."}`
- **JSON 错误响应** — 所有 HTTP 错误统一返回 JSON 格式
- **日志轮转** — 控制台 + 文件双输出，按天轮转保留 30 天
- **API 文档** — Swagger UI（`/apidocs/`），OpenAPI 3.0 格式
- **可配置** — 协议、地址、端口、上下文路径、日志级别均可通过 .env 配置

## API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| GET | `/apidocs/` | Swagger UI API 文档 |
| GET | `/apispec_1.json` | OpenAPI 3.0 规范 JSON |
| GET | `{CONTEXT_PATH}/demo/current` | 当前时间 |

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试
python3 -m pytest tests/ -v

# 启动应用
python run.py
```

## 配置

通过 `.env` 文件配置：

```
SERVER_PROTOCOL=https          # http 或 https（默认 https）
VERIFY_CLIENT_CERT=true        # 是否校验客户端证书（默认 true，仅 HTTPS 生效）
SERVER_HOST=0.0.0.0            # 监听地址（默认 0.0.0.0）
SERVER_PORT=8888               # 监听端口（默认 8888）
CONTEXT_PATH=/PythonWebServer  # 上下文路径前缀（默认 /PythonWebServer）
LOG_LEVEL=INFO                 # 日志级别（默认 INFO）
SERVER_KEY_PASSWORD=...        # 证书密钥密码
```

## 项目结构

项目采用 PyPA 推荐的 **src-layout** 结构，源代码统一置于 `src/` 目录下。

```
PythonWebServer/
├── src/
│   └── server/                   # 应用主包
│       ├── __init__.py           # Flask 工厂 (create_app)、错误处理、健康检查
│       ├── config.py             # 路径常量 (cert/、logs/) 与运行时配置 (从 .env 读取)
│       ├── routes.py             # Blueprint demo_bp，暴露 GET {CONTEXT_PATH}/demo/current
│       ├── swagger.py            # Blueprint swagger_bp，自建 Swagger UI + OpenAPI 3.0 规范
│       └── ssl_context.py        # create_ssl_context()，TLS 1.2+ 证书链与 mTLS 配置
├── tests/                        # pytest 测试套件 (17 个用例)
│   ├── conftest.py               # Fixture: Flask test client
│   ├── test_health.py            # /health 端点
│   ├── test_demo.py              # /demo/current 端点
│   ├── test_errors.py            # 404/405 错误处理
│   └── test_swagger.py           # Swagger 端点
├── cert/                         # 自签名 TLS 证书 (复用 SpringBoot2Demo)
│   ├── server.crt                # 服务端证书 (PEM)
│   ├── server.key                # 服务端私钥 (PEM, 密码保护)
│   ├── rootca.crt                # CA 根证书 (PEM)
│   └── client.p12                # 测试用客户端证书 (PKCS#12)
├── docs/                         # 设计文档
├── logs/                         # 日志输出 (每日轮转，保留 30 天)
├── run.py                        # 应用入口：加载 .env → 配置日志 → 创建 app → waitress 启动
├── pyproject.toml                # 项目元数据与 setuptools src-layout 配置
├── requirements.txt              # 运行时依赖 (Flask, waitress, python-dotenv)
├── .env                          # 本地环境变量 (不纳入版本控制)
└── README.md
```

## 验证

```bash
# 健康检查
curl -k https://localhost:8888/health

# Swagger API 文档
open https://localhost:8888/apidocs/

# 不带客户端证书 → 被拒绝
curl -k https://localhost:8888/PythonWebServer/demo/current

# 带客户端证书 → 正常返回
curl -k --cert-type P12 --cert cert/client.p12:'ClientKeyStore@2024' \
  https://localhost:8888/PythonWebServer/demo/current

# HTTP 模式
SERVER_PROTOCOL=http python run.py
curl http://localhost:8888/PythonWebServer/demo/current
```
