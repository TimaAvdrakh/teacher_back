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
    list = ['Технология', 'Окружающий мир', 'ОБЖ', 'Ритмика']
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

def update_school():
    cn = connect_database()

    sql = (
        f"update org_addr "
        f"set addr_note = 'Бокенбай Батыра, 46' "
        f"where org_i = 1; "
    )
    cr = cn.cursor()
    cr.execute(sql)
    cn.commit()
    close_connection(cn)

update_school()