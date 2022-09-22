from keycloak import KeycloakOpenID
from authlib.integrations.requests_client import OAuth2Session

from fastapi import Security, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from pydantic import Json

from app.core.config import *


# For fastapi docs
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl = SERVER_URL,
    tokenUrl = TOKEN_URL,
)

# For auth check
keycloak_openid = KeycloakOpenID(
    server_url = SERVER_URL,
    client_id = CLIENT_ID,
    realm_name = REALM_NAME,
    client_secret_key = CLIENT_SECRET,
    verify = False
)

# For auth check
def get_idp_public_key():
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )

# Validate token
def get_auth(token: str = Security(oauth2_scheme)) -> Json:
    try:
        return keycloak_openid.decode_token(
            token,
            key = get_idp_public_key(),
            options = {
                "verify_signature": True,
                "verify_aud": False,
                "exp": True,
                "verify": False,

            }
        )

    except Exception as e:
        raise HTTPException(
            status_code = 401,
            detail = str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )