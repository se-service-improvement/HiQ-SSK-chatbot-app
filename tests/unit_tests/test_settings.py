import os
import pytest
from importlib import import_module, reload


@pytest.fixture(scope="function")
def dotenv_path(request):
***REMOVED***test_case_name = request.node.originalname.partition("test_")[2]
***REMOVED***return os.path.join(
***REMOVED***os.path.dirname(__file__),
***REMOVED***"dotenv_data",
***REMOVED***test_case_name
***REMOVED***)


@pytest.fixture(scope="function")
def app_settings(dotenv_path):
***REMOVED***# Reload module object to pick up new environment
***REMOVED***os.environ["DOTENV_PATH"] = dotenv_path
***REMOVED***settings_module = import_module("backend.settings")
***REMOVED***settings_module = reload(settings_module)
***REMOVED***
***REMOVED***yield getattr(settings_module, "app_settings")


def test_dotenv_no_datasource_1(app_settings):***REMOVED***
***REMOVED***# Validate model object
***REMOVED***assert app_settings.base_settings.datasource_type is None
***REMOVED***assert app_settings.datasource is None
***REMOVED***assert app_settings.azure_openai is not None
***REMOVED***
***REMOVED***
def test_dotenv_no_datasource_2(app_settings):***REMOVED***
***REMOVED***# Validate model object
***REMOVED***assert app_settings.datasource is None
***REMOVED***assert app_settings.azure_openai is not None

***REMOVED***
def test_dotenv_with_azure_search_success(app_settings):
***REMOVED***# Validate model object
***REMOVED***assert app_settings.search is not None
***REMOVED***assert app_settings.base_settings.datasource_type == "AzureCognitiveSearch"
***REMOVED***assert app_settings.datasource is not None
***REMOVED***assert app_settings.datasource.service == "search_service"
***REMOVED***assert app_settings.azure_openai is not None
***REMOVED***
***REMOVED***# Validate API payload structure
***REMOVED***payload = app_settings.datasource.construct_payload_configuration()
***REMOVED***assert payload["type"] == "azure_search"
***REMOVED***assert payload["parameters"] is not None
***REMOVED***assert payload["parameters"]["endpoint"] == "https://search_service.search.windows.net"
***REMOVED***print(payload)


def test_dotenv_with_elasticsearch_success(app_settings):
***REMOVED***# Validate model object
***REMOVED***assert app_settings.search is not None
***REMOVED***assert app_settings.base_settings.datasource_type == "Elasticsearch"
***REMOVED***assert app_settings.datasource is not None
***REMOVED***assert app_settings.datasource.endpoint == "dummy"
***REMOVED***assert app_settings.azure_openai is not None
***REMOVED***
***REMOVED***# Validate API payload structure
***REMOVED***payload = app_settings.datasource.construct_payload_configuration()
***REMOVED***assert payload["type"] == "elasticsearch"
***REMOVED***assert payload["parameters"] is not None
***REMOVED***assert payload["parameters"]["endpoint"] == "dummy"
***REMOVED***print(payload)
***REMOVED***
***REMOVED***
***REMOVED***

