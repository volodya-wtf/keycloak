import json

from authlib.integrations.requests_client import OAuth2Session
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.config import Config


app = FastAPI(title="Демонстрация авторизации", openapi_prefix="/api/v1")


config = Config(".env")

REALM = config("REALM")
CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET= config("CLIENT_SECRET")


@app.get("/endpoint/{token}", tags=["Access token required"])
def auth(request: Request, token: str):
    oauth = OAuth2Session(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    result = oauth.introspect_token(
        url=f"https://172.19.0.2/auth/realms/{REALM}/protocol/openid-connect/token/introspect", token=token, verify=False)
    content = json.loads(result.content.decode())
    
    # Если не можем произвести интроспекцию для токена -> 401
    if not content['active'] or not content:
        raise HTTPException(status_code=401, detail="Token expired or invalid")
    else:
        return content
