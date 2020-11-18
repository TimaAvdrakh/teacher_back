from fastapi import FastAPI, Body, Header, Request, BackgroundTasks, HTTPException
from sql import inserts, selects
from utils.find_date import find_date
import datetime
from schemas.schemas import Student, StudentGrade
from typing import List, Optional
from pydantic import BaseModel
import jwt
from redis_utils import my_redis


app = FastAPI()
key = 'asadfasdkfjasdif[jasdifasd[oij'
# def check_jwt(jwt, key):
#     try:
#         jwt.decode(jwt, key, algorithms=["HS256"])
#         print("JWT VALID")
#         return True
#     except jwt.exceptions.InvalidSignatureError or jwt.exceptions.ExpiredSignatureError:
#         print("JWT Error")
#         raise jwt.exceptions.ExpiredSignatureError


@app.middleware("http")
async def check_auth(request: Request, call_next):
    print("MIDDLEWARE")
    print(dir(request.url))
    response = await call_next(request)
    return response

@app.get('/checkredis')
async def check(phone:str, ):
    r = my_redis.RedisDB()
    return r.read(phone)

@app.get("/auth1/")
async def auth(phone: str, jwt_token: Optional[str] = None, debug: Optional[bool] = False):
    obj = {}
    if debug:
        try:
            r = my_redis.RedisDB()
            data = r.read(phone)
            print(data)
            # if data:
            obj['uid'] = data['uid']
            obj['oid'] = data['oid']
            obj['sk'] = data['sk']

            jwt.decode(jwt, data['sk'], algorithms=["HS256"])
        except:
            print("JWT Error")
            raise HTTPException(status_code=400, detail="Authentication Failed JWT ERROR")
    else:
        obj['uid'] = 111
        obj['oid'] = 1
        obj['sk'] = 'fakefakefake'

    cn = selects.connect_database()
    rq = selects.teacher_org(cn, obj['oid'])
    t_id = selects.get_teacher_id(obj['uid'])
    selects.close_connection(cn)
    return {
        'type': 'auth',
        'uid': obj['uid'],
        'school': rq['school'],
        'address': rq['address'],
        't_id': str(t_id[0]),
        'key': obj['sk']
    }


@app.get("/auth/")
async def auth(phone: str, jwt_token: Optional[str] = None):
    print(phone)
    obj = {}
    obj['uid'] = 111
    obj['oid'] = 1
    obj['ti'] = 19
    cn = selects.connect_database()
    rq = selects.teacher_org(cn, obj['oid'])
    print(rq)
    t_id = selects.get_teacher_id(obj['uid'])
    selects.close_connection(cn)
    print({
        'type': 'auth',
        'uid': obj['uid'],
        'school': rq['school'],
        'address': rq['address'],
        't_id': t_id[0]
    })
    return {
        'type': 'auth',
        'uid': obj['uid'],
        'school': rq['school'],
        'address': rq['address'],
        't_id': str(t_id[0]),
        'key': key
    }

@app.get('/subjects/')
async def subjects(t_id: int, date: str, jwt_token: Optional[str] = None):
    cn = selects.connect_database()
    date = [i for i in date.split(' ')]
    date = date[1]
    new_date = find_date(date)
    query = selects.teacher_subjects(cn, t_id, new_date)
    selects.close_connection(cn)
    return {
        'type': 'subjects',
        'key': key,
        'subjects': query['data']
    }


@app.get('/classes/')
async def classes(t_id: int, date: str, subject_i: int, jwt_token: Optional[str] = None):
    date = [i for i in date.split(' ')]
    date = date[1]
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
async def root(class_id: int, jwt_token: Optional[str] = None):
    print("Students")
    cn = selects.connect_database()
    q = selects.all_class_students(cn, class_id)
    selects.close_connection(cn)
    return {
        'type': 'students',
        'key': key,
        'students': q['data']
    }

@app.get('/students/test/')
async def get(class_id:int , subject_i:int, jwt_token: Optional[str] = None):
    print("ALL STUDENT DATA")
    q = selects.all_class_with_final(class_id, subject_i)

    return q

@app.post('/attendance/', status_code=201)
async def attendance(students: List[Student], date: str , sch_i: int, jwt_token: Optional[str]=None):
    print('Attendance')
    print(students)
    cn = selects.connect_database()
    q = inserts.attendance(cn, students, sch_i, date)
    selects.close_connection(cn)
    return {
        "type": "attendace",
        "message": q
    }


@app.post('/grade/', status_code=201)
async def grades(sch_i: int, students: List[StudentGrade], dt: str, jwt_token: Optional[str] = None):
    print("grades")
    cn = selects.connect_database()
    q = inserts.grade(cn, students, sch_i, dt)
    selects.close_connection(cn)
    return {
        'type': 'grade',
        # 'key': key,
        'message': q
    }


@app.post('/task/', status_code=201)
async def tasks(sch_i: int,  dt: str, jwt_token: Optional[str] = None, lbl: str = Body(default="Домашка", embed=True)):
    cn = selects.connect_database()
    q = inserts.task(cn, sch_i, lbl, dt)
    selects.close_connection(cn)
    return {
        'type': 'task',
        'message': q
    }


@app.get('/task_date/', status_code=200)
async def task_dates(teacher_i: int, class_i: int, subject_i: int, dt: str, jwt_token: Optional[str] = None):
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
    dates = [[i, today + datetime.timedelta(days=i)] for i in range(0 - today.weekday(), 6 - today.weekday())]
    d = ['Понедельник','Вторник','Среда','Четверг','Пятница', 'Суббота']
    ans = []
    count = 0
    for date in dates:

        year, month, day = [i for i in str(date[1]).split('-')]
        a = f"{day}/{month}/{year}"
        ans.append([d[count], a])
        count += 1

    return {
        'dates': ans
    }


@app.get('/journal/', status_code=200)
async def teacher_journal(teacher_i: int, date: str, jwt_token: Optional[str]):
    print("Day Journal")
    cn = selects.connect_database()
    date = [i for i in date.split(' ')]
    date = date[1]
    time = find_date(date)
    q = selects.teacher_journal(cn, teacher_i, time)
    day, month, year = [i for i in date.split('/')]
    date = f"{year}-{month}-{day}"
    ans = []
    counter = 1
    print(q)
    for row in q:
        # sc.sch_i, sc.s_time, sub.lbl, cl.lbl
        query = selects.journal_task(cn, row[0], date)
        temp = {
            "id": counter,
            "time": f"{row[1]}",
            "subject": row[2],
            "class": row[3],
            "homework": query,
            "room": f"Кабинет №{row[4]}"
        }

        ans.append(temp)
        counter += 1

    return {
        'data': ans
    }


@app.get('/profile/class')
async def teacher_class(teacher_i: int, jwt_token: Optional[str] = None):
    cn = selects.connect_database()
    data = selects.p_class(cn, teacher_i)
    selects.close_connection(cn)
    return data


@app.get('/profile/parents')
async def parents_of_student(student_i: int, jwt_token: Optional[str] = None):
    cn = selects.connect_database()
    data = selects.student_parents(cn, student_i)
    selects.close_connection(cn)
    return {
        "parents": data
    }


@app.post('/notification/all_class/')
async def all_class_notify(jwt_token: Optional[str] = None,
                           class_i: int = Body(default=None, embed=True),
                           message: str = Body(default='Important Message', embed=True)):

    cn = selects.connect_database()
    selects.class_students_id(cn, class_i, message)
    selects.close_connection(cn)

    return {
        "message": "Notification send to all class"
    }


@app.post('/notification/class_selected')
async def notify_selected_students(jwt_token: Optional[str] = None, students: List[int] = Body(default=[], embed=True), message: str = Body(default='None', embed=True)):
    cn = selects.connect_database()
    ## Todo send To selected students

    for student_i in students:
        inserts.student_log_notification(cn, student_i, message)
    selects.close_connection(cn)
    return {

        "message": "Notification send"
    }


@app.post('/notification/parents/')
async def notify_class_parents(jwt_token: Optional[str] = None,
                               teacher_i: int = Body(None, embed=True),
                               message: str = Body(None,embed=True)):
    cn = selects.connect_database()
    ## Todo send to all parents of the class
    selects.close_connection(cn)
    return {
        "message": "Send to parents of whole class"
    }


@app.post('/finaclass/')
async def get_class_final(jwt_token: Optional[str] = None,
                          students: List[int] = Body(embed=True,default = []),
                          subject_i: int = Body(default=-1, embed =True)):
    data = selects.get_data_final(students, subject_i)

    return {
        'data': data
    }