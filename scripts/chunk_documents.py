import argparse
import dataclasses
import json
import os

from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.keyvault.secrets import SecretClient
from azure.ai.formrecognizer import DocumentAnalysisClient

from data_utils import chunk_directory

def get_document_intelligence_client(config, secret_client):
***REMOVED***print("Setting up Document Intelligence client...")
***REMOVED***secret_name = config.get("document_intelligence_secret_name")

***REMOVED***if not secret_client or not secret_name:
***REMOVED***print("No keyvault url or secret name provided in config file. Document Intelligence client will not be set up.")
***REMOVED***return None

***REMOVED***endpoint = config.get("document_intelligence_endpoint")
***REMOVED***if not endpoint:
***REMOVED***print("No endpoint provided in config file. Document Intelligence client will not be set up.")
***REMOVED***return None
***REMOVED***
***REMOVED***try:
***REMOVED***document_intelligence_secret = secret_client.get_secret(secret_name)
***REMOVED***os.environ["FORM_RECOGNIZER_ENDPOINT"] = endpoint
***REMOVED***os.environ["FORM_RECOGNIZER_KEY"] = document_intelligence_secret.value

***REMOVED***document_intelligence_credential = AzureKeyCredential(document_intelligence_secret.value)

***REMOVED***document_intelligence_client = DocumentAnalysisClient(endpoint, document_intelligence_credential)
***REMOVED***print("Document Intelligence client set up.")
***REMOVED***return document_intelligence_client
***REMOVED***except Exception as e:
***REMOVED***print("Error setting up Document Intelligence client: {}".format(e))
***REMOVED***return None


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

***REMOVED***# Optional client for cracking documents
***REMOVED***document_intelligence_client = get_document_intelligence_client(index_config, secret_client)

***REMOVED***# Crack and chunk documents
***REMOVED***print("Cracking and chunking documents...")

***REMOVED***chunking_result = chunk_directory(
***REMOVED******REMOVED******REMOVED******REMOVED***directory_path=args.input_data_path, 
***REMOVED******REMOVED******REMOVED******REMOVED***num_tokens=index_config.get("chunk_size", 1024),
***REMOVED******REMOVED******REMOVED******REMOVED***token_overlap=index_config.get("token_overlap", 128),
***REMOVED******REMOVED******REMOVED******REMOVED***form_recognizer_client=document_intelligence_client,
***REMOVED******REMOVED******REMOVED******REMOVED***use_layout=index_config.get("use_layout", False),
***REMOVED******REMOVED******REMOVED******REMOVED***njobs=1)
***REMOVED***
***REMOVED***print(f"Processed {chunking_result.total_files} files")
***REMOVED***print(f"Unsupported formats: {chunking_result.num_unsupported_format_files} files")
***REMOVED***print(f"Files with errors: {chunking_result.num_files_with_errors} files")
***REMOVED***print(f"Found {len(chunking_result.chunks)} chunks")

***REMOVED***print("Writing chunking result to {}...".format(args.output_file_path))
***REMOVED***with open(args.output_file_path, "w") as f:
***REMOVED******REMOVED***for chunk in chunking_result.chunks:
***REMOVED******REMOVED***id = 0
***REMOVED******REMOVED***d = dataclasses.asdict(chunk)
***REMOVED******REMOVED***# add id to documents
***REMOVED******REMOVED***d.update({"id": str(id)})
***REMOVED******REMOVED***f.write(json.dumps(d) + "\n")
***REMOVED******REMOVED***id += 1
***REMOVED***print("Chunking result written to {}.".format(args.output_file_path))
