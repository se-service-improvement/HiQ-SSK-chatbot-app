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

***REMOVED***user_object['user_principal_id'] = raw_user_object['X-Ms-Client-Principal-Id']
***REMOVED***user_object['user_name'] = raw_user_object['X-Ms-Client-Principal-Name']
***REMOVED***user_object['auth_provider'] = raw_user_object['X-Ms-Client-Principal-Idp']
***REMOVED***user_object['auth_token'] = raw_user_object['X-Ms-Token-Aad-Id-Token']
***REMOVED***user_object['client_principal_b64'] = raw_user_object['X-Ms-Client-Principal']
***REMOVED***user_object['aad_id_token'] = raw_user_object["X-Ms-Token-Aad-Id-Token"]

***REMOVED***return user_object