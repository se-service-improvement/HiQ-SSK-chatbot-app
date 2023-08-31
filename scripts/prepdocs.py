import argparse
import dataclasses
import time

from tqdm import tqdm
from azure.identity import AzureDeveloperCliCredential
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
***REMOVED***SearchableField,
***REMOVED***SearchField,
***REMOVED***SearchFieldDataType,
***REMOVED***SemanticField,
***REMOVED***SemanticSettings,
***REMOVED***SemanticConfiguration,
***REMOVED***SearchIndex,
***REMOVED***PrioritizedFields,
***REMOVED***VectorSearch,
***REMOVED***VectorSearchAlgorithmConfiguration,
***REMOVED***HnswParameters
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
***REMOVED******REMOVED***SearchableField(
***REMOVED******REMOVED******REMOVED***name="content", type="Edm.String", analyzer_name="en.lucene"
***REMOVED******REMOVED***),
***REMOVED******REMOVED***SearchableField(
***REMOVED******REMOVED******REMOVED***name="title", type="Edm.String", analyzer_name="en.lucene"
***REMOVED******REMOVED***),
***REMOVED******REMOVED***SearchableField(name="filepath", type="Edm.String"),
***REMOVED******REMOVED***SearchableField(name="url", type="Edm.String"),
***REMOVED******REMOVED***SearchableField(name="metadata", type="Edm.String"),
***REMOVED******REMOVED***SearchField(name="contentVector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
***REMOVED******REMOVED******REMOVED******REMOVED***hidden=False, searchable=True, filterable=False, sortable=False, facetable=False,
***REMOVED******REMOVED******REMOVED******REMOVED***vector_search_dimensions=1536, vector_search_configuration="default"),
***REMOVED******REMOVED***],
***REMOVED******REMOVED***semantic_settings=SemanticSettings(
***REMOVED******REMOVED***configurations=[
***REMOVED******REMOVED******REMOVED***SemanticConfiguration(
***REMOVED******REMOVED******REMOVED***name="default",
***REMOVED******REMOVED******REMOVED***prioritized_fields=PrioritizedFields(
***REMOVED******REMOVED******REMOVED******REMOVED***title_field=SemanticField(field_name="title"),
***REMOVED******REMOVED******REMOVED******REMOVED***prioritized_content_fields=[
***REMOVED******REMOVED******REMOVED******REMOVED***SemanticField(field_name="content")
***REMOVED******REMOVED******REMOVED******REMOVED***],
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***)
***REMOVED******REMOVED***]
***REMOVED******REMOVED***),
***REMOVED******REMOVED***vector_search=VectorSearch(
***REMOVED******REMOVED***algorithm_configurations=[
***REMOVED******REMOVED******REMOVED***VectorSearchAlgorithmConfiguration(
***REMOVED******REMOVED******REMOVED***name="default",
***REMOVED******REMOVED******REMOVED***kind="hnsw",
***REMOVED******REMOVED******REMOVED***hnsw_parameters=HnswParameters(metric="cosine")
***REMOVED******REMOVED******REMOVED***)
***REMOVED******REMOVED***]
***REMOVED******REMOVED***)
***REMOVED***)
***REMOVED***print(f"Creating {index_name} search index")
***REMOVED***index_client.create_index(index)
***REMOVED***else:
***REMOVED***print(f"Search index {index_name} already exists")


def upload_documents_to_index(docs, search_client, upload_batch_size=50):
***REMOVED***to_upload_dicts = []

***REMOVED***id = 0
***REMOVED***for document in docs:
***REMOVED***d = dataclasses.asdict(document)
***REMOVED***# add id to documents
***REMOVED***d.update({"@search.action": "upload", "id": str(id)})
***REMOVED***if "contentVector" in d and d["contentVector"] is None:
***REMOVED******REMOVED***del d["contentVector"]
***REMOVED***to_upload_dicts.append(d)
***REMOVED***id += 1

***REMOVED***# Upload the documents in batches of upload_batch_size
***REMOVED***for i in tqdm(
***REMOVED***range(0, len(to_upload_dicts), upload_batch_size), desc="Indexing Chunks..."
***REMOVED***):
***REMOVED***batch = to_upload_dicts[i : i + upload_batch_size]
***REMOVED***results = search_client.upload_documents(documents=batch)
***REMOVED***num_failures = 0
***REMOVED***errors = set()
***REMOVED***for result in results:
***REMOVED******REMOVED***if not result.succeeded:
***REMOVED******REMOVED***print(
***REMOVED******REMOVED******REMOVED***f"Indexing Failed for {result.key} with ERROR: {result.error_message}"
***REMOVED******REMOVED***)
***REMOVED******REMOVED***num_failures += 1
***REMOVED******REMOVED***errors.add(result.error_message)
***REMOVED***if num_failures > 0:
***REMOVED******REMOVED***raise Exception(
***REMOVED******REMOVED***f"INDEXING FAILED for {num_failures} documents. Please recreate the index."
***REMOVED******REMOVED***f"To Debug: PLEASE CHECK chunk_size and upload_batch_size. \n Error Messages: {list(errors)}"
***REMOVED******REMOVED***)


def validate_index(index_name, index_client):
***REMOVED***for retry_count in range(5):
***REMOVED***stats = index_client.get_index_statistics(index_name)
***REMOVED***num_chunks = stats["document_count"]
***REMOVED***if num_chunks == 0 and retry_count < 4:
***REMOVED******REMOVED***print("Index is empty. Waiting 60 seconds to check again...")
***REMOVED******REMOVED***time.sleep(60)
***REMOVED***elif num_chunks == 0 and retry_count == 4:
***REMOVED******REMOVED***print("Index is empty. Please investigate and re-index.")
***REMOVED***else:
***REMOVED******REMOVED***print(f"The index contains {num_chunks} chunks.")
***REMOVED******REMOVED***average_chunk_size = stats["storage_size"] / num_chunks
***REMOVED******REMOVED***print(f"The average chunk size of the index is {average_chunk_size} bytes.")
***REMOVED******REMOVED***break


def create_and_populate_index(
***REMOVED***index_name, index_client, search_client, form_recognizer_client, azure_credential, embedding_endpoint
):
***REMOVED***# create or update search index with compatible schema
***REMOVED***create_search_index(index_name, index_client)

***REMOVED***# chunk directory
***REMOVED***print("Chunking directory...")
***REMOVED***result = chunk_directory(
***REMOVED***"./data",
***REMOVED***form_recognizer_client=form_recognizer_client,
***REMOVED***use_layout=True,
***REMOVED***ignore_errors=False,
***REMOVED***njobs=1,
***REMOVED***add_embeddings=True,
***REMOVED***azure_credential=azd_credential,
***REMOVED***embedding_endpoint=embedding_endpoint
***REMOVED***)

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
***REMOVED***print("Validating index...")
***REMOVED***validate_index(index_name, index_client)
***REMOVED***print("Index validation completed")


if __name__ == "__main__":
***REMOVED***parser = argparse.ArgumentParser(
***REMOVED***description="Prepare documents by extracting content from PDFs, splitting content into sections and indexing in a search index.",
***REMOVED***epilog="Example: prepdocs.py --searchservice mysearch --index myindex",
***REMOVED***)
***REMOVED***parser.add_argument(
***REMOVED***"--tenantid",
***REMOVED***required=False,
***REMOVED***help="Optional. Use this to define the Azure directory where to authenticate)",
***REMOVED***)
***REMOVED***parser.add_argument(
***REMOVED***"--searchservice",
***REMOVED***help="Name of the Azure Cognitive Search service where content should be indexed (must exist already)",
***REMOVED***)
***REMOVED***parser.add_argument(
***REMOVED***"--index",
***REMOVED***help="Name of the Azure Cognitive Search index where content should be indexed (will be created if it doesn't exist)",
***REMOVED***)
***REMOVED***parser.add_argument(
***REMOVED***"--searchkey",
***REMOVED***required=False,
***REMOVED***help="Optional. Use this Azure Cognitive Search account key instead of the current user identity to login (use az login to set current user for Azure)",
***REMOVED***)
***REMOVED***parser.add_argument(
***REMOVED***"--formrecognizerservice",
***REMOVED***required=False,
***REMOVED***help="Optional. Name of the Azure Form Recognizer service which will be used to extract text, tables and layout from the documents (must exist already)",
***REMOVED***)
***REMOVED***parser.add_argument(
***REMOVED***"--formrecognizerkey",
***REMOVED***required=False,
***REMOVED***help="Optional. Use this Azure Form Recognizer account key instead of the current user identity to login (use az login to set current user for Azure)",
***REMOVED***)
***REMOVED***parser.add_argument(
***REMOVED***"--embeddingendpoint",
***REMOVED***required=False,
***REMOVED***help="Optional. Use this OpenAI endpoint to generate embeddings for the documents",
***REMOVED***)
***REMOVED***args = parser.parse_args()

***REMOVED***# Use the current user identity to connect to Azure services unless a key is explicitly set for any of them
***REMOVED***azd_credential = (
***REMOVED***AzureDeveloperCliCredential()
***REMOVED***if args.tenantid == None
***REMOVED***else AzureDeveloperCliCredential(tenant_id=args.tenantid, process_timeout=60)
***REMOVED***)
***REMOVED***default_creds = azd_credential if args.searchkey == None else None
***REMOVED***search_creds = (
***REMOVED***default_creds if args.searchkey == None else AzureKeyCredential(args.searchkey)
***REMOVED***)
***REMOVED***formrecognizer_creds = (
***REMOVED***default_creds
***REMOVED***if args.formrecognizerkey == None
***REMOVED***else AzureKeyCredential(args.formrecognizerkey)
***REMOVED***)

***REMOVED***print("Data preparation script started")
***REMOVED***print("Preparing data for index:", args.index)
***REMOVED***search_endpoint = f"https://{args.searchservice}.search.windows.net/"
***REMOVED***index_client = SearchIndexClient(endpoint=search_endpoint, credential=search_creds)
***REMOVED***search_client = SearchClient(
***REMOVED***endpoint=search_endpoint, credential=search_creds, index_name=args.index
***REMOVED***)
***REMOVED***form_recognizer_client = DocumentAnalysisClient(
***REMOVED***endpoint=f"https://{args.formrecognizerservice}.cognitiveservices.azure.com/",
***REMOVED***credential=formrecognizer_creds,
***REMOVED***)
***REMOVED***create_and_populate_index(
***REMOVED***args.index, index_client, search_client, form_recognizer_client, azd_credential, args.embeddingendpoint
***REMOVED***)
***REMOVED***print("Data preparation for index", args.index, "completed")
