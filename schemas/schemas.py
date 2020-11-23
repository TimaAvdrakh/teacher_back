from pydantic import BaseModel

class Student(BaseModel):
    student_i: int
    vst: bool = False
    pnt: int

class StudentGrade(Student):
    lbl: str

class StudentPhone(BaseModel):
    id: int
    phone: int