from pymilvus import utility
from pymilvus import MilvusClient, DataType
from dotenv import load_dotenv
from pymilvus import connections, db
from pymilvus import CollectionSchema, FieldSchema, DataType
from pymilvus import Collection
import os 

load_dotenv()
db_name = 'finger'
ip_addr = os.getenv('ip_addr')

try:
  assert db.create_database(db_name)
except:
  pass 

conn = connections.connect(
    host=ip_addr,
    port="19530",
    db_name=db_name
)

print(utility.has_collection("data"))
print(utility.list_collections())

from pymilvus import Collection
collection = Collection()