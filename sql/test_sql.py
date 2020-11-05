from selects import *

teacher_i = 19
time = 1

sql = (
        f"select * from school_class where teacher_per_id = 19 limit 1;"
)
con = connect_database()
cr = con.cursor()
rows = p_class(con,19)
print(rows)
cr = close_connection(con)