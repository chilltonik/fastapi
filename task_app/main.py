import asyncio
import time

import uvicorn

from fastapi import BackgroundTasks, FastAPI

app: FastAPI = FastAPI()


def sync_task() -> None:
    """
    Docstring for sync_task
    """
    time.sleep(3)
    print("Send email")


async def async_task() -> None:
    """
    Docstring for async_task
    """
    await asyncio.sleep(3)
    print("Side api requesting")


@app.post("/")
async def some_route(background_tasks: BackgroundTasks) -> dict[str, bool]:
    """
    Docstring for some_route

    :param background_tasks: Description
    :type background_tasks: BackgroundTasks
    :return: Description
    :rtype: dict[str, bool]
    """
    ...
    # sync_task()
    # asyncio.create_task(async_task())
    background_tasks.add_task(sync_task)
    return {"status": True}


# python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
