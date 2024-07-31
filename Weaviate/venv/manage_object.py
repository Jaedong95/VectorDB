import weaviate
import json
import os

client = weaviate.Client(
    url="http://172.30.1.34:8080"
)
print(client.is_ready())
class_name='JeaopardyQuestion'

# 1. Create object
uuid = client.data_object.create(
    class_name=class_name,
    data_object={
        "question": "This vector DB is OSS & supports automatic property type inference on import",
        # "answer": "Weaviate",  # schema properties can be omitted
        "newProperty": 123,  # will be automatically added as a number property
    }
)
print(uuid)  

# 1.1 Create object with a speicifed vector
## object를 생성할 때 벡터 값을 지정해줄 수 있음
vec_uuid = client.data_object.create(
    class_name=class_name,
    data_object={
        "question": "This vector DB is OSS and supports automatic property type inference on import",
        "answer": "Weaviate",
    },
    vector=[0.12345] * 1536
)
print(vec_uuid)

# 1.2 Create object with a specified id 
id_uuid = client.data_object.create(
    class_name=class_name,
    data_object={
        "question": "This vector DB is OSS and supports automatic property type inference on import",
        "answer": "Weaviate",
    },
    uuid="12345678-e64f-5d94-90db-c8cfa3fc9041"
)
print(id_uuid)  # the return value is the object's UUID

# 2. Check object 
# 2.1 check object existence 
check_uuid = "36ddd591-2dee-4e7e-a3cc-eb86d30a4303"
exists = client.data_object.exists(
  check_uuid,
  class_name=class_name,
)
print(exists)

# 2.2 get object info
def get_object(object_id, class_name):
    data_object = client.data_object.get_by_id(
        object_id, 
        class_name=class_name,
        with_vector=True  # boolean
    )
    print(json.dumps(data_object, indent=2))
get_object(check_uuid, class_name)

# 3. Update object 
uuid = "12345678-e64f-5d94-90db-c8cfa3fc5241"  # replace with the id of the object you want to update

# 3.1 Update object properties 
client.data_object.replace(
    uuid=uuid,
    class_name=class_name,
    data_object={
        "answer": "Replaced",
        # The other properties will be deleted
    },
)

# 3.2 Update object vector 
client.data_object.update(
    uuid=uuid,
    class_name=class_name,
    data_object={
        "points": 100,
    },
    vector=[0.12345] * 1536
)

# 3.3 Replace an entire object 
client.data_object.replace(
    uuid=uuid,   # 변경을 원하는 object uuid
    class_name=class_name,
    data_object={
        "answer": "Replaced",
        # The other properties will be deleted
    },
)

# 4. Delete
uuid_to_delete = '...'
class_to_delete = '...'
client.data_object.delete(
    uuid = uuid_to_delete, 
    class_name=class_to_delete,
)

# 4.1 Delete multiple objects 
client.batch.delete_objects(
    class_name=class_to_delete,
    where={
        "path": ["name"],
        "operator": "Like",
        "valueText": "EphemeralObject*"
    },
)

# 4.2 Use ContainsAny / ContainsAll 
client.batch.delete_objects(
    class_name=class_to_delete,
    where={
        "path": ["name"],
        "operator": "ContainsAny",
        "valueTextArray": ["asia", "europe"]  # Note the array syntax
    },
)

# 4.3 Delete multiple objects by id 
client.batch.delete_objects(
    class_name=class_to_delete,
    where={
        "path": ["id"],
        "operator": "ContainsAny",
        "valueTextArray": ["12c88739-7a4e-49fd-bf53-d6a829ba0261", "3022b8be-a6dd-4ef4-b213-821f65cee53b", "30de68c1-dd53-4bed-86ea-915f34faea63"]  # Note the array syntax
    },
)