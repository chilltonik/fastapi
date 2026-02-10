from pydantic import BaseModel, Field


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
