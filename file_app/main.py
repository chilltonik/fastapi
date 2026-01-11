from collections.abc import Generator
from typing import Any, BinaryIO, TextIO

import uvicorn

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse

app: FastAPI = FastAPI()


@app.post("/files", tags=["files"])
async def upload_file(uploaded_file: UploadFile) -> dict[str, Any]:
    """
    Docstring for upload_file

    :param uploaded_file: Description
    :type uploaded_file: UploadFile
    :return: Description
    :rtype: dict[str, Any]
    """
    file = uploaded_file.file
    filename: str | None = uploaded_file.filename

    with open(f"1_{filename}", "wb") as f:
        f.write(file.read())

    return {"success": True, "message": "File is uploaded"}


@app.post("/multiple_files", tags=["files"])
async def upload_files(uploaded_files: list[UploadFile]) -> dict[str, Any]:
    """
    Docstring for upload_files

    :param uploaded_files: Description
    :type uploaded_files: list[UploadFile]
    """
    for uploaded_file in uploaded_files:
        file = uploaded_file.file
        filename: str | None = uploaded_file.filename

        with open(f"1_{filename}", "wb") as f:
            f.write(file.read())
    return {"success": True, "message": "Files are uploaded"}


@app.get("/files/{filename}", tags=["files"])
async def get_file(filename: str) -> FileResponse:
    """
    Docstring for get_file

    :param filename: Description
    :type filename: str
    :return: Description
    :rtype: FileResponse
    """
    return FileResponse(filename)


def iterfile(filename: str) -> Generator[bytes]:
    """
    Docstring for iterfile

    :param filename: Description
    :type filename: str
    """
    with open(filename, "rb") as file:
        while chunk := file.read(1024 * 1024):
            yield chunk


@app.get("/files/streaming/{filename}", tags=["files"])
async def get_streaming_file(filename: str) -> StreamingResponse:
    """
    Docstring for get_streaming_file

    :param filename: Description
    :type filename: str
    """
    return StreamingResponse(
        iterfile(filename=filename), media_type="video/mp4"
    )


# python main.py
# curl.exe -X 'POST' 'http://localhost:8000/files' -H 'accept: application/json' -H 'Content-Type: multipart/form-data' -F 'uploaded_file=@text.txt; type=text/plain'
# curl.exe -X 'GET' 'http://localhost:8000/files/1_text.txt' -H 'accept: application/json'
# curl.exe -X 'GET' 'http://localhost:8000/files/streaming/sea.mp4' -H 'accept: application/json'
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
