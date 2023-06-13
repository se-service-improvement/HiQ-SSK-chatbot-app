import argparse
import subprocess

from azure.identity import AzureDeveloperCliCredential
import urllib3


def get_auth_headers(credential):
***REMOVED***return {
***REMOVED***"Authorization": "Bearer "
***REMOVED***+ credential.get_token("https://graph.microsoft.com/.default").token
***REMOVED***


def check_for_application(credential, app_id):
***REMOVED***resp = urllib3.request(
***REMOVED***"GET",
***REMOVED***f"https://graph.microsoft.com/v1.0/applications/{app_id}",
***REMOVED***headers=get_auth_headers(credential),
***REMOVED***)
***REMOVED***if resp.status != 200:
***REMOVED***print("Application not found")
***REMOVED***return False
***REMOVED***return True


def create_application(credential):
***REMOVED***resp = urllib3.request(
***REMOVED***"POST",
***REMOVED***"https://graph.microsoft.com/v1.0/applications",
***REMOVED***headers=get_auth_headers(credential),
***REMOVED***json={
***REMOVED******REMOVED***"displayName": "WebApp",
***REMOVED******REMOVED***"signInAudience": "AzureADandPersonalMicrosoftAccount",
***REMOVED******REMOVED***"web": {
***REMOVED******REMOVED***"redirectUris": ["http://localhost:5000/.auth/login/aad/callback"],
***REMOVED******REMOVED***"implicitGrantSettings": {"enableIdTokenIssuance": True},
***REMOVED***,
***REMOVED***,
***REMOVED***timeout=urllib3.Timeout(connect=10, read=10),
***REMOVED***)

***REMOVED***app_id = resp.json()["id"]
***REMOVED***client_id = resp.json()["appId"]

***REMOVED***return app_id, client_id


def add_client_secret(credential, app_id):
***REMOVED***resp = urllib3.request(
***REMOVED***"POST",
***REMOVED***f"https://graph.microsoft.com/v1.0/applications/{app_id}/addPassword",
***REMOVED***headers=get_auth_headers(credential),
***REMOVED***json={"passwordCredential": {"displayName": "WebAppSecret"}},
***REMOVED***timeout=urllib3.Timeout(connect=10, read=10),
***REMOVED***)
***REMOVED***client_secret = resp.json()["secretText"]
***REMOVED***return client_secret


def update_azd_env(name, val):
***REMOVED***subprocess.run(f"azd env set {name} {val}", shell=True)


if __name__ == "__main__":
***REMOVED***parser = argparse.ArgumentParser(
***REMOVED***description="Create an App Registration and client secret (if not already created)",
***REMOVED***epilog="Example: auth_update.py",
***REMOVED***)
***REMOVED***parser.add_argument(
***REMOVED***"--appid",
***REMOVED***required=False,
***REMOVED***help="Optional. ID of registered application. If provided, this script just makes sure it exists.",
***REMOVED***)
***REMOVED***args = parser.parse_args()

***REMOVED***credential = AzureDeveloperCliCredential()

***REMOVED***if args.appid:
***REMOVED***print(f"Checking if application {args.appid} exists")
***REMOVED***if check_for_application(credential, args.appid):
***REMOVED******REMOVED***print("Application already exists, not creating new one.")
***REMOVED******REMOVED***exit(0)

***REMOVED***print("Creating application registration")
***REMOVED***app_id, client_id = create_application(credential)

***REMOVED***print(f"Adding client secret to {app_id}")
***REMOVED***client_secret = add_client_secret(credential, app_id)

***REMOVED***print("Updating azd env with AUTH_APP_ID, AUTH_CLIENT_ID, AUTH_CLIENT_SECRET")
***REMOVED***update_azd_env("AUTH_APP_ID", app_id)
***REMOVED***update_azd_env("AUTH_CLIENT_ID", client_id)
***REMOVED***update_azd_env("AUTH_CLIENT_SECRET", client_secret)
