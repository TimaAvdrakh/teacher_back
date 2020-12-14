from fastapi import Request
from inserts import accessment
import jwt
import mariadb
from datetime import datetime
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


def close_connection(con):
    con.close()


def accessment(student_i, subject_i, lbl, grade):
    cn = connect_database()
    cr = cn.cursor()
    time = datetime.now()
    c_y = time.year
    # TODO CHANGE IFS IN CODE
    # if lebel == 'forth_soch':
    #     # ToDO calculate Final
    #     #calculate and add forth and final
    #     #calculate final
    #     ff =
    #     sql2 = (
    #         f"update school_final "
    #         f"set final_grade = {fg} , final_forth = {ff}"
    #         f"where subject_i = {subject_i} "
    #         f"and student_i={subject_i} and "
    #         f"year = {c_y};"
    #     )

    if lbl.split('_')[-1] == 'soch':
        print("SOCH")
        # checker if data if full or none
        name = lbl.split('_')[0]
        sors = ['sor1', 'sor2', 'sor3', 'soch']

        sors_new = list(map(lambda x: f"{name}_{x}", sors))

        s = ', '.join(sors_new)

        sql0 = (
            f"insert into school_final "
            f"(student_i, subject_i, {lbl} , c_year,  own_i) "
            f"values "
            f"({student_i}, {subject_i}, {grade}, {c_y}, 1) "
            f"on duplicate key update "
            f"{lbl} = {grade};"
        )
        print(sql0)
        cr.execute(sql0)
        cn.commit()


        sql1 = (
            f"select {s} from school_final "
            f"where subject_i = {subject_i} "
            f"and student_i = {student_i} "
            f"and c_year = '{c_y}';"
        )
        print(sql1)
        cr.execute(sql1)
        row = cr.fetchone()
        print(row)
        sum_of_all_class_bals = 70
        sem_final = f"{name}_final"
        # row = rows[0]
        sem_final_val = ((row[0] + row[1] + row[2] + sum_of_all_class_bals )/ 8 ) + (row[3] * 0.5)
        final_5 = 0

        if sem_final_val < 40:
            final_5 = 2
        elif sem_final_val >= 40 and sem_final_val < 65:
            final_5 = 3
        elif sem_final_val >= 65 and sem_final_val <= 84:
            final_5 = 4
        else:
            final_5 = 5

        print(final_5)

        sql_final = (
            f"update school_final "
            f"set {sem_final} = {final_5} "
            f"where subject_i = {subject_i} "
            f"and student_i = {student_i} and c_year = {c_y};"
        )
        print(sql_final)
        cr.execute(sql_final)
        cn.commit()


        if name == 'forth':
            ar = ['first', 'second', 'third', 'forth']
            ar = list(map(lambda x: f"{x}_final", ar))
            far = ', '.join(ar)
            sql2 = (
                f"select {far} from school_final "
                f"where subject_i = {subject_i} and student_i = {student_i} and c_year = {c_y};"
            )
            cr = cn.cursor()
            cr.execute(sql2)
            row = cr.fetchone()
            fg = row[0] + row[1] + row[2] + row[3]
            fg = fg/4
            fg = round(fg)
            print(fg)
            sql3 = (
                f"update school_final "
                f"set final_grade = {fg} "
                f"where subject_i = {subject_i} and student_i = {student_i} and c_year = {c_y};"
            )
            cr.execute(sql3)
            cn.commit()

            return {
                'soch': final_5,
                'final_grade': fg
            }

        return {
            'soch': final_5,
        }
    else:
        print("ITS SOR")

        if lbl.split('_')[-1] == 'sor1':
            sql = (
                f"insert into school_final "
                f"(student_i, subject_i, {lbl} , c_year,  own_i) "
                f"values "
                f"({student_i}, {subject_i}, {grade}, {c_y}, 1);"
            )
        else:
             sql = (
                 f"update school_final "
                 f"set {lbl} = {grade} "
                 f"where student_i = {student_i} and subject_i = {subject_i};"
             )
        cr.execute(sql)
        cn.commit()

    close_connection(cn)

    return {}

def test():
    accessment(524, 111, 'first_sor3', 80)

test()