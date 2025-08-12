from fastapi import FastAPI
from app.notes.views import router as notes_router
from app.database import lifespan

app = FastAPI(lifespan=lifespan ,title="Simple Notes App", version="0.1.0")

app.include_router(notes_router)


@app.get("/")
def root():
    return {"status": "ok"}

