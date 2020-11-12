from selects import get_teacher_id, connect_database, close_connection, class_students_id,all_class_students, get_data_final,teacher_org
from fastapi import Request
cn = connect_database()
# print(teacher_org(cn, 111))
# close_connection(cn)

# sf"select o.lbl , oa.addr_note "
#         f"from org as o "
#         f"inner join org_addr as oa "
#         f"on o.org_i= oa.org_i "
#         f"where o.org_i = {org_id};"

sql = (
    f"select * from org;"
)

cr = cn.cursor()
cr.execute(sql)
row = cr.fetchall()
print(row)

close_connection(cn)
