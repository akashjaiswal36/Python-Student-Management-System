from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import Base, engine
from .routers import students

Base.metadata.create_all(bind=engine)     # create table if not exist

app = FastAPI(title="Student Management System")
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
app.include_router(students.router)
