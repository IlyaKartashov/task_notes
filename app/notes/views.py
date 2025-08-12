from fastapi import APIRouter, status
from fastapi import Depends

from . import crud
from .schemas import (
    NoteAddSchema,
    NoteSchema,
    NoteUpdateSchema,
    NoteUpdatePartialSchema,
)

from app.database import db_helper
from app.dependencies import note_by_id_dep


from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/", response_model=list[NoteSchema])
async def get_notes(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_notes(session=session)


@router.get("/{note_id}/", response_model=NoteSchema)
async def get_note_by_id(
    note: NoteSchema = Depends(note_by_id_dep),
):
    return note


@router.post("/", response_model=NoteSchema)
async def create_note(
    note_in: NoteAddSchema,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_note(session=session, note_in=note_in)


@router.put("/{note_id}/", response_model=NoteSchema)
async def update_note(
    note_update: NoteUpdateSchema,
    note: NoteSchema = Depends(note_by_id_dep),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_note(
        session=session,
        note=note,
        note_update=note_update,
    )


@router.patch("/{note_id}/", response_model=NoteSchema)
async def update_note_partial(
    note_update: NoteUpdatePartialSchema,
    note: NoteSchema = Depends(note_by_id_dep),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_note(
        session=session,
        note=note,
        note_update=note_update,
        partial=True,
    )


@router.delete("/{note_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note: NoteSchema = Depends(note_by_id_dep),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_note(session=session, note=note)
