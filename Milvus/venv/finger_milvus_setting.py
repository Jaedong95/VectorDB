'''
Set default env (collection, partition, schema, index) before data management 
dataset: rule-book
'''
from pymilvus import MilvusClient, DataType
from dotenv import load_dotenv
from pymilvus import connections, db
from pymilvus import CollectionSchema, FieldSchema, DataType
from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, utility
import os 

load_dotenv()
db_name = 'finger'
ip_addr = os.getenv('ip_addr')

conn = connections.connect(
    host=ip_addr,
    port="19530",
    db_name=db_name
)

# 1. Set up a Milvus client
client = MilvusClient(
    uri="http://" + ip_addr + ":19530", port=19530
)

# 2. Create collection (Customized)
## 2.1 Create schema
data_id = FieldSchema(
  name="data_id",
  dtype=DataType.INT64,
  is_primary=True,
)
pass 
schema = CollectionSchema(
  fields=[data_id, ...],
  description="Test data search",
  enable_dynamic_field=True
)

## 2.2 Create collection
collection_name = "fin_collection" 
collection = Collection(
    name=collection_name,
    schema=schema,£
    using='default',
    shards_num=2
  )
print(collection)

## 2.3 Build index 
index_params = {
  "metric_type": "L2",    # type of metrics used to measure the similarity of vectors 
  "index_type": "IVF_FLAT",   # type of index used to accelerate vector search 
  "params": {"nlist": 6554},
}

collection.create_index(
  field_name = "data_description",
  index_params = index_params
)
print(f'building index: {utility.index_building_progress(collection_name)}')

## 2.4 Create Partition 
## 윤리규정, 복지제도, ... 파일별 파티션

# 3. Data management 
## 3.1 Insert data

# 4. Search data
