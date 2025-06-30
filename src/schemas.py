from pydantic import BaseModel, Field

class StudentIn(BaseModel):
    id:     int    = Field(..., ge=1)
    name:   str
    course: str

class StudentOut(StudentIn):
    class Config:
        from_attributes = True  # SQLAlchemy → Pydantic
