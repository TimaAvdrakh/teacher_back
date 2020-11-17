key = 'asdjsdlkfjsdfljghaepriogherkjkgelkjghdspfgsdkfjgne77000211021'

tokem = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InNlaXNlbWJheWV2IiwicGhvbmUiOiI3NzAwMDIxMTAyMSIsImRhdGEiOiIyMDIwLTExLTE3IDA5OjU3OjQxLjI0MjE1MyJ9.wWhJxz7rCqcvAwbGJLvLxsULrJzNummsHS38EAcf_JA'

import jwt

try:
    jwt.decode(tokem, key, algorithms=["HS256"])
except:
    print("invalid token")

print('okpyp')