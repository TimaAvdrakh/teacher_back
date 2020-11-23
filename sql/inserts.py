import pymysql
from datetime import datetime, timedelta
import datetime as dtm
import mariadb

# _mysql = pymysql.install_as_MySQLdb()
def reformat_date(str):
    "from 20-10-25 to 25/10/20"
    year , month, day = [i for i in str.split('-')]
    return f"{day}/{month}/{year}"

def connect_database():
    try:
        con = mariadb.connect(
            user="admin",
            password="adm2016@=",
            # host="nst.usmcontrol.com",
            db='odm',
            # port=6033
            host="10.10.20.50",
            port=3306
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return con

def close_connection(con):
    con.close()

def attendance(con, list, sch_i, dt=None):
    cr = con.cursor()
    print(dt)
    date = [i for i in dt.split(' ')]
    dt = date[1]
    day,month, year = [int(i) for i in dt.split('/')]
    dt = f"{year}-{month}-{day}"
    print("Inserting Or Updateing Attendance")
    c_dt = datetime.now()
    c_year = c_dt.year
    # sch_i student_i dt vst

    for row in list:
        print(row.student_i)
        sql = (
            f"insert into school_journal (sch_i, student_i, dt, c_dt,c_year, vst,own_i) "
            f"values ({sch_i}, {row.student_i},'{dt}', '{c_dt}',{c_year}, '{row.vst}', 1) "
            # f"values ({sch_i}, {row['student_i']},'{row['dt']}', '{c_dt}',{c_year}, '{row['vst']}', 1) "
            f"on duplicate key update c_dt = '{c_dt}', vst = '{row.vst}';"
        )
        print(sql)
        cr.execute(sql)
        # print(cr.statement())
        con.commit()
    return {
        'message': "Your data(attendance) was added to journal"
    }


def grade(con, list, sch_i, dt):
    date = [i for i in dt.split(' ')]
    dt = date[1]
    cr = con.cursor()
    day, month, year = [int(i) for i in dt.split('/')]
    dt = f"{year}-{month}-{day}"
    c_dt = datetime.now()
    print("Updating Grade")
    type = 'Посещение'

    for row in list:
        sql = (
            f"update school_journal "
            f"set pnt = {row.pnt}, lbl = '{row.lbl}' "
            f"where sch_i= {sch_i} and student_i = {row.student_i}  and dt = '{dt}'; "
        )

        #INSERT TO LOG
        sql_subject = (
            f"select lbl "
            f"from school_subject sj "
            f"inner join school_schedule sc "
            f"on sj.subject_i = sc.subject_i "
            f"where sc.sch_i = {sch_i} ;"
        )

        cr.execute(sql_subject)
        sub = cr.fetchone()
        e_detail = f"Получил оценку по предмету {sub[0]}, {row.pnt}"
        # print(e_detail)
        sql_log = (
            f"insert into school_log "
            f"(student_i, e_typ,e_time, e_detail) "
            f"values "
            f"({row.student_i}, '{type}', '{c_dt}', '{e_detail}'); "
        )
        print(sql_log)
        cr.execute(sql_log)
        con.commit()

        print(sql)
        cr.execute(sql)
        con.commit()
    return "Your data(grades) added to journal"


def task(cn, sch_i, lbl, dt=None):
    # date_fake = "2020-10-12"
    print(dt)
    print("Inserting task")
    day, month, year = [int(i) for i in dt.split('/')]
    dt = f"{year}-{month}-{day}"
    c_dt = datetime.now()
    c_year = c_dt.year
    cr = cn.cursor()

    sql = (
        f"insert into school_task "
        f"(sch_i, dt, c_dt, c_year, lbl, own_i) "
        f"values ({sch_i}, '{dt}', '{c_dt}', {c_year}, '{lbl}', 1); "
        # f"on duplicate key update   lbl = {lbl} "

    )
    print(sql)
    cr.execute(sql)
    cn.commit()

    return {
        "message": "Homework has been added to journal."
    }


def task_dates(cn, teacher_i,class_i,subject_i, dt):
    date = [i for i in dt.split(' ')]
    dt = date[1]
    day, month, year = [int(i) for i in dt.split('/')]
    date = datetime(year, month, day)

    # dt = f"{year}-{month}-{day}"
    sql = (
        f"select distinct(s_week) "
        f"from school_schedule "
        f"where teacher_i = {teacher_i} "
        f"and class_i = {class_i} "
        f"and subject_i = {subject_i};"
    )

    cr = cn.cursor()
    cr.execute(sql)
    rows = cr.fetchall()
    days = [row[0] for row in rows]
    counter = 0
    ans = []
    add = 1
    while counter < 3:
        if len(days) == 1:
           add = 7
        date += timedelta(days=add)
        if date.weekday() in days:
            d = date.date()
            str = f"{d}"
            str = reformat_date(str)
            ans.append(str)
            counter += 1

    return {
        'date': ans
    }

def student_log_notification(cn, student_i, message):
    cr = cn.cursor()
    m = "Сообщение от учитeля"
    sql = (
        f"insert into school_log "
        f"(student_i, e_typ, e_detail) "
        f"values ({student_i}, '{m}', '{message}'); "
    )
    cr.execute(sql)
    cn.commit()

    return {
        "detail": "message send to student"
    }


def class_notify(class_i, teacher_i, message):
    cn = connect_database()
    cr = cn.cursor()
    # print(datetime.now
    dt = datetime.now()
    print(dt)
    print(dt)
    year = dt.year
    sql = (
        f"insert into school_announcement "
        f"(class_i, teacher_i, lbl, c_dt, c_year, own_i) "
        f"values ({class_i}, {teacher_i}, '{message}' , '{dt}' , '{year}', 1);"
    )
    print(sql)
    cr.execute(sql)
    cn.commit()
    close_connection(cn)

dates = {
    'first': {
        "start": 1,
        "end": 1
    },
    'second': {
        "start": 1,
        "end": 1.
    },
    'third': {
        "start": 1,
        "end": 1
    },
    'forth': {
        "start": 1,
        "end": 1
    },
}

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
        print("SOCH BITCH")
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
            'final_grade': None
        }
    else:
        print("ITS SOR")
        sql = (
            f"insert into school_final "
            f"(student_i, subject_i, {lbl} , c_year,  own_i) "
            f"values "
            f"({student_i}, {subject_i}, {grade}, {c_y}, 1) "
            f"on duplicate key update "
            f"{lbl} = {grade};"
        )
        print(sql)
        cr.execute(sql)
        cn.commit()

    close_connection(cn)

    return {
        'soch': None,
        'final_grade': None
    }