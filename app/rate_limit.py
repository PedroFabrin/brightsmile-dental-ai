from fastapi import Request
from slowapi import Limiter

from app.config import get_settings


def client_ip(request: Request) -> str:
    """Client IP used as the rate-limit key.

    Behind a proxy (e.g. Hugging Face Spaces) the socket address is the proxy, so with
    TRUST_PROXY_HEADERS=true the last X-Forwarded-For entry (added by the nearest proxy) is used.
    """
    if get_settings().trust_proxy_headers:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[-1].strip()
    return request.client.host if request.client else "unknown"


limiter = Limiter(key_func=client_ip, storage_uri="memory://")


def chat_limit() -> str:
    return f"{get_settings().rate_limit_per_minute}/minute"
