import json
import os
import logging
import requests
import openai
import copy
import uuid
from azure.identity import DefaultAzureCredential
from base64 import b64encode
from flask import Flask, Response, request, jsonify, send_from_directory
from dotenv import load_dotenv

from backend.auth.auth_utils import get_authenticated_user_details
from backend.history.cosmosdbservice import CosmosConversationClient

load_dotenv()

app = Flask(__name__, static_folder="static")

# Static Files
@app.route("/")
def index():
***REMOVED***return app.send_static_file("index.html")

@app.route("/favicon.ico")
def favicon():
***REMOVED***return app.send_static_file('favicon.ico')

@app.route("/assets/<path:path>")
def assets(path):
***REMOVED***return send_from_directory("static/assets", path)

# Debug settings
DEBUG = os.environ.get("DEBUG", "false")
DEBUG_LOGGING = DEBUG.lower() == "true"
if DEBUG_LOGGING:
***REMOVED***logging.basicConfig(level=logging.DEBUG)

# On Your Data Settings
DATASOURCE_TYPE = os.environ.get("DATASOURCE_TYPE", "AzureCognitiveSearch")
SEARCH_TOP_K = os.environ.get("SEARCH_TOP_K", 5)
SEARCH_STRICTNESS = os.environ.get("SEARCH_STRICTNESS", 3)
SEARCH_ENABLE_IN_DOMAIN = os.environ.get("SEARCH_ENABLE_IN_DOMAIN", "true")

# ACS Integration Settings
AZURE_SEARCH_SERVICE = os.environ.get("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX")
AZURE_SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY")
AZURE_SEARCH_USE_SEMANTIC_SEARCH = os.environ.get("AZURE_SEARCH_USE_SEMANTIC_SEARCH", "false")
AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG = os.environ.get("AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG", "default")
AZURE_SEARCH_TOP_K = os.environ.get("AZURE_SEARCH_TOP_K", SEARCH_TOP_K)
AZURE_SEARCH_ENABLE_IN_DOMAIN = os.environ.get("AZURE_SEARCH_ENABLE_IN_DOMAIN", SEARCH_ENABLE_IN_DOMAIN)
AZURE_SEARCH_CONTENT_COLUMNS = os.environ.get("AZURE_SEARCH_CONTENT_COLUMNS")
AZURE_SEARCH_FILENAME_COLUMN = os.environ.get("AZURE_SEARCH_FILENAME_COLUMN")
AZURE_SEARCH_TITLE_COLUMN = os.environ.get("AZURE_SEARCH_TITLE_COLUMN")
AZURE_SEARCH_URL_COLUMN = os.environ.get("AZURE_SEARCH_URL_COLUMN")
AZURE_SEARCH_VECTOR_COLUMNS = os.environ.get("AZURE_SEARCH_VECTOR_COLUMNS")
AZURE_SEARCH_QUERY_TYPE = os.environ.get("AZURE_SEARCH_QUERY_TYPE")
AZURE_SEARCH_PERMITTED_GROUPS_COLUMN = os.environ.get("AZURE_SEARCH_PERMITTED_GROUPS_COLUMN")
AZURE_SEARCH_STRICTNESS = os.environ.get("AZURE_SEARCH_STRICTNESS", SEARCH_STRICTNESS)

# AOAI Integration Settings
AZURE_OPENAI_RESOURCE = os.environ.get("AZURE_OPENAI_RESOURCE")
AZURE_OPENAI_MODEL = os.environ.get("AZURE_OPENAI_MODEL")
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
AZURE_OPENAI_TEMPERATURE = os.environ.get("AZURE_OPENAI_TEMPERATURE", 0)
AZURE_OPENAI_TOP_P = os.environ.get("AZURE_OPENAI_TOP_P", 1.0)
AZURE_OPENAI_MAX_TOKENS = os.environ.get("AZURE_OPENAI_MAX_TOKENS", 1000)
AZURE_OPENAI_STOP_SEQUENCE = os.environ.get("AZURE_OPENAI_STOP_SEQUENCE")
AZURE_OPENAI_SYSTEM_MESSAGE = os.environ.get("AZURE_OPENAI_SYSTEM_MESSAGE", "You are an AI assistant that helps people find information.")
AZURE_OPENAI_PREVIEW_API_VERSION = os.environ.get("AZURE_OPENAI_PREVIEW_API_VERSION", "2023-08-01-preview")
AZURE_OPENAI_STREAM = os.environ.get("AZURE_OPENAI_STREAM", "true")
AZURE_OPENAI_MODEL_NAME = os.environ.get("AZURE_OPENAI_MODEL_NAME", "gpt-35-turbo-16k") # Name of the model, e.g. 'gpt-35-turbo-16k' or 'gpt-4'
AZURE_OPENAI_EMBEDDING_ENDPOINT = os.environ.get("AZURE_OPENAI_EMBEDDING_ENDPOINT")
AZURE_OPENAI_EMBEDDING_KEY = os.environ.get("AZURE_OPENAI_EMBEDDING_KEY")
AZURE_OPENAI_EMBEDDING_NAME = os.environ.get("AZURE_OPENAI_EMBEDDING_NAME", "")

# CosmosDB Mongo vcore vector db Settings
AZURE_COSMOSDB_MONGO_VCORE_CONNECTION_STRING = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_CONNECTION_STRING")  #This has to be secure string
AZURE_COSMOSDB_MONGO_VCORE_DATABASE = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_DATABASE")
AZURE_COSMOSDB_MONGO_VCORE_CONTAINER = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_CONTAINER")
AZURE_COSMOSDB_MONGO_VCORE_INDEX = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_INDEX")
AZURE_COSMOSDB_MONGO_VCORE_TOP_K = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_TOP_K", AZURE_SEARCH_TOP_K)
AZURE_COSMOSDB_MONGO_VCORE_STRICTNESS = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_STRICTNESS", AZURE_SEARCH_STRICTNESS)  
AZURE_COSMOSDB_MONGO_VCORE_ENABLE_IN_DOMAIN = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_ENABLE_IN_DOMAIN", AZURE_SEARCH_ENABLE_IN_DOMAIN)
AZURE_COSMOSDB_MONGO_VCORE_CONTENT_COLUMNS = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_CONTENT_COLUMNS", "")
AZURE_COSMOSDB_MONGO_VCORE_FILENAME_COLUMN = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_FILENAME_COLUMN")
AZURE_COSMOSDB_MONGO_VCORE_TITLE_COLUMN = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_TITLE_COLUMN")
AZURE_COSMOSDB_MONGO_VCORE_URL_COLUMN = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_URL_COLUMN")
AZURE_COSMOSDB_MONGO_VCORE_VECTOR_COLUMNS = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_VECTOR_COLUMNS")


SHOULD_STREAM = True if AZURE_OPENAI_STREAM.lower() == "true" else False

# Chat History CosmosDB Integration Settings
AZURE_COSMOSDB_DATABASE = os.environ.get("AZURE_COSMOSDB_DATABASE")
AZURE_COSMOSDB_ACCOUNT = os.environ.get("AZURE_COSMOSDB_ACCOUNT")
AZURE_COSMOSDB_CONVERSATIONS_CONTAINER = os.environ.get("AZURE_COSMOSDB_CONVERSATIONS_CONTAINER")
AZURE_COSMOSDB_ACCOUNT_KEY = os.environ.get("AZURE_COSMOSDB_ACCOUNT_KEY")
AZURE_COSMOSDB_ENABLE_FEEDBACK = os.environ.get("AZURE_COSMOSDB_ENABLE_FEEDBACK", "false").lower() == "true"

# Elasticsearch Integration Settings
ELASTICSEARCH_ENDPOINT = os.environ.get("ELASTICSEARCH_ENDPOINT")
ELASTICSEARCH_ENCODED_API_KEY = os.environ.get("ELASTICSEARCH_ENCODED_API_KEY")
ELASTICSEARCH_INDEX = os.environ.get("ELASTICSEARCH_INDEX")
ELASTICSEARCH_QUERY_TYPE = os.environ.get("ELASTICSEARCH_QUERY_TYPE", "simple")
ELASTICSEARCH_TOP_K = os.environ.get("ELASTICSEARCH_TOP_K", SEARCH_TOP_K)
ELASTICSEARCH_ENABLE_IN_DOMAIN = os.environ.get("ELASTICSEARCH_ENABLE_IN_DOMAIN", SEARCH_ENABLE_IN_DOMAIN)
ELASTICSEARCH_CONTENT_COLUMNS = os.environ.get("ELASTICSEARCH_CONTENT_COLUMNS")
ELASTICSEARCH_FILENAME_COLUMN = os.environ.get("ELASTICSEARCH_FILENAME_COLUMN")
ELASTICSEARCH_TITLE_COLUMN = os.environ.get("ELASTICSEARCH_TITLE_COLUMN")
ELASTICSEARCH_URL_COLUMN = os.environ.get("ELASTICSEARCH_URL_COLUMN")
ELASTICSEARCH_VECTOR_COLUMNS = os.environ.get("ELASTICSEARCH_VECTOR_COLUMNS")
ELASTICSEARCH_STRICTNESS = os.environ.get("ELASTICSEARCH_STRICTNESS", SEARCH_STRICTNESS)
ELASTICSEARCH_EMBEDDING_MODEL_ID = os.environ.get("ELASTICSEARCH_EMBEDDING_MODEL_ID")

# Frontend Settings via Environment Variables
AUTH_ENABLED = os.environ.get("AUTH_ENABLED", "true").lower() == "true"
frontend_settings = { 
***REMOVED***"auth_enabled": AUTH_ENABLED, 
***REMOVED***"feedback_enabled": AZURE_COSMOSDB_ENABLE_FEEDBACK and AZURE_COSMOSDB_DATABASE not in [None, ""],
}

message_uuid = ""

# Initialize a CosmosDB client with AAD auth and containers for Chat History
cosmos_conversation_client = None
if AZURE_COSMOSDB_DATABASE and AZURE_COSMOSDB_ACCOUNT and AZURE_COSMOSDB_CONVERSATIONS_CONTAINER:
***REMOVED***try :
***REMOVED***cosmos_endpoint = f'https://{AZURE_COSMOSDB_ACCOUNT}.documents.azure.com:443/'

***REMOVED***if not AZURE_COSMOSDB_ACCOUNT_KEY:
***REMOVED******REMOVED***credential = DefaultAzureCredential()
***REMOVED***else:
***REMOVED******REMOVED***credential = AZURE_COSMOSDB_ACCOUNT_KEY

***REMOVED***cosmos_conversation_client = CosmosConversationClient(
***REMOVED******REMOVED***cosmosdb_endpoint=cosmos_endpoint, 
***REMOVED******REMOVED***credential=credential, 
***REMOVED******REMOVED***database_name=AZURE_COSMOSDB_DATABASE,
***REMOVED******REMOVED***container_name=AZURE_COSMOSDB_CONVERSATIONS_CONTAINER,
***REMOVED******REMOVED***enable_message_feedback = AZURE_COSMOSDB_ENABLE_FEEDBACK
***REMOVED***)
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in CosmosDB initialization", e)
***REMOVED***cosmodb_error = str(e)
***REMOVED***cosmos_conversation_client = None


def is_chat_model():
***REMOVED***if 'gpt-4' in AZURE_OPENAI_MODEL_NAME.lower() or AZURE_OPENAI_MODEL_NAME.lower() in ['gpt-35-turbo-4k', 'gpt-35-turbo-16k']:
***REMOVED***return True
***REMOVED***return False

def should_use_data():
***REMOVED***if AZURE_SEARCH_SERVICE and AZURE_SEARCH_INDEX and AZURE_SEARCH_KEY:
***REMOVED***if DEBUG_LOGGING:
***REMOVED******REMOVED***logging.debug("Using Azure Cognitive Search")
***REMOVED***return True
***REMOVED***
***REMOVED***if AZURE_COSMOSDB_MONGO_VCORE_DATABASE and AZURE_COSMOSDB_MONGO_VCORE_CONTAINER and AZURE_COSMOSDB_MONGO_VCORE_INDEX and AZURE_COSMOSDB_MONGO_VCORE_CONNECTION_STRING:
***REMOVED***if DEBUG_LOGGING:
***REMOVED******REMOVED***logging.debug("Using Azure CosmosDB Mongo vcore")
***REMOVED***return True
***REMOVED***
***REMOVED***return False


def format_as_ndjson(obj: dict) -> str:
***REMOVED***return json.dumps(obj, ensure_ascii=False) + "\n"

def parse_multi_columns(columns: str) -> list:
***REMOVED***if "|" in columns:
***REMOVED***return columns.split("|")
***REMOVED***else:
***REMOVED***return columns.split(",")

def fetchUserGroups(userToken, nextLink=None):
***REMOVED***# Recursively fetch group membership
***REMOVED***if nextLink:
***REMOVED***endpoint = nextLink
***REMOVED***else:
***REMOVED***endpoint = "https://graph.microsoft.com/v1.0/me/transitiveMemberOf?$select=id"
***REMOVED***
***REMOVED***headers = {
***REMOVED***'Authorization': "bearer " + userToken
***REMOVED***
***REMOVED***try :
***REMOVED***r = requests.get(endpoint, headers=headers)
***REMOVED***if r.status_code != 200:
***REMOVED******REMOVED***if DEBUG_LOGGING:
***REMOVED******REMOVED***logging.error(f"Error fetching user groups: {r.status_code} {r.text}")
***REMOVED******REMOVED***return []
***REMOVED***
***REMOVED***r = r.json()
***REMOVED***if "@odata.nextLink" in r:
***REMOVED******REMOVED***nextLinkData = fetchUserGroups(userToken, r["@odata.nextLink"])
***REMOVED******REMOVED***r['value'].extend(nextLinkData)
***REMOVED***
***REMOVED***return r['value']
***REMOVED***except Exception as e:
***REMOVED***logging.error(f"Exception in fetchUserGroups: {e}")
***REMOVED***return []


def generateFilterString(userToken):
***REMOVED***# Get list of groups user is a member of
***REMOVED***userGroups = fetchUserGroups(userToken)

***REMOVED***# Construct filter string
***REMOVED***if not userGroups:
***REMOVED***logging.debug("No user groups found")

***REMOVED***group_ids = ", ".join([obj['id'] for obj in userGroups])
***REMOVED***return f"{AZURE_SEARCH_PERMITTED_GROUPS_COLUMN}/any(g:search.in(g, '{group_ids}'))"



def prepare_body_headers_with_data(request):
***REMOVED***request_messages = request.json["messages"]

***REMOVED***body = {
***REMOVED***"messages": request_messages,
***REMOVED***"temperature": float(AZURE_OPENAI_TEMPERATURE),
***REMOVED***"max_tokens": int(AZURE_OPENAI_MAX_TOKENS),
***REMOVED***"top_p": float(AZURE_OPENAI_TOP_P),
***REMOVED***"stop": AZURE_OPENAI_STOP_SEQUENCE.split("|") if AZURE_OPENAI_STOP_SEQUENCE else None,
***REMOVED***"stream": SHOULD_STREAM,
***REMOVED***"dataSources": []
***REMOVED***

***REMOVED***if DATASOURCE_TYPE == "AzureCognitiveSearch":
***REMOVED***# Set query type
***REMOVED***query_type = "simple"
***REMOVED***if AZURE_SEARCH_QUERY_TYPE:
***REMOVED******REMOVED***query_type = AZURE_SEARCH_QUERY_TYPE
***REMOVED***elif AZURE_SEARCH_USE_SEMANTIC_SEARCH.lower() == "true" and AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG:
***REMOVED******REMOVED***query_type = "semantic"

***REMOVED***# Set filter
***REMOVED***filter = None
***REMOVED***userToken = None
***REMOVED***if AZURE_SEARCH_PERMITTED_GROUPS_COLUMN:
***REMOVED******REMOVED***userToken = request.headers.get('X-MS-TOKEN-AAD-ACCESS-TOKEN', "")
***REMOVED******REMOVED***if DEBUG_LOGGING:
***REMOVED******REMOVED***logging.debug(f"USER TOKEN is {'present' if userToken else 'not present'}")

***REMOVED******REMOVED***filter = generateFilterString(userToken)
***REMOVED******REMOVED***if DEBUG_LOGGING:
***REMOVED******REMOVED***logging.debug(f"FILTER: {filter}")

***REMOVED***body["dataSources"].append(
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"type": "AzureCognitiveSearch",
***REMOVED******REMOVED***"parameters": {
***REMOVED******REMOVED******REMOVED***"endpoint": f"https://{AZURE_SEARCH_SERVICE}.search.windows.net",
***REMOVED******REMOVED******REMOVED***"key": AZURE_SEARCH_KEY,
***REMOVED******REMOVED******REMOVED***"indexName": AZURE_SEARCH_INDEX,
***REMOVED******REMOVED******REMOVED***"fieldsMapping": {
***REMOVED******REMOVED******REMOVED***"contentFields": parse_multi_columns(AZURE_SEARCH_CONTENT_COLUMNS) if AZURE_SEARCH_CONTENT_COLUMNS else [],
***REMOVED******REMOVED******REMOVED***"titleField": AZURE_SEARCH_TITLE_COLUMN if AZURE_SEARCH_TITLE_COLUMN else None,
***REMOVED******REMOVED******REMOVED***"urlField": AZURE_SEARCH_URL_COLUMN if AZURE_SEARCH_URL_COLUMN else None,
***REMOVED******REMOVED******REMOVED***"filepathField": AZURE_SEARCH_FILENAME_COLUMN if AZURE_SEARCH_FILENAME_COLUMN else None,
***REMOVED******REMOVED******REMOVED***"vectorFields": parse_multi_columns(AZURE_SEARCH_VECTOR_COLUMNS) if AZURE_SEARCH_VECTOR_COLUMNS else []
***REMOVED******REMOVED***,
***REMOVED******REMOVED******REMOVED***"inScope": True if AZURE_SEARCH_ENABLE_IN_DOMAIN.lower() == "true" else False,
***REMOVED******REMOVED******REMOVED***"topNDocuments": int(AZURE_SEARCH_TOP_K),
***REMOVED******REMOVED******REMOVED***"queryType": query_type,
***REMOVED******REMOVED******REMOVED***"semanticConfiguration": AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG if AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG else "",
***REMOVED******REMOVED******REMOVED***"roleInformation": AZURE_OPENAI_SYSTEM_MESSAGE,
***REMOVED******REMOVED******REMOVED***"filter": filter,
***REMOVED******REMOVED******REMOVED***"strictness": int(AZURE_SEARCH_STRICTNESS)
***REMOVED******REMOVED***
***REMOVED***)
***REMOVED***elif DATASOURCE_TYPE == "AzureCosmosDB":
***REMOVED***# Set query type
***REMOVED***query_type = "vector"

***REMOVED***body["dataSources"].append(
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"type": "AzureCosmosDB",
***REMOVED******REMOVED***"parameters": {
***REMOVED******REMOVED******REMOVED***"connectionString": AZURE_COSMOSDB_MONGO_VCORE_CONNECTION_STRING,
***REMOVED******REMOVED******REMOVED***"indexName": AZURE_COSMOSDB_MONGO_VCORE_INDEX,
***REMOVED******REMOVED******REMOVED***"databaseName": AZURE_COSMOSDB_MONGO_VCORE_DATABASE,
***REMOVED******REMOVED******REMOVED***"containerName": AZURE_COSMOSDB_MONGO_VCORE_CONTAINER,***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***"fieldsMapping": {
***REMOVED******REMOVED******REMOVED***"contentFields": parse_multi_columns(AZURE_COSMOSDB_MONGO_VCORE_CONTENT_COLUMNS) if AZURE_COSMOSDB_MONGO_VCORE_CONTENT_COLUMNS else [],
***REMOVED******REMOVED******REMOVED***"titleField": AZURE_COSMOSDB_MONGO_VCORE_TITLE_COLUMN if AZURE_COSMOSDB_MONGO_VCORE_TITLE_COLUMN else None,
***REMOVED******REMOVED******REMOVED***"urlField": AZURE_COSMOSDB_MONGO_VCORE_URL_COLUMN if AZURE_COSMOSDB_MONGO_VCORE_URL_COLUMN else None,
***REMOVED******REMOVED******REMOVED***"filepathField": AZURE_COSMOSDB_MONGO_VCORE_FILENAME_COLUMN if AZURE_COSMOSDB_MONGO_VCORE_FILENAME_COLUMN else None,
***REMOVED******REMOVED******REMOVED***"vectorFields": parse_multi_columns(AZURE_COSMOSDB_MONGO_VCORE_VECTOR_COLUMNS) if AZURE_COSMOSDB_MONGO_VCORE_VECTOR_COLUMNS else []
***REMOVED******REMOVED***,
***REMOVED******REMOVED******REMOVED***"inScope": True if AZURE_COSMOSDB_MONGO_VCORE_ENABLE_IN_DOMAIN.lower() == "true" else False,
***REMOVED******REMOVED******REMOVED***"topNDocuments": int(AZURE_COSMOSDB_MONGO_VCORE_TOP_K),
***REMOVED******REMOVED******REMOVED***"strictness": int(AZURE_COSMOSDB_MONGO_VCORE_STRICTNESS),
***REMOVED******REMOVED******REMOVED***"queryType": query_type,
***REMOVED******REMOVED******REMOVED***"roleInformation": AZURE_OPENAI_SYSTEM_MESSAGE
***REMOVED******REMOVED***
***REMOVED***
***REMOVED***)

***REMOVED***elif DATASOURCE_TYPE == "Elasticsearch":
***REMOVED***body["dataSources"].append(
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"messages": request_messages,
***REMOVED******REMOVED***"temperature": float(AZURE_OPENAI_TEMPERATURE),
***REMOVED******REMOVED***"max_tokens": int(AZURE_OPENAI_MAX_TOKENS),
***REMOVED******REMOVED***"top_p": float(AZURE_OPENAI_TOP_P),
***REMOVED******REMOVED***"stop": AZURE_OPENAI_STOP_SEQUENCE.split("|") if AZURE_OPENAI_STOP_SEQUENCE else None,
***REMOVED******REMOVED***"stream": SHOULD_STREAM,
***REMOVED******REMOVED***"dataSources": [
***REMOVED******REMOVED******REMOVED***{
***REMOVED******REMOVED******REMOVED***"type": "AzureCognitiveSearch",
***REMOVED******REMOVED******REMOVED***"parameters": {
***REMOVED******REMOVED******REMOVED******REMOVED***"endpoint": ELASTICSEARCH_ENDPOINT,
***REMOVED******REMOVED******REMOVED******REMOVED***"encodedApiKey": ELASTICSEARCH_ENCODED_API_KEY,
***REMOVED******REMOVED******REMOVED******REMOVED***"indexName": ELASTICSEARCH_INDEX,
***REMOVED******REMOVED******REMOVED******REMOVED***"fieldsMapping": {
***REMOVED******REMOVED******REMOVED******REMOVED***"contentFields": parse_multi_columns(ELASTICSEARCH_CONTENT_COLUMNS) if ELASTICSEARCH_CONTENT_COLUMNS else [],
***REMOVED******REMOVED******REMOVED******REMOVED***"titleField": ELASTICSEARCH_TITLE_COLUMN if ELASTICSEARCH_TITLE_COLUMN else None,
***REMOVED******REMOVED******REMOVED******REMOVED***"urlField": ELASTICSEARCH_URL_COLUMN if ELASTICSEARCH_URL_COLUMN else None,
***REMOVED******REMOVED******REMOVED******REMOVED***"filepathField": ELASTICSEARCH_FILENAME_COLUMN if ELASTICSEARCH_FILENAME_COLUMN else None,
***REMOVED******REMOVED******REMOVED******REMOVED***"vectorFields": parse_multi_columns(ELASTICSEARCH_VECTOR_COLUMNS) if ELASTICSEARCH_VECTOR_COLUMNS else []
***REMOVED******REMOVED******REMOVED***,
***REMOVED******REMOVED******REMOVED******REMOVED***"inScope": True if ELASTICSEARCH_ENABLE_IN_DOMAIN.lower() == "true" else False,
***REMOVED******REMOVED******REMOVED******REMOVED***"topNDocuments": int(ELASTICSEARCH_TOP_K),
***REMOVED******REMOVED******REMOVED******REMOVED***"queryType": ELASTICSEARCH_QUERY_TYPE,
***REMOVED******REMOVED******REMOVED******REMOVED***"roleInformation": AZURE_OPENAI_SYSTEM_MESSAGE,
***REMOVED******REMOVED******REMOVED******REMOVED***"embeddingEndpoint": AZURE_OPENAI_EMBEDDING_ENDPOINT,
***REMOVED******REMOVED******REMOVED******REMOVED***"embeddingKey": AZURE_OPENAI_EMBEDDING_KEY,
***REMOVED******REMOVED******REMOVED******REMOVED***"embeddingModelId": ELASTICSEARCH_EMBEDDING_MODEL_ID,
***REMOVED******REMOVED******REMOVED******REMOVED***"strictness": int(ELASTICSEARCH_STRICTNESS)
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED***
***REMOVED******REMOVED***]
***REMOVED***
***REMOVED***)
***REMOVED***else:
***REMOVED***raise Exception(f"DATASOURCE_TYPE is not configured or unknown: {DATASOURCE_TYPE}")

***REMOVED***if "vector" in query_type.lower():
***REMOVED***if AZURE_OPENAI_EMBEDDING_NAME:
***REMOVED******REMOVED***body["dataSources"][0]["parameters"]["embeddingDeploymentName"] = AZURE_OPENAI_EMBEDDING_NAME
***REMOVED***else:
***REMOVED******REMOVED***body["dataSources"][0]["parameters"]["embeddingEndpoint"] = AZURE_OPENAI_EMBEDDING_ENDPOINT
***REMOVED******REMOVED***body["dataSources"][0]["parameters"]["embeddingKey"] = AZURE_OPENAI_EMBEDDING_KEY

***REMOVED***if DEBUG_LOGGING:
***REMOVED***body_clean = copy.deepcopy(body)
***REMOVED***if body_clean["dataSources"][0]["parameters"].get("key"):
***REMOVED******REMOVED***body_clean["dataSources"][0]["parameters"]["key"] = "*****"
***REMOVED***if body_clean["dataSources"][0]["parameters"].get("connectionString"):
***REMOVED******REMOVED***body_clean["dataSources"][0]["parameters"]["connectionString"] = "*****"
***REMOVED***if body_clean["dataSources"][0]["parameters"].get("embeddingKey"):
***REMOVED******REMOVED***body_clean["dataSources"][0]["parameters"]["embeddingKey"] = "*****"
***REMOVED******REMOVED***
***REMOVED***logging.debug(f"REQUEST BODY: {json.dumps(body_clean, indent=4)}")

***REMOVED***headers = {
***REMOVED***'Content-Type': 'application/json',
***REMOVED***'api-key': AZURE_OPENAI_KEY,
***REMOVED***"x-ms-useragent": "GitHubSampleWebApp/PublicAPI/3.0.0"
***REMOVED***

***REMOVED***return body, headers


def stream_with_data(body, headers, endpoint, history_metadata={}):
***REMOVED***s = requests.Session()
***REMOVED***try:
***REMOVED***with s.post(endpoint, json=body, headers=headers, stream=True) as r:
***REMOVED******REMOVED***for line in r.iter_lines(chunk_size=10):
***REMOVED******REMOVED***response = {
***REMOVED******REMOVED******REMOVED***"id": "",
***REMOVED******REMOVED******REMOVED***"model": "",
***REMOVED******REMOVED******REMOVED***"created": 0,
***REMOVED******REMOVED******REMOVED***"object": "",
***REMOVED******REMOVED******REMOVED***"choices": [{
***REMOVED******REMOVED******REMOVED***"messages": []
***REMOVED******REMOVED***],
***REMOVED******REMOVED******REMOVED***"apim-request-id": "",
***REMOVED******REMOVED******REMOVED***'history_metadata': history_metadata
***REMOVED******REMOVED***
***REMOVED******REMOVED***if line:
***REMOVED******REMOVED******REMOVED***if AZURE_OPENAI_PREVIEW_API_VERSION == '2023-06-01-preview':
***REMOVED******REMOVED******REMOVED***lineJson = json.loads(line.lstrip(b'data:').decode('utf-8'))
***REMOVED******REMOVED******REMOVED***else:
***REMOVED******REMOVED******REMOVED***try:
***REMOVED******REMOVED******REMOVED******REMOVED***rawResponse = json.loads(line.lstrip(b'data:').decode('utf-8'))
***REMOVED******REMOVED******REMOVED******REMOVED***lineJson = formatApiResponseStreaming(rawResponse)
***REMOVED******REMOVED******REMOVED***except json.decoder.JSONDecodeError:
***REMOVED******REMOVED******REMOVED******REMOVED***continue

***REMOVED******REMOVED******REMOVED***if 'error' in lineJson:
***REMOVED******REMOVED******REMOVED***yield format_as_ndjson(lineJson)
***REMOVED******REMOVED******REMOVED***response["id"] = message_uuid
***REMOVED******REMOVED******REMOVED***response["model"] = lineJson["model"]
***REMOVED******REMOVED******REMOVED***response["created"] = lineJson["created"]
***REMOVED******REMOVED******REMOVED***response["object"] = lineJson["object"]
***REMOVED******REMOVED******REMOVED***response["apim-request-id"] = r.headers.get('apim-request-id')

***REMOVED******REMOVED******REMOVED***role = lineJson["choices"][0]["messages"][0]["delta"].get("role")

***REMOVED******REMOVED******REMOVED***if role == "tool":
***REMOVED******REMOVED******REMOVED***response["choices"][0]["messages"].append(lineJson["choices"][0]["messages"][0]["delta"])
***REMOVED******REMOVED******REMOVED***yield format_as_ndjson(response)
***REMOVED******REMOVED******REMOVED***elif role == "assistant": 
***REMOVED******REMOVED******REMOVED***if response['apim-request-id'] and DEBUG_LOGGING: 
***REMOVED******REMOVED******REMOVED******REMOVED***logging.debug(f"RESPONSE apim-request-id: {response['apim-request-id']}")
***REMOVED******REMOVED******REMOVED***response["choices"][0]["messages"].append({
***REMOVED******REMOVED******REMOVED******REMOVED***"role": "assistant",
***REMOVED******REMOVED******REMOVED******REMOVED***"content": ""
***REMOVED******REMOVED******REMOVED***)
***REMOVED******REMOVED******REMOVED***yield format_as_ndjson(response)
***REMOVED******REMOVED******REMOVED***else:
***REMOVED******REMOVED******REMOVED***deltaText = lineJson["choices"][0]["messages"][0]["delta"]["content"]
***REMOVED******REMOVED******REMOVED***if deltaText != "[DONE]":
***REMOVED******REMOVED******REMOVED******REMOVED***response["choices"][0]["messages"].append({
***REMOVED******REMOVED******REMOVED******REMOVED***"role": "assistant",
***REMOVED******REMOVED******REMOVED******REMOVED***"content": deltaText
***REMOVED******REMOVED******REMOVED***)
***REMOVED******REMOVED******REMOVED******REMOVED***yield format_as_ndjson(response)
***REMOVED***except Exception as e:
***REMOVED***yield format_as_ndjson({"error" + str(e)})

def formatApiResponseNoStreaming(rawResponse):
***REMOVED***if 'error' in rawResponse:
***REMOVED***return {"error": rawResponse["error"]}
***REMOVED***response = {
***REMOVED***"id": rawResponse["id"],
***REMOVED***"model": rawResponse["model"],
***REMOVED***"created": rawResponse["created"],
***REMOVED***"object": rawResponse["object"],
***REMOVED***"choices": [{
***REMOVED******REMOVED***"messages": []
***REMOVED***],
***REMOVED***
***REMOVED***toolMessage = {
***REMOVED***"role": "tool",
***REMOVED***"content": rawResponse["choices"][0]["message"]["context"]["messages"][0]["content"]
***REMOVED***
***REMOVED***assistantMessage = {
***REMOVED***"role": "assistant",
***REMOVED***"content": rawResponse["choices"][0]["message"]["content"]
***REMOVED***
***REMOVED***response["choices"][0]["messages"].append(toolMessage)
***REMOVED***response["choices"][0]["messages"].append(assistantMessage)

***REMOVED***return response

def formatApiResponseStreaming(rawResponse):
***REMOVED***if 'error' in rawResponse:
***REMOVED***return {"error": rawResponse["error"]}
***REMOVED***response = {
***REMOVED***"id": rawResponse["id"],
***REMOVED***"model": rawResponse["model"],
***REMOVED***"created": rawResponse["created"],
***REMOVED***"object": rawResponse["object"],
***REMOVED***"choices": [{
***REMOVED******REMOVED***"messages": []
***REMOVED***],
***REMOVED***

***REMOVED***if rawResponse["choices"][0]["delta"].get("context"):
***REMOVED***messageObj = {
***REMOVED******REMOVED***"delta": {
***REMOVED******REMOVED***"role": "tool",
***REMOVED******REMOVED***"content": rawResponse["choices"][0]["delta"]["context"]["messages"][0]["content"]
***REMOVED***
***REMOVED***
***REMOVED***response["choices"][0]["messages"].append(messageObj)
***REMOVED***elif rawResponse["choices"][0]["delta"].get("role"):
***REMOVED***messageObj = {
***REMOVED******REMOVED***"delta": {
***REMOVED******REMOVED***"role": "assistant",
***REMOVED***
***REMOVED***
***REMOVED***response["choices"][0]["messages"].append(messageObj)
***REMOVED***else:
***REMOVED***if rawResponse["choices"][0]["end_turn"]:
***REMOVED******REMOVED***messageObj = {
***REMOVED******REMOVED***"delta": {
***REMOVED******REMOVED******REMOVED***"content": "[DONE]",
***REMOVED******REMOVED***
***REMOVED***
***REMOVED******REMOVED***response["choices"][0]["messages"].append(messageObj)
***REMOVED***else:
***REMOVED******REMOVED***messageObj = {
***REMOVED******REMOVED***"delta": {
***REMOVED******REMOVED******REMOVED***"content": rawResponse["choices"][0]["delta"]["content"],
***REMOVED******REMOVED***
***REMOVED***
***REMOVED******REMOVED***response["choices"][0]["messages"].append(messageObj)

***REMOVED***return response

def conversation_with_data(request_body):
***REMOVED***body, headers = prepare_body_headers_with_data(request)
***REMOVED***base_url = AZURE_OPENAI_ENDPOINT if AZURE_OPENAI_ENDPOINT else f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/"
***REMOVED***endpoint = f"{base_url}openai/deployments/{AZURE_OPENAI_MODEL}/extensions/chat/completions?api-version={AZURE_OPENAI_PREVIEW_API_VERSION}"
***REMOVED***history_metadata = request_body.get("history_metadata", {})

***REMOVED***if not SHOULD_STREAM:
***REMOVED***r = requests.post(endpoint, headers=headers, json=body)
***REMOVED***status_code = r.status_code
***REMOVED***r = r.json()
***REMOVED***if AZURE_OPENAI_PREVIEW_API_VERSION == "2023-06-01-preview":
***REMOVED******REMOVED***r['history_metadata'] = history_metadata
***REMOVED******REMOVED***return Response(format_as_ndjson(r), status=status_code)
***REMOVED***else:
***REMOVED******REMOVED***result = formatApiResponseNoStreaming(r)
***REMOVED******REMOVED***result['history_metadata'] = history_metadata
***REMOVED******REMOVED***return Response(format_as_ndjson(result), status=status_code)

***REMOVED***else:
***REMOVED***return Response(stream_with_data(body, headers, endpoint, history_metadata), mimetype='text/event-stream')

def stream_without_data(response, history_metadata={}):
***REMOVED***for line in response:
***REMOVED***responseText = ""
***REMOVED***if line["choices"]:
***REMOVED******REMOVED***deltaText = line["choices"][0]["delta"].get('content')
***REMOVED***else:
***REMOVED******REMOVED***deltaText = ""
***REMOVED***if deltaText and deltaText != "[DONE]":
***REMOVED******REMOVED***responseText = deltaText

***REMOVED***response_obj = {
***REMOVED******REMOVED***"id": message_uuid,
***REMOVED******REMOVED***"model": line["model"],
***REMOVED******REMOVED***"created": line["created"],
***REMOVED******REMOVED***"object": line["object"],
***REMOVED******REMOVED***"choices": [{
***REMOVED******REMOVED***"messages": [{
***REMOVED******REMOVED******REMOVED***"role": "assistant",
***REMOVED******REMOVED******REMOVED***"content": responseText
***REMOVED******REMOVED***]
***REMOVED***],
***REMOVED******REMOVED***"history_metadata": history_metadata
***REMOVED***
***REMOVED***yield format_as_ndjson(response_obj)


def conversation_without_data(request_body):
***REMOVED***openai.api_type = "azure"
***REMOVED***openai.api_base = AZURE_OPENAI_ENDPOINT if AZURE_OPENAI_ENDPOINT else f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/"
***REMOVED***openai.api_version = "2023-08-01-preview"
***REMOVED***openai.api_key = AZURE_OPENAI_KEY

***REMOVED***request_messages = request_body["messages"]
***REMOVED***messages = [
***REMOVED***{
***REMOVED******REMOVED***"role": "system",
***REMOVED******REMOVED***"content": AZURE_OPENAI_SYSTEM_MESSAGE
***REMOVED***
***REMOVED***]

***REMOVED***for message in request_messages:
***REMOVED***if message:
***REMOVED******REMOVED***messages.append({
***REMOVED******REMOVED***"role": message["role"] ,
***REMOVED******REMOVED***"content": message["content"]
***REMOVED***)

***REMOVED***response = openai.ChatCompletion.create(
***REMOVED***engine=AZURE_OPENAI_MODEL,
***REMOVED***messages = messages,
***REMOVED***temperature=float(AZURE_OPENAI_TEMPERATURE),
***REMOVED***max_tokens=int(AZURE_OPENAI_MAX_TOKENS),
***REMOVED***top_p=float(AZURE_OPENAI_TOP_P),
***REMOVED***stop=AZURE_OPENAI_STOP_SEQUENCE.split("|") if AZURE_OPENAI_STOP_SEQUENCE else None,
***REMOVED***stream=SHOULD_STREAM
***REMOVED***)

***REMOVED***history_metadata = request_body.get("history_metadata", {})

***REMOVED***if not SHOULD_STREAM:
***REMOVED***response_obj = {
***REMOVED******REMOVED***"id": message_uuid,
***REMOVED******REMOVED***"model": response.model,
***REMOVED******REMOVED***"created": response.created,
***REMOVED******REMOVED***"object": response.object,
***REMOVED******REMOVED***"choices": [{
***REMOVED******REMOVED***"messages": [{
***REMOVED******REMOVED******REMOVED***"role": "assistant",
***REMOVED******REMOVED******REMOVED***"content": response.choices[0].message.content
***REMOVED******REMOVED***]
***REMOVED***],
***REMOVED******REMOVED***"history_metadata": history_metadata
***REMOVED***

***REMOVED***return jsonify(response_obj), 200
***REMOVED***else:
***REMOVED***return Response(stream_without_data(response, history_metadata), mimetype='text/event-stream')


@app.route("/conversation", methods=["GET", "POST"])
def conversation():
***REMOVED***request_body = request.json
***REMOVED***return conversation_internal(request_body)

def conversation_internal(request_body):
***REMOVED***try:
***REMOVED***use_data = should_use_data()
***REMOVED***if use_data:
***REMOVED******REMOVED***return conversation_with_data(request_body)
***REMOVED***else:
***REMOVED******REMOVED***return conversation_without_data(request_body)
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /conversation")
***REMOVED***return jsonify({"error": str(e)}), 500

## Conversation History API ## 
@app.route("/history/generate", methods=["POST"])
def add_conversation():
***REMOVED***global message_uuid
***REMOVED***message_uuid = str(uuid.uuid4())
***REMOVED***authenticated_user = get_authenticated_user_details(request_headers=request.headers)
***REMOVED***user_id = authenticated_user['user_principal_id']

***REMOVED***## check request for conversation_id
***REMOVED***conversation_id = request.json.get("conversation_id", None)

***REMOVED***try:
***REMOVED***# make sure cosmos is configured
***REMOVED***if not cosmos_conversation_client:
***REMOVED******REMOVED***raise Exception("CosmosDB is not configured")

***REMOVED***# check for the conversation_id, if the conversation is not set, we will create a new one
***REMOVED***history_metadata = {}
***REMOVED***if not conversation_id:
***REMOVED******REMOVED***title = generate_title(request.json["messages"])
***REMOVED******REMOVED***conversation_dict = cosmos_conversation_client.create_conversation(user_id=user_id, title=title)
***REMOVED******REMOVED***conversation_id = conversation_dict['id']
***REMOVED******REMOVED***history_metadata['title'] = title
***REMOVED******REMOVED***history_metadata['date'] = conversation_dict['createdAt']
***REMOVED******REMOVED***
***REMOVED***## Format the incoming message object in the "chat/completions" messages format
***REMOVED***## then write it to the conversation history in cosmos
***REMOVED***messages = request.json["messages"]
***REMOVED***if len(messages) > 0 and messages[-1]['role'] == "user":
***REMOVED******REMOVED***createdMessageValue = cosmos_conversation_client.create_message(
***REMOVED******REMOVED***uuid=str(uuid.uuid4()),
***REMOVED******REMOVED***conversation_id=conversation_id,
***REMOVED******REMOVED***user_id=user_id,
***REMOVED******REMOVED***input_message=messages[-1]
***REMOVED******REMOVED***)
***REMOVED******REMOVED***if createdMessageValue == "Conversation not found":
***REMOVED******REMOVED***raise Exception("Conversation not found for the given conversation ID: " + conversation_id + ".")
***REMOVED***else:
***REMOVED******REMOVED***raise Exception("No user message found")
***REMOVED***
***REMOVED***# Submit request to Chat Completions for response
***REMOVED***request_body = request.json
***REMOVED***history_metadata['conversation_id'] = conversation_id
***REMOVED***request_body['history_metadata'] = history_metadata
***REMOVED***return conversation_internal(request_body)
***REMOVED***   
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /history/generate")
***REMOVED***return jsonify({"error": str(e)}), 500


@app.route("/history/update", methods=["POST"])
def update_conversation():
***REMOVED***authenticated_user = get_authenticated_user_details(request_headers=request.headers)
***REMOVED***user_id = authenticated_user['user_principal_id']

***REMOVED***## check request for conversation_id
***REMOVED***conversation_id = request.json.get("conversation_id", None)

***REMOVED***try:
***REMOVED***# make sure cosmos is configured
***REMOVED***if not cosmos_conversation_client:
***REMOVED******REMOVED***raise Exception("CosmosDB is not configured")

***REMOVED***# check for the conversation_id, if the conversation is not set, we will create a new one
***REMOVED***if not conversation_id:
***REMOVED******REMOVED***raise Exception("No conversation_id found")
***REMOVED******REMOVED***
***REMOVED***## Format the incoming message object in the "chat/completions" messages format
***REMOVED***## then write it to the conversation history in cosmos
***REMOVED***messages = request.json["messages"]
***REMOVED***if len(messages) > 0 and messages[-1]['role'] == "assistant":
***REMOVED******REMOVED***if len(messages) > 1 and messages[-2].get('role', None) == "tool":
***REMOVED******REMOVED***# write the tool message first
***REMOVED******REMOVED***cosmos_conversation_client.create_message(
***REMOVED******REMOVED******REMOVED***uuid=str(uuid.uuid4()),
***REMOVED******REMOVED******REMOVED***conversation_id=conversation_id,
***REMOVED******REMOVED******REMOVED***user_id=user_id,
***REMOVED******REMOVED******REMOVED***input_message=messages[-2]
***REMOVED******REMOVED***)
***REMOVED******REMOVED***# write the assistant message
***REMOVED******REMOVED***cosmos_conversation_client.create_message(
***REMOVED******REMOVED***uuid=message_uuid,
***REMOVED******REMOVED***conversation_id=conversation_id,
***REMOVED******REMOVED***user_id=user_id,
***REMOVED******REMOVED***input_message=messages[-1]
***REMOVED******REMOVED***)
***REMOVED***else:
***REMOVED******REMOVED***raise Exception("No bot messages found")
***REMOVED***
***REMOVED***# Submit request to Chat Completions for response
***REMOVED***response = {'success': True}
***REMOVED***return jsonify(response), 200
***REMOVED***   
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /history/update")
***REMOVED***return jsonify({"error": str(e)}), 500

@app.route("/history/message_feedback", methods=["POST"])
def update_message():
***REMOVED***authenticated_user = get_authenticated_user_details(request_headers=request.headers)
***REMOVED***user_id = authenticated_user['user_principal_id']

***REMOVED***## check request for message_id
***REMOVED***message_id = request.json.get("message_id", None)
***REMOVED***message_feedback = request.json.get("message_feedback", None)
***REMOVED***try:
***REMOVED***if not message_id:
***REMOVED******REMOVED***return jsonify({"error": "message_id is required"}), 400
***REMOVED***
***REMOVED***if not message_feedback:
***REMOVED******REMOVED***return jsonify({"error": "message_feedback is required"}), 400
***REMOVED***
***REMOVED***## update the message in cosmos
***REMOVED***updated_message = cosmos_conversation_client.update_message_feedback(user_id, message_id, message_feedback)
***REMOVED***if updated_message:
***REMOVED******REMOVED***return jsonify({"message": f"Successfully updated message with feedback {message_feedback}", "message_id": message_id}), 200
***REMOVED***else:
***REMOVED******REMOVED***return jsonify({"error": f"Unable to update message {message_id}. It either does not exist or the user does not have access to it."}), 404
***REMOVED***
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /history/message_feedback")
***REMOVED***return jsonify({"error": str(e)}), 500


@app.route("/history/delete", methods=["DELETE"])
def delete_conversation():
***REMOVED***## get the user id from the request headers
***REMOVED***authenticated_user = get_authenticated_user_details(request_headers=request.headers)
***REMOVED***user_id = authenticated_user['user_principal_id']
***REMOVED***
***REMOVED***## check request for conversation_id
***REMOVED***conversation_id = request.json.get("conversation_id", None)
***REMOVED***try: 
***REMOVED***if not conversation_id:
***REMOVED******REMOVED***return jsonify({"error": "conversation_id is required"}), 400
***REMOVED***
***REMOVED***## delete the conversation messages from cosmos first
***REMOVED***deleted_messages = cosmos_conversation_client.delete_messages(conversation_id, user_id)

***REMOVED***## Now delete the conversation 
***REMOVED***deleted_conversation = cosmos_conversation_client.delete_conversation(user_id, conversation_id)

***REMOVED***return jsonify({"message": "Successfully deleted conversation and messages", "conversation_id": conversation_id}), 200
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /history/delete")
***REMOVED***return jsonify({"error": str(e)}), 500

@app.route("/history/list", methods=["GET"])
def list_conversations():
***REMOVED***offset = request.args.get("offset", 0)
***REMOVED***authenticated_user = get_authenticated_user_details(request_headers=request.headers)
***REMOVED***user_id = authenticated_user['user_principal_id']

***REMOVED***## get the conversations from cosmos
***REMOVED***conversations = cosmos_conversation_client.get_conversations(user_id, offset=offset, limit=25)
***REMOVED***if not isinstance(conversations, list):
***REMOVED***return jsonify({"error": f"No conversations for {user_id} were found"}), 404

***REMOVED***## return the conversation ids

***REMOVED***return jsonify(conversations), 200

@app.route("/history/read", methods=["POST"])
def get_conversation():
***REMOVED***authenticated_user = get_authenticated_user_details(request_headers=request.headers)
***REMOVED***user_id = authenticated_user['user_principal_id']

***REMOVED***## check request for conversation_id
***REMOVED***conversation_id = request.json.get("conversation_id", None)
***REMOVED***
***REMOVED***if not conversation_id:
***REMOVED***return jsonify({"error": "conversation_id is required"}), 400

***REMOVED***## get the conversation object and the related messages from cosmos
***REMOVED***conversation = cosmos_conversation_client.get_conversation(user_id, conversation_id)
***REMOVED***## return the conversation id and the messages in the bot frontend format
***REMOVED***if not conversation:
***REMOVED***return jsonify({"error": f"Conversation {conversation_id} was not found. It either does not exist or the logged in user does not have access to it."}), 404
***REMOVED***
***REMOVED***# get the messages for the conversation from cosmos
***REMOVED***conversation_messages = cosmos_conversation_client.get_messages(user_id, conversation_id)

***REMOVED***## format the messages in the bot frontend format
***REMOVED***messages = [{'id': msg['id'], 'role': msg['role'], 'content': msg['content'], 'createdAt': msg['createdAt'], 'feedback': msg.get('feedback')} for msg in conversation_messages]

***REMOVED***return jsonify({"conversation_id": conversation_id, "messages": messages}), 200

@app.route("/history/rename", methods=["POST"])
def rename_conversation():
***REMOVED***authenticated_user = get_authenticated_user_details(request_headers=request.headers)
***REMOVED***user_id = authenticated_user['user_principal_id']

***REMOVED***## check request for conversation_id
***REMOVED***conversation_id = request.json.get("conversation_id", None)
***REMOVED***
***REMOVED***if not conversation_id:
***REMOVED***return jsonify({"error": "conversation_id is required"}), 400
***REMOVED***
***REMOVED***## get the conversation from cosmos
***REMOVED***conversation = cosmos_conversation_client.get_conversation(user_id, conversation_id)
***REMOVED***if not conversation:
***REMOVED***return jsonify({"error": f"Conversation {conversation_id} was not found. It either does not exist or the logged in user does not have access to it."}), 404

***REMOVED***## update the title
***REMOVED***title = request.json.get("title", None)
***REMOVED***if not title:
***REMOVED***return jsonify({"error": "title is required"}), 400
***REMOVED***conversation['title'] = title
***REMOVED***updated_conversation = cosmos_conversation_client.upsert_conversation(conversation)

***REMOVED***return jsonify(updated_conversation), 200

@app.route("/history/delete_all", methods=["DELETE"])
def delete_all_conversations():
***REMOVED***## get the user id from the request headers
***REMOVED***authenticated_user = get_authenticated_user_details(request_headers=request.headers)
***REMOVED***user_id = authenticated_user['user_principal_id']

***REMOVED***# get conversations for user
***REMOVED***try:
***REMOVED***conversations = cosmos_conversation_client.get_conversations(user_id, offset=0, limit=None)
***REMOVED***if not conversations:
***REMOVED******REMOVED***return jsonify({"error": f"No conversations for {user_id} were found"}), 404
***REMOVED***
***REMOVED***# delete each conversation
***REMOVED***for conversation in conversations:
***REMOVED******REMOVED***## delete the conversation messages from cosmos first
***REMOVED******REMOVED***deleted_messages = cosmos_conversation_client.delete_messages(conversation['id'], user_id)

***REMOVED******REMOVED***## Now delete the conversation 
***REMOVED******REMOVED***deleted_conversation = cosmos_conversation_client.delete_conversation(user_id, conversation['id'])

***REMOVED***return jsonify({"message": f"Successfully deleted conversation and messages for user {user_id}"}), 200
***REMOVED***
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /history/delete_all")
***REMOVED***return jsonify({"error": str(e)}), 500
***REMOVED***

@app.route("/history/clear", methods=["POST"])
def clear_messages():
***REMOVED***## get the user id from the request headers
***REMOVED***authenticated_user = get_authenticated_user_details(request_headers=request.headers)
***REMOVED***user_id = authenticated_user['user_principal_id']
***REMOVED***
***REMOVED***## check request for conversation_id
***REMOVED***conversation_id = request.json.get("conversation_id", None)
***REMOVED***try: 
***REMOVED***if not conversation_id:
***REMOVED******REMOVED***return jsonify({"error": "conversation_id is required"}), 400
***REMOVED***
***REMOVED***## delete the conversation messages from cosmos
***REMOVED***deleted_messages = cosmos_conversation_client.delete_messages(conversation_id, user_id)

***REMOVED***return jsonify({"message": "Successfully deleted messages in conversation", "conversation_id": conversation_id}), 200
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /history/clear_messages")
***REMOVED***return jsonify({"error": str(e)}), 500

@app.route("/history/ensure", methods=["GET"])
def ensure_cosmos():
***REMOVED***if not AZURE_COSMOSDB_ACCOUNT:
***REMOVED***return jsonify({"error": "CosmosDB is not configured"}), 404
***REMOVED***
***REMOVED***if not cosmos_conversation_client or not cosmos_conversation_client.ensure():
***REMOVED***if cosmodb_error == "Invalid credentials":
***REMOVED******REMOVED***return jsonify({"error": cosmodb_error}), 401
***REMOVED***elif cosmodb_error == "Invalid CosmosDB database name":
***REMOVED******REMOVED***return jsonify({"error": f"{cosmodb_error} {AZURE_COSMOSDB_DATABASE} for account {AZURE_COSMOSDB_ACCOUNT}"}), 422
***REMOVED***elif cosmodb_error == "Invalid CosmosDB container name":
***REMOVED******REMOVED***return jsonify({"error": f"{cosmodb_error}: {AZURE_COSMOSDB_CONVERSATIONS_CONTAINER}"}), 422
***REMOVED***else:
***REMOVED******REMOVED***return jsonify({"error": "CosmosDB is not working"}), 500

***REMOVED***return jsonify({"message": "CosmosDB is configured and working"}), 200

@app.route("/frontend_settings", methods=["GET"])  
def get_frontend_settings():
***REMOVED***try:
***REMOVED***return jsonify(frontend_settings), 200
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /frontend_settings")
***REMOVED***return jsonify({"error": str(e)}), 500  

def generate_title(conversation_messages):
***REMOVED***## make sure the messages are sorted by _ts descending
***REMOVED***title_prompt = 'Summarize the conversation so far into a 4-word or less title. Do not use any quotation marks or punctuation. Respond with a json object in the format {{"title": string}}. Do not include any other commentary or description.'

***REMOVED***messages = [{'role': msg['role'], 'content': msg['content']} for msg in conversation_messages]
***REMOVED***messages.append({'role': 'user', 'content': title_prompt})

***REMOVED***try:
***REMOVED***## Submit prompt to Chat Completions for response
***REMOVED***base_url = AZURE_OPENAI_ENDPOINT if AZURE_OPENAI_ENDPOINT else f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/"
***REMOVED***openai.api_type = "azure"
***REMOVED***openai.api_base = base_url
***REMOVED***openai.api_version = "2023-03-15-preview"
***REMOVED***openai.api_key = AZURE_OPENAI_KEY
***REMOVED***completion = openai.ChatCompletion.create(***REMOVED***
***REMOVED******REMOVED***engine=AZURE_OPENAI_MODEL,
***REMOVED******REMOVED***messages=messages,
***REMOVED******REMOVED***temperature=1,
***REMOVED******REMOVED***max_tokens=64 
***REMOVED***)
***REMOVED***title = json.loads(completion['choices'][0]['message']['content'])['title']
***REMOVED***return title
***REMOVED***except Exception as e:
***REMOVED***return messages[-2]['content']

if __name__ == "__main__":
***REMOVED***app.run()