Python Flask HTTPS Web Server，基于 Flask 3.1.3 + Python 3.9

对应 [SpringBoot2Demo](../SpringBoot2Demo) 的 Python 实现，演示使用自签名证书配置 **双向 TLS (mTLS)**。

## 快速开始

```bash
pip install -r requirements.txt
python run.py
```

服务启动后访问 `https://localhost:8888/PythonWebServer/demo/current`（需客户端证书）。

## 配置

通过 `.env` 文件配置：

```
SERVER_PROTOCOL=https          # http 或 https（默认 https）
VERIFY_CLIENT_CERT=true        # 是否校验客户端证书（默认 true，仅 HTTPS 时生效）
SERVER_HOST=0.0.0.0            # 监听地址（默认 0.0.0.0）
SERVER_PORT=8888               # 监听端口（默认 8888）
CONTEXT_PATH=/PythonWebServer  # 上下文路径前缀（默认 /PythonWebServer）
```

设为 `VERIFY_CLIENT_CERT=false` 即可跳过客户端证书校验，方便开发调试。

## 验证

```bash
# 不带客户端证书 → 被拒绝
curl -k https://localhost:8888/PythonWebServer/demo/current

# 带客户端证书 → 正常返回
curl -k --cert-type P12 --cert cert/client.p12:'ClientKeyStore@2024' \
  https://localhost:8888/PythonWebServer/demo/current
```
