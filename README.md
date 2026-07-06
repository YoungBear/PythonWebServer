Python Flask HTTPS Web Server，基于 Flask 3.x + Python 3.9

对应 [SpringBoot2Demo](../SpringBoot2Demo) 的 Python 实现，演示使用自签名证书配置 **双向 TLS (mTLS)**。

## 快速开始

```bash
pip install -r requirements.txt
python app.py
```

服务启动后访问 `https://localhost:8888/SpringBoot2Demo/demo/current`（需客户端证书）。

## 验证

```bash
# 不带客户端证书 → 被拒绝
curl -k https://localhost:8888/SpringBoot2Demo/demo/current

# 带客户端证书 → 正常返回
curl -k --cert-type P12 --cert cert/client.p12:'ClientKeyStore@2024' \
  https://localhost:8888/SpringBoot2Demo/demo/current
```
