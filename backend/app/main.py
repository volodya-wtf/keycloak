from fastapi import FastAPI, Request

from app.core.security import get_auth

app = FastAPI(title="Демонстрация авторизации", openapi_prefix="/api/v1")


@app.get("/endpoint", tags=["Access token required in header"])
def auth(request: Request):
    # Извлекаем token из заголовка
    header = request.headers.get('Authorization')
    if header and header.startswith("Bearer "):
        token = header[len("Bearer "):]
    else:
        raise HTTPException(status_code=401, detail="Access token required in header")

    return get_auth(token)
