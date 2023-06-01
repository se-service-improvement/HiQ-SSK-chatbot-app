import json
import os
import logging
import requests
import openai
from flask import Flask, Response, request, jsonify
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
AZURE_OPENAI_STREAM = os.environ.get("AZURE_OPENAI_STREAM", "true")
AZURE_OPENAI_MODEL_NAME = os.environ.get("AZURE_OPENAI_MODEL_NAME", "gpt-35-turbo") # Name of the model, e.g. 'gpt-35-turbo' or 'gpt-4'

SHOULD_STREAM = True if AZURE_OPENAI_STREAM.lower() == "true" else False

def is_chat_model():
***REMOVED***if 'gpt-4' in AZURE_OPENAI_MODEL_NAME.lower():
***REMOVED***return True
***REMOVED***return False

def should_use_data():
***REMOVED***if AZURE_SEARCH_SERVICE and AZURE_SEARCH_INDEX and AZURE_SEARCH_KEY:
***REMOVED***return True
***REMOVED***return False

def prepare_body_headers_with_data(request):
***REMOVED***request_messages = request.json["messages"]

***REMOVED***body = {
***REMOVED***"messages": request_messages,
***REMOVED***"temperature": AZURE_OPENAI_TEMPERATURE,
***REMOVED***"max_tokens": AZURE_OPENAI_MAX_TOKENS,
***REMOVED***"top_p": AZURE_OPENAI_TOP_P,
***REMOVED***"stop": AZURE_OPENAI_STOP_SEQUENCE.split("|") if AZURE_OPENAI_STOP_SEQUENCE else [],
***REMOVED***"stream": SHOULD_STREAM,
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
***REMOVED***chatgpt_url = f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/openai/deployments/{AZURE_OPENAI_MODEL}"
***REMOVED***if is_chat_model():
***REMOVED***chatgpt_url += "/chat/completions?api-version=2023-03-15-preview"
***REMOVED***else:
***REMOVED***chatgpt_url += "/completions?api-version=2023-03-15-preview"

***REMOVED***headers = {
***REMOVED***'Content-Type': 'application/json',
***REMOVED***'api-key': AZURE_OPENAI_KEY,
***REMOVED***'chatgpt_url': chatgpt_url,
***REMOVED***'chatgpt_key': AZURE_OPENAI_KEY,
***REMOVED***"x-ms-useragent": "GitHubSampleWebApp/PublicAPI/1.0.0"
***REMOVED***

***REMOVED***return body, headers


def stream_with_data(body, headers, endpoint):
***REMOVED***s = requests.Session()
***REMOVED***response = {
***REMOVED***"id": "",
***REMOVED***"model": "",
***REMOVED***"created": 0,
***REMOVED***"object": "",
***REMOVED***"choices": [{
***REMOVED******REMOVED***"messages": []
***REMOVED***]
***REMOVED***
***REMOVED***try:
***REMOVED***with s.post(endpoint, json=body, headers=headers, stream=True) as r:
***REMOVED******REMOVED***for line in r.iter_lines(chunk_size=10):
***REMOVED******REMOVED***if line:
***REMOVED******REMOVED******REMOVED***lineJson = json.loads(line.lstrip(b'data:').decode('utf-8'))
***REMOVED******REMOVED******REMOVED***if 'error' in lineJson:
***REMOVED******REMOVED******REMOVED***yield json.dumps(lineJson) + "<newline>"
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
***REMOVED******REMOVED******REMOVED******REMOVED***response["choices"][0]["messages"][1]["content"] += deltaText***REMOVED******REMOVED***

***REMOVED******REMOVED******REMOVED***yield json.dumps(response) + "<newline>"
***REMOVED***except Exception as e:
***REMOVED***yield json.dumps({"error": str(e)}) + "<newline>"


def conversation_with_data(request):
***REMOVED***body, headers = prepare_body_headers_with_data(request)
***REMOVED***endpoint = f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/openai/deployments/{AZURE_OPENAI_MODEL}/extensions/chat/completions?api-version={AZURE_OPENAI_PREVIEW_API_VERSION}"
***REMOVED***
***REMOVED***if not SHOULD_STREAM:
***REMOVED***r = requests.post(endpoint, headers=headers, json=body)
***REMOVED***status_code = r.status_code
***REMOVED***r = r.json()

***REMOVED***return Response(json.dumps(r), status=status_code)
***REMOVED***else:
***REMOVED***if request.method == "POST":
***REMOVED******REMOVED***return Response(stream_with_data(body, headers, endpoint), mimetype='text/event-stream')
***REMOVED***else:
***REMOVED******REMOVED***return Response(None, mimetype='text/event-stream')

def stream_without_data(response):
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
***REMOVED***]
***REMOVED***
***REMOVED***yield json.dumps(response_obj) + "<newline>"


def conversation_without_data(request):
***REMOVED***openai.api_type = "azure"
***REMOVED***openai.api_base = f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/"
***REMOVED***openai.api_version = "2023-03-15-preview"
***REMOVED***openai.api_key = AZURE_OPENAI_KEY

***REMOVED***request_messages = request.json["messages"]
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
***REMOVED***]
***REMOVED***

***REMOVED***return jsonify(response_obj), 200
***REMOVED***else:
***REMOVED***if request.method == "POST":
***REMOVED******REMOVED***return Response(stream_without_data(response), mimetype='text/event-stream')
***REMOVED***else:
***REMOVED******REMOVED***return Response(None, mimetype='text/event-stream')

@app.route("/conversation", methods=["GET", "POST"])
def conversation():
***REMOVED***try:
***REMOVED***use_data = should_use_data()
***REMOVED***if use_data:
***REMOVED******REMOVED***return conversation_with_data(request)
***REMOVED***else:
***REMOVED******REMOVED***return conversation_without_data(request)
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /conversation")
***REMOVED***return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
***REMOVED***app.run()
