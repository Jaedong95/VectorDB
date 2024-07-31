import weaviate
import os

client = weaviate.Client(
    url="http://172.30.1.19:8080"
)
print(client.is_ready())

class_name = "Findata5"
class_obj = {"class": class_name}
client.schema.create_class(class_obj)   # Article Class Create

# 1. Create Collection 
## 1.1 define properties
class_obj = {
    "class": class_name + "P",
    "properties": [
        {
            "name": "title",
            "dataType": ["text"],
        },
        {
            "name": "body",
            "dataType": ["text"],
        },
    ],
}
client.schema.create_class(class_obj)

## 1.2 Specify Vectorizer
class_obj = {
    "class": class_name + "vec",
    "vectorizer": "text2vec-openai",  # this could be any vectorizer
    "moduleConfig": {
        "text2vec-openai": {  # this must match the vectorizer used
            "vectorizeClassName": True,
            "model": "text-embedding-3-large",
        }
    }
}
client.schema.create_class(class_obj)

## 1.3 Set vector index type 
class_obj = {
    'class': class_name + "VI",
    'properties': [
        {
            'name': 'title',
            'dataType': ['text'],
        },
    ],
    'vectorizer': 'text2vec-openai',  # this could be any vectorizer
    "vectorIndexType": "hnsw",  # or "flat" or "dynamic"
}
client.schema.create_class(class_obj)

## 1.4 Set vector index parameters 
class_obj = {
    'class': class_name + "VIP",
    # Additional configuration not shown
    "vectorIndexType": "flat",
    "vectorIndexConfig": {
        "bq": {
            "enabled": True,  # Enable BQ compression. Default: False
            "rescoreLimit": 200,  # The minimum number of candidates to fetch before rescoring. Default: -1 (No limit)
            "cache": True,  # Enable use of vector cache. Default: False
        },
        "vectorCacheMaxObjects": 100000,  # Cache size if `cache` enabled. Default: 1000000000000
        # "distance": "cosine",   # specify distance metrics    
    }
}
client.schema.create_class(class_obj)

## 1.5 Property-level settings 
class_obj = {
    "class": "Article",
    "vectorizer": "text2vec-huggingface",  # this could be any vectorizer
    "properties": [
        {
            "name": "title",
            "dataType": ["text"],
            "moduleConfig": {
                "text2vec-huggingface": {  # this must match the vectorizer used
                    "vectorizePropertyName": True,
                    "tokenization": "lowercase"
                }
            }
        },
        {
            "name": "body",
            "dataType": ["text"],
            "moduleConfig": {
                "text2vec-huggingface": {  # this must match the vectorizer used
                    "skip": True,  # Don't vectorize body
                    "tokenization": "whitespace"
                }
            }
        },
    ],
}

client.schema.create_class(class_obj)

# 2. 

import weaviate
from weaviate.embedded import EmbeddedOptions

client = weaviate.Client(
  embedded_options=EmbeddedOptions()
)

response = client.query.get("JeopardyQuestion", ["question"]).do()
print(response)