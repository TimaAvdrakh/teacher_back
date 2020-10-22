import sys
from sshtunnel import SSHTunnelForwarder

ssh_host = '192.168.100.30'
ssh_user = 'zbz'
ssh_port = 8888
ssh_remote_port = 3306
tunnel = None

try:
    tunnel = SSHTunnelForwarder(
        ssh_host=ssh_host,
        ssh_port=ssh_port,
        ssh_username=ssh_user,
        # password='Sas2016-',
        remote_bind_address=('127.0.0.1', ssh_remote_port),
        local_bind_address=('0.0.0.0', 3307)
    )
    print(tunnel)
except Exception as e:
    print(sys.exc_info(), sys.exc_info()[-1].tb_lineno)
    exit(0)
print(tunnel)
tunnel.start()