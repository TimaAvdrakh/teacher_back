from selects import get_teacher_id, connect_database, close_connection, class_students_id,all_class_students, get_data_final,teacher_org,all_class_with_final

from fastapi import Request
# print(teacher_org(cn, 111))
# close_connection(cn)

# sf"select o.lbl , oa.addr_note "
#         f"from org as o "
#         f"inner join org_addr as oa "
#         f"on o.org_i= oa.org_i "
#         f"where o.org_i = {org_id};"


ar = [f"nvl(sf.{num}_{var},0)" for num in ['first', 'second', 'third', 'forth'] for var in
      ['sor1', 'sor2', 'sor3', 'soch', 'final']]

temp = ", ".join(ar)
subject_i = 2
class_i = 2
all_class_with_final(2,2)