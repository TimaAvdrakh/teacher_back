from fastapi import FastAPI
from sql import inserts, selects
from utils import find_date
import datetime
from schemas.schemas import Student
from typing import List, Optional
from pydantic import BaseModel
app = FastAPI()
key = '1231234sda;nsdsajoi123'


@app.post("/auth/")
async def auth(phone: str):
    print(phone)
    obj = {}
    obj['uid'] = 1
    obj['oid'] = 1
    cn = selects.connect_database()
    rq = selects.teacher_org(cn, obj['oid'])
    selects.close_connection(cn)

    return {
        'type': 'auth',
        'uid': obj['uid'],
        'school': rq['school'],
        'address': " Алматы д-14 кв-13",
        't_id': '19'
    }


@app.get('/subjects/')
def subjects(t_id: int, date: str):
    cn = selects.connect_database()
    # new_date = utils.find_date(date)
    # find_date
    query = selects.teacher_subjects(cn, t_id, new_date)
    selects.close_connection(cn)
    return {
        'type': 'subjects',
        'key': key,
        'subjects': query['data']
    }

@app.get('/classes/')
def classes(t_id: int, date: str, subject_i: int):
    time = find_date.find_date(date)
    cn = selects.connect_database()
    print(time)
    q = selects.teacher_classes(cn, t_id, subject_i, time)
    selects.close_connection(cn)

    return {
        'type': 'classes',
        'key': key,
        'classes': q
    }


@app.get('/students/')
def root(class_id: int):
    print("Students")
    cn = selects.connect_database()
    q = selects.all_class_students(cn, class_id)
    selects.close_connection(cn)
    return {
        'type': 'students',
        'key': key,
        'students': q['data']
    }


@app.post('/attendance/', status_code=200)
def attendance(sch_i: int, students: List[Student], date: str):
    print('Attendance')
    print(students)
    cn = selects.connect_database()
    q = inserts.attendance(cn, students, sch_i, date)
    selects.close_connection(cn)
    return {}


@app.post('/grade/', status_code=200)
def grades(sch_i: int, dt: str):
    print("grades")
    cn = selects.connect_database()

    selects.close_connection(cn)
    return {
        'type': 'grade',
        # 'key': key,
        'message': q
    }


@app.post('/task/', status_code=201)
def tasks(sch_i: int, lbl: str, ):
    cn = selects.connect_database()
    # q =
    select.close_connection(cn)
    return {
        'type': 'task',
        'message': q
    }
