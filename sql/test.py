from selects import get_teacher_id,connect_database, close_connection, class_students_id,all_class_students, get_data_final,teacher_org,all_class_with_final

from fastapi import Request

import jwt
import mariadb

# from inserts import class_notify
def connect_database():
    try:
        con = mariadb.connect(
            user="admin",
            password="adm2016@=",
            # host="10.10.20.50",
            port=6033,
            database='odm',
            # port=3306
            host="nst.usmcontrol.com",
            # port=3306
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return con
# class_notify(10,10, 'suckers')



def check(label):
    if label.split('_')[-1] == 'soch':
        name = label.split('_')[0]
        sors = ['sor1', 'sor2', 'sor3', 'soch']

        sors_new = list(map(lambda x: f"{name}_{x}", sors))
        s = ', '.join(sors_new)
        subject_i = 1
        student_i = 1
        sql1 = (
            f"select {s} from school_final "
            f"where subject_i = {subject_i} "
            f"and student_i = {student_i};"
        )

        cn = connect_database()
        cr = cn.cursor()
        cr.execute(sql1)
        rows = cr.fetchall()
        print(rows)
        close_connection(cn)


def insert_subjects():
    cn = connect_database()
    lists = ['Алгебра','Геометрия']
    cr = cn.cursor()
    for row in list:
        sql = (
            f"insert into school_subject "
            f"(lbl, own_i) "
            f"values "
            f"('{row}', 1); "
        )
        print(sql)
        cr.execute(sql)
        cn.commit()

    close_connection(cn)

# classes = ['1A','2B','3B', '4Г']
# class_ids = [30,  3,  33,   36]
#
# schedeule = [
#     {
#         's_time':'08:30:30',
#         'subject_i': 6,
#         's_week': 1,
#     },
#
# ]
def insert_schedule():
    data = [
        {
        's_time': "11:30:00",
        's_week': 1,
        'subject_i': 42,
        'teacher_i': 19,
        'class_i': 39,
        },
        {
        's_time': "12:30:00",
        's_week': 1,
        'subject_i': 45,
        'teacher_i': 19,
        'class_i': 42,
        },
        {
        's_time': "13:30:00",
        's_week': 1,
        'subject_i': 45,
        'teacher_i': 19,
        'class_i': 42,
        },
    ]

    for i in data:

        one = ",".join(i.keys())
        print(one)
        two = ",".join(str(temp) for temp in i.values() if type(temp) == 'int')/
        sql = (
            f"insert into school_schedule "
            f"({one},c_year, own_i, room) "
            f"values ('{i['s_time']}',{}, 2020, 0, 201);"
        )
        print(sql)


insert_schedule()