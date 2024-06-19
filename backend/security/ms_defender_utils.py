import json

def get_msdefender_user_json(authenticated_user_details, request_headers, conversation_id):
***REMOVED***auth_provider = authenticated_user_details.get('auth_provider')
***REMOVED***source_ip = request_headers.get('Remote-Addr', '')
***REMOVED***header_names = ['User-Agent', 'X-Forwarded-For', 'Forwarded', 'X-Real-IP', 'True-Client-IP', 'CF-Connecting-IP']
***REMOVED***user_args = {
***REMOVED***"EndUserId": authenticated_user_details.get('user_principal_id'),
***REMOVED***"EndUserIdType": "EntraId" if auth_provider == "aad" else auth_provider,
***REMOVED***"SourceIp": source_ip.split(':')[0], #remove port
***REMOVED***"SourceRequestHeaders": {header: request_headers[header] for header in header_names if header in request_headers},
***REMOVED***"ConversationId": conversation_id,
***REMOVED***
***REMOVED***return json.dumps(user_args)