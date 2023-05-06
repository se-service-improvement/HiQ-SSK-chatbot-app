import os
import logging
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def static_file(path):
***REMOVED***return app.send_static_file(path)

# ACS Integration Settings
AZURE_SEARCH_SERVICE = os.environ.get("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX")
AZURE_SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY")
AZURE_SEARCH_USE_SEMANTIC_SEARCH = os.environ.get("AZURE_SEARCH_USE_SEMANTIC_SEARCH", False)
AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG = os.environ.get("AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG", "default")
AZURE_SEARCH_INDEX_IS_PRECHUNKED = os.environ.get("AZURE_SEARCH_INDEX_IS_PRECHUNKED", True)
AZURE_SEARCH_TOP_K = os.environ.get("AZURE_SEARCH_TOP_K", 5)
AZURE_SEARCH_ENABLE_IN_DOMAIN = os.environ.get("AZURE_SEARCH_ENABLE_IN_DOMAIN", False)
AZURE_SEARCH_CONTENT_COLUMNS = os.environ.get("AZURE_SEARCH_CONTENT_COLUMNS")
AZURE_SEARCH_FILENAME_COLUMN = os.environ.get("AZURE_SEARCH_FILENAME_COLUMN")
AZURE_SEARCH_TITLE_COLUMN = os.environ.get("AZURE_SEARCH_TITLE_COLUMN")
AZURE_SEARCH_URL_COLUMN = os.environ.get("AZURE_SEARCH_URL_COLUMN")

# AOAI Integration Settings
AZURE_OPENAI_RESOURCE = os.environ.get("AZURE_OPENAI_RESOURCE")
AZURE_OPENAI_MODEL = os.environ.get("AZURE_OPENAI_MODEL")
AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_TEMPERATURE = os.environ.get("AZURE_OPENAI_TEMPERATURE", 0)
AZURE_OPENAI_TOP_P = os.environ.get("AZURE_OPENAI_TOP_P", 1.0)
AZURE_OPENAI_MAX_TOKENS = os.environ.get("AZURE_OPENAI_MAX_TOKENS", 1000)
AZURE_OPENAI_STOP_SEQUENCE = os.environ.get("AZURE_OPENAI_STOP_SEQUENCE")
AZURE_OPENAI_SYSTEM_MESSAGE = os.environ.get("AZURE_OPENAI_SYSTEM_MESSAGE", "You are an AI assistant that helps people find information.")
AZURE_OPENAI_PREVIEW_API_VERSION = os.environ.get("AZURE_OPENAI_PREVIEW_API_VERSION", "2023-03-31-preview")


def prepare_body_headers_with_data(request):
***REMOVED***messages = request.json["messages"]
***REMOVED***body = {
***REMOVED***"messages": messages,
***REMOVED***"enable_Indomain": True if AZURE_SEARCH_ENABLE_IN_DOMAIN.lower() == "true" else False,
***REMOVED***"azure_document_search_top_k": AZURE_SEARCH_TOP_K,
***REMOVED***"temperature": AZURE_OPENAI_TEMPERATURE,
***REMOVED***"top_p": AZURE_OPENAI_TOP_P,
***REMOVED***"max_tokens": AZURE_OPENAI_MAX_TOKENS
***REMOVED***

***REMOVED***if AZURE_OPENAI_STOP_SEQUENCE:
***REMOVED***sequences = AZURE_OPENAI_STOP_SEQUENCE.split("|")
***REMOVED***body["stop"] = sequences
***REMOVED***
***REMOVED***if AZURE_OPENAI_DEPLOYMENT:
***REMOVED***body["deployment"] = AZURE_OPENAI_DEPLOYMENT

***REMOVED***if AZURE_OPENAI_SYSTEM_MESSAGE:
***REMOVED***body["system_message"] = AZURE_OPENAI_SYSTEM_MESSAGE

***REMOVED***index_column_mapping = {}
***REMOVED***if AZURE_SEARCH_CONTENT_COLUMNS:
***REMOVED***index_column_mapping["content_column"] = AZURE_SEARCH_CONTENT_COLUMNS.split("|")
***REMOVED***if AZURE_SEARCH_FILENAME_COLUMN:
***REMOVED***index_column_mapping["filepath_column"] = AZURE_SEARCH_FILENAME_COLUMN
***REMOVED***if AZURE_SEARCH_TITLE_COLUMN:
***REMOVED***index_column_mapping["title_column"] = AZURE_SEARCH_TITLE_COLUMN
***REMOVED***if AZURE_SEARCH_URL_COLUMN:
***REMOVED***index_column_mapping["url_column"] = AZURE_SEARCH_URL_COLUMN
***REMOVED***# TODO: uncomment this when the API is ready
***REMOVED***# if index_column_mapping:
***REMOVED***#***REMOVED*** body["index_column_mapping"] = index_column_mapping

***REMOVED***azure_openai_url = f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/openai/deployments/{AZURE_OPENAI_MODEL}/completions?api-version=2022-12-01"
***REMOVED***search_url = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net"

***REMOVED***headers = {
***REMOVED***"Content-Type": "application/json",
***REMOVED***"azure_document_search_url": search_url,
***REMOVED***"azure_document_search_api_key": AZURE_SEARCH_KEY,
***REMOVED***"azure_document_search_index": AZURE_SEARCH_INDEX,
***REMOVED***"azure_document_is_prechunked": AZURE_SEARCH_INDEX_IS_PRECHUNKED,
***REMOVED***"chatgpt_url": azure_openai_url,
***REMOVED***"chatgpt_key": AZURE_OPENAI_KEY,
***REMOVED***"Ocp-Apim-Subscription-Key": AZURE_OPENAI_KEY,
***REMOVED***'api-key': AZURE_OPENAI_KEY,
***REMOVED***"azure_document_search_configuration": AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG if AZURE_SEARCH_USE_SEMANTIC_SEARCH.lower() == "true" and AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG else "",
***REMOVED***"azure_document_search_query_type": "semantic" if AZURE_SEARCH_USE_SEMANTIC_SEARCH.lower() == "true" else "simple"
***REMOVED***

***REMOVED***return body, headers

def prepare_body_headers_without_data(request):
***REMOVED***request_messages = request.json["messages"]
***REMOVED***body_messages = [
***REMOVED***{
***REMOVED******REMOVED***"role": "system",
***REMOVED******REMOVED***"content": AZURE_OPENAI_SYSTEM_MESSAGE
***REMOVED***
***REMOVED***]

***REMOVED***for message in request_messages:
***REMOVED***body_messages.append({
***REMOVED******REMOVED***"role": "assistant" if  message["role"] == "bot" else "user",
***REMOVED******REMOVED***"content": message["content"]["parts"][0]
***REMOVED***)

***REMOVED***body = {
***REMOVED***"messages": body_messages,
***REMOVED***"temperature": float(AZURE_OPENAI_TEMPERATURE),
***REMOVED***"top_p": float(AZURE_OPENAI_TOP_P),
***REMOVED***"max_tokens": int(AZURE_OPENAI_MAX_TOKENS),
***REMOVED***"stream": False
***REMOVED***

***REMOVED***headers = {
***REMOVED***'Content-Type': 'application/json',
***REMOVED***'api-key': AZURE_OPENAI_KEY
***REMOVED***

***REMOVED***if AZURE_OPENAI_STOP_SEQUENCE:
***REMOVED***sequences = AZURE_OPENAI_STOP_SEQUENCE.split("|")
***REMOVED***body["stop"] = sequences

***REMOVED***return body, headers

def should_use_data():
***REMOVED***if AZURE_SEARCH_SERVICE and AZURE_SEARCH_INDEX and AZURE_SEARCH_KEY:
***REMOVED***return True
***REMOVED***return False

@app.route("/conversation", methods=["POST"])
def conversation():
***REMOVED***try:
***REMOVED***base_url = f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com"
***REMOVED***use_data = should_use_data()
***REMOVED***if use_data:
***REMOVED******REMOVED***body, headers = prepare_body_headers_with_data(request)
***REMOVED******REMOVED***endpoint = f"{base_url}/openai/wednesday-private/conversation?api-version={AZURE_OPENAI_PREVIEW_API_VERSION}"
***REMOVED***else:
***REMOVED******REMOVED***body, headers = prepare_body_headers_without_data(request)
***REMOVED******REMOVED***endpoint = f"{base_url}/openai/deployments/{AZURE_OPENAI_MODEL}/chat/completions?api-version=2023-03-15-preview"

***REMOVED***r = requests.post(endpoint, headers=headers, json=body)
***REMOVED***status_code = r.status_code
***REMOVED***r = r.json()

***REMOVED***if not use_data and status_code == 200:
***REMOVED******REMOVED***# convert to the same format as the data version
***REMOVED******REMOVED***r = {
***REMOVED******REMOVED***"message_id": r["id"],
***REMOVED******REMOVED***"parent_message_id": "",
***REMOVED******REMOVED***"role": "bot",
***REMOVED******REMOVED***"content": {
***REMOVED******REMOVED******REMOVED***"content_type": "text",
***REMOVED******REMOVED******REMOVED***"parts": [
***REMOVED******REMOVED******REMOVED***r["choices"][0]["message"]["content"]
***REMOVED******REMOVED******REMOVED***],
***REMOVED******REMOVED******REMOVED***"top_docs": [],
***REMOVED******REMOVED******REMOVED***"intent": ""
***REMOVED******REMOVED***,
***REMOVED***

***REMOVED***return jsonify(r)
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /conversation")
***REMOVED***return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
***REMOVED***app.run()
