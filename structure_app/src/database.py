from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

engine: AsyncEngine = create_async_engine("sqlite+aiosqlite:///books.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[Any, Any]:
    async with new_session() as session:
        yield session


class Base(DeclarativeBase):
    pass
