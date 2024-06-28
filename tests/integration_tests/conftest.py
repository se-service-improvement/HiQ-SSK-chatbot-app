import json
import os
import pytest
from azure.identity import AzureCliCredential
from azure.keyvault.secrets import SecretClient
from pydantic.alias_generators import to_snake


VAULT_NAME = os.environ.get("VAULT_NAME")


@pytest.fixture(scope="module")
def secret_client() -> SecretClient: 
***REMOVED***kv_uri = f"https://{VAULT_NAME}.vault.azure.net"
***REMOVED***print(f"init secret_client from kv_uri={kv_uri}")
***REMOVED***credential = AzureCliCredential(additionally_allowed_tenants="*")
***REMOVED***return SecretClient(vault_url=kv_uri, credential=credential)


@pytest.fixture(scope="module")
def dotenv_template_params_from_kv(secret_client: SecretClient) -> dict[str, str]:
***REMOVED***secrets_properties_list = secret_client.list_properties_of_secrets()
***REMOVED***secrets = {}
***REMOVED***for secret in secrets_properties_list:
***REMOVED***secret_name = to_snake(secret.name).upper()
***REMOVED***secrets[secret_name] = secret_client.get_secret(secret.name).value

***REMOVED***return secrets


@pytest.fixture(scope="module")
def dotenv_template_params_from_env() -> dict[str, str]:
***REMOVED***def get_and_unset_variable(var_name):
***REMOVED***# we need this function to ensure that the environment is clean before
***REMOVED***# testing with generated dotenv files.
***REMOVED***var_value = os.getenv(var_name)
***REMOVED***os.environ[var_name] = ""
***REMOVED***return var_value
***REMOVED***
***REMOVED***env_secrets = [
***REMOVED***"AZURE_COSMOSDB_ACCOUNT",
***REMOVED***"AZURE_COSMOSDB_ACCOUNT_KEY",
***REMOVED***"AZURE_COSMOSDB_CONVERSATIONS_CONTAINER",
***REMOVED***"AZURE_COSMOSDB_DATABASE",
***REMOVED***"AZURE_OPENAI_EMBEDDING_NAME"
***REMOVED***"AZURE_OPENAI_ENDPOINT",
***REMOVED***"AZURE_OPENAI_MODEL",
***REMOVED***"AZURE_OPENAI_KEY",
***REMOVED***"AZURE_SEARCH_INDEX",
***REMOVED***"AZURE_SEARCH_KEY",
***REMOVED***"AZURE_SEARCH_QUERY",
***REMOVED***"AZURE_SEARCH_SERVICE",
***REMOVED***"ELASTICSEARCH_EMBEDDING_MODEL_ID",
***REMOVED***"ELASTICSEARCH_ENCODED_API_KEY",
***REMOVED***"ELASTICSEARCH_ENDPOINT",
***REMOVED***"ELASTICSEARCH_INDEX",
***REMOVED***"ELASTICSEARCH_QUERY"
***REMOVED***]
***REMOVED***
***REMOVED***return {s: get_and_unset_variable(s) for s in env_secrets}


@pytest.fixture(scope="module")
def dotenv_template_params(request, use_keyvault_secrets):
***REMOVED***if use_keyvault_secrets:
***REMOVED***return request.getfixturevalue("dotenv_template_params_from_kv")
***REMOVED***
***REMOVED***return request.getfixturevalue("dotenv_template_params_from_env")

