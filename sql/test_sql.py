teacher_i = 19
time = 1
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