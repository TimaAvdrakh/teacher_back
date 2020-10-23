from fastapi import FastAPI
from sql import inserts, selects
from utils import find_date
import datetime
from schemas.schemas import Student, StudentGrade
from typing import List, Optional
from pydantic import BaseModel
app = FastAPI()
key = '1231234sda;nsdsajoi123'


@app.get("/auth/")
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
async def subjects(t_id: int, date: str):
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
async def classes(t_id: int, date: str, subject_i: int):
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
async def root(class_id: int):
    print("Students")
    cn = selects.connect_database()
    q = selects.all_class_students(cn, class_id)
    selects.close_connection(cn)
    return {
        'type': 'students',
        'key': key,
        'students': q['data']
    }


@app.post('/attendance/', status_code=201)
def attendance(sch_i: int, students: List[Student], date: str):
    print('Attendance')
    print(students)
    cn = selects.connect_database()
    q = inserts.attendance(cn, students, sch_i, date)
    selects.close_connection(cn)
    return {
        "message": q
    }


@app.post('/grade/', status_code=200)
async def grades(sch_i: int, students: List[StudentGrade], dt: str):
    print("grades")
    cn = selects.connect_database()
    q = inserts.grade(cn, students, sch_i, dt)
    selects.close_connection(cn)
    return {
        'type': 'grade',
        # 'key': key,
        'message': q
    }


@app.post('/task/', status_code=200)
async def tasks(sch_i: int, lbl: str, dt: str):
    cn = selects.connect_database()
    q = inserts.task(cn, sch_i, lbl, dt)
    selects.close_connection(cn)
    return {
        'type': 'task',
        'message': q
    }


@app.get('/task_date/', status_code=200)
async def task_dates(teacher_i: int, class_i: int, subject_i: int, dt: str):
    print("print next 3 dates")
    cn = selects.connect_database()
    q = inserts.task_dates(cn, teacher_i, class_i, subject_i, dt)
    selects.close_connection(cn)
    return {
        'type': 'task-date',
        'dates': q['date']
    }


@app.get('/dates/', status_code=200)
async def week_dates(date: str):
    print('This Week Dates')
    day, month, year = [int(i) for i in date.split('/')]
    today = datetime.date(year, month, day)
    dates = [today + datetime.timedelta(days=i) for i in range(0 - today.weekday(), 5 - today.weekday())]
    return {
        'dates': dates
    }