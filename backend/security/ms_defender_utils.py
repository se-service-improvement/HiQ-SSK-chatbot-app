import json

def get_msdefender_user_json(authenticated_user_details, request_headers):
***REMOVED***auth_provider = authenticated_user_details.get('auth_provider')
***REMOVED***source_ip = request_headers.get('X-Forwarded-For', request_headers.get('Remote-Addr', ''))
***REMOVED***user_args = {
***REMOVED***"EndUserId": authenticated_user_details.get('user_principal_id'),
***REMOVED***"EndUserIdType": "EntraId" if auth_provider == "aad" else auth_provider,
***REMOVED***"SourceIp": source_ip.split(':')[0], #remove port
***REMOVED***
***REMOVED***return json.dumps(user_args)