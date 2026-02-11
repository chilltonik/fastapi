from collections.abc import AsyncGenerator
from typing import Annotated, Any

import uvicorn
from pydantic import BaseModel, Field
from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from fastapi import Depends, FastAPI

app: FastAPI = FastAPI()
engine: AsyncEngine = create_async_engine("sqlite+aiosqlite:///books.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[Any, Any]:
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class PaginationParams(BaseModel):
    limit: int = Field(default=5, ge=0, le=100, description="rows limit")
    offset: int = Field(default=0, ge=0, description="Offset")


PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]


class Base(DeclarativeBase):
    pass


class BookModel(Base):
    """
    Docstring for BookModel
    """

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]


@app.post("/setup_db", tags=["DB"])
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


class BookAddSchema(BaseModel):
    """
    Docstring for BookAddSchema
    """

    title: str = Field(max_length=100)
    author: str = Field(max_length=10)


class BookSchema(BookAddSchema):
    """
    Docstring for BookSchema
    """

    id: int


@app.post("/books", tags=["books"])
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


@app.get("/books", tags=["books"])
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


@app.get("/books_limit", tags=["books"])
async def get_books_limit(
    session: SessionDep, pagination: PaginationDep
) -> list[BookSchema]:
    """
    Docstring for get_books

    :param session: Description
    :type session: SessionDep
    :return: Description
    :rtype: tuple[BookModel]
    """
    query: Select[tuple[BookModel]] = (
        select(BookModel)
        .limit(limit=pagination.limit)
        .offset(offset=pagination.offset)
    )

    result: Result[tuple[BookModel]] = await session.execute(query)
    return result.scalars().all()  # type: ignore


# python3 main.py
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
