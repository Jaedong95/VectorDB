from pymilvus import MilvusClient
from dotenv import load_dotenv
from pymilvus import connections, db
import os

load_dotenv()
db_name = 'finger'
ip_addr = os.getenv('ip_addr')
conn = connections.connect(host=ip_addr, port=19530)
try:
  assert db.create_database(db_name)
except:
  pass
print(db.list_database())

# select database 
db.using_database('finger')

from pymilvus import MilvusClient, DataType
# 1. Set up a Milvus client
client = MilvusClient(
    uri=f"http://" + ip_addr+ ":19530"
)

# 2. Create a collection in quick setup mode
client.create_collection(
    collection_name="quick_setup",
    dimension=5
)
print('ok')

from pymilvus import CollectionSchema, FieldSchema, DataType
book_id = FieldSchema(
  name="book_id",
  dtype=DataType.INT64,
  is_primary=True,
)
book_name = FieldSchema(
  name="book_name",
  dtype=DataType.VARCHAR,
  max_length=200,
)
word_count = FieldSchema(
  name="word_count",
  dtype=DataType.INT64,
)
book_intro = FieldSchema(
  name="book_intro",
  dtype=DataType.FLOAT_VECTOR,
  dim=2
)
schema = CollectionSchema(
  fields=[book_id, book_name, word_count, book_intro],
  description="Test book search",
  enable_dynamic_field=True
)
collection_name = "book" 
from pymilvus import Collection
collection = Collection(
    name=collection_name,
    schema=schema,
    using='default',
    shards_num=2
  )

print(collection)