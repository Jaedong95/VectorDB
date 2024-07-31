import weaviate 

client = weaviate.Client(
    url="http://172.30.1.99:8080"
)
print(client.is_ready())