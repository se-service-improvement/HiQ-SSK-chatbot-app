import os
import pytest
from tempfile import NamedTemporaryFile
from importlib import import_module, reload
from jinja2 import FileSystemLoader
from jinja2 import Environment
from quart import Quart


datasources = [
***REMOVED***"AzureCognitiveSearch",
***REMOVED***"Elasticsearch",
***REMOVED***"none"  # TODO: add tests for additional data sources
]


def render_template_to_tempfile(
***REMOVED***template_prefix,
***REMOVED***input_template,
***REMOVED*****template_params
):
***REMOVED***template_environment = Environment()
***REMOVED***template_environment.loader = FileSystemLoader(
***REMOVED***os.path.dirname(input_template)
***REMOVED***)
***REMOVED***template_environment.trim_blocks = True
***REMOVED***template = template_environment.get_template(
***REMOVED***os.path.basename(input_template)
***REMOVED***)

***REMOVED***with NamedTemporaryFile(
***REMOVED***'w',
***REMOVED***prefix=f"{template_prefix}-",
***REMOVED***delete=False
***REMOVED***) as g:
***REMOVED***g.write(template.render(**template_params))
***REMOVED***rendered_output = g.name

***REMOVED***print(f"Rendered template at {rendered_output}")
***REMOVED***return rendered_output


@pytest.fixture(scope="function", params=datasources, ids=datasources)
def datasource(request):
***REMOVED***return request.param


@pytest.fixture(scope="function", params=[True, False], ids=["with_chat_history", "no_chat_history"])
def enable_chat_history(request):
***REMOVED***return request.param


@pytest.fixture(scope="function", params=[True, False], ids=["streaming", "nonstreaming"])
def stream(request):
***REMOVED***return request.param


@pytest.fixture(scope="function", params=[True, False], ids=["with_aoai_embeddings", "no_aoai_embeddings"])
def use_aoai_embeddings(request):
***REMOVED***return request.param


@pytest.fixture(scope="function", params=[True, False], ids=["with_es_embeddings", "no_es_embeddings"])
def use_elasticsearch_embeddings(request):
***REMOVED***return request.param


@pytest.fixture(scope="function")
def dotenv_rendered_template_path(
***REMOVED***request,
***REMOVED***dotenv_template_params,
***REMOVED***datasource,
***REMOVED***enable_chat_history,
***REMOVED***stream, 
***REMOVED***use_aoai_embeddings,
***REMOVED***use_elasticsearch_embeddings
):
***REMOVED***rendered_template_name = request.node.name.replace("[", "_").replace("]", "_")
***REMOVED***template_path = os.path.join(
***REMOVED***os.path.dirname(__file__),
***REMOVED***"dotenv_templates",
***REMOVED***"dotenv.jinja2"
***REMOVED***)

***REMOVED***if datasource != "none":
***REMOVED***dotenv_template_params["datasourceType"] = datasource
***REMOVED***
***REMOVED***if datasource != "Elasticsearch" and use_elasticsearch_embeddings:
***REMOVED***pytest.skip("Elasticsearch embeddings not supported for test.")
***REMOVED***
***REMOVED***if datasource == "Elasticsearch":
***REMOVED***dotenv_template_params["useElasticsearchEmbeddings"] = use_elasticsearch_embeddings
***REMOVED***
***REMOVED***dotenv_template_params["useAoaiEmbeddings"] = use_aoai_embeddings
***REMOVED***
***REMOVED***if use_aoai_embeddings or use_elasticsearch_embeddings:
***REMOVED***dotenv_template_params["azureSearchQueryType"] = "vector"
***REMOVED***dotenv_template_params["elasticsearchQueryType"] = "vector"
***REMOVED***else:
***REMOVED***dotenv_template_params["azureSearchQueryType"] = "simple"
***REMOVED***dotenv_template_params["elasticsearchQueryType"] = "simple"
***REMOVED***
***REMOVED***dotenv_template_params["enableChatHistory"] = enable_chat_history
***REMOVED***dotenv_template_params["azureOpenaiStream"] = stream
***REMOVED***
***REMOVED***return render_template_to_tempfile(
***REMOVED***rendered_template_name,
***REMOVED***template_path,
***REMOVED*****dotenv_template_params
***REMOVED***)


@pytest.fixture(scope="function")
def test_app(dotenv_rendered_template_path) -> Quart:
***REMOVED***os.environ["DOTENV_PATH"] = dotenv_rendered_template_path
***REMOVED***app_module = import_module("app")
***REMOVED***app_module = reload(app_module)
***REMOVED***
***REMOVED***app = getattr(app_module, "app")
***REMOVED***return app


@pytest.mark.asyncio
async def test_dotenv(test_app: Quart, dotenv_template_params: dict[str, str]):
***REMOVED***if dotenv_template_params["datasourceType"] == "AzureCognitiveSearch":
***REMOVED***message_content = dotenv_template_params["azureSearchQuery"]
***REMOVED***
***REMOVED***elif dotenv_template_params["datasourceType"] == "Elasticsearch":
***REMOVED***message_content = dotenv_template_params["elasticsearchQuery"]
***REMOVED***
***REMOVED***else:
***REMOVED***message_content = "What is Contoso?"
***REMOVED***
***REMOVED***request_path = "/conversation"
***REMOVED***request_data = {
***REMOVED***"messages": [
***REMOVED******REMOVED***{
***REMOVED******REMOVED***"role": "user",
***REMOVED******REMOVED***"content": message_content
***REMOVED***
***REMOVED***]
***REMOVED***
***REMOVED***test_client = test_app.test_client()
***REMOVED***response = await test_client.post(request_path, json=request_data)
***REMOVED***assert response.status_code == 200
***REMOVED***response_content = await response.get_data()
***REMOVED***print(response_content)
