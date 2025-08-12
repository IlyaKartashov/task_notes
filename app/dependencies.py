from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends, Path, HTTPException, status

from app.notes.models import Note
from app.notes import crud
from app.database import db_helper


async def note_by_id_dep(
    note_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Note:
    note = await crud.get_note_by_id(session=session, note_id=note_id)
    if note is not None:
        return note

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Note {note_id} is not found!(",
    )
