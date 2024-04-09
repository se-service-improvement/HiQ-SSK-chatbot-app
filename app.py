import copy
import json
import os
import logging
import uuid
from dotenv import load_dotenv
import httpx
from quart import (
***REMOVED***Blueprint,
***REMOVED***Quart,
***REMOVED***jsonify,
***REMOVED***make_response,
***REMOVED***request,
***REMOVED***send_from_directory,
***REMOVED***render_template,
)

from openai import AsyncAzureOpenAI
from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider
from backend.auth.auth_utils import get_authenticated_user_details
from backend.history.cosmosdbservice import CosmosConversationClient

from backend.utils import (
***REMOVED***format_as_ndjson,
***REMOVED***format_stream_response,
***REMOVED***generateFilterString,
***REMOVED***parse_multi_columns,
***REMOVED***format_non_streaming_response,
***REMOVED***convert_to_pf_format,
***REMOVED***format_pf_non_streaming_response,
)

bp = Blueprint("routes", __name__, static_folder="static", template_folder="static")

# Current minimum Azure OpenAI version supported
MINIMUM_SUPPORTED_AZURE_OPENAI_PREVIEW_API_VERSION = "2024-02-15-preview"

load_dotenv()

# UI configuration (optional)
UI_TITLE = os.environ.get("UI_TITLE") or "Contoso"
UI_LOGO = os.environ.get("UI_LOGO")
UI_CHAT_LOGO = os.environ.get("UI_CHAT_LOGO")
UI_CHAT_TITLE = os.environ.get("UI_CHAT_TITLE") or "Start chatting"
UI_CHAT_DESCRIPTION = (
***REMOVED***os.environ.get("UI_CHAT_DESCRIPTION")
***REMOVED***or "This chatbot is configured to answer your questions"
)
UI_FAVICON = os.environ.get("UI_FAVICON") or "/favicon.ico"
UI_SHOW_SHARE_BUTTON = os.environ.get("UI_SHOW_SHARE_BUTTON", "true").lower() == "true"


def create_app():
***REMOVED***app = Quart(__name__)
***REMOVED***app.register_blueprint(bp)
***REMOVED***app.config["TEMPLATES_AUTO_RELOAD"] = True
***REMOVED***return app


@bp.route("/")
async def index():
***REMOVED***return await render_template("index.html", title=UI_TITLE, favicon=UI_FAVICON)


@bp.route("/favicon.ico")
async def favicon():
***REMOVED***return await bp.send_static_file("favicon.ico")


@bp.route("/assets/<path:path>")
async def assets(path):
***REMOVED***return await send_from_directory("static/assets", path)


# Debug settings
DEBUG = os.environ.get("DEBUG", "false")
if DEBUG.lower() == "true":
***REMOVED***logging.basicConfig(level=logging.DEBUG)

USER_AGENT = "GitHubSampleWebApp/AsyncAzureOpenAI/1.0.0"

# On Your Data Settings
DATASOURCE_TYPE = os.environ.get("DATASOURCE_TYPE", "AzureCognitiveSearch")
SEARCH_TOP_K = os.environ.get("SEARCH_TOP_K", 5)
SEARCH_STRICTNESS = os.environ.get("SEARCH_STRICTNESS", 3)
SEARCH_ENABLE_IN_DOMAIN = os.environ.get("SEARCH_ENABLE_IN_DOMAIN", "true")

# ACS Integration Settings
AZURE_SEARCH_SERVICE = os.environ.get("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX")
AZURE_SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY", None)
AZURE_SEARCH_USE_SEMANTIC_SEARCH = os.environ.get(
***REMOVED***"AZURE_SEARCH_USE_SEMANTIC_SEARCH", "false"
)
AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG = os.environ.get(
***REMOVED***"AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG", "default"
)
AZURE_SEARCH_TOP_K = os.environ.get("AZURE_SEARCH_TOP_K", SEARCH_TOP_K)
AZURE_SEARCH_ENABLE_IN_DOMAIN = os.environ.get(
***REMOVED***"AZURE_SEARCH_ENABLE_IN_DOMAIN", SEARCH_ENABLE_IN_DOMAIN
)
AZURE_SEARCH_CONTENT_COLUMNS = os.environ.get("AZURE_SEARCH_CONTENT_COLUMNS")
AZURE_SEARCH_FILENAME_COLUMN = os.environ.get("AZURE_SEARCH_FILENAME_COLUMN")
AZURE_SEARCH_TITLE_COLUMN = os.environ.get("AZURE_SEARCH_TITLE_COLUMN")
AZURE_SEARCH_URL_COLUMN = os.environ.get("AZURE_SEARCH_URL_COLUMN")
AZURE_SEARCH_VECTOR_COLUMNS = os.environ.get("AZURE_SEARCH_VECTOR_COLUMNS")
AZURE_SEARCH_QUERY_TYPE = os.environ.get("AZURE_SEARCH_QUERY_TYPE")
AZURE_SEARCH_PERMITTED_GROUPS_COLUMN = os.environ.get(
***REMOVED***"AZURE_SEARCH_PERMITTED_GROUPS_COLUMN"
)
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
AZURE_OPENAI_SYSTEM_MESSAGE = os.environ.get(
***REMOVED***"AZURE_OPENAI_SYSTEM_MESSAGE",
***REMOVED***"You are an AI assistant that helps people find information.",
)
AZURE_OPENAI_PREVIEW_API_VERSION = os.environ.get(
***REMOVED***"AZURE_OPENAI_PREVIEW_API_VERSION",
***REMOVED***MINIMUM_SUPPORTED_AZURE_OPENAI_PREVIEW_API_VERSION,
)
AZURE_OPENAI_STREAM = os.environ.get("AZURE_OPENAI_STREAM", "true")
AZURE_OPENAI_MODEL_NAME = os.environ.get(
***REMOVED***"AZURE_OPENAI_MODEL_NAME", "gpt-35-turbo-16k"
)  # Name of the model, e.g. 'gpt-35-turbo-16k' or 'gpt-4'
AZURE_OPENAI_EMBEDDING_ENDPOINT = os.environ.get("AZURE_OPENAI_EMBEDDING_ENDPOINT")
AZURE_OPENAI_EMBEDDING_KEY = os.environ.get("AZURE_OPENAI_EMBEDDING_KEY")
AZURE_OPENAI_EMBEDDING_NAME = os.environ.get("AZURE_OPENAI_EMBEDDING_NAME", "")

# CosmosDB Mongo vcore vector db Settings
AZURE_COSMOSDB_MONGO_VCORE_CONNECTION_STRING = os.environ.get(
***REMOVED***"AZURE_COSMOSDB_MONGO_VCORE_CONNECTION_STRING"
)  # This has to be secure string
AZURE_COSMOSDB_MONGO_VCORE_DATABASE = os.environ.get(
***REMOVED***"AZURE_COSMOSDB_MONGO_VCORE_DATABASE"
)
AZURE_COSMOSDB_MONGO_VCORE_CONTAINER = os.environ.get(
***REMOVED***"AZURE_COSMOSDB_MONGO_VCORE_CONTAINER"
)
AZURE_COSMOSDB_MONGO_VCORE_INDEX = os.environ.get("AZURE_COSMOSDB_MONGO_VCORE_INDEX")
AZURE_COSMOSDB_MONGO_VCORE_TOP_K = os.environ.get(
***REMOVED***"AZURE_COSMOSDB_MONGO_VCORE_TOP_K", AZURE_SEARCH_TOP_K
)
AZURE_COSMOSDB_MONGO_VCORE_STRICTNESS = os.environ.get(
***REMOVED***"AZURE_COSMOSDB_MONGO_VCORE_STRICTNESS", AZURE_SEARCH_STRICTNESS
)
AZURE_COSMOSDB_MONGO_VCORE_ENABLE_IN_DOMAIN = os.environ.get(
***REMOVED***"AZURE_COSMOSDB_MONGO_VCORE_ENABLE_IN_DOMAIN", AZURE_SEARCH_ENABLE_IN_DOMAIN
)
AZURE_COSMOSDB_MONGO_VCORE_CONTENT_COLUMNS = os.environ.get(
***REMOVED***"AZURE_COSMOSDB_MONGO_VCORE_CONTENT_COLUMNS", ""
)
AZURE_COSMOSDB_MONGO_VCORE_FILENAME_COLUMN = os.environ.get(
***REMOVED***"AZURE_COSMOSDB_MONGO_VCORE_FILENAME_COLUMN"
)
AZURE_COSMOSDB_MONGO_VCORE_TITLE_COLUMN = os.environ.get(
***REMOVED***"AZURE_COSMOSDB_MONGO_VCORE_TITLE_COLUMN"
)
AZURE_COSMOSDB_MONGO_VCORE_URL_COLUMN = os.environ.get(
***REMOVED***"AZURE_COSMOSDB_MONGO_VCORE_URL_COLUMN"
)
AZURE_COSMOSDB_MONGO_VCORE_VECTOR_COLUMNS = os.environ.get(
***REMOVED***"AZURE_COSMOSDB_MONGO_VCORE_VECTOR_COLUMNS"
)

SHOULD_STREAM = True if AZURE_OPENAI_STREAM.lower() == "true" else False

# Chat History CosmosDB Integration Settings
AZURE_COSMOSDB_DATABASE = os.environ.get("AZURE_COSMOSDB_DATABASE")
AZURE_COSMOSDB_ACCOUNT = os.environ.get("AZURE_COSMOSDB_ACCOUNT")
AZURE_COSMOSDB_CONVERSATIONS_CONTAINER = os.environ.get(
***REMOVED***"AZURE_COSMOSDB_CONVERSATIONS_CONTAINER"
)
AZURE_COSMOSDB_ACCOUNT_KEY = os.environ.get("AZURE_COSMOSDB_ACCOUNT_KEY")
AZURE_COSMOSDB_ENABLE_FEEDBACK = (
***REMOVED***os.environ.get("AZURE_COSMOSDB_ENABLE_FEEDBACK", "false").lower() == "true"
)

# Elasticsearch Integration Settings
ELASTICSEARCH_ENDPOINT = os.environ.get("ELASTICSEARCH_ENDPOINT")
ELASTICSEARCH_ENCODED_API_KEY = os.environ.get("ELASTICSEARCH_ENCODED_API_KEY")
ELASTICSEARCH_INDEX = os.environ.get("ELASTICSEARCH_INDEX")
ELASTICSEARCH_QUERY_TYPE = os.environ.get("ELASTICSEARCH_QUERY_TYPE", "simple")
ELASTICSEARCH_TOP_K = os.environ.get("ELASTICSEARCH_TOP_K", SEARCH_TOP_K)
ELASTICSEARCH_ENABLE_IN_DOMAIN = os.environ.get(
***REMOVED***"ELASTICSEARCH_ENABLE_IN_DOMAIN", SEARCH_ENABLE_IN_DOMAIN
)
ELASTICSEARCH_CONTENT_COLUMNS = os.environ.get("ELASTICSEARCH_CONTENT_COLUMNS")
ELASTICSEARCH_FILENAME_COLUMN = os.environ.get("ELASTICSEARCH_FILENAME_COLUMN")
ELASTICSEARCH_TITLE_COLUMN = os.environ.get("ELASTICSEARCH_TITLE_COLUMN")
ELASTICSEARCH_URL_COLUMN = os.environ.get("ELASTICSEARCH_URL_COLUMN")
ELASTICSEARCH_VECTOR_COLUMNS = os.environ.get("ELASTICSEARCH_VECTOR_COLUMNS")
ELASTICSEARCH_STRICTNESS = os.environ.get("ELASTICSEARCH_STRICTNESS", SEARCH_STRICTNESS)
ELASTICSEARCH_EMBEDDING_MODEL_ID = os.environ.get("ELASTICSEARCH_EMBEDDING_MODEL_ID")

# Pinecone Integration Settings
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")
PINECONE_TOP_K = os.environ.get("PINECONE_TOP_K", SEARCH_TOP_K)
PINECONE_STRICTNESS = os.environ.get("PINECONE_STRICTNESS", SEARCH_STRICTNESS)
PINECONE_ENABLE_IN_DOMAIN = os.environ.get(
***REMOVED***"PINECONE_ENABLE_IN_DOMAIN", SEARCH_ENABLE_IN_DOMAIN
)
PINECONE_CONTENT_COLUMNS = os.environ.get("PINECONE_CONTENT_COLUMNS", "")
PINECONE_FILENAME_COLUMN = os.environ.get("PINECONE_FILENAME_COLUMN")
PINECONE_TITLE_COLUMN = os.environ.get("PINECONE_TITLE_COLUMN")
PINECONE_URL_COLUMN = os.environ.get("PINECONE_URL_COLUMN")
PINECONE_VECTOR_COLUMNS = os.environ.get("PINECONE_VECTOR_COLUMNS")

# Azure AI MLIndex Integration Settings - for use with MLIndex data assets created in Azure AI Studio
AZURE_MLINDEX_NAME = os.environ.get("AZURE_MLINDEX_NAME")
AZURE_MLINDEX_VERSION = os.environ.get("AZURE_MLINDEX_VERSION")
AZURE_ML_PROJECT_RESOURCE_ID = os.environ.get(
***REMOVED***"AZURE_ML_PROJECT_RESOURCE_ID"
)  # /subscriptions/{sub ID}/resourceGroups/{rg name}/providers/Microsoft.MachineLearningServices/workspaces/{AML project name}
AZURE_MLINDEX_TOP_K = os.environ.get("AZURE_MLINDEX_TOP_K", SEARCH_TOP_K)
AZURE_MLINDEX_STRICTNESS = os.environ.get("AZURE_MLINDEX_STRICTNESS", SEARCH_STRICTNESS)
AZURE_MLINDEX_ENABLE_IN_DOMAIN = os.environ.get(
***REMOVED***"AZURE_MLINDEX_ENABLE_IN_DOMAIN", SEARCH_ENABLE_IN_DOMAIN
)
AZURE_MLINDEX_CONTENT_COLUMNS = os.environ.get("AZURE_MLINDEX_CONTENT_COLUMNS", "")
AZURE_MLINDEX_FILENAME_COLUMN = os.environ.get("AZURE_MLINDEX_FILENAME_COLUMN")
AZURE_MLINDEX_TITLE_COLUMN = os.environ.get("AZURE_MLINDEX_TITLE_COLUMN")
AZURE_MLINDEX_URL_COLUMN = os.environ.get("AZURE_MLINDEX_URL_COLUMN")
AZURE_MLINDEX_VECTOR_COLUMNS = os.environ.get("AZURE_MLINDEX_VECTOR_COLUMNS")
AZURE_MLINDEX_QUERY_TYPE = os.environ.get("AZURE_MLINDEX_QUERY_TYPE")
# Promptflow Integration Settings
USE_PROMPTFLOW = os.environ.get("USE_PROMPTFLOW", "false").lower() == "true"
PROMPTFLOW_ENDPOINT = os.environ.get("PROMPTFLOW_ENDPOINT")
PROMPTFLOW_API_KEY = os.environ.get("PROMPTFLOW_API_KEY")
PROMPTFLOW_RESPONSE_TIMEOUT = os.environ.get("PROMPTFLOW_RESPONSE_TIMEOUT", 30.0)
# default request and response field names are input -> 'query' and output -> 'reply'
PROMPTFLOW_REQUEST_FIELD_NAME = os.environ.get("PROMPTFLOW_REQUEST_FIELD_NAME", "query")
PROMPTFLOW_RESPONSE_FIELD_NAME = os.environ.get(
***REMOVED***"PROMPTFLOW_RESPONSE_FIELD_NAME", "reply"
)
# Frontend Settings via Environment Variables
AUTH_ENABLED = os.environ.get("AUTH_ENABLED", "true").lower() == "true"
CHAT_HISTORY_ENABLED = (
***REMOVED***AZURE_COSMOSDB_ACCOUNT
***REMOVED***and AZURE_COSMOSDB_DATABASE
***REMOVED***and AZURE_COSMOSDB_CONVERSATIONS_CONTAINER
)
SANITIZE_ANSWER = os.environ.get("SANITIZE_ANSWER", "false").lower() == "true"
frontend_settings = {
***REMOVED***"auth_enabled": AUTH_ENABLED,
***REMOVED***"feedback_enabled": AZURE_COSMOSDB_ENABLE_FEEDBACK and CHAT_HISTORY_ENABLED,
***REMOVED***"ui": {
***REMOVED***"title": UI_TITLE,
***REMOVED***"logo": UI_LOGO,
***REMOVED***"chat_logo": UI_CHAT_LOGO or UI_LOGO,
***REMOVED***"chat_title": UI_CHAT_TITLE,
***REMOVED***"chat_description": UI_CHAT_DESCRIPTION,
***REMOVED***"show_share_button": UI_SHOW_SHARE_BUTTON,
***REMOVED***,
***REMOVED***"sanitize_answer": SANITIZE_ANSWER,
}


def should_use_data():
***REMOVED***global DATASOURCE_TYPE
***REMOVED***if AZURE_SEARCH_SERVICE and AZURE_SEARCH_INDEX:
***REMOVED***DATASOURCE_TYPE = "AzureCognitiveSearch"
***REMOVED***logging.debug("Using Azure Cognitive Search")
***REMOVED***return True

***REMOVED***if (
***REMOVED***AZURE_COSMOSDB_MONGO_VCORE_DATABASE
***REMOVED***and AZURE_COSMOSDB_MONGO_VCORE_CONTAINER
***REMOVED***and AZURE_COSMOSDB_MONGO_VCORE_INDEX
***REMOVED***and AZURE_COSMOSDB_MONGO_VCORE_CONNECTION_STRING
***REMOVED***):
***REMOVED***DATASOURCE_TYPE = "AzureCosmosDB"
***REMOVED***logging.debug("Using Azure CosmosDB Mongo vcore")
***REMOVED***return True

***REMOVED***if ELASTICSEARCH_ENDPOINT and ELASTICSEARCH_ENCODED_API_KEY and ELASTICSEARCH_INDEX:
***REMOVED***DATASOURCE_TYPE = "Elasticsearch"
***REMOVED***logging.debug("Using Elasticsearch")
***REMOVED***return True

***REMOVED***if PINECONE_ENVIRONMENT and PINECONE_API_KEY and PINECONE_INDEX_NAME:
***REMOVED***DATASOURCE_TYPE = "Pinecone"
***REMOVED***logging.debug("Using Pinecone")
***REMOVED***return True

***REMOVED***if AZURE_MLINDEX_NAME and AZURE_MLINDEX_VERSION and AZURE_ML_PROJECT_RESOURCE_ID:
***REMOVED***DATASOURCE_TYPE = "AzureMLIndex"
***REMOVED***logging.debug("Using Azure ML Index")
***REMOVED***return True

***REMOVED***return False


SHOULD_USE_DATA = should_use_data()


# Initialize Azure OpenAI Client
def init_openai_client(use_data=SHOULD_USE_DATA):
***REMOVED***azure_openai_client = None
***REMOVED***try:
***REMOVED***# API version check
***REMOVED***if (
***REMOVED******REMOVED***AZURE_OPENAI_PREVIEW_API_VERSION
***REMOVED******REMOVED***< MINIMUM_SUPPORTED_AZURE_OPENAI_PREVIEW_API_VERSION
***REMOVED***):
***REMOVED******REMOVED***raise Exception(
***REMOVED******REMOVED***f"The minimum supported Azure OpenAI preview API version is '{MINIMUM_SUPPORTED_AZURE_OPENAI_PREVIEW_API_VERSION}'"
***REMOVED******REMOVED***)

***REMOVED***# Endpoint
***REMOVED***if not AZURE_OPENAI_ENDPOINT and not AZURE_OPENAI_RESOURCE:
***REMOVED******REMOVED***raise Exception(
***REMOVED******REMOVED***"AZURE_OPENAI_ENDPOINT or AZURE_OPENAI_RESOURCE is required"
***REMOVED******REMOVED***)

***REMOVED***endpoint = (
***REMOVED******REMOVED***AZURE_OPENAI_ENDPOINT
***REMOVED******REMOVED***if AZURE_OPENAI_ENDPOINT
***REMOVED******REMOVED***else f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/"
***REMOVED***)

***REMOVED***# Authentication
***REMOVED***aoai_api_key = AZURE_OPENAI_KEY
***REMOVED***ad_token_provider = None
***REMOVED***if not aoai_api_key:
***REMOVED******REMOVED***logging.debug("No AZURE_OPENAI_KEY found, using Azure AD auth")
***REMOVED******REMOVED***ad_token_provider = get_bearer_token_provider(
***REMOVED******REMOVED***DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
***REMOVED******REMOVED***)

***REMOVED***# Deployment
***REMOVED***deployment = AZURE_OPENAI_MODEL
***REMOVED***if not deployment:
***REMOVED******REMOVED***raise Exception("AZURE_OPENAI_MODEL is required")

***REMOVED***# Default Headers
***REMOVED***default_headers = {"x-ms-useragent": USER_AGENT}

***REMOVED***azure_openai_client = AsyncAzureOpenAI(
***REMOVED******REMOVED***api_version=AZURE_OPENAI_PREVIEW_API_VERSION,
***REMOVED******REMOVED***api_key=aoai_api_key,
***REMOVED******REMOVED***azure_ad_token_provider=ad_token_provider,
***REMOVED******REMOVED***default_headers=default_headers,
***REMOVED******REMOVED***azure_endpoint=endpoint,
***REMOVED***)

***REMOVED***return azure_openai_client
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in Azure OpenAI initialization", e)
***REMOVED***azure_openai_client = None
***REMOVED***raise e


def init_cosmosdb_client():
***REMOVED***cosmos_conversation_client = None
***REMOVED***if CHAT_HISTORY_ENABLED:
***REMOVED***try:
***REMOVED******REMOVED***cosmos_endpoint = (
***REMOVED******REMOVED***f"https://{AZURE_COSMOSDB_ACCOUNT}.documents.azure.com:443/"
***REMOVED******REMOVED***)

***REMOVED******REMOVED***if not AZURE_COSMOSDB_ACCOUNT_KEY:
***REMOVED******REMOVED***credential = DefaultAzureCredential()
***REMOVED******REMOVED***else:
***REMOVED******REMOVED***credential = AZURE_COSMOSDB_ACCOUNT_KEY

***REMOVED******REMOVED***cosmos_conversation_client = CosmosConversationClient(
***REMOVED******REMOVED***cosmosdb_endpoint=cosmos_endpoint,
***REMOVED******REMOVED***credential=credential,
***REMOVED******REMOVED***database_name=AZURE_COSMOSDB_DATABASE,
***REMOVED******REMOVED***container_name=AZURE_COSMOSDB_CONVERSATIONS_CONTAINER,
***REMOVED******REMOVED***enable_message_feedback=AZURE_COSMOSDB_ENABLE_FEEDBACK,
***REMOVED******REMOVED***)
***REMOVED***except Exception as e:
***REMOVED******REMOVED***logging.exception("Exception in CosmosDB initialization", e)
***REMOVED******REMOVED***cosmos_conversation_client = None
***REMOVED******REMOVED***raise e
***REMOVED***else:
***REMOVED***logging.debug("CosmosDB not configured")

***REMOVED***return cosmos_conversation_client


def get_configured_data_source():
***REMOVED***data_source = {}
***REMOVED***query_type = "simple"
***REMOVED***if DATASOURCE_TYPE == "AzureCognitiveSearch":
***REMOVED***# Set query type
***REMOVED***if AZURE_SEARCH_QUERY_TYPE:
***REMOVED******REMOVED***query_type = AZURE_SEARCH_QUERY_TYPE
***REMOVED***elif (
***REMOVED******REMOVED***AZURE_SEARCH_USE_SEMANTIC_SEARCH.lower() == "true"
***REMOVED******REMOVED***and AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG
***REMOVED***):
***REMOVED******REMOVED***query_type = "semantic"

***REMOVED***# Set filter
***REMOVED***filter = None
***REMOVED***userToken = None
***REMOVED***if AZURE_SEARCH_PERMITTED_GROUPS_COLUMN:
***REMOVED******REMOVED***userToken = request.headers.get("X-MS-TOKEN-AAD-ACCESS-TOKEN", "")
***REMOVED******REMOVED***logging.debug(f"USER TOKEN is {'present' if userToken else 'not present'}")
***REMOVED******REMOVED***if not userToken:
***REMOVED******REMOVED***raise Exception(
***REMOVED******REMOVED******REMOVED***"Document-level access control is enabled, but user access token could not be fetched."
***REMOVED******REMOVED***)

***REMOVED******REMOVED***filter = generateFilterString(userToken)
***REMOVED******REMOVED***logging.debug(f"FILTER: {filter}")

***REMOVED***# Set authentication
***REMOVED***authentication = {}
***REMOVED***if AZURE_SEARCH_KEY:
***REMOVED******REMOVED***authentication = {"type": "api_key", "api_key": AZURE_SEARCH_KEY}
***REMOVED***else:
***REMOVED******REMOVED***# If key is not provided, assume AOAI resource identity has been granted access to the search service
***REMOVED******REMOVED***authentication = {"type": "system_assigned_managed_identity"}

***REMOVED***data_source = {
***REMOVED******REMOVED***"type": "azure_search",
***REMOVED******REMOVED***"parameters": {
***REMOVED******REMOVED***"endpoint": f"https://{AZURE_SEARCH_SERVICE}.search.windows.net",
***REMOVED******REMOVED***"authentication": authentication,
***REMOVED******REMOVED***"index_name": AZURE_SEARCH_INDEX,
***REMOVED******REMOVED***"fields_mapping": {
***REMOVED******REMOVED******REMOVED***"content_fields": (
***REMOVED******REMOVED******REMOVED***parse_multi_columns(AZURE_SEARCH_CONTENT_COLUMNS)
***REMOVED******REMOVED******REMOVED***if AZURE_SEARCH_CONTENT_COLUMNS
***REMOVED******REMOVED******REMOVED***else []
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***"title_field": (
***REMOVED******REMOVED******REMOVED***AZURE_SEARCH_TITLE_COLUMN if AZURE_SEARCH_TITLE_COLUMN else None
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***"url_field": (
***REMOVED******REMOVED******REMOVED***AZURE_SEARCH_URL_COLUMN if AZURE_SEARCH_URL_COLUMN else None
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***"filepath_field": (
***REMOVED******REMOVED******REMOVED***AZURE_SEARCH_FILENAME_COLUMN
***REMOVED******REMOVED******REMOVED***if AZURE_SEARCH_FILENAME_COLUMN
***REMOVED******REMOVED******REMOVED***else None
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***"vector_fields": (
***REMOVED******REMOVED******REMOVED***parse_multi_columns(AZURE_SEARCH_VECTOR_COLUMNS)
***REMOVED******REMOVED******REMOVED***if AZURE_SEARCH_VECTOR_COLUMNS
***REMOVED******REMOVED******REMOVED***else []
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED***,
***REMOVED******REMOVED***"in_scope": (
***REMOVED******REMOVED******REMOVED***True if AZURE_SEARCH_ENABLE_IN_DOMAIN.lower() == "true" else False
***REMOVED******REMOVED***),
***REMOVED******REMOVED***"top_n_documents": (
***REMOVED******REMOVED******REMOVED***int(AZURE_SEARCH_TOP_K) if AZURE_SEARCH_TOP_K else int(SEARCH_TOP_K)
***REMOVED******REMOVED***),
***REMOVED******REMOVED***"query_type": query_type,
***REMOVED******REMOVED***"semantic_configuration": (
***REMOVED******REMOVED******REMOVED***AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG
***REMOVED******REMOVED******REMOVED***if AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG
***REMOVED******REMOVED******REMOVED***else ""
***REMOVED******REMOVED***),
***REMOVED******REMOVED***"role_information": AZURE_OPENAI_SYSTEM_MESSAGE,
***REMOVED******REMOVED***"filter": filter,
***REMOVED******REMOVED***"strictness": (
***REMOVED******REMOVED******REMOVED***int(AZURE_SEARCH_STRICTNESS)
***REMOVED******REMOVED******REMOVED***if AZURE_SEARCH_STRICTNESS
***REMOVED******REMOVED******REMOVED***else int(SEARCH_STRICTNESS)
***REMOVED******REMOVED***),
***REMOVED***,
***REMOVED***
***REMOVED***elif DATASOURCE_TYPE == "AzureCosmosDB":
***REMOVED***query_type = "vector"

***REMOVED***data_source = {
***REMOVED******REMOVED***"type": "azure_cosmos_db",
***REMOVED******REMOVED***"parameters": {
***REMOVED******REMOVED***"authentication": {
***REMOVED******REMOVED******REMOVED***"type": "connection_string",
***REMOVED******REMOVED******REMOVED***"connection_string": AZURE_COSMOSDB_MONGO_VCORE_CONNECTION_STRING,
***REMOVED******REMOVED***,
***REMOVED******REMOVED***"index_name": AZURE_COSMOSDB_MONGO_VCORE_INDEX,
***REMOVED******REMOVED***"database_name": AZURE_COSMOSDB_MONGO_VCORE_DATABASE,
***REMOVED******REMOVED***"container_name": AZURE_COSMOSDB_MONGO_VCORE_CONTAINER,
***REMOVED******REMOVED***"fields_mapping": {
***REMOVED******REMOVED******REMOVED***"content_fields": (
***REMOVED******REMOVED******REMOVED***parse_multi_columns(AZURE_COSMOSDB_MONGO_VCORE_CONTENT_COLUMNS)
***REMOVED******REMOVED******REMOVED***if AZURE_COSMOSDB_MONGO_VCORE_CONTENT_COLUMNS
***REMOVED******REMOVED******REMOVED***else []
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***"title_field": (
***REMOVED******REMOVED******REMOVED***AZURE_COSMOSDB_MONGO_VCORE_TITLE_COLUMN
***REMOVED******REMOVED******REMOVED***if AZURE_COSMOSDB_MONGO_VCORE_TITLE_COLUMN
***REMOVED******REMOVED******REMOVED***else None
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***"url_field": (
***REMOVED******REMOVED******REMOVED***AZURE_COSMOSDB_MONGO_VCORE_URL_COLUMN
***REMOVED******REMOVED******REMOVED***if AZURE_COSMOSDB_MONGO_VCORE_URL_COLUMN
***REMOVED******REMOVED******REMOVED***else None
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***"filepath_field": (
***REMOVED******REMOVED******REMOVED***AZURE_COSMOSDB_MONGO_VCORE_FILENAME_COLUMN
***REMOVED******REMOVED******REMOVED***if AZURE_COSMOSDB_MONGO_VCORE_FILENAME_COLUMN
***REMOVED******REMOVED******REMOVED***else None
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***"vector_fields": (
***REMOVED******REMOVED******REMOVED***parse_multi_columns(AZURE_COSMOSDB_MONGO_VCORE_VECTOR_COLUMNS)
***REMOVED******REMOVED******REMOVED***if AZURE_COSMOSDB_MONGO_VCORE_VECTOR_COLUMNS
***REMOVED******REMOVED******REMOVED***else []
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED***,
***REMOVED******REMOVED***"in_scope": (
***REMOVED******REMOVED******REMOVED***True
***REMOVED******REMOVED******REMOVED***if AZURE_COSMOSDB_MONGO_VCORE_ENABLE_IN_DOMAIN.lower() == "true"
***REMOVED******REMOVED******REMOVED***else False
***REMOVED******REMOVED***),
***REMOVED******REMOVED***"top_n_documents": (
***REMOVED******REMOVED******REMOVED***int(AZURE_COSMOSDB_MONGO_VCORE_TOP_K)
***REMOVED******REMOVED******REMOVED***if AZURE_COSMOSDB_MONGO_VCORE_TOP_K
***REMOVED******REMOVED******REMOVED***else int(SEARCH_TOP_K)
***REMOVED******REMOVED***),
***REMOVED******REMOVED***"strictness": (
***REMOVED******REMOVED******REMOVED***int(AZURE_COSMOSDB_MONGO_VCORE_STRICTNESS)
***REMOVED******REMOVED******REMOVED***if AZURE_COSMOSDB_MONGO_VCORE_STRICTNESS
***REMOVED******REMOVED******REMOVED***else int(SEARCH_STRICTNESS)
***REMOVED******REMOVED***),
***REMOVED******REMOVED***"query_type": query_type,
***REMOVED******REMOVED***"role_information": AZURE_OPENAI_SYSTEM_MESSAGE,
***REMOVED***,
***REMOVED***
***REMOVED***elif DATASOURCE_TYPE == "Elasticsearch":
***REMOVED***if ELASTICSEARCH_QUERY_TYPE:
***REMOVED******REMOVED***query_type = ELASTICSEARCH_QUERY_TYPE

***REMOVED***data_source = {
***REMOVED******REMOVED***"type": "elasticsearch",
***REMOVED******REMOVED***"parameters": {
***REMOVED******REMOVED***"endpoint": ELASTICSEARCH_ENDPOINT,
***REMOVED******REMOVED***"authentication": {
***REMOVED******REMOVED******REMOVED***"type": "encoded_api_key",
***REMOVED******REMOVED******REMOVED***"encoded_api_key": ELASTICSEARCH_ENCODED_API_KEY,
***REMOVED******REMOVED***,
***REMOVED******REMOVED***"index_name": ELASTICSEARCH_INDEX,
***REMOVED******REMOVED***"fields_mapping": {
***REMOVED******REMOVED******REMOVED***"content_fields": (
***REMOVED******REMOVED******REMOVED***parse_multi_columns(ELASTICSEARCH_CONTENT_COLUMNS)
***REMOVED******REMOVED******REMOVED***if ELASTICSEARCH_CONTENT_COLUMNS
***REMOVED******REMOVED******REMOVED***else []
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***"title_field": (
***REMOVED******REMOVED******REMOVED***ELASTICSEARCH_TITLE_COLUMN
***REMOVED******REMOVED******REMOVED***if ELASTICSEARCH_TITLE_COLUMN
***REMOVED******REMOVED******REMOVED***else None
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***"url_field": (
***REMOVED******REMOVED******REMOVED***ELASTICSEARCH_URL_COLUMN if ELASTICSEARCH_URL_COLUMN else None
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***"filepath_field": (
***REMOVED******REMOVED******REMOVED***ELASTICSEARCH_FILENAME_COLUMN
***REMOVED******REMOVED******REMOVED***if ELASTICSEARCH_FILENAME_COLUMN
***REMOVED******REMOVED******REMOVED***else None
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***"vector_fields": (
***REMOVED******REMOVED******REMOVED***parse_multi_columns(ELASTICSEARCH_VECTOR_COLUMNS)
***REMOVED******REMOVED******REMOVED***if ELASTICSEARCH_VECTOR_COLUMNS
***REMOVED******REMOVED******REMOVED***else []
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED***,
***REMOVED******REMOVED***"in_scope": (
***REMOVED******REMOVED******REMOVED***True if ELASTICSEARCH_ENABLE_IN_DOMAIN.lower() == "true" else False
***REMOVED******REMOVED***),
***REMOVED******REMOVED***"top_n_documents": (
***REMOVED******REMOVED******REMOVED***int(ELASTICSEARCH_TOP_K)
***REMOVED******REMOVED******REMOVED***if ELASTICSEARCH_TOP_K
***REMOVED******REMOVED******REMOVED***else int(SEARCH_TOP_K)
***REMOVED******REMOVED***),
***REMOVED******REMOVED***"query_type": query_type,
***REMOVED******REMOVED***"role_information": AZURE_OPENAI_SYSTEM_MESSAGE,
***REMOVED******REMOVED***"strictness": (
***REMOVED******REMOVED******REMOVED***int(ELASTICSEARCH_STRICTNESS)
***REMOVED******REMOVED******REMOVED***if ELASTICSEARCH_STRICTNESS
***REMOVED******REMOVED******REMOVED***else int(SEARCH_STRICTNESS)
***REMOVED******REMOVED***),
***REMOVED***,
***REMOVED***
***REMOVED***elif DATASOURCE_TYPE == "AzureMLIndex":
***REMOVED***if AZURE_MLINDEX_QUERY_TYPE:
***REMOVED******REMOVED***query_type = AZURE_MLINDEX_QUERY_TYPE

***REMOVED***data_source = {
***REMOVED******REMOVED***"type": "azure_ml_index",
***REMOVED******REMOVED***"parameters": {
***REMOVED******REMOVED***"name": AZURE_MLINDEX_NAME,
***REMOVED******REMOVED***"version": AZURE_MLINDEX_VERSION,
***REMOVED******REMOVED***"project_resource_id": AZURE_ML_PROJECT_RESOURCE_ID,
***REMOVED******REMOVED***"fieldsMapping": {
***REMOVED******REMOVED******REMOVED***"content_fields": (
***REMOVED******REMOVED******REMOVED***parse_multi_columns(AZURE_MLINDEX_CONTENT_COLUMNS)
***REMOVED******REMOVED******REMOVED***if AZURE_MLINDEX_CONTENT_COLUMNS
***REMOVED******REMOVED******REMOVED***else []
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***"title_field": (
***REMOVED******REMOVED******REMOVED***AZURE_MLINDEX_TITLE_COLUMN
***REMOVED******REMOVED******REMOVED***if AZURE_MLINDEX_TITLE_COLUMN
***REMOVED******REMOVED******REMOVED***else None
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***"url_field": (
***REMOVED******REMOVED******REMOVED***AZURE_MLINDEX_URL_COLUMN if AZURE_MLINDEX_URL_COLUMN else None
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***"filepath_field": (
***REMOVED******REMOVED******REMOVED***AZURE_MLINDEX_FILENAME_COLUMN
***REMOVED******REMOVED******REMOVED***if AZURE_MLINDEX_FILENAME_COLUMN
***REMOVED******REMOVED******REMOVED***else None
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***"vector_fields": (
***REMOVED******REMOVED******REMOVED***parse_multi_columns(AZURE_MLINDEX_VECTOR_COLUMNS)
***REMOVED******REMOVED******REMOVED***if AZURE_MLINDEX_VECTOR_COLUMNS
***REMOVED******REMOVED******REMOVED***else []
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED***,
***REMOVED******REMOVED***"in_scope": (
***REMOVED******REMOVED******REMOVED***True if AZURE_MLINDEX_ENABLE_IN_DOMAIN.lower() == "true" else False
***REMOVED******REMOVED***),
***REMOVED******REMOVED***"top_n_documents": (
***REMOVED******REMOVED******REMOVED***int(AZURE_MLINDEX_TOP_K)
***REMOVED******REMOVED******REMOVED***if AZURE_MLINDEX_TOP_K
***REMOVED******REMOVED******REMOVED***else int(SEARCH_TOP_K)
***REMOVED******REMOVED***),
***REMOVED******REMOVED***"query_type": query_type,
***REMOVED******REMOVED***"role_information": AZURE_OPENAI_SYSTEM_MESSAGE,
***REMOVED******REMOVED***"strictness": (
***REMOVED******REMOVED******REMOVED***int(AZURE_MLINDEX_STRICTNESS)
***REMOVED******REMOVED******REMOVED***if AZURE_MLINDEX_STRICTNESS
***REMOVED******REMOVED******REMOVED***else int(SEARCH_STRICTNESS)
***REMOVED******REMOVED***),
***REMOVED***,
***REMOVED***
***REMOVED***elif DATASOURCE_TYPE == "Pinecone":
***REMOVED***query_type = "vector"

***REMOVED***data_source = {
***REMOVED******REMOVED***"type": "pinecone",
***REMOVED******REMOVED***"parameters": {
***REMOVED******REMOVED***"environment": PINECONE_ENVIRONMENT,
***REMOVED******REMOVED***"authentication": {"type": "api_key", "key": PINECONE_API_KEY},
***REMOVED******REMOVED***"index_name": PINECONE_INDEX_NAME,
***REMOVED******REMOVED***"fields_mapping": {
***REMOVED******REMOVED******REMOVED***"content_fields": (
***REMOVED******REMOVED******REMOVED***parse_multi_columns(PINECONE_CONTENT_COLUMNS)
***REMOVED******REMOVED******REMOVED***if PINECONE_CONTENT_COLUMNS
***REMOVED******REMOVED******REMOVED***else []
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***"title_field": (
***REMOVED******REMOVED******REMOVED***PINECONE_TITLE_COLUMN if PINECONE_TITLE_COLUMN else None
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***"url_field": PINECONE_URL_COLUMN if PINECONE_URL_COLUMN else None,
***REMOVED******REMOVED******REMOVED***"filepath_field": (
***REMOVED******REMOVED******REMOVED***PINECONE_FILENAME_COLUMN if PINECONE_FILENAME_COLUMN else None
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED******REMOVED***"vector_fields": (
***REMOVED******REMOVED******REMOVED***parse_multi_columns(PINECONE_VECTOR_COLUMNS)
***REMOVED******REMOVED******REMOVED***if PINECONE_VECTOR_COLUMNS
***REMOVED******REMOVED******REMOVED***else []
***REMOVED******REMOVED******REMOVED***),
***REMOVED******REMOVED***,
***REMOVED******REMOVED***"in_scope": (
***REMOVED******REMOVED******REMOVED***True if PINECONE_ENABLE_IN_DOMAIN.lower() == "true" else False
***REMOVED******REMOVED***),
***REMOVED******REMOVED***"top_n_documents": (
***REMOVED******REMOVED******REMOVED***int(PINECONE_TOP_K) if PINECONE_TOP_K else int(SEARCH_TOP_K)
***REMOVED******REMOVED***),
***REMOVED******REMOVED***"strictness": (
***REMOVED******REMOVED******REMOVED***int(PINECONE_STRICTNESS)
***REMOVED******REMOVED******REMOVED***if PINECONE_STRICTNESS
***REMOVED******REMOVED******REMOVED***else int(SEARCH_STRICTNESS)
***REMOVED******REMOVED***),
***REMOVED******REMOVED***"query_type": query_type,
***REMOVED******REMOVED***"role_information": AZURE_OPENAI_SYSTEM_MESSAGE,
***REMOVED***,
***REMOVED***
***REMOVED***else:
***REMOVED***raise Exception(
***REMOVED******REMOVED***f"DATASOURCE_TYPE is not configured or unknown: {DATASOURCE_TYPE}"
***REMOVED***)

***REMOVED***if "vector" in query_type.lower() and DATASOURCE_TYPE != "AzureMLIndex":
***REMOVED***embeddingDependency = {}
***REMOVED***if AZURE_OPENAI_EMBEDDING_NAME:
***REMOVED******REMOVED***embeddingDependency = {
***REMOVED******REMOVED***"type": "deployment_name",
***REMOVED******REMOVED***"deployment_name": AZURE_OPENAI_EMBEDDING_NAME,
***REMOVED***
***REMOVED***elif AZURE_OPENAI_EMBEDDING_ENDPOINT and AZURE_OPENAI_EMBEDDING_KEY:
***REMOVED******REMOVED***embeddingDependency = {
***REMOVED******REMOVED***"type": "endpoint",
***REMOVED******REMOVED***"endpoint": AZURE_OPENAI_EMBEDDING_ENDPOINT,
***REMOVED******REMOVED***"authentication": {
***REMOVED******REMOVED******REMOVED***"type": "api_key",
***REMOVED******REMOVED******REMOVED***"key": AZURE_OPENAI_EMBEDDING_KEY,
***REMOVED******REMOVED***,
***REMOVED***
***REMOVED***elif DATASOURCE_TYPE == "Elasticsearch" and ELASTICSEARCH_EMBEDDING_MODEL_ID:
***REMOVED******REMOVED***embeddingDependency = {
***REMOVED******REMOVED***"type": "model_id",
***REMOVED******REMOVED***"model_id": ELASTICSEARCH_EMBEDDING_MODEL_ID,
***REMOVED***
***REMOVED***else:
***REMOVED******REMOVED***raise Exception(
***REMOVED******REMOVED***f"Vector query type ({query_type}) is selected for data source type {DATASOURCE_TYPE} but no embedding dependency is configured"
***REMOVED******REMOVED***)
***REMOVED***data_source["parameters"]["embedding_dependency"] = embeddingDependency

***REMOVED***return data_source


def prepare_model_args(request_body):
***REMOVED***request_messages = request_body.get("messages", [])
***REMOVED***messages = []
***REMOVED***if not SHOULD_USE_DATA:
***REMOVED***messages = [{"role": "system", "content": AZURE_OPENAI_SYSTEM_MESSAGE}]

***REMOVED***for message in request_messages:
***REMOVED***if message:
***REMOVED******REMOVED***messages.append({"role": message["role"], "content": message["content"]})

***REMOVED***model_args = {
***REMOVED***"messages": messages,
***REMOVED***"temperature": float(AZURE_OPENAI_TEMPERATURE),
***REMOVED***"max_tokens": int(AZURE_OPENAI_MAX_TOKENS),
***REMOVED***"top_p": float(AZURE_OPENAI_TOP_P),
***REMOVED***"stop": (
***REMOVED******REMOVED***parse_multi_columns(AZURE_OPENAI_STOP_SEQUENCE)
***REMOVED******REMOVED***if AZURE_OPENAI_STOP_SEQUENCE
***REMOVED******REMOVED***else None
***REMOVED***),
***REMOVED***"stream": SHOULD_STREAM,
***REMOVED***"model": AZURE_OPENAI_MODEL,
***REMOVED***

***REMOVED***if SHOULD_USE_DATA:
***REMOVED***model_args["extra_body"] = {"data_sources": [get_configured_data_source()]}

***REMOVED***model_args_clean = copy.deepcopy(model_args)
***REMOVED***if model_args_clean.get("extra_body"):
***REMOVED***secret_params = [
***REMOVED******REMOVED***"key",
***REMOVED******REMOVED***"connection_string",
***REMOVED******REMOVED***"embedding_key",
***REMOVED******REMOVED***"encoded_api_key",
***REMOVED******REMOVED***"api_key",
***REMOVED***]
***REMOVED***for secret_param in secret_params:
***REMOVED******REMOVED***if model_args_clean["extra_body"]["data_sources"][0]["parameters"].get(
***REMOVED******REMOVED***secret_param
***REMOVED******REMOVED***):
***REMOVED******REMOVED***model_args_clean["extra_body"]["data_sources"][0]["parameters"][
***REMOVED******REMOVED******REMOVED***secret_param
***REMOVED******REMOVED***] = "*****"
***REMOVED***authentication = model_args_clean["extra_body"]["data_sources"][0][
***REMOVED******REMOVED***"parameters"
***REMOVED***].get("authentication", {})
***REMOVED***for field in authentication:
***REMOVED******REMOVED***if field in secret_params:
***REMOVED******REMOVED***model_args_clean["extra_body"]["data_sources"][0]["parameters"][
***REMOVED******REMOVED******REMOVED***"authentication"
***REMOVED******REMOVED***][field] = "*****"
***REMOVED***embeddingDependency = model_args_clean["extra_body"]["data_sources"][0][
***REMOVED******REMOVED***"parameters"
***REMOVED***].get("embedding_dependency", {})
***REMOVED***if "authentication" in embeddingDependency:
***REMOVED******REMOVED***for field in embeddingDependency["authentication"]:
***REMOVED******REMOVED***if field in secret_params:
***REMOVED******REMOVED******REMOVED***model_args_clean["extra_body"]["data_sources"][0]["parameters"][
***REMOVED******REMOVED******REMOVED***"embedding_dependency"
***REMOVED******REMOVED******REMOVED***]["authentication"][field] = "*****"

***REMOVED***logging.debug(f"REQUEST BODY: {json.dumps(model_args_clean, indent=4)}")

***REMOVED***return model_args


async def promptflow_request(request):
***REMOVED***try:
***REMOVED***headers = {
***REMOVED******REMOVED***"Content-Type": "application/json",
***REMOVED******REMOVED***"Authorization": f"Bearer {PROMPTFLOW_API_KEY}",
***REMOVED***
***REMOVED***# Adding timeout for scenarios where response takes longer to come back
***REMOVED***logging.debug(f"Setting timeout to {PROMPTFLOW_RESPONSE_TIMEOUT}")
***REMOVED***async with httpx.AsyncClient(
***REMOVED******REMOVED***timeout=float(PROMPTFLOW_RESPONSE_TIMEOUT)
***REMOVED***) as client:
***REMOVED******REMOVED***pf_formatted_obj = convert_to_pf_format(
***REMOVED******REMOVED***request, PROMPTFLOW_REQUEST_FIELD_NAME, PROMPTFLOW_RESPONSE_FIELD_NAME
***REMOVED******REMOVED***)
***REMOVED******REMOVED***# NOTE: This only support question and chat_history parameters
***REMOVED******REMOVED***# If you need to add more parameters, you need to modify the request body
***REMOVED******REMOVED***response = await client.post(
***REMOVED******REMOVED***PROMPTFLOW_ENDPOINT,
***REMOVED******REMOVED***json={
***REMOVED******REMOVED******REMOVED***f"{PROMPTFLOW_REQUEST_FIELD_NAME}": pf_formatted_obj[-1]["inputs"][
***REMOVED******REMOVED******REMOVED***PROMPTFLOW_REQUEST_FIELD_NAME
***REMOVED******REMOVED******REMOVED***],
***REMOVED******REMOVED******REMOVED***"chat_history": pf_formatted_obj[:-1],
***REMOVED******REMOVED***,
***REMOVED******REMOVED***headers=headers,
***REMOVED******REMOVED***)
***REMOVED***resp = response.json()
***REMOVED***resp["id"] = request["messages"][-1]["id"]
***REMOVED***return resp
***REMOVED***except Exception as e:
***REMOVED***logging.error(f"An error occurred while making promptflow_request: {e}")


async def send_chat_request(request):
***REMOVED***filtered_messages = [message for message in request['messages'] if message['role'] != 'tool']
***REMOVED***request['messages'] = filtered_messages
***REMOVED***model_args = prepare_model_args(request)

***REMOVED***try:
***REMOVED***azure_openai_client = init_openai_client()
***REMOVED***response = await azure_openai_client.chat.completions.create(**model_args)

***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in send_chat_request")
***REMOVED***raise e

***REMOVED***return response


async def complete_chat_request(request_body):
***REMOVED***if USE_PROMPTFLOW and PROMPTFLOW_ENDPOINT and PROMPTFLOW_API_KEY:
***REMOVED***response = await promptflow_request(request_body)
***REMOVED***history_metadata = request_body.get("history_metadata", {})
***REMOVED***return format_pf_non_streaming_response(
***REMOVED******REMOVED***response, history_metadata, PROMPTFLOW_RESPONSE_FIELD_NAME
***REMOVED***)
***REMOVED***else:
***REMOVED***response = await send_chat_request(request_body)
***REMOVED***history_metadata = request_body.get("history_metadata", {})
***REMOVED***return format_non_streaming_response(response, history_metadata)


async def stream_chat_request(request_body):
***REMOVED***response = await send_chat_request(request_body)
***REMOVED***history_metadata = request_body.get("history_metadata", {})

***REMOVED***async def generate():
***REMOVED***async for completionChunk in response:
***REMOVED******REMOVED***yield format_stream_response(completionChunk, history_metadata)

***REMOVED***return generate()


async def conversation_internal(request_body):
***REMOVED***try:
***REMOVED***if SHOULD_STREAM:
***REMOVED******REMOVED***result = await stream_chat_request(request_body)
***REMOVED******REMOVED***response = await make_response(format_as_ndjson(result))
***REMOVED******REMOVED***response.timeout = None
***REMOVED******REMOVED***response.mimetype = "application/json-lines"
***REMOVED******REMOVED***return response
***REMOVED***else:
***REMOVED******REMOVED***result = await complete_chat_request(request_body)
***REMOVED******REMOVED***return jsonify(result)

***REMOVED***except Exception as ex:
***REMOVED***logging.exception(ex)
***REMOVED***if hasattr(ex, "status_code"):
***REMOVED******REMOVED***return jsonify({"error": str(ex)}), ex.status_code
***REMOVED***else:
***REMOVED******REMOVED***return jsonify({"error": str(ex)}), 500


@bp.route("/conversation", methods=["POST"])
async def conversation():
***REMOVED***if not request.is_json:
***REMOVED***return jsonify({"error": "request must be json"}), 415
***REMOVED***request_json = await request.get_json()

***REMOVED***return await conversation_internal(request_json)


@bp.route("/frontend_settings", methods=["GET"])
def get_frontend_settings():
***REMOVED***try:
***REMOVED***return jsonify(frontend_settings), 200
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /frontend_settings")
***REMOVED***return jsonify({"error": str(e)}), 500


## Conversation History API ##
@bp.route("/history/generate", methods=["POST"])
async def add_conversation():
***REMOVED***authenticated_user = get_authenticated_user_details(request_headers=request.headers)
***REMOVED***user_id = authenticated_user["user_principal_id"]

***REMOVED***## check request for conversation_id
***REMOVED***request_json = await request.get_json()
***REMOVED***conversation_id = request_json.get("conversation_id", None)

***REMOVED***try:
***REMOVED***# make sure cosmos is configured
***REMOVED***cosmos_conversation_client = init_cosmosdb_client()
***REMOVED***if not cosmos_conversation_client:
***REMOVED******REMOVED***raise Exception("CosmosDB is not configured or not working")

***REMOVED***# check for the conversation_id, if the conversation is not set, we will create a new one
***REMOVED***history_metadata = {}
***REMOVED***if not conversation_id:
***REMOVED******REMOVED***title = await generate_title(request_json["messages"])
***REMOVED******REMOVED***conversation_dict = await cosmos_conversation_client.create_conversation(
***REMOVED******REMOVED***user_id=user_id, title=title
***REMOVED******REMOVED***)
***REMOVED******REMOVED***conversation_id = conversation_dict["id"]
***REMOVED******REMOVED***history_metadata["title"] = title
***REMOVED******REMOVED***history_metadata["date"] = conversation_dict["createdAt"]

***REMOVED***## Format the incoming message object in the "chat/completions" messages format
***REMOVED***## then write it to the conversation history in cosmos
***REMOVED***messages = request_json["messages"]
***REMOVED***if len(messages) > 0 and messages[-1]["role"] == "user":
***REMOVED******REMOVED***createdMessageValue = await cosmos_conversation_client.create_message(
***REMOVED******REMOVED***uuid=str(uuid.uuid4()),
***REMOVED******REMOVED***conversation_id=conversation_id,
***REMOVED******REMOVED***user_id=user_id,
***REMOVED******REMOVED***input_message=messages[-1],
***REMOVED******REMOVED***)
***REMOVED******REMOVED***if createdMessageValue == "Conversation not found":
***REMOVED******REMOVED***raise Exception(
***REMOVED******REMOVED******REMOVED***"Conversation not found for the given conversation ID: "
***REMOVED******REMOVED******REMOVED***+ conversation_id
***REMOVED******REMOVED******REMOVED***+ "."
***REMOVED******REMOVED***)
***REMOVED***else:
***REMOVED******REMOVED***raise Exception("No user message found")

***REMOVED***await cosmos_conversation_client.cosmosdb_client.close()

***REMOVED***# Submit request to Chat Completions for response
***REMOVED***request_body = await request.get_json()
***REMOVED***history_metadata["conversation_id"] = conversation_id
***REMOVED***request_body["history_metadata"] = history_metadata
***REMOVED***return await conversation_internal(request_body)

***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /history/generate")
***REMOVED***return jsonify({"error": str(e)}), 500


@bp.route("/history/update", methods=["POST"])
async def update_conversation():
***REMOVED***authenticated_user = get_authenticated_user_details(request_headers=request.headers)
***REMOVED***user_id = authenticated_user["user_principal_id"]

***REMOVED***## check request for conversation_id
***REMOVED***request_json = await request.get_json()
***REMOVED***conversation_id = request_json.get("conversation_id", None)

***REMOVED***try:
***REMOVED***# make sure cosmos is configured
***REMOVED***cosmos_conversation_client = init_cosmosdb_client()
***REMOVED***if not cosmos_conversation_client:
***REMOVED******REMOVED***raise Exception("CosmosDB is not configured or not working")

***REMOVED***# check for the conversation_id, if the conversation is not set, we will create a new one
***REMOVED***if not conversation_id:
***REMOVED******REMOVED***raise Exception("No conversation_id found")

***REMOVED***## Format the incoming message object in the "chat/completions" messages format
***REMOVED***## then write it to the conversation history in cosmos
***REMOVED***messages = request_json["messages"]
***REMOVED***if len(messages) > 0 and messages[-1]["role"] == "assistant":
***REMOVED******REMOVED***if len(messages) > 1 and messages[-2].get("role", None) == "tool":
***REMOVED******REMOVED***# write the tool message first
***REMOVED******REMOVED***await cosmos_conversation_client.create_message(
***REMOVED******REMOVED******REMOVED***uuid=str(uuid.uuid4()),
***REMOVED******REMOVED******REMOVED***conversation_id=conversation_id,
***REMOVED******REMOVED******REMOVED***user_id=user_id,
***REMOVED******REMOVED******REMOVED***input_message=messages[-2],
***REMOVED******REMOVED***)
***REMOVED******REMOVED***# write the assistant message
***REMOVED******REMOVED***await cosmos_conversation_client.create_message(
***REMOVED******REMOVED***uuid=messages[-1]["id"],
***REMOVED******REMOVED***conversation_id=conversation_id,
***REMOVED******REMOVED***user_id=user_id,
***REMOVED******REMOVED***input_message=messages[-1],
***REMOVED******REMOVED***)
***REMOVED***else:
***REMOVED******REMOVED***raise Exception("No bot messages found")

***REMOVED***# Submit request to Chat Completions for response
***REMOVED***await cosmos_conversation_client.cosmosdb_client.close()
***REMOVED***response = {"success": True}
***REMOVED***return jsonify(response), 200

***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /history/update")
***REMOVED***return jsonify({"error": str(e)}), 500


@bp.route("/history/message_feedback", methods=["POST"])
async def update_message():
***REMOVED***authenticated_user = get_authenticated_user_details(request_headers=request.headers)
***REMOVED***user_id = authenticated_user["user_principal_id"]
***REMOVED***cosmos_conversation_client = init_cosmosdb_client()

***REMOVED***## check request for message_id
***REMOVED***request_json = await request.get_json()
***REMOVED***message_id = request_json.get("message_id", None)
***REMOVED***message_feedback = request_json.get("message_feedback", None)
***REMOVED***try:
***REMOVED***if not message_id:
***REMOVED******REMOVED***return jsonify({"error": "message_id is required"}), 400

***REMOVED***if not message_feedback:
***REMOVED******REMOVED***return jsonify({"error": "message_feedback is required"}), 400

***REMOVED***## update the message in cosmos
***REMOVED***updated_message = await cosmos_conversation_client.update_message_feedback(
***REMOVED******REMOVED***user_id, message_id, message_feedback
***REMOVED***)
***REMOVED***if updated_message:
***REMOVED******REMOVED***return (
***REMOVED******REMOVED***jsonify(
***REMOVED******REMOVED******REMOVED***{
***REMOVED******REMOVED******REMOVED***"message": f"Successfully updated message with feedback {message_feedback}",
***REMOVED******REMOVED******REMOVED***"message_id": message_id,
***REMOVED******REMOVED***
***REMOVED******REMOVED***),
***REMOVED******REMOVED***200,
***REMOVED******REMOVED***)
***REMOVED***else:
***REMOVED******REMOVED***return (
***REMOVED******REMOVED***jsonify(
***REMOVED******REMOVED******REMOVED***{
***REMOVED******REMOVED******REMOVED***"error": f"Unable to update message {message_id}. It either does not exist or the user does not have access to it."
***REMOVED******REMOVED***
***REMOVED******REMOVED***),
***REMOVED******REMOVED***404,
***REMOVED******REMOVED***)

***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /history/message_feedback")
***REMOVED***return jsonify({"error": str(e)}), 500


@bp.route("/history/delete", methods=["DELETE"])
async def delete_conversation():
***REMOVED***## get the user id from the request headers
***REMOVED***authenticated_user = get_authenticated_user_details(request_headers=request.headers)
***REMOVED***user_id = authenticated_user["user_principal_id"]

***REMOVED***## check request for conversation_id
***REMOVED***request_json = await request.get_json()
***REMOVED***conversation_id = request_json.get("conversation_id", None)

***REMOVED***try:
***REMOVED***if not conversation_id:
***REMOVED******REMOVED***return jsonify({"error": "conversation_id is required"}), 400

***REMOVED***## make sure cosmos is configured
***REMOVED***cosmos_conversation_client = init_cosmosdb_client()
***REMOVED***if not cosmos_conversation_client:
***REMOVED******REMOVED***raise Exception("CosmosDB is not configured or not working")

***REMOVED***## delete the conversation messages from cosmos first
***REMOVED***deleted_messages = await cosmos_conversation_client.delete_messages(
***REMOVED******REMOVED***conversation_id, user_id
***REMOVED***)

***REMOVED***## Now delete the conversation
***REMOVED***deleted_conversation = await cosmos_conversation_client.delete_conversation(
***REMOVED******REMOVED***user_id, conversation_id
***REMOVED***)

***REMOVED***await cosmos_conversation_client.cosmosdb_client.close()

***REMOVED***return (
***REMOVED******REMOVED***jsonify(
***REMOVED******REMOVED***{
***REMOVED******REMOVED******REMOVED***"message": "Successfully deleted conversation and messages",
***REMOVED******REMOVED******REMOVED***"conversation_id": conversation_id,
***REMOVED******REMOVED***
***REMOVED******REMOVED***),
***REMOVED******REMOVED***200,
***REMOVED***)
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /history/delete")
***REMOVED***return jsonify({"error": str(e)}), 500


@bp.route("/history/list", methods=["GET"])
async def list_conversations():
***REMOVED***offset = request.args.get("offset", 0)
***REMOVED***authenticated_user = get_authenticated_user_details(request_headers=request.headers)
***REMOVED***user_id = authenticated_user["user_principal_id"]

***REMOVED***## make sure cosmos is configured
***REMOVED***cosmos_conversation_client = init_cosmosdb_client()
***REMOVED***if not cosmos_conversation_client:
***REMOVED***raise Exception("CosmosDB is not configured or not working")

***REMOVED***## get the conversations from cosmos
***REMOVED***conversations = await cosmos_conversation_client.get_conversations(
***REMOVED***user_id, offset=offset, limit=25
***REMOVED***)
***REMOVED***await cosmos_conversation_client.cosmosdb_client.close()
***REMOVED***if not isinstance(conversations, list):
***REMOVED***return jsonify({"error": f"No conversations for {user_id} were found"}), 404

***REMOVED***## return the conversation ids

***REMOVED***return jsonify(conversations), 200


@bp.route("/history/read", methods=["POST"])
async def get_conversation():
***REMOVED***authenticated_user = get_authenticated_user_details(request_headers=request.headers)
***REMOVED***user_id = authenticated_user["user_principal_id"]

***REMOVED***## check request for conversation_id
***REMOVED***request_json = await request.get_json()
***REMOVED***conversation_id = request_json.get("conversation_id", None)

***REMOVED***if not conversation_id:
***REMOVED***return jsonify({"error": "conversation_id is required"}), 400

***REMOVED***## make sure cosmos is configured
***REMOVED***cosmos_conversation_client = init_cosmosdb_client()
***REMOVED***if not cosmos_conversation_client:
***REMOVED***raise Exception("CosmosDB is not configured or not working")

***REMOVED***## get the conversation object and the related messages from cosmos
***REMOVED***conversation = await cosmos_conversation_client.get_conversation(
***REMOVED***user_id, conversation_id
***REMOVED***)
***REMOVED***## return the conversation id and the messages in the bot frontend format
***REMOVED***if not conversation:
***REMOVED***return (
***REMOVED******REMOVED***jsonify(
***REMOVED******REMOVED***{
***REMOVED******REMOVED******REMOVED***"error": f"Conversation {conversation_id} was not found. It either does not exist or the logged in user does not have access to it."
***REMOVED******REMOVED***
***REMOVED******REMOVED***),
***REMOVED******REMOVED***404,
***REMOVED***)

***REMOVED***# get the messages for the conversation from cosmos
***REMOVED***conversation_messages = await cosmos_conversation_client.get_messages(
***REMOVED***user_id, conversation_id
***REMOVED***)

***REMOVED***## format the messages in the bot frontend format
***REMOVED***messages = [
***REMOVED***{
***REMOVED******REMOVED***"id": msg["id"],
***REMOVED******REMOVED***"role": msg["role"],
***REMOVED******REMOVED***"content": msg["content"],
***REMOVED******REMOVED***"createdAt": msg["createdAt"],
***REMOVED******REMOVED***"feedback": msg.get("feedback"),
***REMOVED***
***REMOVED***for msg in conversation_messages
***REMOVED***]

***REMOVED***await cosmos_conversation_client.cosmosdb_client.close()
***REMOVED***return jsonify({"conversation_id": conversation_id, "messages": messages}), 200


@bp.route("/history/rename", methods=["POST"])
async def rename_conversation():
***REMOVED***authenticated_user = get_authenticated_user_details(request_headers=request.headers)
***REMOVED***user_id = authenticated_user["user_principal_id"]

***REMOVED***## check request for conversation_id
***REMOVED***request_json = await request.get_json()
***REMOVED***conversation_id = request_json.get("conversation_id", None)

***REMOVED***if not conversation_id:
***REMOVED***return jsonify({"error": "conversation_id is required"}), 400

***REMOVED***## make sure cosmos is configured
***REMOVED***cosmos_conversation_client = init_cosmosdb_client()
***REMOVED***if not cosmos_conversation_client:
***REMOVED***raise Exception("CosmosDB is not configured or not working")

***REMOVED***## get the conversation from cosmos
***REMOVED***conversation = await cosmos_conversation_client.get_conversation(
***REMOVED***user_id, conversation_id
***REMOVED***)
***REMOVED***if not conversation:
***REMOVED***return (
***REMOVED******REMOVED***jsonify(
***REMOVED******REMOVED***{
***REMOVED******REMOVED******REMOVED***"error": f"Conversation {conversation_id} was not found. It either does not exist or the logged in user does not have access to it."
***REMOVED******REMOVED***
***REMOVED******REMOVED***),
***REMOVED******REMOVED***404,
***REMOVED***)

***REMOVED***## update the title
***REMOVED***title = request_json.get("title", None)
***REMOVED***if not title:
***REMOVED***return jsonify({"error": "title is required"}), 400
***REMOVED***conversation["title"] = title
***REMOVED***updated_conversation = await cosmos_conversation_client.upsert_conversation(
***REMOVED***conversation
***REMOVED***)

***REMOVED***await cosmos_conversation_client.cosmosdb_client.close()
***REMOVED***return jsonify(updated_conversation), 200


@bp.route("/history/delete_all", methods=["DELETE"])
async def delete_all_conversations():
***REMOVED***## get the user id from the request headers
***REMOVED***authenticated_user = get_authenticated_user_details(request_headers=request.headers)
***REMOVED***user_id = authenticated_user["user_principal_id"]

***REMOVED***# get conversations for user
***REMOVED***try:
***REMOVED***## make sure cosmos is configured
***REMOVED***cosmos_conversation_client = init_cosmosdb_client()
***REMOVED***if not cosmos_conversation_client:
***REMOVED******REMOVED***raise Exception("CosmosDB is not configured or not working")

***REMOVED***conversations = await cosmos_conversation_client.get_conversations(
***REMOVED******REMOVED***user_id, offset=0, limit=None
***REMOVED***)
***REMOVED***if not conversations:
***REMOVED******REMOVED***return jsonify({"error": f"No conversations for {user_id} were found"}), 404

***REMOVED***# delete each conversation
***REMOVED***for conversation in conversations:
***REMOVED******REMOVED***## delete the conversation messages from cosmos first
***REMOVED******REMOVED***deleted_messages = await cosmos_conversation_client.delete_messages(
***REMOVED******REMOVED***conversation["id"], user_id
***REMOVED******REMOVED***)

***REMOVED******REMOVED***## Now delete the conversation
***REMOVED******REMOVED***deleted_conversation = await cosmos_conversation_client.delete_conversation(
***REMOVED******REMOVED***user_id, conversation["id"]
***REMOVED******REMOVED***)
***REMOVED***await cosmos_conversation_client.cosmosdb_client.close()
***REMOVED***return (
***REMOVED******REMOVED***jsonify(
***REMOVED******REMOVED***{
***REMOVED******REMOVED******REMOVED***"message": f"Successfully deleted conversation and messages for user {user_id}"
***REMOVED******REMOVED***
***REMOVED******REMOVED***),
***REMOVED******REMOVED***200,
***REMOVED***)

***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /history/delete_all")
***REMOVED***return jsonify({"error": str(e)}), 500


@bp.route("/history/clear", methods=["POST"])
async def clear_messages():
***REMOVED***## get the user id from the request headers
***REMOVED***authenticated_user = get_authenticated_user_details(request_headers=request.headers)
***REMOVED***user_id = authenticated_user["user_principal_id"]

***REMOVED***## check request for conversation_id
***REMOVED***request_json = await request.get_json()
***REMOVED***conversation_id = request_json.get("conversation_id", None)

***REMOVED***try:
***REMOVED***if not conversation_id:
***REMOVED******REMOVED***return jsonify({"error": "conversation_id is required"}), 400

***REMOVED***## make sure cosmos is configured
***REMOVED***cosmos_conversation_client = init_cosmosdb_client()
***REMOVED***if not cosmos_conversation_client:
***REMOVED******REMOVED***raise Exception("CosmosDB is not configured or not working")

***REMOVED***## delete the conversation messages from cosmos
***REMOVED***deleted_messages = await cosmos_conversation_client.delete_messages(
***REMOVED******REMOVED***conversation_id, user_id
***REMOVED***)

***REMOVED***return (
***REMOVED******REMOVED***jsonify(
***REMOVED******REMOVED***{
***REMOVED******REMOVED******REMOVED***"message": "Successfully deleted messages in conversation",
***REMOVED******REMOVED******REMOVED***"conversation_id": conversation_id,
***REMOVED******REMOVED***
***REMOVED******REMOVED***),
***REMOVED******REMOVED***200,
***REMOVED***)
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /history/clear_messages")
***REMOVED***return jsonify({"error": str(e)}), 500


@bp.route("/history/ensure", methods=["GET"])
async def ensure_cosmos():
***REMOVED***if not AZURE_COSMOSDB_ACCOUNT:
***REMOVED***return jsonify({"error": "CosmosDB is not configured"}), 404

***REMOVED***try:
***REMOVED***cosmos_conversation_client = init_cosmosdb_client()
***REMOVED***success, err = await cosmos_conversation_client.ensure()
***REMOVED***if not cosmos_conversation_client or not success:
***REMOVED******REMOVED***if err:
***REMOVED******REMOVED***return jsonify({"error": err}), 422
***REMOVED******REMOVED***return jsonify({"error": "CosmosDB is not configured or not working"}), 500

***REMOVED***await cosmos_conversation_client.cosmosdb_client.close()
***REMOVED***return jsonify({"message": "CosmosDB is configured and working"}), 200
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /history/ensure")
***REMOVED***cosmos_exception = str(e)
***REMOVED***if "Invalid credentials" in cosmos_exception:
***REMOVED******REMOVED***return jsonify({"error": cosmos_exception}), 401
***REMOVED***elif "Invalid CosmosDB database name" in cosmos_exception:
***REMOVED******REMOVED***return (
***REMOVED******REMOVED***jsonify(
***REMOVED******REMOVED******REMOVED***{
***REMOVED******REMOVED******REMOVED***"error": f"{cosmos_exception} {AZURE_COSMOSDB_DATABASE} for account {AZURE_COSMOSDB_ACCOUNT}"
***REMOVED******REMOVED***
***REMOVED******REMOVED***),
***REMOVED******REMOVED***422,
***REMOVED******REMOVED***)
***REMOVED***elif "Invalid CosmosDB container name" in cosmos_exception:
***REMOVED******REMOVED***return (
***REMOVED******REMOVED***jsonify(
***REMOVED******REMOVED******REMOVED***{
***REMOVED******REMOVED******REMOVED***"error": f"{cosmos_exception}: {AZURE_COSMOSDB_CONVERSATIONS_CONTAINER}"
***REMOVED******REMOVED***
***REMOVED******REMOVED***),
***REMOVED******REMOVED***422,
***REMOVED******REMOVED***)
***REMOVED***else:
***REMOVED******REMOVED***return jsonify({"error": "CosmosDB is not working"}), 500


async def generate_title(conversation_messages):
***REMOVED***## make sure the messages are sorted by _ts descending
***REMOVED***title_prompt = 'Summarize the conversation so far into a 4-word or less title. Do not use any quotation marks or punctuation. Respond with a json object in the format {{"title": string}}. Do not include any other commentary or description.'

***REMOVED***messages = [
***REMOVED***{"role": msg["role"], "content": msg["content"]}
***REMOVED***for msg in conversation_messages
***REMOVED***]
***REMOVED***messages.append({"role": "user", "content": title_prompt})

***REMOVED***try:
***REMOVED***azure_openai_client = init_openai_client(use_data=False)
***REMOVED***response = await azure_openai_client.chat.completions.create(
***REMOVED******REMOVED***model=AZURE_OPENAI_MODEL, messages=messages, temperature=1, max_tokens=64
***REMOVED***)

***REMOVED***title = json.loads(response.choices[0].message.content)["title"]
***REMOVED***return title
***REMOVED***except Exception as e:
***REMOVED***return messages[-2]["content"]


app = create_app()
