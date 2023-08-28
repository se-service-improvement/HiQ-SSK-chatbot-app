import os
import uuid
from datetime import datetime
from flask import Flask, request
from azure.identity import DefaultAzureCredential  
from azure.cosmos import CosmosClient, PartitionKey  
  
class CosmosConversationClient():
***REMOVED***
***REMOVED***def __init__(self, cosmosdb_endpoint: str, credential: any, database_name: str, container_name: str):
***REMOVED***self.cosmosdb_endpoint = cosmosdb_endpoint
***REMOVED***self.credential = credential
***REMOVED***self.database_name = database_name
***REMOVED***self.container_name = container_name
***REMOVED***self.cosmosdb_client = CosmosClient(self.cosmosdb_endpoint, credential=credential)
***REMOVED***self.database_client = self.cosmosdb_client.get_database_client(database_name)
***REMOVED***self.container_client = self.database_client.get_container_client(container_name)

***REMOVED***def ensure(self):
***REMOVED***try:
***REMOVED******REMOVED***if not self.cosmosdb_client or not self.database_client or not self.container_client:
***REMOVED******REMOVED***return False
***REMOVED******REMOVED***
***REMOVED******REMOVED***container_info = self.container_client.read()
***REMOVED******REMOVED***if not container_info:
***REMOVED******REMOVED***return False
***REMOVED******REMOVED***
***REMOVED******REMOVED***return True
***REMOVED***except:
***REMOVED******REMOVED***return False

***REMOVED***def create_conversation(self, user_id, title = ''):
***REMOVED***conversation = {
***REMOVED******REMOVED***'id': str(uuid.uuid4()),  
***REMOVED******REMOVED***'type': 'conversation',
***REMOVED******REMOVED***'createdAt': datetime.utcnow().isoformat(),  
***REMOVED******REMOVED***'updatedAt': datetime.utcnow().isoformat(),  
***REMOVED******REMOVED***'userId': user_id,
***REMOVED******REMOVED***'title': title
***REMOVED***
***REMOVED***## TODO: add some error handling based on the output of the upsert_item call
***REMOVED***resp = self.container_client.upsert_item(conversation)  
***REMOVED***if resp:
***REMOVED******REMOVED***return resp
***REMOVED***else:
***REMOVED******REMOVED***return False
***REMOVED***
***REMOVED***def upsert_conversation(self, conversation):
***REMOVED***resp = self.container_client.upsert_item(conversation)
***REMOVED***if resp:
***REMOVED******REMOVED***return resp
***REMOVED***else:
***REMOVED******REMOVED***return False

***REMOVED***def delete_conversation(self, user_id, conversation_id):
***REMOVED***conversation = self.container_client.read_item(item=conversation_id, partition_key=user_id)***REMOVED***
***REMOVED***if conversation:
***REMOVED******REMOVED***resp = self.container_client.delete_item(item=conversation_id, partition_key=user_id)
***REMOVED******REMOVED***return resp
***REMOVED***else:
***REMOVED******REMOVED***return True

***REMOVED***
***REMOVED***def delete_messages(self, conversation_id, user_id):
***REMOVED***## get a list of all the messages in the conversation
***REMOVED***messages = self.get_messages(user_id, conversation_id)
***REMOVED***response_list = []
***REMOVED***if messages:
***REMOVED******REMOVED***for message in messages:
***REMOVED******REMOVED***resp = self.container_client.delete_item(item=message['id'], partition_key=user_id)
***REMOVED******REMOVED***response_list.append(resp)
***REMOVED******REMOVED***return response_list


***REMOVED***def get_conversations(self, user_id, sort_order = 'DESC'):
***REMOVED***parameters = [
***REMOVED******REMOVED***{
***REMOVED******REMOVED***'name': '@userId',
***REMOVED******REMOVED***'value': user_id
***REMOVED***
***REMOVED***]
***REMOVED***query = f"SELECT * FROM c where c.userId = @userId and c.type='conversation' order by c.updatedAt {sort_order}"
***REMOVED***conversations = list(self.container_client.query_items(query=query, parameters=parameters,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***   enable_cross_partition_query =True))
***REMOVED***## if no conversations are found, return None
***REMOVED***if len(conversations) == 0:
***REMOVED******REMOVED***return []
***REMOVED***else:
***REMOVED******REMOVED***return conversations

***REMOVED***def get_conversation(self, user_id, conversation_id):
***REMOVED***parameters = [
***REMOVED******REMOVED***{
***REMOVED******REMOVED***'name': '@conversationId',
***REMOVED******REMOVED***'value': conversation_id
***REMOVED***,
***REMOVED******REMOVED***{
***REMOVED******REMOVED***'name': '@userId',
***REMOVED******REMOVED***'value': user_id
***REMOVED***
***REMOVED***]
***REMOVED***query = f"SELECT * FROM c where c.id = @conversationId and c.type='conversation' and c.userId = @userId"
***REMOVED***conversation = list(self.container_client.query_items(query=query, parameters=parameters,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***   enable_cross_partition_query =True))
***REMOVED***## if no conversations are found, return None
***REMOVED***if len(conversation) == 0:
***REMOVED******REMOVED***return None
***REMOVED***else:
***REMOVED******REMOVED***return conversation[0]
 
***REMOVED***def create_message(self, conversation_id, user_id, input_message: dict):
***REMOVED***message = {
***REMOVED******REMOVED***'id': str(uuid.uuid4()),
***REMOVED******REMOVED***'type': 'message',
***REMOVED******REMOVED***'userId' : user_id,
***REMOVED******REMOVED***'createdAt': datetime.utcnow().isoformat(),
***REMOVED******REMOVED***'updatedAt': datetime.utcnow().isoformat(),
***REMOVED******REMOVED***'conversationId' : conversation_id,
***REMOVED******REMOVED***'role': input_message['role'],
***REMOVED******REMOVED***'content': input_message['content']
***REMOVED***
***REMOVED***
***REMOVED***resp = self.container_client.upsert_item(message)  
***REMOVED***if resp:
***REMOVED******REMOVED***## update the parent conversations's updatedAt field with the current message's createdAt datetime value
***REMOVED******REMOVED***conversation = self.get_conversation(user_id, conversation_id)
***REMOVED******REMOVED***conversation['updatedAt'] = message['createdAt']
***REMOVED******REMOVED***self.upsert_conversation(conversation)
***REMOVED******REMOVED***return resp
***REMOVED***else:
***REMOVED******REMOVED***return False
***REMOVED***


***REMOVED***def get_messages(self, user_id, conversation_id):
***REMOVED***parameters = [
***REMOVED******REMOVED***{
***REMOVED******REMOVED***'name': '@conversationId',
***REMOVED******REMOVED***'value': conversation_id
***REMOVED***,
***REMOVED******REMOVED***{
***REMOVED******REMOVED***'name': '@userId',
***REMOVED******REMOVED***'value': user_id
***REMOVED***
***REMOVED***]
***REMOVED***query = f"SELECT * FROM c WHERE c.conversationId = @conversationId AND c.type='message' AND c.userId = @userId ORDER BY c.timestamp ASC"
***REMOVED***messages = list(self.container_client.query_items(query=query, parameters=parameters,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED*** enable_cross_partition_query =True))
***REMOVED***## if no messages are found, return false
***REMOVED***if len(messages) == 0:
***REMOVED******REMOVED***return []
***REMOVED***else:
***REMOVED******REMOVED***return messages

