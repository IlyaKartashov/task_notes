from fastapi import FastAPI

from contextlib import asynccontextmanager

from asyncio import current_task

from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings

"""Простой способ создания таблиц через sqlalchemy - Base.metadata.create_all(engine)
    metadata - объект хранит информацию о всех таблицах которые есть
    crate_all - синхронная функция, которую приходится оборачивать в асинхронный код: создать async-движок,
      в котором сделать run_sync(.create_all())"""


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine = create_async_engine(url=url, echo=echo)  # True для отладки
        self.session_factory = async_sessionmaker(  # autoflush - подготовка к комиту, expire_on_commit - автоудалние информации из сессии
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        """Актуальная сессия при каждом запросе, эта функция принимает фабрику сессий"""
        session = async_scoped_session(
            session_factory=self.session_factory, scopefunc=current_task
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        async with session() as sess:
            yield sess
            await session.remove()


db_helper = DatabaseHelper(
    url=settings.db_url,
    echo=settings.db_echo,
)


# Модель алхимии от которой наследуются остальные
class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


# Mapped указывает на то что это именно колонки в таблице


# Cоздание базы данных для lifespan (on startup приложения)


@asynccontextmanager
async def lifespan(app: FastAPI):  # по документации
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
