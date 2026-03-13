import asyncio
import io

from app.main import app as fastapi_app

_STATUS = {
    200: "OK", 201: "Created", 204: "No Content",
    400: "Bad Request", 401: "Unauthorized", 404: "Not Found",
    405: "Method Not Allowed", 422: "Unprocessable Entity",
    500: "Internal Server Error",
}


def application(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    query = environ.get("QUERY_STRING", "").encode()
    method = environ.get("REQUEST_METHOD", "GET")
    server = (environ.get("SERVER_NAME", "localhost"),
              int(environ.get("SERVER_PORT", 80)))

    headers = []
    for key, val in environ.items():
        if key.startswith("HTTP_"):
            name = key[5:].lower().replace("_", "-").encode()
            headers.append((name, val.encode()))
        elif key in ("CONTENT_TYPE", "CONTENT_LENGTH") and val:
            headers.append((key.lower().replace("_", "-").encode(), val.encode()))

    length = int(environ.get("CONTENT_LENGTH") or 0)
    body = environ["wsgi.input"].read(length) if length else b""

    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": method,
        "path": path,
        "raw_path": path.encode(),
        "query_string": query,
        "root_path": environ.get("SCRIPT_NAME", ""),
        "scheme": environ.get("wsgi.url_scheme", "http"),
        "server": server,
        "headers": headers,
    }

    status_code = None
    resp_headers = None
    resp_body = io.BytesIO()

    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    async def send(message):
        nonlocal status_code, resp_headers
        if message["type"] == "http.response.start":
            status_code = message["status"]
            resp_headers = [
                (k.decode(), v.decode()) for k, v in message.get("headers", [])
            ]
        elif message["type"] == "http.response.body":
            resp_body.write(message.get("body", b""))

    asyncio.run(fastapi_app(scope, receive, send))

    status_line = f"{status_code} {_STATUS.get(status_code, 'Unknown')}"
    start_response(status_line, resp_headers or [])
    return [resp_body.getvalue()]
