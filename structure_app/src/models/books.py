from database import Base
from sqlalchemy.orm import Mapped, mapped_column


class BookModel(Base):
    """
    Docstring for BookModel
    """

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
