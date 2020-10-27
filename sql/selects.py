import pymysql
# _mysql = pymysql.install_as_MySQLdb()
import mariadb
import sys

def connect_database():
    try:
        con = mariadb.connect(
            user="admin",
            password="adm2016@=",
            host="nst.usmcontrol.com",
            db='odm',
            port=6033
            # host = "nst.usmcontrol.com",
            #host ="10.10.20.50
            #port = 3306
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return con

def close_connection(con):
    con.close()



def teacher_org(cn, org_id):
    cr = cn.cursor()
    print('Selecting teacher')

    sql = (
        f"select lbl "
        f"from org "
        f"where org_i = {org_id};"
    )
    cr.execute(sql)
    # print(cr.statement)
    row = cr.fetchone()
    print(row[0])
    return {
        'school': row[0]
    }

def teacher_subjects(cn, teacher_id, time):
    # select
    # lbl
    # from school_subject where
    # subject_i in (select distinct(subject_i)
    # from school_schedule where
    # teacher_i = 19 and class_i = 2);
    cr = cn.cursor()
    print("ALL DAY SUBJECTS")
    sql = (
        f"select subject_i, lbl "
        f"from school_subject "
        f"where subject_i in ( "
        f"select distinct(subject_i) "
        f"from school_schedule "
        f"where teacher_i = {teacher_id} "
        f"and s_week = {time});"
    )
    print(sql)
    cr.execute(sql)
    rows = cr.fetchall()
    ans = []
    for row in rows:
        d = {
            'id': row[0],
            'lesson': row[1]
        }

        ans.append(d)
    print(ans)
    return {
        "data": ans
    }

def teacher_classes(con, teacher_i, subject_i, s_week):
    print("Teacher classes")
    sql = (
        f"select s.sch_i,  s.class_i, c.lbl "
        f"from school_schedule s "
        f"inner join school_class c "
        f"on c.class_id = s.class_i "
        f"where s.teacher_i= {teacher_i} "
        f"and s.subject_i = {subject_i} "
        f"and s.s_week = {s_week}  "
        f"order by s.class_i;"
    )
    cr = con.cursor()
    cr.execute(sql)
    print(sql)
    ans = []
    rows = cr.fetchall()
    for row in rows:
        d = {
            'sch_i': row[0],
            'class_i': row[1],
            'lbl': row[2]
        }
        ans.append(d)

    # for i in range(8-10):
    #     for j in ('A', 'Б', 'В' ,'Г'):
    #         d = {
    #             'sch_i': -1,
    #             'class_i': -1,
    #             'lbl': str(i)+j
    #         }
    #         ans.append(d)
    # print(ans)
    # ans = add_to_class(ans)
    return ans


def all_class_students(cn, class_id):
    """ Get all students from class with given class_id"""
    cr = cn.cursor()
    print("ALL STUDENTS")

    sql = (
        f"select student_per_id, first_name, last_name "
        f"from person as p "
        f"inner join school_student as s "
        f"on student_per_id = person_i "
        f"where class_id = {class_id}; "
    )
    cr.execute(sql)
    ans = []
    rows = cr.fetchall()

    for row in rows:
        temp = {
            'student_per_id': row[0],
            'last_name': row[1],
            'first_name': row[2],
            'grade': 0,
            'attendance': True,
        }
        ans.append(temp)
    print(ans)

    return {
        'data': ans
    }


def teacher_journal(cn,teacher_i, time):
    sql = (
        f"select sc.sch_i, sc.s_time, sub.lbl, cl.lbl "
        f"from school_schedule sc "
        f"inner join school_subject sub "
        f"on sc.subject_i = sub.subject_i "
        f"inner join school_class cl "
        f"on sc.class_i = cl.class_id "
        f"where sc.teacher_i = {teacher_i} and sc.s_week={time} "
        f"order by sc.s_time;"
    )
    print(sql)

    sqlfake = (
        f"select sc.s_time, sub.lbl, cl.lbl, sc.kab  "
        f"from school_schedule sc "
        f"inner join school_subject sub "
        f"on sc.subject_i = sub.subject_i "
        f"inner join school_class cl "
        f"on sc.class_i = cl.class_id "
        f"where sc.teacher_i = {teacher_i} and s_week={time} "
        f"order by sc.s_time;"
    )
    cr = cn.cursor()
    print("Journal")
    cr.execute(sql)
    rows = cr.fetchall()
    print(rows)
    return rows


def journal_task(cn, sch_i, dt):
    sql = (
        f"select lbl "
        f"from school_task "
        f"where sch_i={sch_i} and dt={dt};"
    )

    cr = cn.cursor()
    cr.execute(sql)
    homework = cr.fetchone()
    print(homework)
    if homework:
        return homework
    return "No homework"