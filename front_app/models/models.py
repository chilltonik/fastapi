from pydantic import BaseModel


class NewBook(BaseModel):
    """
    Docstring for NewBook
    """

    id: str
    name: str
    size: int
