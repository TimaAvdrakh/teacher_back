from pydantic import BaseModel

class Student(BaseModel):
    student_i: int
    vst: bool = False
    pnt: int