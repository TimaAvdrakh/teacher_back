from pydantic import BaseModel, Field
from typing import Optional


class Student(BaseModel):
    student_i: int
    vst: bool = False
    pnt: int


class StudentGrade(Student):
    lbl: Optional[str] = Field(None, max_length=300)


class StudentPhone(BaseModel):
    id: int
    phone: int