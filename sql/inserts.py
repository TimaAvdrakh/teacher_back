import pymysql
from datetime import datetime, timedelta
import datetime as dtm
# _mysql = pymysql.install_as_MySQLdb()


def connect_database():
    con = pymysql.connect(host='localhost',
                          port=3307,
                          user='root',
                          db='odm',
                          password='Sas2016-')

    return con


def close_connection(con):
    con.close()


def attendance(con, list, sch_i, dt=None):
    cr = con.cursor()
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
    return "Your data(attendance) was added to journal"


def grade(con, list, sch_i, dt=None):
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


def task(cn, sch_i, lbl, dt = None):
    # date_fake = "2020-10-12"
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
    print(days)
    counter = 0
    ans = []
    add = 1
    while counter < 3:
        if len(days) == 1:
           add = 7
        date += timedelta(days=add)
        if date.weekday() in days:
            ans.append(date.date())
            counter += 1
    return {
        'date': ans
    }