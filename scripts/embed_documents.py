import argparse
from asyncio import sleep
import json

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from data_utils import get_embedding

RETRY_COUNT = 5

if __name__ == "__main__":
***REMOVED***parser = argparse.ArgumentParser()
***REMOVED***parser.add_argument("--input_data_path", type=str, required=True)
***REMOVED***parser.add_argument("--output_file_path", type=str, required=True)
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
***REMOVED***keyvault_url = index_config.get("keyvault_url")
***REMOVED***if not keyvault_url:
***REMOVED******REMOVED***print("No keyvault url provided in config file. Secret client will not be set up.")
***REMOVED******REMOVED***secret_client = None
***REMOVED***else:
***REMOVED******REMOVED***secret_client = SecretClient(keyvault_url, credential)

***REMOVED***# Get Embedding key
***REMOVED***embedding_key_secret_name = index_config.get("embedding_key_secret_name")
***REMOVED***if not embedding_key_secret_name:
***REMOVED******REMOVED***raise ValueError("No embedding key secret name provided in config file. Embeddings will not be generated.")
***REMOVED***else:
***REMOVED******REMOVED***embedding_key_secret = secret_client.get_secret(embedding_key_secret_name)
***REMOVED******REMOVED***embedding_key = embedding_key_secret.value

***REMOVED***embedding_endpoint = index_config.get("embedding_endpoint")
***REMOVED***if not embedding_endpoint:
***REMOVED******REMOVED***raise ValueError("No embedding endpoint provided in config file. Embeddings will not be generated.")

***REMOVED***# Embed documents
***REMOVED***print("Generating embeddings...")
***REMOVED***with open(args.input_data_path) as input_file, open(args.output_file_path, "w") as output_file:
***REMOVED******REMOVED***for line in input_file:
***REMOVED******REMOVED***document = json.loads(line)
***REMOVED******REMOVED***# Sleep/Retry in case embedding model is rate limited.
***REMOVED******REMOVED***for _ in range(RETRY_COUNT):
***REMOVED******REMOVED******REMOVED***try:
***REMOVED******REMOVED******REMOVED***embedding = get_embedding(document["content"], embedding_endpoint,  embedding_key)
***REMOVED******REMOVED******REMOVED***document["contentVector"] = embedding
***REMOVED******REMOVED******REMOVED***break
***REMOVED******REMOVED******REMOVED***except:
***REMOVED******REMOVED******REMOVED***print("Error generating embedding. Retrying...")
***REMOVED******REMOVED******REMOVED***sleep(30)
***REMOVED******REMOVED***
***REMOVED******REMOVED***output_file.write(json.dumps(document) + "\n")

***REMOVED***print("Embeddings generated and saved to {}.".format(args.output_file_path))

