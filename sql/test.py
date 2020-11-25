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


# 42 45 2
def insert_schedule():
    sql = (
        f"insert into school_schedule "
        f"(s_time, s_week, subject_i, teacher_i, class_i, c_year, own_i, room) "
        f"values "
        f"('11:00:00', 1, 42, 19, 1, 2020, 1, 201);"
    )
    cn = connect_database()
    cr = cn.cursor()
    cr.execute(sql)
    cn.commit()
    close_connection(cn)

def update_schedule():
    sql = (
        f"update school_schedule "
        f"set class_i = 48 where "
        f"sch_i=60;"
    )
    cn = connect_database()
    cr = cn.cursor()
    cr.execute(sql)
    cn.commit()
    close_connection(cn)
def select():
    sql = (
        f"select * from school_schedule "
        f"where teacher_i = 19 and s_week = 1;"
    )
    cn = connect_database()
    cr =cn.cursor()
    cr.execute(sql)
    rows = cr.fetchall()
    print(rows)
    close_connection(cn)
insert_schedule()
