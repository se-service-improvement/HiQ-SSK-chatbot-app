"""Data Preparation Script for an Azure Cognitive Search Index."""
import argparse
import dataclasses
import json
import os
import subprocess
import time

import requests
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import AzureCliCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv
from tqdm import tqdm

from data_utils import chunk_directory, chunk_blob_container

# Configure environment variables  
load_dotenv() # take environment variables from .env.

SUPPORTED_LANGUAGE_CODES = {
***REMOVED***"ar": "Arabic",
***REMOVED***"hy": "Armenian",
***REMOVED***"eu": "Basque",
***REMOVED***"bg": "Bulgarian",
***REMOVED***"ca": "Catalan",
***REMOVED***"zh-Hans": "Chinese Simplified",
***REMOVED***"zh-Hant": "Chinese Traditional",
***REMOVED***"cs": "Czech",
***REMOVED***"da": "Danish",
***REMOVED***"nl": "Dutch",
***REMOVED***"en": "English",
***REMOVED***"fi": "Finnish",
***REMOVED***"fr": "French",
***REMOVED***"gl": "Galician",
***REMOVED***"de": "German",
***REMOVED***"el": "Greek",
***REMOVED***"hi": "Hindi",
***REMOVED***"hu": "Hungarian",
***REMOVED***"id": "Indonesian (Bahasa)",
***REMOVED***"ga": "Irish",
***REMOVED***"it": "Italian",
***REMOVED***"ja": "Japanese",
***REMOVED***"ko": "Korean",
***REMOVED***"lv": "Latvian",
***REMOVED***"no": "Norwegian",
***REMOVED***"fa": "Persian",
***REMOVED***"pl": "Polish",
***REMOVED***"pt-Br": "Portuguese (Brazil)",
***REMOVED***"pt-Pt": "Portuguese (Portugal)",
***REMOVED***"ro": "Romanian",
***REMOVED***"ru": "Russian",
***REMOVED***"es": "Spanish",
***REMOVED***"sv": "Swedish",
***REMOVED***"th": "Thai",
***REMOVED***"tr": "Turkish"
}


def check_if_search_service_exists(search_service_name: str,
***REMOVED***subscription_id: str,
***REMOVED***resource_group: str,
***REMOVED***credential = None):
***REMOVED***"""_summary_

***REMOVED***Args:
***REMOVED***search_service_name (str): _description_
***REMOVED***subscription_id (str): _description_
***REMOVED***resource_group (str): _description_
***REMOVED***credential: Azure credential to use for getting acs instance
***REMOVED***"""
***REMOVED***if credential is None:
***REMOVED***raise ValueError("credential cannot be None")
***REMOVED***url = (
***REMOVED***f"https://management.azure.com/subscriptions/{subscription_id}"
***REMOVED***f"/resourceGroups/{resource_group}/providers/Microsoft.Search/searchServices"
***REMOVED***f"/{search_service_name}?api-version=2024-03-01-Preview"
***REMOVED***)

***REMOVED***headers = {
***REMOVED***"Content-Type": "application/json",
***REMOVED***"Authorization": f"Bearer {credential.get_token('https://management.azure.com/.default').token}",
***REMOVED***

***REMOVED***response = requests.get(url, headers=headers)
***REMOVED***return response.status_code == 200


def create_search_service(
***REMOVED***search_service_name: str,
***REMOVED***subscription_id: str,
***REMOVED***resource_group: str,
***REMOVED***location: str,
***REMOVED***sku: str = "standard",
***REMOVED***credential = None,
):
***REMOVED***"""_summary_

***REMOVED***Args:
***REMOVED***search_service_name (str): _description_
***REMOVED***subscription_id (str): _description_
***REMOVED***resource_group (str): _description_
***REMOVED***location (str): _description_
***REMOVED***credential: Azure credential to use for creating acs instance

***REMOVED***Raises:
***REMOVED***Exception: _description_
***REMOVED***"""
***REMOVED***if credential is None:
***REMOVED***raise ValueError("credential cannot be None")
***REMOVED***url = (
***REMOVED***f"https://management.azure.com/subscriptions/{subscription_id}"
***REMOVED***f"/resourceGroups/{resource_group}/providers/Microsoft.Search/searchServices"
***REMOVED***f"/{search_service_name}?api-version=2024-03-01-Preview"
***REMOVED***)

***REMOVED***payload = {
***REMOVED***"location": f"{location}",
***REMOVED***"sku": {"name": sku},
***REMOVED***"properties": {
***REMOVED******REMOVED***"replicaCount": 1,
***REMOVED******REMOVED***"partitionCount": 1,
***REMOVED******REMOVED***"hostingMode": "default",
***REMOVED******REMOVED***"semanticSearch": "free",
***REMOVED***,
***REMOVED***

***REMOVED***headers = {
***REMOVED***"Content-Type": "application/json",
***REMOVED***"Authorization": f"Bearer {credential.get_token('https://management.azure.com/.default').token}",
***REMOVED***

***REMOVED***response = requests.put(url, json=payload, headers=headers)
***REMOVED***if response.status_code != 201:
***REMOVED***raise Exception(
***REMOVED******REMOVED***f"Failed to create search service. Error: {response.text}")

def create_or_update_search_index(
***REMOVED***service_name, 
***REMOVED***subscription_id=None, 
***REMOVED***resource_group=None, 
***REMOVED***index_name="default-index", 
***REMOVED***semantic_config_name="default", 
***REMOVED***credential=None, 
***REMOVED***language=None,
***REMOVED***vector_config_name=None,
***REMOVED***admin_key=None):
***REMOVED***
***REMOVED***if credential is None and admin_key is None:
***REMOVED***raise ValueError("credential and admin key cannot be None")
***REMOVED***
***REMOVED***if not admin_key:
***REMOVED***admin_key = json.loads(
***REMOVED******REMOVED***subprocess.run(
***REMOVED******REMOVED***f"az search admin-key show --subscription {subscription_id} --resource-group {resource_group} --service-name {service_name}",
***REMOVED******REMOVED***shell=True,
***REMOVED******REMOVED***capture_output=True,
***REMOVED******REMOVED***).stdout
***REMOVED***)["primaryKey"]

***REMOVED***url = f"https://{service_name}.search.windows.net/indexes/{index_name}?api-version=2024-03-01-Preview"
***REMOVED***headers = {
***REMOVED***"Content-Type": "application/json",
***REMOVED***"api-key": admin_key,
***REMOVED***

***REMOVED***body = {
***REMOVED***"fields": [
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"name": "id",
***REMOVED******REMOVED***"type": "Edm.String",
***REMOVED******REMOVED***"searchable": True,
***REMOVED******REMOVED***"key": True,
***REMOVED***,
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"name": "content",
***REMOVED******REMOVED***"type": "Edm.String",
***REMOVED******REMOVED***"searchable": True,
***REMOVED******REMOVED***"sortable": False,
***REMOVED******REMOVED***"facetable": False,
***REMOVED******REMOVED***"filterable": False,
***REMOVED******REMOVED***"analyzer": f"{language}.lucene" if language else None,
***REMOVED***,
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"name": "title",
***REMOVED******REMOVED***"type": "Edm.String",
***REMOVED******REMOVED***"searchable": True,
***REMOVED******REMOVED***"sortable": False,
***REMOVED******REMOVED***"facetable": False,
***REMOVED******REMOVED***"filterable": False,
***REMOVED******REMOVED***"analyzer": f"{language}.lucene" if language else None,
***REMOVED***,
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"name": "filepath",
***REMOVED******REMOVED***"type": "Edm.String",
***REMOVED******REMOVED***"searchable": True,
***REMOVED******REMOVED***"sortable": False,
***REMOVED******REMOVED***"facetable": False,
***REMOVED******REMOVED***"filterable": False,
***REMOVED***,
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"name": "url",
***REMOVED******REMOVED***"type": "Edm.String",
***REMOVED******REMOVED***"searchable": True,
***REMOVED***,
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"name": "metadata",
***REMOVED******REMOVED***"type": "Edm.String",
***REMOVED******REMOVED***"searchable": True,
***REMOVED***,
***REMOVED***],
***REMOVED***"suggesters": [],
***REMOVED***"scoringProfiles": [],
***REMOVED***"semantic": {
***REMOVED******REMOVED***"configurations": [
***REMOVED******REMOVED***{
***REMOVED******REMOVED******REMOVED***"name": semantic_config_name,
***REMOVED******REMOVED******REMOVED***"prioritizedFields": {
***REMOVED******REMOVED******REMOVED***"titleField": {"fieldName": "title"},
***REMOVED******REMOVED******REMOVED***"prioritizedContentFields": [{"fieldName": "content"}],
***REMOVED******REMOVED******REMOVED***"prioritizedKeywordsFields": [],
***REMOVED******REMOVED***,
***REMOVED******REMOVED***
***REMOVED******REMOVED***]
***REMOVED***,
***REMOVED***

***REMOVED***if vector_config_name:
***REMOVED***body["fields"].append({
***REMOVED******REMOVED***"name": "contentVector",
***REMOVED******REMOVED***"type": "Collection(Edm.Single)",
***REMOVED******REMOVED***"searchable": True,
***REMOVED******REMOVED***"retrievable": True,
***REMOVED******REMOVED***"stored": True,
***REMOVED******REMOVED***"dimensions": int(os.getenv("VECTOR_DIMENSION", 1536)),
***REMOVED******REMOVED***"vectorSearchProfile": vector_config_name
***REMOVED***)

***REMOVED***body["vectorSearch"] = {
***REMOVED***"algorithms": [
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"name": "my-hnsw-config-1",
***REMOVED******REMOVED***"kind": "hnsw",
***REMOVED******REMOVED***"hnswParameters": {
***REMOVED******REMOVED******REMOVED***"m": 4,
***REMOVED******REMOVED******REMOVED***"efConstruction": 400,
***REMOVED******REMOVED******REMOVED***"efSearch": 500,
***REMOVED******REMOVED******REMOVED***"metric": "cosine"
***REMOVED******REMOVED***
***REMOVED***
***REMOVED***],
***REMOVED***"profiles": [
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"name": vector_config_name,
***REMOVED******REMOVED***"algorithm": "my-hnsw-config-1"
***REMOVED***
***REMOVED***]
***REMOVED***

***REMOVED***response = requests.put(url, json=body, headers=headers)
***REMOVED***if response.status_code == 201:
***REMOVED***print(f"Created search index {index_name}")
***REMOVED***elif response.status_code == 204:
***REMOVED***print(f"Updated existing search index {index_name}")
***REMOVED***else:
***REMOVED***raise Exception(f"Failed to create search index. Error: {response.text}")
***REMOVED***
***REMOVED***return True


def upload_documents_to_index(service_name, subscription_id, resource_group, index_name, docs, credential=None, upload_batch_size = 50, admin_key=None):
***REMOVED***if credential is None and admin_key is None:
***REMOVED***raise ValueError("credential and admin_key cannot be None")
***REMOVED***
***REMOVED***to_upload_dicts = []

***REMOVED***id = 0
***REMOVED***for d in docs:
***REMOVED***if type(d) is not dict:
***REMOVED******REMOVED***d = dataclasses.asdict(d)
***REMOVED***# add id to documents
***REMOVED***d.update({"@search.action": "upload", "id": str(id)})
***REMOVED***if "contentVector" in d and d["contentVector"] is None:
***REMOVED******REMOVED***del d["contentVector"]
***REMOVED***to_upload_dicts.append(d)
***REMOVED***id += 1
***REMOVED***
***REMOVED***endpoint = "https://{}.search.windows.net/".format(service_name)
***REMOVED***if not admin_key:
***REMOVED***admin_key = json.loads(
***REMOVED******REMOVED***subprocess.run(
***REMOVED******REMOVED***f"az search admin-key show --subscription {subscription_id} --resource-group {resource_group} --service-name {service_name}",
***REMOVED******REMOVED***shell=True,
***REMOVED******REMOVED***capture_output=True,
***REMOVED******REMOVED***).stdout
***REMOVED***)["primaryKey"]

***REMOVED***search_client = SearchClient(
***REMOVED***endpoint=endpoint,
***REMOVED***index_name=index_name,
***REMOVED***credential=AzureKeyCredential(admin_key),
***REMOVED***)
***REMOVED***# Upload the documents in batches of upload_batch_size
***REMOVED***for i in tqdm(range(0, len(to_upload_dicts), upload_batch_size), desc="Indexing Chunks..."):
***REMOVED***batch = to_upload_dicts[i: i + upload_batch_size]
***REMOVED***results = search_client.upload_documents(documents=batch)
***REMOVED***num_failures = 0
***REMOVED***errors = set()
***REMOVED***for result in results:
***REMOVED******REMOVED***if not result.succeeded:
***REMOVED******REMOVED***print(f"Indexing Failed for {result.key} with ERROR: {result.error_message}")
***REMOVED******REMOVED***num_failures += 1
***REMOVED******REMOVED***errors.add(result.error_message)
***REMOVED***if num_failures > 0:
***REMOVED******REMOVED***raise Exception(f"INDEXING FAILED for {num_failures} documents. Please recreate the index."
***REMOVED******REMOVED******REMOVED******REMOVED***f"To Debug: PLEASE CHECK chunk_size and upload_batch_size. \n Error Messages: {list(errors)}")

def validate_index(service_name, subscription_id, resource_group, index_name):
***REMOVED***api_version = "2024-03-01-Preview"
***REMOVED***admin_key = json.loads(
***REMOVED***subprocess.run(
***REMOVED******REMOVED***f"az search admin-key show --subscription {subscription_id} --resource-group {resource_group} --service-name {service_name}",
***REMOVED******REMOVED***shell=True,
***REMOVED******REMOVED***capture_output=True,
***REMOVED***).stdout
***REMOVED***)["primaryKey"]

***REMOVED***headers = {
***REMOVED***"Content-Type": "application/json", 
***REMOVED***"api-key": admin_key}
***REMOVED***params = {"api-version": api_version}
***REMOVED***url = f"https://{service_name}.search.windows.net/indexes/{index_name}/stats"
***REMOVED***for retry_count in range(5):
***REMOVED***response = requests.get(url, headers=headers, params=params)

***REMOVED***if response.status_code == 200:
***REMOVED******REMOVED***response = response.json()
***REMOVED******REMOVED***num_chunks = response['documentCount']
***REMOVED******REMOVED***if num_chunks==0 and retry_count < 4:
***REMOVED******REMOVED***print("Index is empty. Waiting 60 seconds to check again...")
***REMOVED******REMOVED***time.sleep(60)
***REMOVED******REMOVED***elif num_chunks==0 and retry_count == 4:
***REMOVED******REMOVED***print("Index is empty. Please investigate and re-index.")
***REMOVED******REMOVED***else:
***REMOVED******REMOVED***print(f"The index contains {num_chunks} chunks.")
***REMOVED******REMOVED***average_chunk_size = response['storageSize']/num_chunks
***REMOVED******REMOVED***print(f"The average chunk size of the index is {average_chunk_size} bytes.")
***REMOVED******REMOVED***break
***REMOVED***else:
***REMOVED******REMOVED***if response.status_code==404:
***REMOVED******REMOVED***print(f"The index does not seem to exist. Please make sure the index was created correctly, and that you are using the correct service and index names")
***REMOVED******REMOVED***elif response.status_code==403:
***REMOVED******REMOVED***print(f"Authentication Failure: Make sure you are using the correct key")
***REMOVED******REMOVED***else:
***REMOVED******REMOVED***print(f"Request failed. Please investigate. Status code: {response.status_code}")
***REMOVED******REMOVED***break

def create_index(config, credential, form_recognizer_client=None, embedding_model_endpoint=None, use_layout=False, njobs=4):
***REMOVED***service_name = config["search_service_name"]
***REMOVED***subscription_id = config["subscription_id"]
***REMOVED***resource_group = config["resource_group"]
***REMOVED***location = config["location"]
***REMOVED***index_name = config["index_name"]
***REMOVED***language = config.get("language", None)

***REMOVED***if language and language not in SUPPORTED_LANGUAGE_CODES:
***REMOVED***raise Exception(f"ERROR: Ingestion does not support {language} documents. "
***REMOVED******REMOVED******REMOVED***f"Please use one of {SUPPORTED_LANGUAGE_CODES}."
***REMOVED******REMOVED******REMOVED***f"Language is set as two letter code for e.g. 'en' for English."
***REMOVED******REMOVED******REMOVED***f"If you donot want to set a language just remove this prompt config or set as None")


***REMOVED***# check if search service exists, create if not
***REMOVED***try:
***REMOVED***if check_if_search_service_exists(service_name, subscription_id, resource_group, credential):
***REMOVED******REMOVED***print(f"Using existing search service {service_name}")
***REMOVED***else:
***REMOVED******REMOVED***print(f"Creating search service {service_name}")
***REMOVED******REMOVED***create_search_service(service_name, subscription_id, resource_group, location, credential=credential)
***REMOVED***except Exception as e:
***REMOVED***print(f"Unable to verify if search service exists. Error: {e}")
***REMOVED***print("Proceeding to attempt to create index.")

***REMOVED***# create or update search index with compatible schema
***REMOVED***admin_key = os.environ.get("AZURE_SEARCH_ADMIN_KEY", None)
***REMOVED***if not create_or_update_search_index(service_name, subscription_id, resource_group, index_name, config["semantic_config_name"], credential, language, vector_config_name=config.get("vector_config_name", None), admin_key=admin_key):
***REMOVED***raise Exception(f"Failed to create or update index {index_name}")
***REMOVED***
***REMOVED***data_configs = []
***REMOVED***if "data_path" in config:
***REMOVED***data_configs.append({
***REMOVED******REMOVED***"path": config["data_path"],
***REMOVED******REMOVED***"url_prefix": config.get("url_prefix", None),
***REMOVED***)
***REMOVED***if "data_paths" in config:
***REMOVED***data_configs.extend(config["data_paths"])

***REMOVED***for data_config in data_configs:
***REMOVED***# chunk directory
***REMOVED***print(f"Chunking path {data_config['path']}...")
***REMOVED***add_embeddings = False
***REMOVED***if config.get("vector_config_name") and embedding_model_endpoint:
***REMOVED******REMOVED***add_embeddings = True

***REMOVED***if "blob.core" in data_config["path"]:
***REMOVED******REMOVED***result = chunk_blob_container(data_config["path"], credential=credential, num_tokens=config["chunk_size"], token_overlap=config.get("token_overlap",0),
***REMOVED******REMOVED******REMOVED******REMOVED***azure_credential=credential, form_recognizer_client=form_recognizer_client, use_layout=use_layout, njobs=njobs,
***REMOVED******REMOVED******REMOVED******REMOVED***add_embeddings=add_embeddings, embedding_endpoint=embedding_model_endpoint, url_prefix=data_config["url_prefix"])
***REMOVED***elif os.path.exists(data_config["path"]):
***REMOVED******REMOVED***result = chunk_directory(data_config["path"], num_tokens=config["chunk_size"], token_overlap=config.get("token_overlap",0),
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***azure_credential=credential, form_recognizer_client=form_recognizer_client, use_layout=use_layout, njobs=njobs,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***add_embeddings=add_embeddings, embedding_endpoint=embedding_model_endpoint, url_prefix=data_config["url_prefix"])
***REMOVED***else:
***REMOVED******REMOVED***raise Exception(f"Path {data_config['path']} does not exist and is not a blob URL. Please check the path and try again.")

***REMOVED***if len(result.chunks) == 0:
***REMOVED******REMOVED***raise Exception("No chunks found. Please check the data path and chunk size.")

***REMOVED***print(f"Processed {result.total_files} files")
***REMOVED***print(f"Unsupported formats: {result.num_unsupported_format_files} files")
***REMOVED***print(f"Files with errors: {result.num_files_with_errors} files")
***REMOVED***print(f"Found {len(result.chunks)} chunks")

***REMOVED***# upload documents to index
***REMOVED***print("Uploading documents to index...")
***REMOVED***upload_documents_to_index(service_name, subscription_id, resource_group, index_name, result.chunks, credential)

***REMOVED***# check if index is ready/validate index
***REMOVED***print("Validating index...")
***REMOVED***validate_index(service_name, subscription_id, resource_group, index_name)
***REMOVED***print("Index validation completed")


def valid_range(n):
***REMOVED***n = int(n)
***REMOVED***if n < 1 or n > 32:
***REMOVED***raise argparse.ArgumentTypeError("njobs must be an Integer between 1 and 32.")
***REMOVED***return n

if __name__ == "__main__": 
***REMOVED***parser = argparse.ArgumentParser()
***REMOVED***parser.add_argument("--config", type=str, help="Path to config file containing settings for data preparation")
***REMOVED***parser.add_argument("--form-rec-resource", type=str, help="Name of your Form Recognizer resource to use for PDF cracking.")
***REMOVED***parser.add_argument("--form-rec-key", type=str, help="Key for your Form Recognizer resource to use for PDF cracking.")
***REMOVED***parser.add_argument("--form-rec-use-layout", default=False, action='store_true', help="Whether to use Layout model for PDF cracking, if False will use Read model.")
***REMOVED***parser.add_argument("--njobs", type=valid_range, default=4, help="Number of jobs to run (between 1 and 32). Default=4")
***REMOVED***parser.add_argument("--embedding-model-endpoint", type=str, help="Endpoint for the embedding model to use for vector search. Format: 'https://<AOAI resource name>.openai.azure.com/openai/deployments/<Ada deployment name>/embeddings?api-version=2024-03-01-Preview'")
***REMOVED***parser.add_argument("--embedding-model-key", type=str, help="Key for the embedding model to use for vector search.")
***REMOVED***parser.add_argument("--search-admin-key", type=str, help="Admin key for the search service. If not provided, will use Azure CLI to get the key.")
***REMOVED***args = parser.parse_args()

***REMOVED***with open(args.config) as f:
***REMOVED***config = json.load(f)

***REMOVED***credential = AzureCliCredential()
***REMOVED***form_recognizer_client = None

***REMOVED***print("Data preparation script started")
***REMOVED***if args.search_admin_key:
***REMOVED***os.environ["AZURE_SEARCH_ADMIN_KEY"] = args.search_admin_key

***REMOVED***if args.form_rec_resource and args.form_rec_key:
***REMOVED***os.environ["FORM_RECOGNIZER_ENDPOINT"] = f"https://{args.form_rec_resource}.cognitiveservices.azure.com/"
***REMOVED***os.environ["FORM_RECOGNIZER_KEY"] = args.form_rec_key
***REMOVED***if args.njobs==1:
***REMOVED******REMOVED***form_recognizer_client = DocumentAnalysisClient(endpoint=f"https://{args.form_rec_resource}.cognitiveservices.azure.com/", credential=AzureKeyCredential(args.form_rec_key))
***REMOVED***print(f"Using Form Recognizer resource {args.form_rec_resource} for PDF cracking, with the {'Layout' if args.form_rec_use_layout else 'Read'} model.")

***REMOVED***for index_config in config:
***REMOVED***print("Preparing data for index:", index_config["index_name"])
***REMOVED***if index_config.get("vector_config_name") and not args.embedding_model_endpoint:
***REMOVED******REMOVED***raise Exception("ERROR: Vector search is enabled in the config, but no embedding model endpoint and key were provided. Please provide these values or disable vector search.")
***REMOVED***
***REMOVED***create_index(index_config, credential, form_recognizer_client, embedding_model_endpoint=args.embedding_model_endpoint, use_layout=args.form_rec_use_layout, njobs=args.njobs)
***REMOVED***print("Data preparation for index", index_config["index_name"], "completed")

***REMOVED***print(f"Data preparation script completed. {len(config)} indexes updated.")