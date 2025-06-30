from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import Base, engine
from .routers import students

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management System")

# Mount the static files relative to this file
app.mount("/", StaticFiles(directory="src/static", html=True), name="static")

# Include API routes
app.include_router(students.router)
