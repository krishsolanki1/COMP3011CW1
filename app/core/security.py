import secrets

from fastapi import Header, HTTPException, status

from app.core.config import settings


def require_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    # CW1 polish: compare_digest avoids tiny timing leaks vs plain string ==
    provided = x_api_key or ""
    expected = settings.api_key or ""

    if not provided or not secrets.compare_digest(provided, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )

    return provided