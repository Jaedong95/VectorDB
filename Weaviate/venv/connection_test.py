import weaviate
import os
  
# Set these environment variables
URL = "https://jvmtrkkqugjjln1ow2fq.c0.asia-southeast1.gcp.weaviate.cloud"
APIKEY = "GTdegq6zD5vqbZ29V3kZLsqJfTlT0GXn3uwt"
  
# Connect to a WCS instance
client = weaviate.connect_to_wcs(
    cluster_url=URL,
    auth_credentials=weaviate.auth.AuthApiKey(APIKEY)
)