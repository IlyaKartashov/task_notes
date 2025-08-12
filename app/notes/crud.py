from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Note
from .schemas import NoteAddSchema, NoteUpdateSchema, NoteUpdatePartialSchema


"""
Круды используют сессию базы данных для получения данных из бд, делают асинхронные или синхронные запросы в бд, 
возвращается объект Result, здесь он для аннотации
"""


async def get_notes(session: AsyncSession) -> list[Note]:
    statement = select(Note).order_by(Note.id)  # Запрос через орм не выполняется
    result: Result = await session.execute(
        statement=statement
    )  # Исполнение запроса с await
    notes = (
        result.scalars().all()
    )  # scalars() - объекты в result возврщается тюплами (note,), (note,), result.scalars()-генератор
    # scalars - достает сами данные note note, .all() -> список, .first() - первное значение

    return list(notes)


async def get_note_by_id(session: AsyncSession, note_id: int) -> Note | None:
    return await session.get(Note, note_id)


async def create_note(session: AsyncSession, note_in: NoteAddSchema) -> Note:
    note = Note(**note_in.model_dump())
    session.add(note)  # добавляем в отслеживание
    await session.commit()  # совершаем запрос на создание, взаимодействуем с бд - await
    return note


async def update_note(
    session: AsyncSession,
    note: Note,
    note_update: NoteUpdateSchema | NoteUpdatePartialSchema,
    partial: bool = False,
) -> Note:
    for name, value in note_update.model_dump(exclude_unset=partial).items():
        setattr(note, name, value)
    await session.commit()
    return note


async def delete_note(
    session: AsyncSession,
    note: Note,
) -> None: 
    await session.delete(note)
    await session.commit()
