from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Note(Base):
    __tablename__ = "notes"

    title: Mapped[str] = mapped_column(
        String(100)
    )  # Mapped указывает на то что это именно колонки в таблице
    content: Mapped[str] = mapped_column(String(900))
