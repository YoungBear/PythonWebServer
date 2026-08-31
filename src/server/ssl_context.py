import ssl

from . import config


def create_ssl_context():
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.load_cert_chain(
        certfile=config.SERVER_CERT,
        keyfile=config.SERVER_KEY,
        password=config.SERVER_KEY_PASSWORD,
    )
    ctx.load_verify_locations(cafile=config.ROOTCA_CERT)
    ctx.verify_mode = ssl.CERT_REQUIRED if config.VERIFY_CLIENT_CERT else ssl.CERT_NONE
    return ctx
