import argparse

from azure.identity import AzureDeveloperCliCredential
import urllib3


def update_redirect_uris(credential, app_id, uri):
***REMOVED***redirect_uris = [
***REMOVED******REMOVED******REMOVED***"http://localhost:5000/.auth/login/aad/callback",
***REMOVED******REMOVED******REMOVED***f"{uri}/.auth/login/aad/callback",
***REMOVED******REMOVED***]
***REMOVED***urllib3.request(
***REMOVED***"PATCH",
***REMOVED***f"https://graph.microsoft.com/v1.0/applications/{app_id}",
***REMOVED***headers={
***REMOVED******REMOVED***"Authorization": "Bearer "
***REMOVED******REMOVED***+ credential.get_token("https://graph.microsoft.com/.default").token,
***REMOVED***,
***REMOVED***json={
***REMOVED******REMOVED***"web": {
***REMOVED******REMOVED***"redirectUris": redirect_uris
***REMOVED***
***REMOVED***,
***REMOVED***)


if __name__ == "__main__":
***REMOVED***parser = argparse.ArgumentParser(
***REMOVED***description="Add a redirect URI to a registered application",
***REMOVED***epilog="Example: auth_update.py --appid 123 --uri https://abc.azureservices.net",
***REMOVED***)
***REMOVED***parser.add_argument(
***REMOVED***"--appid",
***REMOVED***required=False,
***REMOVED***help="Required. ID of the application to update.",
***REMOVED***)
***REMOVED***parser.add_argument(
***REMOVED***"--uri",
***REMOVED***required=False,
***REMOVED***help="Required. URI of the deployed application.",
***REMOVED***)
***REMOVED***args = parser.parse_args()

***REMOVED***credential = AzureDeveloperCliCredential()

***REMOVED***print(f"Updating application registration {args.appid} with redirect URI for {args.uri}")
***REMOVED***update_redirect_uris(credential, args.appid, args.uri)
