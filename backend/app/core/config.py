from starlette.config import Config


config = Config(".env")

REALM_NAME = config("REALM_NAME")
CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")
SERVER_URL = config("SERVER_URL")
TOKEN_URL = config("TOKEN_URL")