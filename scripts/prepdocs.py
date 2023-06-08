import argparse
import dataclasses

from tqdm import tqdm
from azure.identity import AzureDeveloperCliCredential
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
***REMOVED***SearchableField,
***REMOVED***SemanticField,
***REMOVED***SemanticSettings,
***REMOVED***SemanticConfiguration,
***REMOVED***SearchIndex,
***REMOVED***PrioritizedFields
)
from azure.search.documents import SearchClient
from azure.ai.formrecognizer import DocumentAnalysisClient


from data_utils import chunk_directory



def create_search_index(index_name, index_client):
***REMOVED***print(f"Ensuring search index {index_name} exists")
***REMOVED***if index_name not in index_client.list_index_names():
***REMOVED***index = SearchIndex(
***REMOVED******REMOVED***name=index_name,
***REMOVED******REMOVED***fields=[
***REMOVED******REMOVED***SearchableField(name="id", type="Edm.String", key=True),
***REMOVED******REMOVED***SearchableField(name="content", type="Edm.String", analyzer_name="en.lucene"),
***REMOVED******REMOVED***SearchableField(name="title", type="Edm.String", analyzer_name="en.lucene"),
***REMOVED******REMOVED***SearchableField(name="filepath", type="Edm.String"),
***REMOVED******REMOVED***SearchableField(name="url", type="Edm.String"),
***REMOVED******REMOVED***SearchableField(name="metadata", type="Edm.String")
***REMOVED******REMOVED***],
***REMOVED******REMOVED***semantic_settings=SemanticSettings(
***REMOVED******REMOVED***configurations=[SemanticConfiguration(
***REMOVED******REMOVED******REMOVED***name='default',
***REMOVED******REMOVED******REMOVED***prioritized_fields=PrioritizedFields(
***REMOVED******REMOVED******REMOVED***title_field=SemanticField(field_name='title'),
***REMOVED******REMOVED******REMOVED***prioritized_content_fields=[SemanticField(field_name='content')]))])
***REMOVED***)
***REMOVED***print(f"Creating {index_name} search index")
***REMOVED***index_client.create_index(index)
***REMOVED***else:
***REMOVED***print(f"Search index {index_name} already exists")

def upload_documents_to_index(docs, search_client, upload_batch_size = 50):
***REMOVED***to_upload_dicts = []

***REMOVED***id = 0
***REMOVED***for document in docs:
***REMOVED***d = dataclasses.asdict(document)
***REMOVED***# add id to documents
***REMOVED***d.update({"@search.action": "upload", "id": str(id)})
***REMOVED***to_upload_dicts.append(d)
***REMOVED***id += 1
***REMOVED***

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


def create_and_populate_index(index_name, index_client, search_client, form_recognizer_client):

***REMOVED***# create or update search index with compatible schema
***REMOVED***create_search_index(index_name, index_client)

***REMOVED***# chunk directory
***REMOVED***print("Chunking directory...")
***REMOVED***result = chunk_directory("./data", form_recognizer_client=form_recognizer_client, use_layout=True, ignore_errors=False)

***REMOVED***if len(result.chunks) == 0:
***REMOVED***raise Exception("No chunks found. Please check the data path and chunk size.")

***REMOVED***print(f"Processed {result.total_files} files")
***REMOVED***print(f"Unsupported formats: {result.num_unsupported_format_files} files")
***REMOVED***print(f"Files with errors: {result.num_files_with_errors} files")
***REMOVED***print(f"Found {len(result.chunks)} chunks")

***REMOVED***# upload documents to index
***REMOVED***print("Uploading documents to index...")
***REMOVED***upload_documents_to_index(result.chunks, search_client)

***REMOVED***# check if index is ready/validate index
***REMOVED***# print("Validating index...")
***REMOVED***# TODO: validate_index(index_name) - Port to Azure CLI
***REMOVED***# print("Index validation completed")


if __name__ == "__main__": 
***REMOVED***parser = argparse.ArgumentParser(
***REMOVED***description="Prepare documents by extracting content from PDFs, splitting content into sections, uploading to blob storage, and indexing in a search index.",
***REMOVED***epilog="Example: prepdocs.py '..\data\*' --storageaccount myaccount --container mycontainer --searchservice mysearch --index myindex -v"
***REMOVED***)
***REMOVED***parser.add_argument("files", help="Files to be processed")
***REMOVED***parser.add_argument("--storageaccount", help="Azure Blob Storage account name")
***REMOVED***parser.add_argument("--container", help="Azure Blob Storage container name")
***REMOVED***parser.add_argument("--storagekey", required=False, help="Optional. Use this Azure Blob Storage account key instead of the current user identity to login (use az login to set current user for Azure)")
***REMOVED***parser.add_argument("--tenantid", required=False, help="Optional. Use this to define the Azure directory where to authenticate)")
***REMOVED***parser.add_argument("--searchservice", help="Name of the Azure Cognitive Search service where content should be indexed (must exist already)")
***REMOVED***parser.add_argument("--index", help="Name of the Azure Cognitive Search index where content should be indexed (will be created if it doesn't exist)")
***REMOVED***parser.add_argument("--searchkey", required=False, help="Optional. Use this Azure Cognitive Search account key instead of the current user identity to login (use az login to set current user for Azure)")
***REMOVED***parser.add_argument("--formrecognizerservice", required=False, help="Optional. Name of the Azure Form Recognizer service which will be used to extract text, tables and layout from the documents (must exist already)")
***REMOVED***parser.add_argument("--formrecognizerkey", required=False, help="Optional. Use this Azure Form Recognizer account key instead of the current user identity to login (use az login to set current user for Azure)")
***REMOVED***args = parser.parse_args()

***REMOVED***# Use the current user identity to connect to Azure services unless a key is explicitly set for any of them
***REMOVED***azd_credential = AzureDeveloperCliCredential() if args.tenantid == None else AzureDeveloperCliCredential(tenant_id=args.tenantid, process_timeout=60)
***REMOVED***default_creds = azd_credential if args.searchkey == None or args.storagekey == None else None
***REMOVED***search_creds = default_creds if args.searchkey == None else AzureKeyCredential(args.searchkey)
***REMOVED***formrecognizer_creds = default_creds if args.formrecognizerkey == None else AzureKeyCredential(args.formrecognizerkey)

***REMOVED***print("Data preparation script started")
***REMOVED***print("Preparing data for index:", args.index)
***REMOVED***search_endpoint = f"https://{args.searchservice}.search.windows.net/" 
***REMOVED***index_client = SearchIndexClient(endpoint=search_endpoint, credential=search_creds)
***REMOVED***search_client = SearchClient(endpoint=search_endpoint, credential=search_creds, index_name=args.index)
***REMOVED***form_recognizer_client = DocumentAnalysisClient(
***REMOVED***endpoint=f"https://{args.formrecognizerservice}.cognitiveservices.azure.com/",
***REMOVED***credential=formrecognizer_creds)

***REMOVED***create_and_populate_index(args.index, index_client, search_client, form_recognizer_client)
***REMOVED***print("Data preparation for index", args.index, "completed")
