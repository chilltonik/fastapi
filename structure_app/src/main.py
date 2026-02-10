import uvicorn
from api import main_router

from fastapi import FastAPI

app: FastAPI = FastAPI()
app.include_router(main_router)


# python3 main.py
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
