import weaviate
import os

client = weaviate.Client(
    url="http://172.30.1.19:8080"
)
print(client.is_ready())

class_name = "Findata5P"
class_obj = {"class": class_name}
# client.schema.create_class(class_obj)   # Article Class Create

response = client.query.get(class_name, ["Question"]).do()
print(response)