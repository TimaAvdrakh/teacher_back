key = 'asdjsdlkfjsdfljghaepriogherkjkgelkjghdspfgsdkfjgne77000211021'

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InNlaXNlbWJheWV2IiwicGhvbmUiOiI3NzAwMDIxMTAyMSIsImRhdGEiOiIyMDIwLTExLTE4IDA1OjAwOjQ0LjU5OTQ3OCJ9.298e2R9oD_MMgUgOlSui6YZZK4fzPRp3cmwUMgy9Yao'
import jwt

try:
    jwt.decode(token, key, algorithms=["HS256"])
except:
    print("invalid token")

print('ok dude')