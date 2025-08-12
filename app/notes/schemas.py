from pydantic import BaseModel, ConfigDict


class NoteBaseSchema(BaseModel):  # Схема для пользователя не дожна иметь поля id
    title: str
    content: str


class NoteSchema(NoteBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class NoteAddSchema(NoteBaseSchema):
    pass


class NoteUpdateSchema(NoteAddSchema):
    pass


class NoteUpdatePartialSchema(NoteUpdateSchema):
    title: str | None = None
    content: str | None = None
