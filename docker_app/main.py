from typing import Any

import uvicorn

from fastapi import FastAPI

app: FastAPI = FastAPI()


@app.get("/users")
async def get_users() -> list[dict[str, Any]]:
    ...
    return [{"id": 1, "name": "Toni"}]


# python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
