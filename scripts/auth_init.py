import subprocess

from azure.identity import AzureDeveloperCliCredential
import urllib3

credential = AzureDeveloperCliCredential()

resp = urllib3.request(
***REMOVED***"POST",
***REMOVED***"https://graph.microsoft.com/v1.0/applications",
***REMOVED***headers={
***REMOVED***"Authorization": "Bearer "
***REMOVED***+ credential.get_token("https://graph.microsoft.com/.default").token,
***REMOVED***,
***REMOVED***json={
***REMOVED***"displayName": "WebApp",
***REMOVED***"signInAudience": "AzureADandPersonalMicrosoftAccount",
***REMOVED***"web": {"redirectUris": ["http://localhost:5000/.auth/login/aad/callback"]},
***REMOVED***,
***REMOVED***timeout=urllib3.Timeout(connect=10, read=10),
)

app_id = resp.json()["id"]
client_id = resp.json()["appId"]

# Add a client secret to the application
# using https://graph.microsoft.com/v1.0/applications/{id}/addPassword
# where {id} is the application ID returned from the previous step
resp = urllib3.request(
***REMOVED***"POST",
***REMOVED***f"https://graph.microsoft.com/v1.0/applications/{app_id}/addPassword",
***REMOVED***headers={
***REMOVED***"Authorization": "Bearer "
***REMOVED***+ credential.get_token("https://graph.microsoft.com/.default").token,
***REMOVED***,
***REMOVED***json={"passwordCredential": {"displayName": "WebAppSecret"}},
***REMOVED***timeout=urllib3.Timeout(connect=10, read=10),
)
client_secret = resp.json()["secretText"]

subprocess.run(f"azd env set AUTH_APP_ID {app_id}", shell=True)
subprocess.run(f"azd env set AUTH_CLIENT_ID {client_id}", shell=True)
subprocess.run(f"azd env set AUTH_CLIENT_SECRET {client_secret}", shell=True)
