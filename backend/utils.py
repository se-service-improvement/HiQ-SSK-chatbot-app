import os
import json
import logging
import requests
import dataclasses

from typing import List

DEBUG = os.environ.get("DEBUG", "false")
if DEBUG.lower() == "true":
***REMOVED***logging.basicConfig(level=logging.DEBUG)

AZURE_SEARCH_PERMITTED_GROUPS_COLUMN = os.environ.get(
***REMOVED***"AZURE_SEARCH_PERMITTED_GROUPS_COLUMN"
)


class JSONEncoder(json.JSONEncoder):
***REMOVED***def default(self, o):
***REMOVED***if dataclasses.is_dataclass(o):
***REMOVED******REMOVED***return dataclasses.asdict(o)
***REMOVED***return super().default(o)


async def format_as_ndjson(r):
***REMOVED***try:
***REMOVED***async for event in r:
***REMOVED******REMOVED***yield json.dumps(event, cls=JSONEncoder) + "\n"
***REMOVED***except Exception as error:
***REMOVED***logging.exception("Exception while generating response stream: %s", error)
***REMOVED***yield json.dumps({"error": str(error)})


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

***REMOVED***headers = {"Authorization": "bearer " + userToken}
***REMOVED***try:
***REMOVED***r = requests.get(endpoint, headers=headers)
***REMOVED***if r.status_code != 200:
***REMOVED******REMOVED***logging.error(f"Error fetching user groups: {r.status_code} {r.text}")
***REMOVED******REMOVED***return []

***REMOVED***r = r.json()
***REMOVED***if "@odata.nextLink" in r:
***REMOVED******REMOVED***nextLinkData = fetchUserGroups(userToken, r["@odata.nextLink"])
***REMOVED******REMOVED***r["value"].extend(nextLinkData)

***REMOVED***return r["value"]
***REMOVED***except Exception as e:
***REMOVED***logging.error(f"Exception in fetchUserGroups: {e}")
***REMOVED***return []


def generateFilterString(userToken):
***REMOVED***# Get list of groups user is a member of
***REMOVED***userGroups = fetchUserGroups(userToken)

***REMOVED***# Construct filter string
***REMOVED***if not userGroups:
***REMOVED***logging.debug("No user groups found")

***REMOVED***group_ids = ", ".join([obj["id"] for obj in userGroups])
***REMOVED***return f"{AZURE_SEARCH_PERMITTED_GROUPS_COLUMN}/any(g:search.in(g, '{group_ids}'))"


def format_non_streaming_response(chatCompletion, history_metadata, apim_request_id):
***REMOVED***response_obj = {
***REMOVED***"id": chatCompletion.id,
***REMOVED***"model": chatCompletion.model,
***REMOVED***"created": chatCompletion.created,
***REMOVED***"object": chatCompletion.object,
***REMOVED***"choices": [{"messages": []}],
***REMOVED***"history_metadata": history_metadata,
***REMOVED***"apim-request-id": apim_request_id,
***REMOVED***

***REMOVED***if len(chatCompletion.choices) > 0:
***REMOVED***message = chatCompletion.choices[0].message
***REMOVED***if message:
***REMOVED******REMOVED***if hasattr(message, "context"):
***REMOVED******REMOVED***response_obj["choices"][0]["messages"].append(
***REMOVED******REMOVED******REMOVED***{
***REMOVED******REMOVED******REMOVED***"role": "tool",
***REMOVED******REMOVED******REMOVED***"content": json.dumps(message.context),
***REMOVED******REMOVED***
***REMOVED******REMOVED***)
***REMOVED******REMOVED***response_obj["choices"][0]["messages"].append(
***REMOVED******REMOVED***{
***REMOVED******REMOVED******REMOVED***"role": "assistant",
***REMOVED******REMOVED******REMOVED***"content": message.content,
***REMOVED******REMOVED***
***REMOVED******REMOVED***)
***REMOVED******REMOVED***return response_obj

***REMOVED***return {}

def format_stream_response(chatCompletionChunk, history_metadata, apim_request_id):
***REMOVED***response_obj = {
***REMOVED***"id": chatCompletionChunk.id,
***REMOVED***"model": chatCompletionChunk.model,
***REMOVED***"created": chatCompletionChunk.created,
***REMOVED***"object": chatCompletionChunk.object,
***REMOVED***"choices": [{"messages": []}],
***REMOVED***"history_metadata": history_metadata,
***REMOVED***"apim-request-id": apim_request_id,
***REMOVED***

***REMOVED***if len(chatCompletionChunk.choices) > 0:
***REMOVED***delta = chatCompletionChunk.choices[0].delta
***REMOVED***if delta:
***REMOVED******REMOVED***if hasattr(delta, "context"):
***REMOVED******REMOVED***messageObj = {"role": "tool", "content": json.dumps(delta.context)}
***REMOVED******REMOVED***response_obj["choices"][0]["messages"].append(messageObj)
***REMOVED******REMOVED***return response_obj
***REMOVED******REMOVED***if delta.role == "assistant" and hasattr(delta, "context"):
***REMOVED******REMOVED***messageObj = {
***REMOVED******REMOVED******REMOVED***"role": "assistant",
***REMOVED******REMOVED******REMOVED***"context": delta.context,
***REMOVED******REMOVED***
***REMOVED******REMOVED***response_obj["choices"][0]["messages"].append(messageObj)
***REMOVED******REMOVED***return response_obj
***REMOVED******REMOVED***if delta.tool_calls:
***REMOVED******REMOVED***messageObj = {
***REMOVED******REMOVED******REMOVED***"role": "tool",
***REMOVED******REMOVED******REMOVED***"tool_calls": {
***REMOVED******REMOVED******REMOVED***"id": delta.tool_calls[0].id,
***REMOVED******REMOVED******REMOVED***"function": {
***REMOVED******REMOVED******REMOVED******REMOVED***"name" : delta.tool_calls[0].function.name,
***REMOVED******REMOVED******REMOVED******REMOVED***"arguments": delta.tool_calls[0].function.arguments
***REMOVED******REMOVED******REMOVED***,
***REMOVED******REMOVED******REMOVED***"type": delta.tool_calls[0].type
***REMOVED******REMOVED***
***REMOVED******REMOVED***
***REMOVED******REMOVED***if hasattr(delta, "context"):
***REMOVED******REMOVED******REMOVED***messageObj["context"] = json.dumps(delta.context)
***REMOVED******REMOVED***response_obj["choices"][0]["messages"].append(messageObj)
***REMOVED******REMOVED***return response_obj
***REMOVED******REMOVED***else:
***REMOVED******REMOVED***if delta.content:
***REMOVED******REMOVED******REMOVED***messageObj = {
***REMOVED******REMOVED******REMOVED***"role": "assistant",
***REMOVED******REMOVED******REMOVED***"content": delta.content,
***REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***response_obj["choices"][0]["messages"].append(messageObj)
***REMOVED******REMOVED******REMOVED***return response_obj

***REMOVED***return {}


def format_pf_non_streaming_response(
***REMOVED***chatCompletion, history_metadata, response_field_name, citations_field_name, message_uuid=None
):
***REMOVED***if chatCompletion is None:
***REMOVED***logging.error(
***REMOVED******REMOVED***"chatCompletion object is None - Increase PROMPTFLOW_RESPONSE_TIMEOUT parameter"
***REMOVED***)
***REMOVED***return {
***REMOVED******REMOVED***"error": "No response received from promptflow endpoint increase PROMPTFLOW_RESPONSE_TIMEOUT parameter or check the promptflow endpoint."
***REMOVED***
***REMOVED***if "error" in chatCompletion:
***REMOVED***logging.error(f"Error in promptflow response api: {chatCompletion['error']}")
***REMOVED***return {"error": chatCompletion["error"]}

***REMOVED***logging.debug(f"chatCompletion: {chatCompletion}")
***REMOVED***try:
***REMOVED***messages = []
***REMOVED***if response_field_name in chatCompletion:
***REMOVED******REMOVED***messages.append({
***REMOVED******REMOVED***"role": "assistant",
***REMOVED******REMOVED***"content": chatCompletion[response_field_name] 
***REMOVED***)
***REMOVED***if citations_field_name in chatCompletion:
***REMOVED******REMOVED***citation_content= {"citations": chatCompletion[citations_field_name]}
***REMOVED******REMOVED***messages.append({ 
***REMOVED******REMOVED***"role": "tool",
***REMOVED******REMOVED***"content": json.dumps(citation_content)
***REMOVED***)

***REMOVED***response_obj = {
***REMOVED******REMOVED***"id": chatCompletion["id"],
***REMOVED******REMOVED***"model": "",
***REMOVED******REMOVED***"created": "",
***REMOVED******REMOVED***"object": "",
***REMOVED******REMOVED***"history_metadata": history_metadata,
***REMOVED******REMOVED***"choices": [
***REMOVED******REMOVED***{
***REMOVED******REMOVED******REMOVED***"messages": messages,
***REMOVED******REMOVED***
***REMOVED******REMOVED***]
***REMOVED***
***REMOVED***return response_obj
***REMOVED***except Exception as e:
***REMOVED***logging.error(f"Exception in format_pf_non_streaming_response: {e}")
***REMOVED***return {}


def convert_to_pf_format(input_json, request_field_name, response_field_name):
***REMOVED***output_json = []
***REMOVED***logging.debug(f"Input json: {input_json}")
***REMOVED***# align the input json to the format expected by promptflow chat flow
***REMOVED***for message in input_json["messages"]:
***REMOVED***if message:
***REMOVED******REMOVED***if message["role"] == "user":
***REMOVED******REMOVED***new_obj = {
***REMOVED******REMOVED******REMOVED***"inputs": {request_field_name: message["content"]},
***REMOVED******REMOVED******REMOVED***"outputs": {response_field_name: ""},
***REMOVED******REMOVED***
***REMOVED******REMOVED***output_json.append(new_obj)
***REMOVED******REMOVED***elif message["role"] == "assistant" and len(output_json) > 0:
***REMOVED******REMOVED***output_json[-1]["outputs"][response_field_name] = message["content"]
***REMOVED***logging.debug(f"PF formatted response: {output_json}")
***REMOVED***return output_json


def comma_separated_string_to_list(s: str) -> List[str]:
***REMOVED***'''
***REMOVED***Split comma-separated values into a list.
***REMOVED***'''
***REMOVED***return s.strip().replace(' ', '').split(',')

