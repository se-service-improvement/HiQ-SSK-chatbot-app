import argparse
from asyncio import sleep
import dataclasses
import json
import os

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from data_preparation import create_or_update_search_index, upload_documents_to_index

RETRY_COUNT = 5

if __name__ == "__main__":
***REMOVED***parser = argparse.ArgumentParser()
***REMOVED***parser.add_argument("--input_data_path", type=str, required=True)
***REMOVED***parser.add_argument("--config_file", type=str, required=True)

***REMOVED***args = parser.parse_args()

***REMOVED***with open(args.config_file) as f:
***REMOVED***config = json.load(f)

***REMOVED***credential = DefaultAzureCredential()

***REMOVED***if type(config) is not list:
***REMOVED***config = [config]
***REMOVED***
***REMOVED***for index_config in config:
***REMOVED***# Keyvault Secret Client
***REMOVED***print("Connecting to keyvault...")
***REMOVED***keyvault_url = index_config.get("keyvault_url")
***REMOVED***if not keyvault_url:
***REMOVED******REMOVED***print("No keyvault url provided in config file. Secret client will not be set up.")
***REMOVED******REMOVED***secret_client = None
***REMOVED***else:
***REMOVED******REMOVED***secret_client = SecretClient(keyvault_url, credential)

***REMOVED***# Get Search Key
***REMOVED***search_key_secret_name = index_config.get("search_key_secret_name")
***REMOVED***if not search_key_secret_name:
***REMOVED******REMOVED***raise ValueError("No search key secret name provided in config file. Index will not be created.")
***REMOVED***else:
***REMOVED******REMOVED***search_key_secret = secret_client.get_secret(search_key_secret_name)
***REMOVED******REMOVED***search_key = search_key_secret.value

***REMOVED***search_service_name = index_config.get("search_service_name")
***REMOVED***if not search_service_name:
***REMOVED******REMOVED***raise ValueError("No search service name provided in config file. Index will not be created.")

***REMOVED***# Create Index
***REMOVED***print("Creating index...")
***REMOVED***index_name = index_config.get("index_name", "default-index")
***REMOVED***create_or_update_search_index(
***REMOVED******REMOVED***service_name=search_service_name,
***REMOVED******REMOVED***index_name=index_name,
***REMOVED******REMOVED***vector_config_name="default" if "embedding_endpoint" in index_config else None,
***REMOVED******REMOVED***admin_key=search_key
***REMOVED***)
***REMOVED***print(f"Index {index_name} created.")

***REMOVED***# Upload Documents
***REMOVED***print("Uploading documents...")
***REMOVED***with open(args.input_data_path) as input_file:
***REMOVED******REMOVED***documents = [json.loads(line) for line in input_file]
***REMOVED***
***REMOVED***upload_documents_to_index(search_service_name, "", "", index_name, documents, admin_key=search_key)
***REMOVED***print("Done.")

