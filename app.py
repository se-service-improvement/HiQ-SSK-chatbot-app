import json
import os
import logging
import requests
import openai
from azure.identity import DefaultAzureCredential
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


# ACS Integration Settings
AZURE_SEARCH_SERVICE = os.environ.get("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX")
AZURE_SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY")
AZURE_SEARCH_USE_SEMANTIC_SEARCH = os.environ.get("AZURE_SEARCH_USE_SEMANTIC_SEARCH", "false")
AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG = os.environ.get("AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG", "default")
AZURE_SEARCH_TOP_K = os.environ.get("AZURE_SEARCH_TOP_K", 5)
AZURE_SEARCH_ENABLE_IN_DOMAIN = os.environ.get("AZURE_SEARCH_ENABLE_IN_DOMAIN", "true")
AZURE_SEARCH_CONTENT_COLUMNS = os.environ.get("AZURE_SEARCH_CONTENT_COLUMNS")
AZURE_SEARCH_FILENAME_COLUMN = os.environ.get("AZURE_SEARCH_FILENAME_COLUMN")
AZURE_SEARCH_TITLE_COLUMN = os.environ.get("AZURE_SEARCH_TITLE_COLUMN")
AZURE_SEARCH_URL_COLUMN = os.environ.get("AZURE_SEARCH_URL_COLUMN")
AZURE_SEARCH_VECTOR_COLUMNS = os.environ.get("AZURE_SEARCH_VECTOR_COLUMNS")
AZURE_SEARCH_QUERY_TYPE = os.environ.get("AZURE_SEARCH_QUERY_TYPE")
AZURE_SEARCH_PERMITTED_GROUPS_COLUMN = os.environ.get("AZURE_SEARCH_PERMITTED_GROUPS_COLUMN")
AZURE_SEARCH_STRICTNESS = os.environ.get("AZURE_SEARCH_STRICTNESS", 3)

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
AZURE_OPENAI_PREVIEW_API_VERSION = os.environ.get("AZURE_OPENAI_PREVIEW_API_VERSION", "2023-06-01-preview")
AZURE_OPENAI_STREAM = os.environ.get("AZURE_OPENAI_STREAM", "true")
AZURE_OPENAI_MODEL_NAME = os.environ.get("AZURE_OPENAI_MODEL_NAME", "gpt-35-turbo-16k") # Name of the model, e.g. 'gpt-35-turbo-16k' or 'gpt-4'
AZURE_OPENAI_EMBEDDING_ENDPOINT = os.environ.get("AZURE_OPENAI_EMBEDDING_ENDPOINT")
AZURE_OPENAI_EMBEDDING_KEY = os.environ.get("AZURE_OPENAI_EMBEDDING_KEY")


SHOULD_STREAM = True if AZURE_OPENAI_STREAM.lower() == "true" else False

# CosmosDB Integration Settings
AZURE_COSMOSDB_DATABASE = os.environ.get("AZURE_COSMOSDB_DATABASE")
AZURE_COSMOSDB_ACCOUNT = os.environ.get("AZURE_COSMOSDB_ACCOUNT")
AZURE_COSMOSDB_CONVERSATIONS_CONTAINER = os.environ.get("AZURE_COSMOSDB_CONVERSATIONS_CONTAINER")
AZURE_COSMOSDB_ACCOUNT_KEY = os.environ.get("AZURE_COSMOSDB_ACCOUNT_KEY")

# Initialize a CosmosDB client with AAD auth and containers
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
***REMOVED******REMOVED***container_name=AZURE_COSMOSDB_CONVERSATIONS_CONTAINER
***REMOVED***)
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in CosmosDB initialization", e)
***REMOVED***cosmos_conversation_client = None


def is_chat_model():
***REMOVED***if 'gpt-4' in AZURE_OPENAI_MODEL_NAME.lower() or AZURE_OPENAI_MODEL_NAME.lower() in ['gpt-35-turbo-4k', 'gpt-35-turbo-16k']:
***REMOVED***return True
***REMOVED***return False

def should_use_data():
***REMOVED***if AZURE_SEARCH_SERVICE and AZURE_SEARCH_INDEX and AZURE_SEARCH_KEY:
***REMOVED***return True
***REMOVED***return False


def format_as_ndjson(obj: dict) -> str:
***REMOVED***return json.dumps(obj, ensure_ascii=False) + "\n"

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
***REMOVED******REMOVED***return []
***REMOVED***
***REMOVED***r = r.json()
***REMOVED***if "@odata.nextLink" in r:
***REMOVED******REMOVED***nextLinkData = fetchUserGroups(userToken, r["@odata.nextLink"])
***REMOVED******REMOVED***r['value'].extend(nextLinkData)
***REMOVED***
***REMOVED***return r['value']
***REMOVED***except Exception as e:
***REMOVED***return []


def generateFilterString(userToken):
***REMOVED***# Get list of groups user is a member of
***REMOVED***userGroups = fetchUserGroups(userToken)

***REMOVED***# Construct filter string
***REMOVED***if userGroups:
***REMOVED***group_ids = ", ".join([obj['id'] for obj in userGroups])
***REMOVED***return f"{AZURE_SEARCH_PERMITTED_GROUPS_COLUMN}/any(g:search.in(g, '{group_ids}'))"
***REMOVED***
***REMOVED***return None


def prepare_body_headers_with_data(request):
***REMOVED***request_messages = request.json["messages"]

***REMOVED***# Set query type
***REMOVED***query_type = "simple"
***REMOVED***if AZURE_SEARCH_QUERY_TYPE:
***REMOVED***query_type = AZURE_SEARCH_QUERY_TYPE
***REMOVED***elif AZURE_SEARCH_USE_SEMANTIC_SEARCH.lower() == "true" and AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG:
***REMOVED***query_type = "semantic"

***REMOVED***# Set filter
***REMOVED***filter = None
***REMOVED***userToken = None
***REMOVED***if AZURE_SEARCH_PERMITTED_GROUPS_COLUMN:
***REMOVED***userToken = request.headers.get('X-MS-TOKEN-AAD-ACCESS-TOKEN', "")
***REMOVED***filter = generateFilterString(userToken)

***REMOVED***body = {
***REMOVED***"messages": request_messages,
***REMOVED***"temperature": float(AZURE_OPENAI_TEMPERATURE),
***REMOVED***"max_tokens": int(AZURE_OPENAI_MAX_TOKENS),
***REMOVED***"top_p": float(AZURE_OPENAI_TOP_P),
***REMOVED***"stop": AZURE_OPENAI_STOP_SEQUENCE.split("|") if AZURE_OPENAI_STOP_SEQUENCE else None,
***REMOVED***"stream": SHOULD_STREAM,
***REMOVED***"dataSources": [
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"type": "AzureCognitiveSearch",
***REMOVED******REMOVED***"parameters": {
***REMOVED******REMOVED******REMOVED***"endpoint": f"https://{AZURE_SEARCH_SERVICE}.search.windows.net",
***REMOVED******REMOVED******REMOVED***"key": AZURE_SEARCH_KEY,
***REMOVED******REMOVED******REMOVED***"indexName": AZURE_SEARCH_INDEX,
***REMOVED******REMOVED******REMOVED***"fieldsMapping": {
***REMOVED******REMOVED******REMOVED***"contentFields": AZURE_SEARCH_CONTENT_COLUMNS.split("|") if AZURE_SEARCH_CONTENT_COLUMNS else [],
***REMOVED******REMOVED******REMOVED***"titleField": AZURE_SEARCH_TITLE_COLUMN if AZURE_SEARCH_TITLE_COLUMN else None,
***REMOVED******REMOVED******REMOVED***"urlField": AZURE_SEARCH_URL_COLUMN if AZURE_SEARCH_URL_COLUMN else None,
***REMOVED******REMOVED******REMOVED***"filepathField": AZURE_SEARCH_FILENAME_COLUMN if AZURE_SEARCH_FILENAME_COLUMN else None,
***REMOVED******REMOVED******REMOVED***"vectorFields": AZURE_SEARCH_VECTOR_COLUMNS.split("|") if AZURE_SEARCH_VECTOR_COLUMNS else []
***REMOVED******REMOVED***,
***REMOVED******REMOVED******REMOVED***"inScope": True if AZURE_SEARCH_ENABLE_IN_DOMAIN.lower() == "true" else False,
***REMOVED******REMOVED******REMOVED***"topNDocuments": AZURE_SEARCH_TOP_K,
***REMOVED******REMOVED******REMOVED***"queryType": query_type,
***REMOVED******REMOVED******REMOVED***"semanticConfiguration": AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG if AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG else "",
***REMOVED******REMOVED******REMOVED***"roleInformation": AZURE_OPENAI_SYSTEM_MESSAGE,
***REMOVED******REMOVED******REMOVED***"embeddingEndpoint": AZURE_OPENAI_EMBEDDING_ENDPOINT,
***REMOVED******REMOVED******REMOVED***"embeddingKey": AZURE_OPENAI_EMBEDDING_KEY,
***REMOVED******REMOVED******REMOVED***"filter": filter,
***REMOVED******REMOVED******REMOVED***"strictness": int(AZURE_SEARCH_STRICTNESS)
***REMOVED******REMOVED***
***REMOVED***
***REMOVED***]
***REMOVED***

***REMOVED***headers = {
***REMOVED***'Content-Type': 'application/json',
***REMOVED***'api-key': AZURE_OPENAI_KEY,
***REMOVED***"x-ms-useragent": "GitHubSampleWebApp/PublicAPI/2.0.0"
***REMOVED***

***REMOVED***return body, headers


def stream_with_data(body, headers, endpoint, history_metadata={}):
***REMOVED***s = requests.Session()
***REMOVED***response = {
***REMOVED***"id": "",
***REMOVED***"model": "",
***REMOVED***"created": 0,
***REMOVED***"object": "",
***REMOVED***"choices": [{
***REMOVED******REMOVED***"messages": []
***REMOVED***],
***REMOVED***'history_metadata': history_metadata
***REMOVED***
***REMOVED***try:
***REMOVED***with s.post(endpoint, json=body, headers=headers, stream=True) as r:
***REMOVED******REMOVED***for line in r.iter_lines(chunk_size=10):
***REMOVED******REMOVED***if line:
***REMOVED******REMOVED******REMOVED***lineJson = json.loads(line.lstrip(b'data:').decode('utf-8'))
***REMOVED******REMOVED******REMOVED***if 'error' in lineJson:
***REMOVED******REMOVED******REMOVED***yield format_as_ndjson(lineJson)
***REMOVED******REMOVED******REMOVED***response["id"] = lineJson["id"]
***REMOVED******REMOVED******REMOVED***response["model"] = lineJson["model"]
***REMOVED******REMOVED******REMOVED***response["created"] = lineJson["created"]
***REMOVED******REMOVED******REMOVED***response["object"] = lineJson["object"]

***REMOVED******REMOVED******REMOVED***role = lineJson["choices"][0]["messages"][0]["delta"].get("role")
***REMOVED******REMOVED******REMOVED***if role == "tool":
***REMOVED******REMOVED******REMOVED***response["choices"][0]["messages"].append(lineJson["choices"][0]["messages"][0]["delta"])
***REMOVED******REMOVED******REMOVED***elif role == "assistant": 
***REMOVED******REMOVED******REMOVED***response["choices"][0]["messages"].append({
***REMOVED******REMOVED******REMOVED******REMOVED***"role": "assistant",
***REMOVED******REMOVED******REMOVED******REMOVED***"content": ""
***REMOVED******REMOVED******REMOVED***)
***REMOVED******REMOVED******REMOVED***else:
***REMOVED******REMOVED******REMOVED***deltaText = lineJson["choices"][0]["messages"][0]["delta"]["content"]
***REMOVED******REMOVED******REMOVED***if deltaText != "[DONE]":
***REMOVED******REMOVED******REMOVED******REMOVED***response["choices"][0]["messages"][1]["content"] += deltaText

***REMOVED******REMOVED******REMOVED***yield format_as_ndjson(response)
***REMOVED***except Exception as e:
***REMOVED***yield format_as_ndjson({"error": str(e)})


def conversation_with_data(request_body):
***REMOVED***body, headers = prepare_body_headers_with_data(request)
***REMOVED***base_url = AZURE_OPENAI_ENDPOINT if AZURE_OPENAI_ENDPOINT else f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/"
***REMOVED***endpoint = f"{base_url}openai/deployments/{AZURE_OPENAI_MODEL}/extensions/chat/completions?api-version={AZURE_OPENAI_PREVIEW_API_VERSION}"
***REMOVED***history_metadata = request_body.get("history_metadata", {})

***REMOVED***if not SHOULD_STREAM:
***REMOVED***r = requests.post(endpoint, headers=headers, json=body)
***REMOVED***status_code = r.status_code
***REMOVED***r = r.json()
***REMOVED***r['history_metadata'] = history_metadata

***REMOVED***return Response(format_as_ndjson(r), status=status_code)
***REMOVED***else:
***REMOVED***return Response(stream_with_data(body, headers, endpoint, history_metadata), mimetype='text/event-stream')


def stream_without_data(response, history_metadata={}):
***REMOVED***responseText = ""
***REMOVED***for line in response:
***REMOVED***deltaText = line["choices"][0]["delta"].get('content')
***REMOVED***if deltaText and deltaText != "[DONE]":
***REMOVED******REMOVED***responseText += deltaText

***REMOVED***response_obj = {
***REMOVED******REMOVED***"id": line["id"],
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
***REMOVED***openai.api_version = "2023-03-15-preview"
***REMOVED***openai.api_key = AZURE_OPENAI_KEY

***REMOVED***request_messages = request_body["messages"]
***REMOVED***messages = [
***REMOVED***{
***REMOVED******REMOVED***"role": "system",
***REMOVED******REMOVED***"content": AZURE_OPENAI_SYSTEM_MESSAGE
***REMOVED***
***REMOVED***]

***REMOVED***for message in request_messages:
***REMOVED***messages.append({
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
***REMOVED******REMOVED***"id": response,
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
***REMOVED******REMOVED***cosmos_conversation_client.create_message(
***REMOVED******REMOVED***conversation_id=conversation_id,
***REMOVED******REMOVED***user_id=user_id,
***REMOVED******REMOVED***input_message=messages[-1]
***REMOVED******REMOVED***)
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
***REMOVED******REMOVED***if len(messages) > 1 and messages[-2]['role'] == "tool":
***REMOVED******REMOVED***# write the tool message first
***REMOVED******REMOVED***cosmos_conversation_client.create_message(
***REMOVED******REMOVED******REMOVED***conversation_id=conversation_id,
***REMOVED******REMOVED******REMOVED***user_id=user_id,
***REMOVED******REMOVED******REMOVED***input_message=messages[-2]
***REMOVED******REMOVED***)
***REMOVED******REMOVED***# write the assistant message
***REMOVED******REMOVED***cosmos_conversation_client.create_message(
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
***REMOVED***authenticated_user = get_authenticated_user_details(request_headers=request.headers)
***REMOVED***user_id = authenticated_user['user_principal_id']

***REMOVED***## get the conversations from cosmos
***REMOVED***conversations = cosmos_conversation_client.get_conversations(user_id)
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
***REMOVED***messages = [{'id': msg['id'], 'role': msg['role'], 'content': msg['content'], 'createdAt': msg['createdAt']} for msg in conversation_messages]

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
***REMOVED***conversations = cosmos_conversation_client.get_conversations(user_id)
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
***REMOVED***return jsonify({"error": "CosmosDB is not working"}), 500

***REMOVED***return jsonify({"message": "CosmosDB is configured and working"}), 200


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
