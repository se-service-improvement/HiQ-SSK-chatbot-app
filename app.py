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
AZURE_SEARCH_USE_SEMANTIC_SEARCH = os.environ.get("AZURE_SEARCH_USE_SEMANTIC_SEARCH")
AZURE_SEARCH_INDEX_IS_PRECHUNKED = os.environ.get("AZURE_SEARCH_INDEX_IS_PRECHUNKED")

# AOAI Integration Settings
AZURE_OPENAI_RESOURCE = os.environ.get("AZURE_OPENAI_RESOURCE")
AZURE_OPENAI_MODEL = os.environ.get("AZURE_OPENAI_MODEL")
AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")

# Private API Management Key (temporary)
AZURE_APIM_KEY = os.environ.get("AZURE_APIM_KEY")

@app.route("/conversation", methods=["POST"])
def conversation():
***REMOVED***try:
***REMOVED***messages = request.json["messages"]
***REMOVED***body = {
***REMOVED******REMOVED***"messages": messages
***REMOVED***
***REMOVED***
***REMOVED***azure_openai_url = f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/openai/deployments/{AZURE_OPENAI_MODEL}/completions?api-version=2022-12-01"
***REMOVED***search_url = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net"

***REMOVED***headers = {
***REMOVED******REMOVED***"Content-Type": "application/json",
***REMOVED******REMOVED***"azure_document_search_url": search_url,
***REMOVED******REMOVED***"azure_document_search_api_key": AZURE_SEARCH_KEY,
***REMOVED******REMOVED***"azure_document_search_index": AZURE_SEARCH_INDEX,
***REMOVED******REMOVED***"azure_document_is_prechunked": AZURE_SEARCH_INDEX_IS_PRECHUNKED,
***REMOVED******REMOVED***"chatgpt_url": azure_openai_url,
***REMOVED******REMOVED***"chatgpt_key": AZURE_OPENAI_KEY,
***REMOVED******REMOVED***"Ocp-Apim-Subscription-Key": AZURE_APIM_KEY,
***REMOVED******REMOVED***"azure_document_search_configuration": "default" if AZURE_SEARCH_USE_SEMANTIC_SEARCH else "",
***REMOVED******REMOVED***"azure_document_search_query_type": "semantic" if AZURE_SEARCH_USE_SEMANTIC_SEARCH else "simple"
***REMOVED***

***REMOVED***endpoint = "https://tadevusw2.azure-api.net/svc/inferenceservice/conversation"
***REMOVED***r = requests.post(endpoint, headers=headers, json=body)
***REMOVED***r = r.json()

***REMOVED***return jsonify(r)
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /conversation")
***REMOVED***return jsonify({"error": str(e)}), 500

@app.route("/feedback", methods=["POST"])
def feedback():
***REMOVED***try:
***REMOVED***headers = {
***REMOVED******REMOVED***"Content-Type": "application/json",
***REMOVED******REMOVED***"Ocp-Apim-Subscription-Key": AZURE_APIM_KEY
***REMOVED***
***REMOVED***endpoint = "https://tadevusw2.azure-api.net/svc/inferenceservice/feedback"
***REMOVED***r = requests.post(endpoint, headers=headers, json=request.json)
***REMOVED***return jsonify({"status": r.status_code, "ok": r.ok})
***REMOVED***except Exception as e:
***REMOVED***logging.exception("Exception in /feedback")
***REMOVED***return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
***REMOVED***app.run()
