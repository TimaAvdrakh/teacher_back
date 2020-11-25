import pymysql
# _mysql = pymysql.install_as_MySQLdb()
import mariadb
import sys
import datetime

def connect_database():
    try:
        con = mariadb.connect(
            user="admin",
            password="adm2016@=",
            host="10.10.20.50",
            # port=6033,
            database='odm',
            port=3306
            # host = "nst.usmcontrol.com",
            # port=3306
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return con

def close_connection(con):
    con.close()


def get_teacher_id(cn, uuid):
    cr = cn.cursor()
    print("Selecting teacher Id")
    sql = (
        f"select teacher_per_id "
        f"from school_teacher "
        f"where uuid={uuid};"
    )
    cr.execute(sql)
    row = cr.fetchone()
    # print(row)
    return row[0]

def teacher_org_address(cn, org_id):
    cr = cn.cursor()
    print("selecting organizaton address")

    sql = (
        f"select addr_note "
        f"from org_addr "
        f"where org_i = {org_id};"
    )
    cr.execute(sql)
    row = cr.fetchone()
    return row[0]

def teacher_org(cn, org_id):
    cr = cn.cursor()
    print('Selecting teacher organization')
    sql = (
        f"select o.lbl , oa.addr_note "
        f"from org as o "
        f"inner join org_addr as oa "
        f"on o.org_i= oa.org_i "
        f"where o.org_i = {org_id};"
    )
    print(sql)
    cr.execute(sql)
    # print(cr.statement)
    row = cr.fetchone()
    print(row)
    return {
        'school': row[0],
        'address': row[1]
    }

def get_teacher_id(uuid):
    # print(uuid)
    cn = connect_database()

    sql = (
        f"select teacher_per_id "
        f"from school_teacher "
        f"where uuid = '{uuid}';"
    )
    cr = cn.cursor()
    cr.execute(sql)
    ans = cr.fetchone()
    close_connection(cn)

    return ans


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
            'subject_i': row[0],
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
    counter = 0
    for row in rows:
        d = {
            'id': counter,
            'sch_i': row[0],
            'class_i': row[1],
            'lbl': row[2]
        }
        ans.append(d)
        counter += 1

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
        f"on s.student_per_id = p.person_i "
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

def all_class_with_final(class_i, subject_i):
    cn = connect_database()

    ar = [f"nvl(sf.{num}_{var},0)" for num in ['first', 'second', 'third', 'forth'] for var in
          ['sor1', 'sor2', 'sor3', 'soch', 'final']]


    temp = ", ".join(ar)
    sql = (
        f"select student_per_id, first_name, last_name,  {temp} , nvl(sf.final_grade, 0) "
        f"from person as p "
        f"inner join school_student as s "
        f"on s.student_per_id = p.person_i "
        f"left join school_final sf "
        f"on student_per_id = student_i and subject_i = {subject_i} "
        f"where class_id = {class_i}; "
    )
    print(sql)
    cr = cn.cursor()
    cr.execute(sql)
    rows = cr.fetchall()
    ans = []


    for row in rows:
        temp = {
            'student_per_id': row[0],
            'last_name': row[1],
            'first_name': row[2],
            'grade': 0,
            'attendance': True,
            'first_sor1': row[3],
            'first_sor2': row[4],
            'first_sor3': row[5],
            'first_soch': row[6],
            'first_final': row[7],
            'second_sor1': row[8],
            'second_sor2': row[9],
            'second_sor3': row[10],
            'second_soch': row[11],
            'second_final': row[12],
            'third_sor1': row[13],
            'third_sor2': row[14],
            'third_sor3': row[15],
            'third_soch': row[16],
            'third_final': row[17],
            'forth_sor1': row[18],
            'forth_sor2': row[19],
            'forth_sor3': row[20],
            'forth_soch': row[21],
            'forth_final': row[22],
            'final_grade': row[23]
        }
        ans.append(temp)
    print(ans)
    close_connection(cn)

    return {
        'data': ans
    }
def teacher_journal(cn, teacher_i, time):
    sql = (
        f"select sc.sch_i, sc.s_time, sub.lbl, cl.lbl, sc.room "
        f"from school_schedule sc "
        f"inner join school_subject sub "
        f"on sc.subject_i = sub.subject_i "
        f"inner join school_class cl "
        f"on sc.class_i = cl.class_id "
        f"where sc.teacher_i = {teacher_i} and sc.s_week={time} "
        f"order by sc.s_time;"
    )
    print(sql)
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
    return "Повторение"


def p_class(cn, teacher_i):
    sql = (
        f"select s.student_per_id, cl.lbl, p.first_name, p.last_name,  cl.teacher_per_id , cl.class_id "
        f"from person as p "
        f"inner join school_student as s "
        f"on student_per_id = person_i "
        f"inner join school_class as cl "
        f"on cl.class_id = s.class_id "
        f"where cl.class_id = ( "
        f"select distinct(class_id) from school_class where teacher_per_id = {teacher_i} limit 1"
        f"); "
    )
    cr = cn.cursor()
    cr.execute(sql)
    rows = cr.fetchall()
    students = []
    amount = len(rows)
    cl = rows[0][1]
    cl_i = rows[0][5]
    teacher_i = rows[0][4]
    saparhan = {
        'name': f"Сапархан Тургынбаев",
        'student_i': 40,
        'phone': "+77022966496"
    }
    students.append(saparhan)
    for row in rows:
        phone = f"+77771233{row[0]}"
        temp = {
            'name': f"{row[2]} {row[3]}",
            'student_i': row[0],
            'phone': phone[:10]
        }
        students.append(temp)

    return {
        'class': cl,
        'teacher_i': teacher_i,
        'class_id': cl_i,
        'amount': amount+1,
        'students': students
    }


def student_parents(cn, student_id):
    sql = (
        f"select p.first_name, p.last_name "
        f"from person as p "
        f"inner join school_parent sp "
        f"on sp.parent_per_id = p.person_i "
        f"where sp.student_per_id = {student_id};"
    )
    cr = cn.cursor()
    cr.execute(sql)
    rows = cr.fetchall()

    bolatbek_agai = {
        "name": "Болатбек Жанбыршиев",
        "phone": "+77083353601",
    }
    ans = []
    ans.append(bolatbek_agai)
    for row in rows[:2]:
        temp = {
            "name": f"{row[0]} {row[1]}",
            "phone": "8273388393"
        }
        ans.append(temp)

    return ans


def class_students_id(cn, class_id, message):
    sql = (
        f"select student_per_id "
        f"from person as p "
        f"inner join school_student as s "
        f"on s.student_per_id = p.person_i "
        f"where class_id = {class_id}; "
    )

    cr = cn.cursor()
    cr.execute(sql)
    rows = cr.fetchall()
    print(rows)

    m = "Важное сообщение"

    for row in rows:
        print(row[0])
        sql1 = (
            f"insert into school_log "
            f"(student_i, e_typ, e_detail) "
            f"values ({row[0]}, '{m}' , '{message}'); "
        )
        print(sql)
        cr.execute(sql1)
        cn.commit()
        print(sql1)
    return {
        "Notification_send"
    }

def get_data_final(students, subject_i):
    cn = connect_database()
    ans = []
    for student in students:
        sql = (
            f"select first_frth, secnd_frth, thrd_frth, frth_frth "
            f"from school_final "
            f"where student_i = {student} and subject_i = {subject_i};"
        )
        cr = cn.cursor()
        cr.execute(sql)
        row = cr.fetchone()
        part = ['first', 'second', 'third', 'fourth']
        if row:
            temp = dict(zip(part, list(row)))
        else:
            temp = dict(zip(part, [0, 0, 0, 0]))

        ans.append(temp)
    close_connection(cn)

    return ans


