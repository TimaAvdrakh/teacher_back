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


def update_org_name():
    sql = (
        f"update org set "
        f"lbl = 'Средняя IT школа-лицей №72' "
        f"where org_i = 1;"
    )
    cn = connect_database()
    cr = cn.cursor()
    cr.execute(sql)
    cn.commit()
    close_connection(cn)
update_org_name()