"""Data Preparation Script for an Azure Cognitive Search Index."""
import argparse
import json
import time
import requests
import subprocess
import dataclasses
from tqdm import tqdm
from azure.core.credentials import AzureKeyCredential
from azure.identity import AzureCliCredential
from data_utils import chunk_directory
from azure.search.documents import SearchClient

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
***REMOVED***f"/{search_service_name}?api-version=2021-04-01-preview"
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
***REMOVED***f"/{search_service_name}?api-version=2021-04-01-preview"
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

def create_or_update_search_index(service_name, subscription_id, resource_group, index_name, semantic_config_name, credential):
***REMOVED***if credential is None:
***REMOVED***raise ValueError("credential cannot be None")
***REMOVED***admin_key = json.loads(
***REMOVED***subprocess.run(
***REMOVED******REMOVED***f"az search admin-key show --subscription {subscription_id} --resource-group {resource_group} --service-name {service_name}",
***REMOVED******REMOVED***shell=True,
***REMOVED******REMOVED***capture_output=True,
***REMOVED***).stdout
***REMOVED***)["primaryKey"]

***REMOVED***url = f"https://{service_name}.search.windows.net/indexes/{index_name}?api-version=2021-04-30-Preview"
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
***REMOVED******REMOVED***"analyzer": "en.lucene",
***REMOVED******REMOVED***"key": True,
***REMOVED***,
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"name": "content",
***REMOVED******REMOVED***"type": "Edm.String",
***REMOVED******REMOVED***"searchable": True,
***REMOVED******REMOVED***"sortable": False,
***REMOVED******REMOVED***"facetable": False,
***REMOVED******REMOVED***"filterable": False,
***REMOVED******REMOVED***"analyzer": "en.lucene",
***REMOVED***,
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"name": "title",
***REMOVED******REMOVED***"type": "Edm.String",
***REMOVED******REMOVED***"searchable": True,
***REMOVED******REMOVED***"sortable": False,
***REMOVED******REMOVED***"facetable": False,
***REMOVED******REMOVED***"filterable": False,
***REMOVED******REMOVED***"analyzer": "en.lucene",
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

***REMOVED***response = requests.put(url, json=body, headers=headers)
***REMOVED***if response.status_code == 201:
***REMOVED***print(f"Created search index {index_name}")
***REMOVED***elif response.status_code == 204:
***REMOVED***print(f"Updated existing search index {index_name}")
***REMOVED***else:
***REMOVED***raise Exception(f"Failed to create search index. Error: {response.text}")
***REMOVED***
***REMOVED***return True

def upload_documents_to_index(service_name, subscription_id, resource_group, index_name, docs, credential, upload_batch_size = 1000):
***REMOVED***if credential is None:
***REMOVED***raise ValueError("credential cannot be None")
***REMOVED***
***REMOVED***to_upload_dicts = []

***REMOVED***id = 0
***REMOVED***for document in docs:
***REMOVED***d = dataclasses.asdict(document)
***REMOVED***# add id to documents
***REMOVED***d.update({"@search.action": "upload", "id": str(id)})
***REMOVED***to_upload_dicts.append(d)
***REMOVED***id += 1
***REMOVED***
***REMOVED***endpoint = "https://{}.search.windows.net/".format(service_name)
***REMOVED***admin_key = json.loads(
***REMOVED***subprocess.run(
***REMOVED******REMOVED***f"az search admin-key show --subscription {subscription_id} --resource-group {resource_group} --service-name {service_name}",
***REMOVED******REMOVED***shell=True,
***REMOVED******REMOVED***capture_output=True,
***REMOVED***).stdout
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
***REMOVED***api_version = "2021-04-30-Preview"
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

def create_index(config, credential):
***REMOVED***service_name = config["search_service_name"]
***REMOVED***subscription_id = config["subscription_id"]
***REMOVED***resource_group = config["resource_group"]
***REMOVED***location = config["location"]
***REMOVED***index_name = config["index_name"]

***REMOVED***# check if search service exists, create if not
***REMOVED***if check_if_search_service_exists(service_name, subscription_id, resource_group, credential):
***REMOVED***print(f"Using existing search service {service_name}")
***REMOVED***else:
***REMOVED***print(f"Creating search service {service_name}")
***REMOVED***create_search_service(service_name, subscription_id, resource_group, location, credential=credential)

***REMOVED***# create or update search index with compatible schema
***REMOVED***if not create_or_update_search_index(service_name, subscription_id, resource_group, index_name, config["semantic_config_name"], credential):
***REMOVED***raise Exception(f"Failed to create or update index {index_name}")
***REMOVED***
***REMOVED***# chunk directory
***REMOVED***print("Chunking directory...")
***REMOVED***result = chunk_directory(config["data_path"], num_tokens=config["chunk_size"])

***REMOVED***# upload documents to index
***REMOVED***print("Uploading documents to index...")
***REMOVED***upload_documents_to_index(service_name, subscription_id, resource_group, index_name, result.chunks, credential)

***REMOVED***# check if index is ready/validate index
***REMOVED***print("Validating index...")
***REMOVED***validate_index(service_name, subscription_id, resource_group, index_name)
***REMOVED***print("Index validation completed")

if __name__ == "__main__": 
***REMOVED***parser = argparse.ArgumentParser()
***REMOVED***parser.add_argument("--config", type=str, help="Path to config file containing settings for data preparation")
***REMOVED***args = parser.parse_args()

***REMOVED***with open(args.config) as f:
***REMOVED***config = json.load(f)

***REMOVED***credential = AzureCliCredential()

***REMOVED***print("Data preparation script started")
***REMOVED***for index_config in config:
***REMOVED***print("Preparing data for index:", index_config["index_name"])
***REMOVED***create_index(index_config, credential)
***REMOVED***print("Data preparation for index", index_config["index_name"], "completed")

***REMOVED***print(f"Data preparation script completed. {len(config)} indexes updated.")