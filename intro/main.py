import uvicorn
from fastapi import FastAPI

app: FastAPI = FastAPI()


@app.get("/", summary="main method")
def home() -> str:
    return "Hello world"


# python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
