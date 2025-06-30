from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/api/students", tags=["students"])

def get_db():
    db = database.SessionLocal()
    try:   yield db
    finally: db.close()

@router.get("/", response_model=list[schemas.StudentOut])
def all_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

@router.get("/{student_id}", response_model=schemas.StudentOut)
def one_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).get(student_id)
    if not student:
        raise HTTPException(404, "Student not found")
    return student

@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schemas.StudentOut)
def add_student(s: schemas.StudentIn, db: Session = Depends(get_db)):
    db.add(models.Student(**s.model_dump()))
    db.commit()
    return s

@router.delete("/{student_id}", status_code=status.HTTP_200_OK)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    deleted = db.query(models.Student).filter_by(id=student_id).delete()
    db.commit()
    if not deleted:
        raise HTTPException(404, "Student not found")
