from selects import get_teacher_id, connect_database, close_connection, class_students_id,all_class_students, get_data_final,teacher_org,all_class_with_final

from fastapi import Request

import jwt


# from inserts import class_notify

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


sql = (
    f"select dt, c_dt from school_journal where student_i = 15;"
)
# check('first_soch')
cn = connect_database()
cr = cn.cursor()
cr.execute(sql)
rows = cr.fetchone()
print(rows)
close_connection(cn)