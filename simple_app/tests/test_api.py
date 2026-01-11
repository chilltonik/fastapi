import pytest
from httpx import ASGITransport, AsyncClient
from main import app

from fastapi import Response


# pytest -v -s
def func(num: int) -> float:
    """
    Docstring for func

    :param num: Description
    :type num: int
    :return: Description
    :rtype: float
    """
    return 1 / num


def test_func() -> None:
    """
    Docstring for test_func
    """
    assert func(1) == 1
    assert func(2) == 0.5


@pytest.mark.asyncio
async def test_get_books() -> None:
    """
    Docstring for test_get_books
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.get("books")
        assert response.status_code == 200

        data = response.json()
        assert type(data) is dict


@pytest.mark.asyncio
async def test_add_books() -> None:
    """
    Docstring for test_add_books
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response: Response = await ac.post(
            "books", json={"id": "5", "name": "gfg", "size": 1024}
        )
        assert response.status_code == 200

        data = response.json()
        assert data == {
            "success": True,
            "message": "New book successfully added",
        }
