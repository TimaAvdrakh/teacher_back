from fastapi import FastAPI
from sql import inserts, selects
from utils.find_date import find_date
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
    new_date = find_date.find_date(date)
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
    time = find_date(date)
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


d = {
        1: 'Понидельник',
        2: 'Вторник',
        3: 'Среда',
        4: 'Четверг',
        5: 'Пятница',
        6: 'Суббота',
    }

@app.get('/dates/', status_code=200)
async def week_dates(date: str):
    print('This Week Dates')
    day, month, year = [int(i) for i in date.split('/')]
    today = datetime.date(year, month, day)
    dates = [[i, today + datetime.timedelta(days=i)] for i in range(0 - today.weekday(), 6 - today.weekday())]
    d = ('Понедельник','Вторник','Среда','Четверг','Пятница', 'Суббота')
    ans = []
    count = 0
    for date in dates:
        year, month, day = [i for i in str(date[1]).split('-')]
        s = str(date[0])
        a = f"{day}/{month}/{year}"
        ans.append([d[count], a])
        count += 1



    return {
        'dates': dates
    }

@app.get('/journal/', status_code=200)
async def teacher_journal(teacher_i: int, date: str):
    print("Day Journal")
    cn = selects.connect_database()
    time = find_date(date)
    q = selects.teacher_journal(cn, teacher_i, time)
    day, month, year = [i for i in date.split('/')]
    date = f"{year}-{month}-{day}"
    ans = []
    print(q)
    for row in q:
        # sc.sch_i, sc.s_time, sub.lbl, cl.lbl
        query = selects.journal_task(cn, row[0], date)
        hour = row[1].seconds//3600
        minutes = row[1].seconds-hour
        temp = {
            "time": f"{row[1]}",
            "subject": row[2],
            "class": row[3],
            "homework": query,
        }
        ans.append(temp)
    return {
        'data': ans
    }