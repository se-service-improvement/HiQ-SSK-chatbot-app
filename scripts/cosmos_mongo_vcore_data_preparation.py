"""Data Preparation Script for an Azure Cognitive Search Index."""
import argparse
import json
import os
import uuid

import requests
from data_utils import Document
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import AzureCliCredential
from pymongo.mongo_client import MongoClient
from typing import List

from data_utils import chunk_directory

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

def check_if_cosmos_mongo_db_exists(
***REMOVED***account_name: str,
***REMOVED***subscription_id: str,
***REMOVED***resource_group: str,
***REMOVED***credential = None):
***REMOVED***"""_summary_

***REMOVED***Args:
***REMOVED***account_name (str): _description_
***REMOVED***database_name (str): _description_
***REMOVED***subscription_id (str): _description_
***REMOVED***resource_group (str): _description_
***REMOVED***credential: Azure credential to use for getting acs instance
***REMOVED***"""
***REMOVED***if credential is None:
***REMOVED***raise ValueError("credential cannot be None")
***REMOVED***url = (
***REMOVED***f"https://management.azure.com/subscriptions/{subscription_id}"
***REMOVED***f"/resourceGroups/{resource_group}/providers/Microsoft.DocumentDB"
***REMOVED***f"/mongoClusters/{account_name}?api-version=2023-03-01-preview"
***REMOVED***)   

***REMOVED***headers = {
***REMOVED***"Content-Type": "application/json",
***REMOVED***"Authorization": f"Bearer {credential.get_token('https://management.azure.com/.default').token}",
***REMOVED***

***REMOVED***response = requests.get(url, headers=headers)
***REMOVED***return response.status_code == 200

def create_or_update_vector_search_index(
***REMOVED***mongo_client: MongoClient,
***REMOVED***database_name: str,
***REMOVED***collection_name: str,
***REMOVED***index_name,
***REMOVED***vector_field, 
***REMOVED***credential, 
***REMOVED***language):
***REMOVED***if credential is None:
***REMOVED***raise ValueError("credential cannot be None")

***REMOVED***try:
***REMOVED***dbs=mongo_client.list_database_names()
***REMOVED***if (database_name in dbs):
***REMOVED******REMOVED***print(f"database {database_name} exist")
***REMOVED******REMOVED***collections=mongo_client[database_name].list_collection_names()
***REMOVED******REMOVED***if (collection_name in collections):
***REMOVED******REMOVED***print(f"collection {collection_name} exist")

***REMOVED***mongo_collection = mongo_client[database_name][collection_name]  
***REMOVED***indexes = mongo_collection.index_information()
***REMOVED***if (indexes.get(index_name) == None):
***REMOVED******REMOVED***# Ensure the vector index exists.
***REMOVED******REMOVED***indexDefs:List[any] = [
***REMOVED******REMOVED***{ "name": index_name, "key": { vector_field: "cosmosSearch" }, "cosmosSearchOptions": { "kind": "vector-ivf", "similarity": "COS", "dimensions": 1536 } }
***REMOVED******REMOVED***]
***REMOVED******REMOVED***mongo_client[database_name].command("createIndexes", collection_name, indexes = indexDefs)
***REMOVED***except Exception as e:
***REMOVED***raise Exception(
***REMOVED******REMOVED***f"Failed to create vector index {index_name} for collection {collection_name} under database {database_name}. Error: {str(e)}")
***REMOVED***return True

def initialize_mongo_client(
***REMOVED***connection_string: str) -> MongoClient:
***REMOVED***return MongoClient(connection_string)
***REMOVED*** 
def upsert_documents_to_index(
***REMOVED***mongo_client: MongoClient,
***REMOVED***database_name: str,
***REMOVED***collection_name: str,
***REMOVED***docs: List[Document]
***REMOVED***):
***REMOVED***for document in docs:
***REMOVED***finalDocChunk:dict = {}
***REMOVED***finalDocChunk["_id"] = f"doc:{uuid.uuid4()}"
***REMOVED***finalDocChunk['title'] = document.title
***REMOVED***finalDocChunk["filepath"] = document.filepath
***REMOVED***finalDocChunk["url"] = document.url
***REMOVED***finalDocChunk["content"] = document.content
***REMOVED***finalDocChunk["contentvector"] = document.contentVector
***REMOVED***finalDocChunk["metadata"] = document.metadata

***REMOVED***mongo_collection = mongo_client[database_name][collection_name]

***REMOVED***try:
***REMOVED******REMOVED***mongo_collection.insert_one(finalDocChunk)
***REMOVED******REMOVED***print(f"Upsert doc chunk {document.id} successfully")
***REMOVED***
***REMOVED***except Exception as e:
***REMOVED******REMOVED***print(f"Failed to upsert doc chunk {document.id}")
***REMOVED******REMOVED***continue

def validate_index(
***REMOVED***mongo_client: MongoClient,
***REMOVED***database_name: str,
***REMOVED***collection_name: str,
***REMOVED***index_name):
***REMOVED***try:
***REMOVED***mongo_collection = mongo_client[database_name][collection_name]  
***REMOVED***indexes = mongo_collection.index_information()
***REMOVED***if (indexes.get(index_name) == None):
***REMOVED******REMOVED***raise Exception(
***REMOVED******REMOVED***f"Failed to create vector index {index_name} for collection {collection_name} under database {database_name}. Error: {str(e)}")

***REMOVED***except Exception as e:
***REMOVED***raise Exception(
***REMOVED******REMOVED***f"Failed to validate vector index {index_name} for collection {collection_name} under database {database_name}. Error: {str(e)}")  

def create_index(config, credential, form_recognizer_client=None, embedding_model_endpoint=None, use_layout=False, njobs=4):
***REMOVED***account_name = config["account_name"]
***REMOVED***database_name = config["database_name"]
***REMOVED***collection_name = config["collection_name"]
***REMOVED***subscription_id = config["subscription_id"]
***REMOVED***resource_group = config["resource_group"]
***REMOVED***index_name = config["index_name"]
***REMOVED***vector_field = config["vector_field"]
***REMOVED***language = config.get("language", None)

***REMOVED***if language and language not in SUPPORTED_LANGUAGE_CODES:
***REMOVED***raise Exception(f"ERROR: Ingestion does not support {language} documents. "
***REMOVED******REMOVED******REMOVED***f"Please use one of {SUPPORTED_LANGUAGE_CODES}."
***REMOVED******REMOVED******REMOVED***f"Language is set as two letter code for e.g. 'en' for English."
***REMOVED******REMOVED******REMOVED***f"If you do not want to set a language just remove this prompt config or set as None")


***REMOVED***# check if cosmos mongo vcore database account exists
***REMOVED***if check_if_cosmos_mongo_db_exists(account_name, subscription_id, resource_group, credential):
***REMOVED***print(f"Using existing cosmos vcore database account {account_name}")
***REMOVED***else:
***REMOVED***# Won't create the database account automatically for user since it needs set admin password
***REMOVED***raise Exception(f"Database account {account_name} doesn't exist. Please follow this page https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/vcore/quickstart-portal to create the resource")

***REMOVED***# Initialize Cosmos Mongo Client
***REMOVED***mongo_client = initialize_mongo_client(config.get("connection_string"))

***REMOVED***# create or update vector search index with compatible schema
***REMOVED***if not create_or_update_vector_search_index(mongo_client, database_name, collection_name, index_name, vector_field, credential, language):
***REMOVED***raise Exception(f"Failed to create or update index {index_name}")
***REMOVED***
***REMOVED***# chunk directory
***REMOVED***print("Chunking directory...")
***REMOVED***add_embeddings = True

***REMOVED***result = chunk_directory(config["data_path"], num_tokens=config["chunk_size"], token_overlap=config.get("token_overlap",0),
***REMOVED******REMOVED******REMOVED******REMOVED*** azure_credential=credential, form_recognizer_client=form_recognizer_client, use_layout=use_layout, njobs=njobs,
***REMOVED******REMOVED******REMOVED******REMOVED*** add_embeddings=add_embeddings, embedding_endpoint=embedding_model_endpoint)

***REMOVED***if len(result.chunks) == 0:
***REMOVED***raise Exception("No chunks found. Please check the data path and chunk size.")

***REMOVED***print(f"Processed {result.total_files} files")
***REMOVED***print(f"Unsupported formats: {result.num_unsupported_format_files} files")
***REMOVED***print(f"Files with errors: {result.num_files_with_errors} files")
***REMOVED***print(f"Found {len(result.chunks)} chunks")

***REMOVED***# upsert documents to index
***REMOVED***print("Upserting documents to index...")
***REMOVED***upsert_documents_to_index(mongo_client, database_name, collection_name, result.chunks)

***REMOVED***# check if index is ready/validate index
***REMOVED***print("Validating index...")
***REMOVED***validate_index(mongo_client, database_name, collection_name, index_name)
***REMOVED***print("Index validation completed")

def valid_range(n):
***REMOVED***n = int(n)
***REMOVED***if n < 1 or n > 32:
***REMOVED***raise argparse.ArgumentTypeError("njobs must be an Integer between 1 and 32.")
***REMOVED***return n

if __name__ == "__main__": 
***REMOVED***parser = argparse.ArgumentParser()
***REMOVED***parser.add_argument("--cosmos-config", type=str, help="Path to config file containing settings for data preparation")
***REMOVED***parser.add_argument("--form-rec-resource", type=str, help="Name of your Form Recognizer resource to use for PDF cracking.")
***REMOVED***parser.add_argument("--form-rec-key", type=str, help="Key for your Form Recognizer resource to use for PDF cracking.")
***REMOVED***parser.add_argument("--form-rec-use-layout", default=False, action='store_true', help="Whether to use Layout model for PDF cracking, if False will use Read model.")
***REMOVED***parser.add_argument("--njobs", type=valid_range, default=4, help="Number of jobs to run (between 1 and 32). Default=4")
***REMOVED***parser.add_argument("--embedding-model-endpoint", type=str, help="Endpoint for the embedding model to use for vector search. Format: 'https://<AOAI resource name>.openai.azure.com/openai/deployments/<Ada deployment name>/embeddings?api-version=2023-03-15-preview'")
***REMOVED***parser.add_argument("--embedding-model-key", type=str, help="Key for the embedding model to use for vector search.")
***REMOVED***args = parser.parse_args()

***REMOVED***with open(args.cosmos_config) as f:
***REMOVED***config = json.load(f)

***REMOVED***credential = AzureCliCredential()
***REMOVED***form_recognizer_client = None

***REMOVED***print("Data preparation script started")
***REMOVED***if args.form_rec_resource and args.form_rec_key:
***REMOVED***os.environ["FORM_RECOGNIZER_ENDPOINT"] = f"https://{args.form_rec_resource}.cognitiveservices.azure.com/"
***REMOVED***os.environ["FORM_RECOGNIZER_KEY"] = args.form_rec_key
***REMOVED***if args.njobs==1:
***REMOVED******REMOVED***form_recognizer_client = DocumentAnalysisClient(endpoint=f"https://{args.form_rec_resource}.cognitiveservices.azure.com/", credential=AzureKeyCredential(args.form_rec_key))
***REMOVED***print(f"Using Form Recognizer resource {args.form_rec_resource} for PDF cracking, with the {'Layout' if args.form_rec_use_layout else 'Read'} model.")

***REMOVED***for index_config in config:***REMOVED***
***REMOVED***if index_config.get("index_name") and not args.embedding_model_endpoint:
***REMOVED******REMOVED***raise Exception("ERROR: Vector search is enabled in the config, but no embedding model endpoint and key were provided. Please provide these values or disable vector search.")
***REMOVED***print("Preparing data for index:", index_config["index_name"])

***REMOVED***create_index(index_config, credential, form_recognizer_client, embedding_model_endpoint=args.embedding_model_endpoint, use_layout=args.form_rec_use_layout, njobs=args.njobs)
***REMOVED***print("Data preparation for index", index_config["index_name"], "completed")

***REMOVED***print(f"Data preparation script completed. {len(config)} indexes updated.")