'''
Manage Partitions using pymilvus 2.2.x 
'''
from pymilvus import MilvusClient, DataType
from dotenv import load_dotenv
from pymilvus import connections, db
from pymilvus import CollectionSchema, FieldSchema, DataType
from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, Partition
import os 

load_dotenv()
db_name = 'finger'
ip_addr = os.getenv('ip_addr')
collection_name = 'fin_collection'

def collection_info(collection_name):
    collection = Collection(collection_name)
    print(f'schema info: {collection.schema}') 
    print(f'collection info: {collection.description}')
    print(f'collection name: {collection.name}')
    print(f'is collection empty ?: {collection.is_empty}')
    print(f'num of data: {collection.num_entities}')
    print(f'primary key of collection: {collection.primary_field}')
    print(f'partition of collection: {collection.partition}')
    print(f'index of collection: {collection.index}')
    # print(f'properties of collection: {collection.properties}')

conn = connections.connect(
    host=ip_addr,
    port="19530",
    db_name=db_name
)

# 1. Set up a Milvus client
client = MilvusClient(
    uri="http://" + ip_addr + ":19530", port=19530
)

# 2. Create a partition 
## divide the bulk of data into a small number of partitions 
collection = Collection(collection_name)      # Get an existing collection.

try:
    assert collection.create_partition("card")
except:
    pass
# print(collection_info(collection_name))

# 3. Check partition
collection = Collection(collection_name)
collection.has_partition('card')
print(f'partitions: {collection.partitions}')

# 4. Drop partition
## collection.drop_partition('card')

# 5. Load partition
## 메모리에 전체 컬렉션을 로드하는 것보다, 파티션을 로드하는 것은 메모리 사용량을 크게 감소시킬 수 있음 
collection = Collection(collection_name)
collection.load(["card"], replica_number=1)   # collection, partition 모두 replica 값이 2이상이면 오류 발생

# or
partition = Partition(name='card', collection=collection)
partition.load(replica_number=1)
result = partition.get_replicas()

# 6. Release partition
partition.release()