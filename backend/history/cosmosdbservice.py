import uuid
from datetime import datetime
from azure.cosmos.aio import CosmosClient
from azure.cosmos import exceptions
  
class CosmosConversationClient():
***REMOVED***
***REMOVED***def __init__(self, cosmosdb_endpoint: str, credential: any, database_name: str, container_name: str, enable_message_feedback: bool = False):
***REMOVED***self.cosmosdb_endpoint = cosmosdb_endpoint
***REMOVED***self.credential = credential
***REMOVED***self.database_name = database_name
***REMOVED***self.container_name = container_name
***REMOVED***self.enable_message_feedback = enable_message_feedback
***REMOVED***try:
***REMOVED******REMOVED***self.cosmosdb_client = CosmosClient(self.cosmosdb_endpoint, credential=credential)
***REMOVED***except exceptions.CosmosHttpResponseError as e:
***REMOVED******REMOVED***if e.status_code == 401:
***REMOVED******REMOVED***raise ValueError("Invalid credentials") from e
***REMOVED******REMOVED***else:
***REMOVED******REMOVED***raise ValueError("Invalid CosmosDB endpoint") from e

***REMOVED***try:
***REMOVED******REMOVED***self.database_client = self.cosmosdb_client.get_database_client(database_name)
***REMOVED***except exceptions.CosmosResourceNotFoundError:
***REMOVED******REMOVED***raise ValueError("Invalid CosmosDB database name") 
***REMOVED***
***REMOVED***try:
***REMOVED******REMOVED***self.container_client = self.database_client.get_container_client(container_name)
***REMOVED***except exceptions.CosmosResourceNotFoundError:
***REMOVED******REMOVED***raise ValueError("Invalid CosmosDB container name") 
***REMOVED***

***REMOVED***async def ensure(self):
***REMOVED***if not self.cosmosdb_client or not self.database_client or not self.container_client:
***REMOVED******REMOVED***return False, "CosmosDB client not initialized correctly"
***REMOVED******REMOVED***
***REMOVED***try:
***REMOVED******REMOVED***database_info = await self.database_client.read()
***REMOVED***except:
***REMOVED******REMOVED***return False, f"CosmosDB database {self.database_name} on account {self.cosmosdb_endpoint} not found"
***REMOVED***
***REMOVED***try:
***REMOVED******REMOVED***container_info = await self.container_client.read()
***REMOVED***except:
***REMOVED******REMOVED***return False, f"CosmosDB container {self.container_name} not found"
***REMOVED******REMOVED***
***REMOVED***return True, "CosmosDB client initialized successfully"

***REMOVED***async def create_conversation(self, user_id, title = ''):
***REMOVED***conversation = {
***REMOVED******REMOVED***'id': str(uuid.uuid4()),  
***REMOVED******REMOVED***'type': 'conversation',
***REMOVED******REMOVED***'createdAt': datetime.utcnow().isoformat(),  
***REMOVED******REMOVED***'updatedAt': datetime.utcnow().isoformat(),  
***REMOVED******REMOVED***'userId': user_id,
***REMOVED******REMOVED***'title': title
***REMOVED***
***REMOVED***## TODO: add some error handling based on the output of the upsert_item call
***REMOVED***resp = await self.container_client.upsert_item(conversation)  
***REMOVED***if resp:
***REMOVED******REMOVED***return resp
***REMOVED***else:
***REMOVED******REMOVED***return False
***REMOVED***
***REMOVED***async def upsert_conversation(self, conversation):
***REMOVED***resp = await self.container_client.upsert_item(conversation)
***REMOVED***if resp:
***REMOVED******REMOVED***return resp
***REMOVED***else:
***REMOVED******REMOVED***return False

***REMOVED***async def delete_conversation(self, user_id, conversation_id):
***REMOVED***conversation = await self.container_client.read_item(item=conversation_id, partition_key=user_id)***REMOVED***
***REMOVED***if conversation:
***REMOVED******REMOVED***resp = await self.container_client.delete_item(item=conversation_id, partition_key=user_id)
***REMOVED******REMOVED***return resp
***REMOVED***else:
***REMOVED******REMOVED***return True

***REMOVED***
***REMOVED***async def delete_messages(self, conversation_id, user_id):
***REMOVED***## get a list of all the messages in the conversation
***REMOVED***messages = await self.get_messages(user_id, conversation_id)
***REMOVED***response_list = []
***REMOVED***if messages:
***REMOVED******REMOVED***for message in messages:
***REMOVED******REMOVED***resp = await self.container_client.delete_item(item=message['id'], partition_key=user_id)
***REMOVED******REMOVED***response_list.append(resp)
***REMOVED******REMOVED***return response_list


***REMOVED***async def get_conversations(self, user_id, limit, sort_order = 'DESC', offset = 0):
***REMOVED***parameters = [
***REMOVED******REMOVED***{
***REMOVED******REMOVED***'name': '@userId',
***REMOVED******REMOVED***'value': user_id
***REMOVED***
***REMOVED***]
***REMOVED***query = f"SELECT * FROM c where c.userId = @userId and c.type='conversation' order by c.updatedAt {sort_order}"
***REMOVED***if limit is not None:
***REMOVED******REMOVED***query += f" offset {offset} limit {limit}" 
***REMOVED***
***REMOVED***conversations = []
***REMOVED***async for item in self.container_client.query_items(query=query, parameters=parameters):
***REMOVED******REMOVED***conversations.append(item)
***REMOVED***
***REMOVED***return conversations

***REMOVED***async def get_conversation(self, user_id, conversation_id):
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
***REMOVED***conversations = []
***REMOVED***async for item in self.container_client.query_items(query=query, parameters=parameters):
***REMOVED******REMOVED***conversations.append(item)

***REMOVED***## if no conversations are found, return None
***REMOVED***if len(conversations) == 0:
***REMOVED******REMOVED***return None
***REMOVED***else:
***REMOVED******REMOVED***return conversations[0]
 
***REMOVED***async def create_message(self, uuid, conversation_id, user_id, input_message: dict):
***REMOVED***message = {
***REMOVED******REMOVED***'id': uuid,
***REMOVED******REMOVED***'type': 'message',
***REMOVED******REMOVED***'userId' : user_id,
***REMOVED******REMOVED***'createdAt': datetime.utcnow().isoformat(),
***REMOVED******REMOVED***'updatedAt': datetime.utcnow().isoformat(),
***REMOVED******REMOVED***'conversationId' : conversation_id,
***REMOVED******REMOVED***'role': input_message['role'],
***REMOVED******REMOVED***'content': input_message['content']
***REMOVED***

***REMOVED***if self.enable_message_feedback:
***REMOVED******REMOVED***message['feedback'] = ''
***REMOVED***
***REMOVED***resp = await self.container_client.upsert_item(message)  
***REMOVED***if resp:
***REMOVED******REMOVED***## update the parent conversations's updatedAt field with the current message's createdAt datetime value
***REMOVED******REMOVED***conversation = await self.get_conversation(user_id, conversation_id)
***REMOVED******REMOVED***if not conversation:
***REMOVED******REMOVED***return "Conversation not found"
***REMOVED******REMOVED***conversation['updatedAt'] = message['createdAt']
***REMOVED******REMOVED***await self.upsert_conversation(conversation)
***REMOVED******REMOVED***return resp
***REMOVED***else:
***REMOVED******REMOVED***return False
***REMOVED***
***REMOVED***async def update_message_feedback(self, user_id, message_id, feedback):
***REMOVED***message = await self.container_client.read_item(item=message_id, partition_key=user_id)
***REMOVED***if message:
***REMOVED******REMOVED***message['feedback'] = feedback
***REMOVED******REMOVED***resp = await self.container_client.upsert_item(message)
***REMOVED******REMOVED***return resp
***REMOVED***else:
***REMOVED******REMOVED***return False

***REMOVED***async def get_messages(self, user_id, conversation_id):
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
***REMOVED***messages = []
***REMOVED***async for item in self.container_client.query_items(query=query, parameters=parameters):
***REMOVED******REMOVED***messages.append(item)

***REMOVED***return messages

