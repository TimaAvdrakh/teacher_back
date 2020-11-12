from selects import get_teacher_id, connect_database, close_connection, class_students_id

cn = connect_database()
print(class_students_id(cn,3, "123"))
close_connection(cn)
