import os
import logging
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

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
AZURE_SEARCH_TOP_K = os.environ.get("AZURE_SEARCH_TOP_K", 5)
AZURE_SEARCH_ENABLE_IN_DOMAIN = os.environ.get("AZURE_SEARCH_ENABLE_IN_DOMAIN", "true")
AZURE_SEARCH_CONTENT_COLUMNS = os.environ.get("AZURE_SEARCH_CONTENT_COLUMNS")
AZURE_SEARCH_FILENAME_COLUMN = os.environ.get("AZURE_SEARCH_FILENAME_COLUMN")
AZURE_SEARCH_TITLE_COLUMN = os.environ.get("AZURE_SEARCH_TITLE_COLUMN")
AZURE_SEARCH_URL_COLUMN = os.environ.get("AZURE_SEARCH_URL_COLUMN")

# AOAI Integration Settings
AZURE_OPENAI_RESOURCE = os.environ.get("AZURE_OPENAI_RESOURCE")
AZURE_OPENAI_MODEL = os.environ.get("AZURE_OPENAI_MODEL")
AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
AZURE_OPENAI_TEMPERATURE = os.environ.get("AZURE_OPENAI_TEMPERATURE", 0)
AZURE_OPENAI_TOP_P = os.environ.get("AZURE_OPENAI_TOP_P", 1.0)
AZURE_OPENAI_MAX_TOKENS = os.environ.get("AZURE_OPENAI_MAX_TOKENS", 1000)
AZURE_OPENAI_STOP_SEQUENCE = os.environ.get("AZURE_OPENAI_STOP_SEQUENCE")
AZURE_OPENAI_SYSTEM_MESSAGE = os.environ.get("AZURE_OPENAI_SYSTEM_MESSAGE", "You are an AI assistant that helps people find information.")
AZURE_OPENAI_PREVIEW_API_VERSION = os.environ.get("AZURE_OPENAI_PREVIEW_API_VERSION", "2023-06-01-preview")


def prepare_body_headers_with_data(request):
***REMOVED***request_messages = request.json["messages"]

***REMOVED***body = {
***REMOVED***"messages": request_messages,
***REMOVED***"temperature": AZURE_OPENAI_TEMPERATURE,
***REMOVED***"max_tokens": AZURE_OPENAI_MAX_TOKENS,
***REMOVED***"top_p": AZURE_OPENAI_TOP_P,
***REMOVED***"stop": AZURE_OPENAI_STOP_SEQUENCE.split("|") if AZURE_OPENAI_STOP_SEQUENCE else [],
***REMOVED***"stream": False,
***REMOVED***"dataSources": [
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"type": "AzureCognitiveSearch",
***REMOVED******REMOVED***"parameters": {
***REMOVED******REMOVED******REMOVED***"endpoint": f"https://{AZURE_SEARCH_SERVICE}.search.windows.net",
***REMOVED******REMOVED******REMOVED***"key": AZURE_SEARCH_KEY,
***REMOVED******REMOVED******REMOVED***"indexName": AZURE_SEARCH_INDEX,
***REMOVED******REMOVED******REMOVED***"fieldsMapping": {
***REMOVED******REMOVED******REMOVED***"contentField": AZURE_SEARCH_CONTENT_COLUMNS.split("|") if AZURE_SEARCH_CONTENT_COLUMNS else [],
***REMOVED******REMOVED******REMOVED***"titleField": AZURE_SEARCH_TITLE_COLUMN if AZURE_SEARCH_TITLE_COLUMN else None,
***REMOVED******REMOVED******REMOVED***"urlField": AZURE_SEARCH_URL_COLUMN if AZURE_SEARCH_URL_COLUMN else None,
***REMOVED******REMOVED******REMOVED***"filepathField": AZURE_SEARCH_FILENAME_COLUMN if AZURE_SEARCH_FILENAME_COLUMN else None
***REMOVED******REMOVED***,
***REMOVED******REMOVED******REMOVED***"inScope": True if AZURE_SEARCH_ENABLE_IN_DOMAIN.lower() == "true" else False,
***REMOVED******REMOVED******REMOVED***"topNDocuments": AZURE_SEARCH_TOP_K,
***REMOVED******REMOVED******REMOVED***"queryType": "semantic" if AZURE_SEARCH_USE_SEMANTIC_SEARCH.lower() == "true" else "simple",
***REMOVED******REMOVED******REMOVED***"semanticConfiguration": AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG if AZURE_SEARCH_USE_SEMANTIC_SEARCH.lower() == "true" and AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG else "",
***REMOVED******REMOVED******REMOVED***"roleInformation": AZURE_OPENAI_SYSTEM_MESSAGE
***REMOVED******REMOVED***
***REMOVED***
***REMOVED***]
***REMOVED***
***REMOVED***
***REMOVED***headers = {
***REMOVED***'Content-Type': 'application/json',
***REMOVED***'api-key': AZURE_OPENAI_KEY,
***REMOVED***'chatgpt_url': f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/openai/deployments/{AZURE_OPENAI_MODEL}/completions?api-version=2023-03-31-preview",
***REMOVED***'chatgpt_key': AZURE_OPENAI_KEY,
***REMOVED***"x-ms-useragent": "GitHubSampleWebApp/PublicAPI/1.0.0"
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
***REMOVED******REMOVED***"role": message["role"] ,
***REMOVED******REMOVED***"content": message["content"]
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
***REMOVED******REMOVED***endpoint = f"{base_url}/openai/deployments/{AZURE_OPENAI_MODEL}/extensions/chat/completions?api-version={AZURE_OPENAI_PREVIEW_API_VERSION}"
***REMOVED***else:
***REMOVED******REMOVED***body, headers = prepare_body_headers_without_data(request)
***REMOVED******REMOVED***endpoint = f"{base_url}/openai/deployments/{AZURE_OPENAI_MODEL}/chat/completions?api-version=2023-03-15-preview"

***REMOVED***r = requests.post(endpoint, headers=headers, json=body)
***REMOVED***status_code = r.status_code
***REMOVED***r = r.json()

***REMOVED***if not use_data and status_code == 200:
***REMOVED******REMOVED***# convert to the same format as the data version
***REMOVED******REMOVED***r["choices"][0]["messages"] = [{
***REMOVED******REMOVED***"content": r["choices"][0]["message"]["content"],
***REMOVED******REMOVED***"role": "assistant"
***REMOVED******REMOVED***]

***REMOVED***return jsonify(r), status_code
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /conversation")
***REMOVED***return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
***REMOVED***app.run()
