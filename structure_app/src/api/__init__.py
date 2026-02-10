from fastapi import APIRouter

from .books import router as books_router

main_router: APIRouter = APIRouter()
main_router.include_router(books_router)

__all__: list[str] = ["main_router"]
