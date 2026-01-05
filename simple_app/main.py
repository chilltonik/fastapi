import json
from pathlib import Path
from typing import Any, TextIO

import uvicorn
from models import NewBook

from fastapi import FastAPI, HTTPException

app: FastAPI = FastAPI()


@app.get("/books", tags=["books"], summary="get all books")
def get_books() -> dict[str, dict[str, Any]]:
    """
    Docstring for get_books

    :return: Description
    :rtype: dict[str, dict[str, Any]]
    """
    data: dict[str, dict[str, Any]] | None = None
    file: TextIO
    with open(Path("books.json")) as file:
        data = json.load(file)
    if data is not None:
        return data
    raise HTTPException(status_code=404, detail="Data is not founded")


@app.get("/books/{book_id}", tags=["books"], summary="get book by id")
def get_book_by_id(book_id: str) -> dict[str, Any]:
    """
    Docstring for get_book_by_id

    :param book_id: Description
    :type book_id: str
    :return: Description
    :rtype: dict[str, Any]
    """
    books: dict[str, dict[str, Any]] = get_books()
    if book_id in books.keys():
        return books[book_id]
    raise HTTPException(status_code=404, detail="Wrong book_id")


@app.post("/books", tags=["books"], summary="add new book")
def add_book(book: NewBook) -> dict[str, Any]:
    """
    Docstring for add_book

    :param book: Description
    :type book: NewBook
    :return: Description
    :rtype: dict[str, Any]
    """
    books: dict[str, dict[str, Any]] = get_books()
    books[book.id] = {"id": book.id, "name": book.name, "size": book.size}
    file: TextIO
    with open("books.json", "w+", encoding="utf-8") as file:
        json.dump(books, file, indent=4)
    return {"success": True, "message": "New book successfully added"}


# python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
