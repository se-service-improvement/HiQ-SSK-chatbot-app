import copy
import json
import os
import logging
import uuid
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
from azure.identity.aio import (
***REMOVED***DefaultAzureCredential,
***REMOVED***get_bearer_token_provider
)
from backend.auth.auth_utils import get_authenticated_user_details
from backend.security.ms_defender_utils import get_msdefender_user_json
from backend.history.cosmosdbservice import CosmosConversationClient
from backend.settings import (
***REMOVED***app_settings,
***REMOVED***MINIMUM_SUPPORTED_AZURE_OPENAI_PREVIEW_API_VERSION
)
from backend.utils import (
***REMOVED***format_as_ndjson,
***REMOVED***format_stream_response,
***REMOVED***format_non_streaming_response,
***REMOVED***convert_to_pf_format,
***REMOVED***format_pf_non_streaming_response,
)

bp = Blueprint("routes", __name__, static_folder="static", template_folder="static")


def create_app():
***REMOVED***app = Quart(__name__)
***REMOVED***app.register_blueprint(bp)
***REMOVED***app.config["TEMPLATES_AUTO_RELOAD"] = True
***REMOVED***return app


@bp.route("/")
async def index():
***REMOVED***return await render_template(
***REMOVED***"index.html",
***REMOVED***title=app_settings.ui.title,
***REMOVED***favicon=app_settings.ui.favicon
***REMOVED***)


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


# Frontend Settings via Environment Variables
frontend_settings = {
***REMOVED***"auth_enabled": app_settings.base_settings.auth_enabled,
***REMOVED***"feedback_enabled": (
***REMOVED***app_settings.chat_history and
***REMOVED***app_settings.chat_history.enable_feedback
***REMOVED***),
***REMOVED***"ui": {
***REMOVED***"title": app_settings.ui.title,
***REMOVED***"logo": app_settings.ui.logo,
***REMOVED***"chat_logo": app_settings.ui.chat_logo or app_settings.ui.logo,
***REMOVED***"chat_title": app_settings.ui.chat_title,
***REMOVED***"chat_description": app_settings.ui.chat_description,
***REMOVED***"show_share_button": app_settings.ui.show_share_button,
***REMOVED***,
***REMOVED***"sanitize_answer": app_settings.base_settings.sanitize_answer,
}
# Enable Microsoft Defender for Cloud Integration
MS_DEFENDER_ENABLED = os.environ.get("MS_DEFENDER_ENABLED", "true").lower() == "true"

# Initialize Azure OpenAI Client
def init_openai_client():
***REMOVED***azure_openai_client = None
***REMOVED***try:
***REMOVED***# API version check
***REMOVED***if (
***REMOVED******REMOVED***app_settings.azure_openai.preview_api_version
***REMOVED******REMOVED***< MINIMUM_SUPPORTED_AZURE_OPENAI_PREVIEW_API_VERSION
***REMOVED***):
***REMOVED******REMOVED***raise ValueError(
***REMOVED******REMOVED***f"The minimum supported Azure OpenAI preview API version is '{MINIMUM_SUPPORTED_AZURE_OPENAI_PREVIEW_API_VERSION}'"
***REMOVED******REMOVED***)

***REMOVED***# Endpoint
***REMOVED***if (
***REMOVED******REMOVED***not app_settings.azure_openai.endpoint and
***REMOVED******REMOVED***not app_settings.azure_openai.resource
***REMOVED***):
***REMOVED******REMOVED***raise ValueError(
***REMOVED******REMOVED***"AZURE_OPENAI_ENDPOINT or AZURE_OPENAI_RESOURCE is required"
***REMOVED******REMOVED***)

***REMOVED***endpoint = (
***REMOVED******REMOVED***app_settings.azure_openai.endpoint
***REMOVED******REMOVED***if app_settings.azure_openai.endpoint
***REMOVED******REMOVED***else f"https://{app_settings.azure_openai.resource}.openai.azure.com/"
***REMOVED***)

***REMOVED***# Authentication
***REMOVED***aoai_api_key = app_settings.azure_openai.key
***REMOVED***ad_token_provider = None
***REMOVED***if not aoai_api_key:
***REMOVED******REMOVED***logging.debug("No AZURE_OPENAI_KEY found, using Azure AD auth")
***REMOVED******REMOVED***ad_token_provider = get_bearer_token_provider(
***REMOVED******REMOVED***DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
***REMOVED******REMOVED***)

***REMOVED***# Deployment
***REMOVED***deployment = app_settings.azure_openai.model
***REMOVED***if not deployment:
***REMOVED******REMOVED***raise ValueError("AZURE_OPENAI_MODEL is required")

***REMOVED***# Default Headers
***REMOVED***default_headers = {"x-ms-useragent": USER_AGENT}

***REMOVED***azure_openai_client = AsyncAzureOpenAI(
***REMOVED******REMOVED***api_version=app_settings.azure_openai.preview_api_version,
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
***REMOVED***if app_settings.chat_history:
***REMOVED***try:
***REMOVED******REMOVED***cosmos_endpoint = (
***REMOVED******REMOVED***f"https://{app_settings.chat_history.account}.documents.azure.com:443/"
***REMOVED******REMOVED***)

***REMOVED******REMOVED***if not app_settings.chat_history.account_key:
***REMOVED******REMOVED***credential = DefaultAzureCredential()
***REMOVED******REMOVED***else:
***REMOVED******REMOVED***credential = app_settings.chat_history.account_key

***REMOVED******REMOVED***cosmos_conversation_client = CosmosConversationClient(
***REMOVED******REMOVED***cosmosdb_endpoint=cosmos_endpoint,
***REMOVED******REMOVED***credential=credential,
***REMOVED******REMOVED***database_name=app_settings.chat_history.database,
***REMOVED******REMOVED***container_name=app_settings.chat_history.conversations_container,
***REMOVED******REMOVED***enable_message_feedback=app_settings.chat_history.enable_feedback,
***REMOVED******REMOVED***)
***REMOVED***except Exception as e:
***REMOVED******REMOVED***logging.exception("Exception in CosmosDB initialization", e)
***REMOVED******REMOVED***cosmos_conversation_client = None
***REMOVED******REMOVED***raise e
***REMOVED***else:
***REMOVED***logging.debug("CosmosDB not configured")

***REMOVED***return cosmos_conversation_client


def prepare_model_args(request_body, request_headers):
***REMOVED***request_messages = request_body.get("messages", [])
***REMOVED***messages = []
***REMOVED***if not app_settings.datasource:
***REMOVED***messages = [
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"role": "system",
***REMOVED******REMOVED***"content": app_settings.azure_openai.system_message
***REMOVED***
***REMOVED***]

***REMOVED***for message in request_messages:
***REMOVED***if message:
***REMOVED******REMOVED***messages.append(
***REMOVED******REMOVED***{
***REMOVED******REMOVED******REMOVED***"role": message["role"],
***REMOVED******REMOVED******REMOVED***"content": message["content"]
***REMOVED******REMOVED***
***REMOVED******REMOVED***)

***REMOVED***user_json = None
***REMOVED***if (MS_DEFENDER_ENABLED):
***REMOVED***authenticated_user_details = get_authenticated_user_details(request_headers)
***REMOVED***user_json = get_msdefender_user_json(authenticated_user_details, request_headers)

***REMOVED***model_args = {
***REMOVED***"messages": messages,
***REMOVED***"temperature": app_settings.azure_openai.temperature,
***REMOVED***"max_tokens": app_settings.azure_openai.max_tokens,
***REMOVED***"top_p": app_settings.azure_openai.top_p,
***REMOVED***"stop": app_settings.azure_openai.stop_sequence,
***REMOVED***"stream": app_settings.azure_openai.stream,
***REMOVED***"model": app_settings.azure_openai.model,
***REMOVED***"user": user_json
***REMOVED***

***REMOVED***if app_settings.datasource:
***REMOVED***model_args["extra_body"] = {
***REMOVED******REMOVED***"data_sources": [
***REMOVED******REMOVED***app_settings.datasource.construct_payload_configuration(
***REMOVED******REMOVED******REMOVED***request=request
***REMOVED******REMOVED***)
***REMOVED******REMOVED***]
***REMOVED***

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
***REMOVED******REMOVED***"Authorization": f"Bearer {app_settings.promptflow.api_key}",
***REMOVED***
***REMOVED***# Adding timeout for scenarios where response takes longer to come back
***REMOVED***logging.debug(f"Setting timeout to {app_settings.promptflow.response_timeout}")
***REMOVED***async with httpx.AsyncClient(
***REMOVED******REMOVED***timeout=float(app_settings.promptflow.response_timeout)
***REMOVED***) as client:
***REMOVED******REMOVED***pf_formatted_obj = convert_to_pf_format(
***REMOVED******REMOVED***request,
***REMOVED******REMOVED***app_settings.promptflow.request_field_name,
***REMOVED******REMOVED***app_settings.promptflow.response_field_name
***REMOVED******REMOVED***)
***REMOVED******REMOVED***# NOTE: This only support question and chat_history parameters
***REMOVED******REMOVED***# If you need to add more parameters, you need to modify the request body
***REMOVED******REMOVED***response = await client.post(
***REMOVED******REMOVED***app_settings.promptflow.endpoint,
***REMOVED******REMOVED***json={
***REMOVED******REMOVED******REMOVED***app_settings.promptflow.request_field_name: pf_formatted_obj[-1]["inputs"][app_settings.promptflow.request_field_name],
***REMOVED******REMOVED******REMOVED***"chat_history": pf_formatted_obj[:-1],
***REMOVED******REMOVED***,
***REMOVED******REMOVED***headers=headers,
***REMOVED******REMOVED***)
***REMOVED***resp = response.json()
***REMOVED***resp["id"] = request["messages"][-1]["id"]
***REMOVED***return resp
***REMOVED***except Exception as e:
***REMOVED***logging.error(f"An error occurred while making promptflow_request: {e}")


async def send_chat_request(request_body, request_headers):
***REMOVED***filtered_messages = []
***REMOVED***messages = request_body.get("messages", [])
***REMOVED***for message in messages:
***REMOVED***if message.get("role") != 'tool':
***REMOVED******REMOVED***filtered_messages.append(message)
***REMOVED******REMOVED***
***REMOVED***request_body['messages'] = filtered_messages
***REMOVED***model_args = prepare_model_args(request_body, request_headers)

***REMOVED***try:
***REMOVED***azure_openai_client = init_openai_client()
***REMOVED***raw_response = await azure_openai_client.chat.completions.with_raw_response.create(**model_args)
***REMOVED***response = raw_response.parse()
***REMOVED***apim_request_id = raw_response.headers.get("apim-request-id") 
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in send_chat_request")
***REMOVED***raise e

***REMOVED***return response, apim_request_id


async def complete_chat_request(request_body, request_headers):
***REMOVED***if app_settings.base_settings.use_promptflow:
***REMOVED***response = await promptflow_request(request_body)
***REMOVED***history_metadata = request_body.get("history_metadata", {})
***REMOVED***return format_pf_non_streaming_response(
***REMOVED******REMOVED***response,
***REMOVED******REMOVED***history_metadata,
***REMOVED******REMOVED***app_settings.promptflow.response_field_name,
***REMOVED******REMOVED***app_settings.promptflow.citations_field_name
***REMOVED***)
***REMOVED***else:
***REMOVED***response, apim_request_id = await send_chat_request(request_body, request_headers)
***REMOVED***history_metadata = request_body.get("history_metadata", {})
***REMOVED***return format_non_streaming_response(response, history_metadata, apim_request_id)


async def stream_chat_request(request_body, request_headers):
***REMOVED***response, apim_request_id = await send_chat_request(request_body, request_headers)
***REMOVED***history_metadata = request_body.get("history_metadata", {})
***REMOVED***
***REMOVED***async def generate():
***REMOVED***async for completionChunk in response:
***REMOVED******REMOVED***yield format_stream_response(completionChunk, history_metadata, apim_request_id)

***REMOVED***return generate()


async def conversation_internal(request_body, request_headers):
***REMOVED***try:
***REMOVED***if app_settings.azure_openai.stream:
***REMOVED******REMOVED***result = await stream_chat_request(request_body, request_headers)
***REMOVED******REMOVED***response = await make_response(format_as_ndjson(result))
***REMOVED******REMOVED***response.timeout = None
***REMOVED******REMOVED***response.mimetype = "application/json-lines"
***REMOVED******REMOVED***return response
***REMOVED***else:
***REMOVED******REMOVED***result = await complete_chat_request(request_body, request_headers)
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

***REMOVED***return await conversation_internal(request_json, request.headers)


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
***REMOVED***return await conversation_internal(request_body, request.headers)

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
***REMOVED***if not app_settings.chat_history:
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
***REMOVED******REMOVED******REMOVED***"error": f"{cosmos_exception} {app_settings.chat_history.database} for account {app_settings.chat_history.account}"
***REMOVED******REMOVED***
***REMOVED******REMOVED***),
***REMOVED******REMOVED***422,
***REMOVED******REMOVED***)
***REMOVED***elif "Invalid CosmosDB container name" in cosmos_exception:
***REMOVED******REMOVED***return (
***REMOVED******REMOVED***jsonify(
***REMOVED******REMOVED******REMOVED***{
***REMOVED******REMOVED******REMOVED***"error": f"{cosmos_exception}: {app_settings.chat_history.conversations_container}"
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
***REMOVED******REMOVED***model=app_settings.azure_openai.model, messages=messages, temperature=1, max_tokens=64
***REMOVED***)

***REMOVED***title = json.loads(response.choices[0].message.content)["title"]
***REMOVED***return title
***REMOVED***except Exception as e:
***REMOVED***return messages[-2]["content"]


app = create_app()
