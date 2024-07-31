'''
Manage data using pymilvus 2.2.x 
'''
from pymilvus import MilvusClient, DataType
from dotenv import load_dotenv
from pymilvus import connections, db
from pymilvus import CollectionSchema, FieldSchema, DataType
from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, utility
import random
import os 

load_dotenv()
db_name = 'finger'
ip_addr = os.getenv('ip_addr')

conn = connections.connect(
    host=ip_addr,
    port="19530",
    db_name=db_name
)

collection_name = 'fin_collection'

# 1. Set up a Milvus client
client = MilvusClient(
    uri="http://" + ip_addr + ":19530", port=19530
)

data = [
  [i for i in range(2000)],
  [str(i) for i in range(2000)],
  [i for i in range(10000, 12000)],
  [[random.random() for _ in range(2)] for _ in range(2000)]
]

# print(f'data before append: {data}')
## Once your collection is enabled with dynamic schema,
## you can add non-existing field values.
# data.append([str("dy"*i) for i in range(2000)])
# print(f'data after append: {data}')

from pymilvus import Collection
print(f'insert data into collection')
collection = Collection(collection_name)      # Get an existing collection.
collection.insert(data)

def collection_info(collection_name):
    print(f'collection info')
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

search_params = {
    "metric_type": "L2", 
    "offset": 5,   # num of entities to skip during the search 
    "ignore_growing": False, 
    "params": {"nprobe": 10}
}

collection.load()   # load the collection to memeory before conducting vector search
results = collection.search(
    data=[[0.1, 0.2]], 
    anns_field="data_description", 
    # the sum of `offset` in `param` and `limit` 
    # should be less than 16384.
    param=search_params,
    limit=10,
    expr=None,
    # set the names of the fields you want to 
    # retrieve from the search result.
    output_fields=['data_name'],
    consistency_level="Strong"
)

# get the IDs of all returned hits
results[0].ids

# get the distances to the query vector from all returned hits
results[0].distances

# get the value of an output field specified in the search request.
hit = results[0][0]
print(hit)
print(hit.entity.get('data_name'))
collection.release()