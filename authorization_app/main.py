from typing import Any

import uvicorn
from authx import AuthX, AuthXConfig
from pydantic import BaseModel

from fastapi import Depends, FastAPI, HTTPException, Response

app: FastAPI = FastAPI()

config: AuthXConfig = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security: AuthX = AuthX(config=config)


class UserLoginSchema(BaseModel):
    """
    Docstring for UserLoginSchema
    """

    username: str
    password: str


@app.post("/login")
def login(credentials: UserLoginSchema, response: Response) -> dict[str, Any]:
    """
    Docstring for login

    :param credentials: Description
    :type credentials: UserLoginSchema
    :param response: Description
    :type response: Response
    """
    if credentials.username == "test" and credentials.password == "test":
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)

        return {"success_token": token}
    raise HTTPException(
        status_code=401, detail="Incorrect username or password"
    )


@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected() -> dict[str, Any]:
    """
    Docstring for protected
    """
    return {"data": "TOP_SECRET"}


# python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
