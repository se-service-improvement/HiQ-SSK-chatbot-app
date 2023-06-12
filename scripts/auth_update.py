import argparse
import subprocess

from azure.identity import AzureDeveloperCliCredential
import urllib3


def update_redirect_uris(credential, app_id, uri):
***REMOVED***urllib3.request(
***REMOVED***"PATCH",
***REMOVED***f"https://graph.microsoft.com/v1.0/applications/{app_id}",
***REMOVED***headers={
***REMOVED******REMOVED***"Authorization": "Bearer "
***REMOVED******REMOVED***+ credential.get_token("https://graph.microsoft.com/.default").token,
***REMOVED***,
***REMOVED***json={
***REMOVED******REMOVED***"web": {
***REMOVED******REMOVED***"redirectUris": [
***REMOVED******REMOVED******REMOVED***"http://localhost:5000/.auth/login/aad/callback",
***REMOVED******REMOVED******REMOVED***f"{uri}/.auth/login/aad/callback",
***REMOVED******REMOVED***]
***REMOVED***
***REMOVED***,
***REMOVED***)


if __name__ == "__main__":
***REMOVED***parser = argparse.ArgumentParser(
***REMOVED***description="Prepare documents by extracting content from PDFs, splitting content into sections and indexing in a search index.",
***REMOVED***epilog="Example: prepdocs.py --searchservice mysearch --index myindex",
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
***REMOVED***update_redirect_uris(credential, args.appid, args.uri)
