import time

import uvicorn

from fastapi import FastAPI, Request, Response

app: FastAPI = FastAPI()


@app.middleware("http")
async def my_middleware(request: Request, call_next: callable):  # type: ignore
    ip_address = request.client.host
    print(f"IP address: {ip_address}")
    # if ip_address in ["127.0.0.1", "localhost"]:
    #     return Response(status_code=429, content="Limit requesting")

    start = time.perf_counter()
    response = await call_next(request)  # type: ignore
    end = time.perf_counter() - start
    print(f"Time: {end}")

    response.headers["X-Special"] = "I'm special"
    return response


@app.get("/", summary="main method")
def home() -> list[dict[str, int | str]]:
    time.sleep(5)
    return [{"id": 1, "name": "Toni"}]


# python3 main.py
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
