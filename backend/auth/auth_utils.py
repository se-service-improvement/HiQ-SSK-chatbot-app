import base64
import json
import logging

def get_authenticated_user_details(request_headers):
***REMOVED***user_object = {}

***REMOVED***## check the headers for the Principal-Id (the guid of the signed in user)
***REMOVED***if "X-Ms-Client-Principal-Id" not in request_headers.keys():
***REMOVED***## if it's not, assume we're in development mode and return a default user
***REMOVED***from . import sample_user
***REMOVED***raw_user_object = sample_user.sample_user
***REMOVED***else:
***REMOVED***## if it is, get the user details from the EasyAuth headers
***REMOVED***raw_user_object = {k:v for k,v in request_headers.items()}

***REMOVED***user_object['user_principal_id'] = raw_user_object.get('X-Ms-Client-Principal-Id')
***REMOVED***user_object['user_name'] = raw_user_object.get('X-Ms-Client-Principal-Name')
***REMOVED***user_object['auth_provider'] = raw_user_object.get('X-Ms-Client-Principal-Idp')
***REMOVED***user_object['auth_token'] = raw_user_object.get('X-Ms-Token-Aad-Id-Token')
***REMOVED***user_object['client_principal_b64'] = raw_user_object.get('X-Ms-Client-Principal')
***REMOVED***user_object['aad_id_token'] = raw_user_object.get('X-Ms-Token-Aad-Id-Token')

***REMOVED***return user_object

def get_tenantid(client_principal_b64):
***REMOVED***tenant_id = ''
***REMOVED***if client_principal_b64:   
***REMOVED***try:
***REMOVED******REMOVED***# Decode the base64 header to get the JSON string
***REMOVED******REMOVED***decoded_bytes = base64.b64decode(client_principal_b64)
***REMOVED******REMOVED***decoded_string = decoded_bytes.decode('utf-8')
***REMOVED******REMOVED***# Convert the JSON string1into a Python dictionary
***REMOVED******REMOVED***user_info = json.loads(decoded_string)
***REMOVED******REMOVED***# Extract the tenant ID
***REMOVED******REMOVED***tenant_id = user_info.get('tid')  # 'tid' typically holds the tenant ID
***REMOVED***except Exception as ex:
***REMOVED******REMOVED***logging.exception(ex)
***REMOVED***return tenant_id