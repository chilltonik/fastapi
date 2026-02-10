from typing import Any

from database import Base, engine
from models.books import BookModel
from schemas.books import BookAddSchema
from sqlalchemy import Result, Select, select

from api.dependencies import SessionDep
from fastapi import APIRouter

router: APIRouter = APIRouter()


@router.post("/setup_db", tags=["DB"])
async def setup_database() -> dict[str, Any]:
    """
    Docstring for setup_database

    :return: Description
    :rtype: dict[str, Any]
    """
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    return {"success": True, "message": "Setup db"}


@router.post("/books", tags=["books"])
async def add_book(book: BookAddSchema, session: SessionDep) -> dict[str, Any]:
    """
    Docstring for add_book

    :param book: Description
    :type book: BookAddSchema
    :param session: Description
    :type session: SessionDep
    :return: Description
    :rtype: dict[str, Any]
    """
    new_book: BookModel = BookModel()
    new_book.title = book.title
    new_book.author = book.author

    session.add(new_book)

    await session.commit()
    return {"success": True, "message": "Book added"}


@router.get("/books", tags=["books"])
async def get_books(session: SessionDep):  # type: ignore[no-untyped-def]
    """
    Docstring for get_books

    :param session: Description
    :type session: SessionDep
    :return: Description
    :rtype: tuple[BookModel]
    """
    query: Select[tuple[BookModel]] = select(BookModel)

    result: Result[tuple[BookModel]] = await session.execute(query)
    return result.scalars().all()
