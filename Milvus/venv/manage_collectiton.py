'''
Manage Collections using pymilvus 2.2.x 
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

try:
  assert db.create_database(db_name)
except:
  pass 

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
# 2.1 Create schema
data_id = FieldSchema(
  name="data_id",
  dtype=DataType.INT64,
  is_primary=True,
)
data_name = FieldSchema(
  name="data_name",
  dtype=DataType.VARCHAR,
  max_length=200,
)
word_count = FieldSchema(
  name="word_count",
  dtype=DataType.INT64,
)
data_desc = FieldSchema(
  name="data_description",
  dtype=DataType.FLOAT_VECTOR,
  dim=2
)

schema = CollectionSchema(
  fields=[data_id, data_name, word_count, data_desc],
  description="Test data search",
  enable_dynamic_field=True
)

# 2.2 Create collection
collection_name = "fin_collection" 
collection = Collection(
    name=collection_name,
    schema=schema,£
    using='default',
    shards_num=2
  )
print(collection)

# 2.3 (optional) Modify collection 
collection = Collection(collection_name)
collection.set_properties(properties={"collection.ttl.seconds": 1800})    # 시간 제한을 설정한다. 만료된 데이터는 컬렉션에서 정리되며 검색이나 쿼리에 포함되지 않는다. 

# 2.4 (optional) Check collection 
def collection_info(collection_name):
    collection = Collection(collection_name)
    print(f'schema info: {collection.schema}') 
    print(f'collection info: {collection.description}')
    print(f'collection name: {collection.name}')
    print(f'is collection empty ?: {collection.is_empty}')
    print(f'num of data: {collection.num_entities}')
    print(f'primary key of collection: {collection.primary_field}')
    print(f'partition of collection: {collection.partition}')
    # print(f'index of collection: {collection.indexs}')
    # print(f'properties of collection: {collection.properties}')

print(f'info of collection: {collection_info(collection_name)}')
# 2.5 Drop collection 
# utility.drop_collection(collection_name)

# 2.6 Load collection
## 사용자가 추가 쿼리 노드의 CPU 및 메모리 자원을 활용하기 위해 컬렉션을 여러 복제본으로 로드하며, 해당 기능은 추가 하드웨어 없이 전체 GPS (초당 쿼리 수)와 처리량을 향상 시킴
## 컬렉션 로드 전에 인덱스가 설정되어 있는지 확인이 필요함

# 2.6.1 Prepare index parameter 
index_params = {
  "metric_type": "L2",    # type of metrics used to measure the similarity of vectors 
  "index_type": "IVF_FLAT",   # type of index used to accelerate vector search 
  "params": {"nlist": 6554},
}

# 2.6.2 Build index 
collection.create_index(
  field_name = "data_description",
  index_params = index_params
)
print(f'building index: {utility.index_building_progress(collection_name)}')

# 2.6.3 Drop index 
# collection.drop_index()

# 2.6.4 load collection
collection = Collection(collection_name)
print(collection)
collection.load(replica_number=1)   # 현재는 replica number를 2이상으로 설정했을 때 오류 발생 
utility.load_state(collection_name)
utility.loading_progress(collection_name)
result = collection.get_replicas()
print(result)

# 2.7 Release collection
## release collection after a search or query to reduce memory usage 
collection.release()