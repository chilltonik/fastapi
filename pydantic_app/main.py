from typing import Any

import uvicorn
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from fastapi import FastAPI

app: FastAPI = FastAPI()


class UserSchema(BaseModel):
    """
    Docstring for UserSchema
    """

    email: EmailStr
    bio: str | None = Field(max_length=1000, default=None)

    model_config: ConfigDict = ConfigDict(extra="forbid")  # type: ignore[misc]


class UserAgeSchema(UserSchema):
    """
    Docstring for UserAgeSchema
    """

    age: int = Field(ge=0, le=130)


def process(data: dict[str, Any]) -> None:
    """
    Docstring for process

    :param data: Description
    :type data: dict[str, Any]
    """
    data["age"] += 1


def main() -> None:
    data: dict[str, Any] = {
        "email": "wsw@mail.com",
        "bio": None,
        "age": 12,
        # "gender": "male",
    }

    user: UserAgeSchema = UserAgeSchema(**data)
    print(repr(user))


# FastAPI
users: list[UserSchema] = []


@app.post("/users", tags=["users"], summary="Add user")
def add_user(user: UserAgeSchema) -> dict[str, Any]:
    users.append(user)
    return {"success": True, "message": "User added"}


@app.get("/users", tags=["users"], summary="Get user")
def get_users() -> list[UserSchema]:
    return users


# python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
