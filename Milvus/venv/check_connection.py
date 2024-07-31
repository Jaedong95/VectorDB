from pymilvus import connections, db
from dotenv import load_dotenv
import os 

load_dotenv()
ip_addr = os.getenv('ip_addr')
# print(f'ip_addr: {ip_addr}')
conn = connections.connect(host=ip_addr, port=19530)
try:
    assert(conn)
except:
    print(f'connection successful!')
    print(f'보유 DB: {db.list_database()}')