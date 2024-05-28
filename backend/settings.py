import os
import json
import logging
from abc import ABC, abstractmethod
from pydantic import (
***REMOVED***BaseModel,
***REMOVED***confloat,
***REMOVED***conint,
***REMOVED***conlist,
***REMOVED***Field,
***REMOVED***field_validator,
***REMOVED***model_validator,
***REMOVED***PrivateAttr,
***REMOVED***ValidationError,
***REMOVED***ValidationInfo
)
from pydantic.alias_generators import to_snake
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Literal, Optional
from typing_extensions import Self
from quart import Request
from backend.utils import parse_multi_columns, generateFilterString

DOTENV_PATH = os.environ.get(
***REMOVED***"DOTENV_PATH",
***REMOVED***os.path.join(
***REMOVED***os.path.dirname(
***REMOVED******REMOVED***os.path.dirname(__file__)
***REMOVED***),
***REMOVED***".env"
***REMOVED***)
)
MINIMUM_SUPPORTED_AZURE_OPENAI_PREVIEW_API_VERSION = "2024-05-01-preview"


class _UiSettings(BaseSettings):
***REMOVED***model_config = SettingsConfigDict(
***REMOVED***env_prefix="UI_",
***REMOVED***env_file=DOTENV_PATH,
***REMOVED***extra="ignore",
***REMOVED***env_ignore_empty=True
***REMOVED***)

***REMOVED***title: str = "Contoso"
***REMOVED***logo: Optional[str] = None
***REMOVED***chat_logo: Optional[str] = None
***REMOVED***chat_title: str = "Start chatting"
***REMOVED***chat_description: str = "This chatbot is configured to answer your questions"
***REMOVED***favicon: str = "/favicon.ico"
***REMOVED***show_share_button: bool = True


class _ChatHistorySettings(BaseSettings):
***REMOVED***model_config = SettingsConfigDict(
***REMOVED***env_prefix="AZURE_COSMOSDB_",
***REMOVED***env_file=DOTENV_PATH,
***REMOVED***extra="ignore",
***REMOVED***env_ignore_empty=True
***REMOVED***)

***REMOVED***database: str
***REMOVED***account: str
***REMOVED***account_key: str
***REMOVED***conversations_container: str
***REMOVED***enable_feedback: bool = False


class _PromptflowSettings(BaseSettings):
***REMOVED***model_config = SettingsConfigDict(
***REMOVED***env_prefix="PROMPTFLOW_",
***REMOVED***env_file=DOTENV_PATH,
***REMOVED***extra="ignore",
***REMOVED***env_ignore_empty=True
***REMOVED***)

***REMOVED***endpoint: str
***REMOVED***api_key: str
***REMOVED***response_timeout: float = 30.0
***REMOVED***request_field_name: str = "query"
***REMOVED***response_field_name: str = "reply"
***REMOVED***citations_field_name: str = "documents"


class _AzureOpenAIFunction(BaseModel):
***REMOVED***name: str = Field(..., min_length=1)
***REMOVED***description: str = Field(..., min_length=1)
***REMOVED***parameters: Optional[dict] = None


class _AzureOpenAITool(BaseModel):
***REMOVED***type: Literal['function'] = 'function'
***REMOVED***function: _AzureOpenAIFunction
***REMOVED***

class _AzureOpenAISettings(BaseSettings):
***REMOVED***model_config = SettingsConfigDict(
***REMOVED***env_prefix="AZURE_OPENAI_",
***REMOVED***env_file=DOTENV_PATH,
***REMOVED***extra='ignore',
***REMOVED***env_ignore_empty=True
***REMOVED***)
***REMOVED***
***REMOVED***model: str
***REMOVED***key: str
***REMOVED***resource: Optional[str] = None
***REMOVED***endpoint: Optional[str] = None
***REMOVED***temperature: float = 0
***REMOVED***top_p: float = 0
***REMOVED***max_tokens: int = 1000
***REMOVED***stream: bool = True
***REMOVED***stop_sequence: Optional[List[str]] = None
***REMOVED***seed: Optional[int] = None
***REMOVED***choices_count: Optional[conint(ge=1, le=128)] = Field(default=1, serialization_alias="n")
***REMOVED***user: Optional[str] = None
***REMOVED***tools: Optional[conlist(_AzureOpenAITool, min_length=1)] = None
***REMOVED***tool_choice: Optional[str] = None
***REMOVED***logit_bias: Optional[dict] = None
***REMOVED***presence_penalty: Optional[confloat(ge=-2.0, le=2.0)] = 0.0
***REMOVED***frequency_penalty: Optional[confloat(ge=-2.0, le=2.0)] = 0.0
***REMOVED***system_message: str = "You are an AI assistant that helps people find information."
***REMOVED***preview_api_version: str = MINIMUM_SUPPORTED_AZURE_OPENAI_PREVIEW_API_VERSION
***REMOVED***embedding_endpoint: Optional[str] = None
***REMOVED***embedding_key: Optional[str] = None
***REMOVED***embedding_name: Optional[str] = None
***REMOVED***
***REMOVED***@field_validator('tools', mode='before')
***REMOVED***@classmethod
***REMOVED***def deserialize_tools(cls, tools_json_str: str) -> List[_AzureOpenAITool]:
***REMOVED***if isinstance(tools_json_str, str):
***REMOVED******REMOVED***try:
***REMOVED******REMOVED***tools_dict = json.loads(tools_json_str)
***REMOVED******REMOVED***return _AzureOpenAITool(**tools_dict)
***REMOVED******REMOVED***except json.JSONDecodeError:
***REMOVED******REMOVED***logging.warning("No valid tool definition found in the environment.  If you believe this to be in error, please check that the value of AZURE_OPENAI_TOOLS is a valid JSON string.")
***REMOVED******REMOVED***
***REMOVED******REMOVED***except ValidationError as e:
***REMOVED******REMOVED***logging.warning(f"An error occurred while deserializing the tool definition - {str(e)}")
***REMOVED******REMOVED***
***REMOVED***return None
***REMOVED***
***REMOVED***@field_validator('logit_bias', mode='before')
***REMOVED***@classmethod
***REMOVED***def deserialize_logit_bias(cls, logit_bias_json_str: str) -> dict:
***REMOVED***if isinstance(logit_bias_json_str, str):
***REMOVED******REMOVED***try:
***REMOVED******REMOVED***return json.loads(logit_bias_json_str)
***REMOVED******REMOVED***except json.JSONDecodeError as e:
***REMOVED******REMOVED***logging.warning(f"An error occurred while deserializing the logit bias string -- {str(e)}")
***REMOVED******REMOVED***
***REMOVED***return None
***REMOVED***
***REMOVED***@field_validator('stop_sequence', mode='before')
***REMOVED***@classmethod
***REMOVED***def split_contexts(cls, comma_separated_string: str) -> List[str]:
***REMOVED***if isinstance(comma_separated_string, str) and len(comma_separated_string) > 0:
***REMOVED******REMOVED***return parse_multi_columns(comma_separated_string)
***REMOVED***
***REMOVED***return None
***REMOVED***
***REMOVED***@model_validator(mode="after")
***REMOVED***def ensure_endpoint(self) -> Self:
***REMOVED***if self.endpoint:
***REMOVED******REMOVED***return Self
***REMOVED***
***REMOVED***elif self.resource:
***REMOVED******REMOVED***self.endpoint = f"https://{self.resource}.openai.azure.com"
***REMOVED******REMOVED***return Self
***REMOVED***
***REMOVED***raise ValidationError("AZURE_OPENAI_ENDPOINT or AZURE_OPENAI_RESOURCE is required")
***REMOVED***
***REMOVED***def extract_embedding_dependency(self) -> Optional[dict]:
***REMOVED***if self.embedding_name:
***REMOVED******REMOVED***return {
***REMOVED******REMOVED***"type": "deployment_name",
***REMOVED******REMOVED***"deployment_name": self.embedding_name
***REMOVED***
***REMOVED***
***REMOVED***elif self.embedding_endpoint and self.embedding_key:
***REMOVED******REMOVED***return {
***REMOVED******REMOVED***"type": "endpoint",
***REMOVED******REMOVED***"endpoint": self.embedding_endpoint,
***REMOVED******REMOVED***"authentication": {
***REMOVED******REMOVED******REMOVED***"type": "api_key",
***REMOVED******REMOVED******REMOVED***"api_key": self.embedding_key
***REMOVED******REMOVED***
***REMOVED***
***REMOVED***else:   
***REMOVED******REMOVED***return None
***REMOVED***

class _SearchCommonSettings(BaseSettings):
***REMOVED***model_config = SettingsConfigDict(
***REMOVED***env_prefix="SEARCH_",
***REMOVED***env_file=DOTENV_PATH,
***REMOVED***extra="ignore",
***REMOVED***env_ignore_empty=True
***REMOVED***)
***REMOVED***max_search_queries: Optional[int] = None
***REMOVED***allow_partial_result: bool = False
***REMOVED***include_contexts: Optional[List[str]] = ["citations", "intent"]
***REMOVED***vectorization_dimensions: Optional[int] = None
***REMOVED***role_information: str = Field(
***REMOVED***validation_alias="AZURE_OPENAI_SYSTEM_MESSAGE"
***REMOVED***)

***REMOVED***@field_validator('include_contexts', mode='before')
***REMOVED***@classmethod
***REMOVED***def split_contexts(cls, comma_separated_string: str, info: ValidationInfo) -> List[str]:
***REMOVED***if isinstance(comma_separated_string, str) and len(comma_separated_string) > 0:
***REMOVED******REMOVED***return parse_multi_columns(comma_separated_string)
***REMOVED***
***REMOVED***return cls.model_fields[info.field_name].get_default()


class DatasourcePayloadConstructor(BaseModel, ABC):
***REMOVED***_settings: '_AppSettings' = PrivateAttr()
***REMOVED***
***REMOVED***def __init__(self, settings: '_AppSettings', **data):
***REMOVED***super().__init__(**data)
***REMOVED***self._settings = settings
***REMOVED***
***REMOVED***@abstractmethod
***REMOVED***def construct_payload_configuration(
***REMOVED***self,
***REMOVED****args,
***REMOVED*****kwargs
***REMOVED***):
***REMOVED***pass


class _AzureSearchSettings(BaseSettings, DatasourcePayloadConstructor):
***REMOVED***model_config = SettingsConfigDict(
***REMOVED***env_prefix="AZURE_SEARCH_",
***REMOVED***env_file=DOTENV_PATH,
***REMOVED***extra="ignore",
***REMOVED***env_ignore_empty=True
***REMOVED***)
***REMOVED***_type: Literal["azure_search"] = PrivateAttr(default="azure_search")
***REMOVED***top_k: int = Field(default=5, serialization_alias="top_n_documents")
***REMOVED***strictness: int = 3
***REMOVED***enable_in_domain: bool = Field(default=True, serialization_alias="in_scope")
***REMOVED***service: str = Field(exclude=True)
***REMOVED***endpoint_suffix: str = Field(default="search.windows.net", exclude=True)
***REMOVED***index: str = Field(serialization_alias="index_name")
***REMOVED***key: Optional[str] = Field(default=None, exclude=True)
***REMOVED***use_semantic_search: bool = Field(default=False, exclude=True)
***REMOVED***semantic_search_config: str = Field(default="", serialization_alias="semantic_configuration")
***REMOVED***content_columns: Optional[List[str]] = Field(default=None, exclude=True)
***REMOVED***vector_columns: Optional[List[str]] = Field(default=None, exclude=True)
***REMOVED***title_column: Optional[str] = Field(default=None, exclude=True)
***REMOVED***url_column: Optional[str] = Field(default=None, exclude=True)
***REMOVED***filename_column: Optional[str] = Field(default=None, exclude=True)
***REMOVED***query_type: Literal[
***REMOVED***'simple',
***REMOVED***'vector',
***REMOVED***'semantic',
***REMOVED***'vector_simple_hybrid',
***REMOVED***'vectorSimpleHybrid',
***REMOVED***'vector_semantic_hybrid',
***REMOVED***'vectorSemanticHybrid'
***REMOVED***] = "simple"
***REMOVED***permitted_groups_column: Optional[str] = Field(default=None, exclude=True)
***REMOVED***
***REMOVED***# Constructed fields
***REMOVED***endpoint: Optional[str] = None
***REMOVED***authentication: Optional[dict] = None
***REMOVED***embedding_dependency: Optional[dict] = None
***REMOVED***fields_mapping: Optional[dict] = None
***REMOVED***filter: Optional[str] = Field(default=None, exclude=True)
***REMOVED***
***REMOVED***@field_validator('content_columns', 'vector_columns', mode="before")
***REMOVED***@classmethod
***REMOVED***def split_columns(cls, comma_separated_string: str) -> List[str]:
***REMOVED***if isinstance(comma_separated_string, str) and len(comma_separated_string) > 0:
***REMOVED******REMOVED***return parse_multi_columns(comma_separated_string)
***REMOVED***
***REMOVED***return None
***REMOVED***
***REMOVED***@model_validator(mode="after")
***REMOVED***def set_endpoint(self) -> Self:
***REMOVED***self.endpoint = f"https://{self.service}.{self.endpoint_suffix}"
***REMOVED***return self
***REMOVED***
***REMOVED***@model_validator(mode="after")
***REMOVED***def set_authentication(self) -> Self:
***REMOVED***if self.key:
***REMOVED******REMOVED***self.authentication = {"type": "api_key", "key": self.key}
***REMOVED***else:
***REMOVED******REMOVED***self.authentication = {"type": "system_assigned_managed_identity"}
***REMOVED******REMOVED***
***REMOVED***return self
***REMOVED***
***REMOVED***@model_validator(mode="after")
***REMOVED***def set_fields_mapping(self) -> Self:
***REMOVED***self.fields_mapping = {
***REMOVED******REMOVED***"content_fields": self.content_columns,
***REMOVED******REMOVED***"title_field": self.title_column,
***REMOVED******REMOVED***"url_field": self.url_column,
***REMOVED******REMOVED***"filepath_field": self.filename_column,
***REMOVED******REMOVED***"vector_fields": self.vector_columns
***REMOVED***
***REMOVED***return self
***REMOVED***
***REMOVED***@model_validator(mode="after")
***REMOVED***def set_query_type(self) -> Self:
***REMOVED***self.query_type = to_snake(self.query_type)

***REMOVED***def _set_filter_string(self, request: Request) -> str:
***REMOVED***if self.permitted_groups_column:
***REMOVED******REMOVED***user_token = request.headers.get("X-MS-TOKEN-AAD-ACCESS-TOKEN", "")
***REMOVED******REMOVED***logging.debug(f"USER TOKEN is {'present' if user_token else 'not present'}")
***REMOVED******REMOVED***if not user_token:
***REMOVED******REMOVED***raise ValueError(
***REMOVED******REMOVED******REMOVED***"Document-level access control is enabled, but user access token could not be fetched."
***REMOVED******REMOVED***)

***REMOVED******REMOVED***filter_string = generateFilterString(user_token)
***REMOVED******REMOVED***logging.debug(f"FILTER: {filter_string}")
***REMOVED******REMOVED***return filter_string
***REMOVED***
***REMOVED***return None
***REMOVED******REMOVED***
***REMOVED***def construct_payload_configuration(
***REMOVED***self,
***REMOVED****args,
***REMOVED*****kwargs
***REMOVED***):
***REMOVED***request = kwargs.pop('request', None)
***REMOVED***if request and self.permitted_groups_column:
***REMOVED******REMOVED***self.filter = self._set_filter_string(request)
***REMOVED******REMOVED***
***REMOVED***self.embedding_dependency = \
***REMOVED******REMOVED***self._settings.azure_openai.extract_embedding_dependency()
***REMOVED***parameters = self.model_dump(exclude_none=True, by_alias=True)
***REMOVED***parameters.update(self._settings.search.model_dump(exclude_none=True, by_alias=True))
***REMOVED***
***REMOVED***return {
***REMOVED******REMOVED***"type": self._type,
***REMOVED******REMOVED***"parameters": parameters
***REMOVED***


class _AzureCosmosDbMongoVcoreSettings(
***REMOVED***BaseSettings,
***REMOVED***DatasourcePayloadConstructor
):
***REMOVED***model_config = SettingsConfigDict(
***REMOVED***env_prefix="AZURE_COSMOSDB_MONGO_VCORE_",
***REMOVED***env_file=DOTENV_PATH,
***REMOVED***extra="ignore",
***REMOVED***env_ignore_empty=True
***REMOVED***)
***REMOVED***_type: Literal["azure_cosmosdb"] = PrivateAttr(default="azure_cosmosdb")
***REMOVED***top_k: int = Field(default=5, serialization_alias="top_n_documents")
***REMOVED***strictness: int = 3
***REMOVED***enable_in_domain: bool = Field(default=True, serialization_alias="in_scope")
***REMOVED***query_type: Literal['vector'] = "vector"
***REMOVED***connection_string: str = Field(exclude=True)
***REMOVED***index: str = Field(serialization_alias="index_name")
***REMOVED***database: str = Field(serialization_alias="database_name")
***REMOVED***container: str = Field(serialization_alias="container_name")
***REMOVED***content_columns: Optional[List[str]] = Field(default=None, exclude=True)
***REMOVED***vector_columns: Optional[List[str]] = Field(default=None, exclude=True)
***REMOVED***title_column: Optional[str] = Field(default=None, exclude=True)
***REMOVED***url_column: Optional[str] = Field(default=None, exclude=True)
***REMOVED***filename_column: Optional[str] = Field(default=None, exclude=True)
***REMOVED***
***REMOVED***# Constructed fields
***REMOVED***authentication: Optional[dict] = None
***REMOVED***embedding_dependency: Optional[dict] = None
***REMOVED***fields_mapping: Optional[dict] = None
***REMOVED***
***REMOVED***@field_validator('content_columns', 'vector_columns', mode="before")
***REMOVED***@classmethod
***REMOVED***def split_columns(cls, comma_separated_string: str) -> List[str]:
***REMOVED***if isinstance(comma_separated_string, str) and len(comma_separated_string) > 0:
***REMOVED******REMOVED***return parse_multi_columns(comma_separated_string)
***REMOVED***
***REMOVED***return None
***REMOVED***
***REMOVED***@model_validator(mode="after")
***REMOVED***def construct_authentication(self) -> Self:
***REMOVED***self.authentication = {
***REMOVED******REMOVED***"type": "connection_string",
***REMOVED******REMOVED***"connection_string": self.connection_string
***REMOVED***
***REMOVED***return self
***REMOVED***
***REMOVED***@model_validator(mode="after")
***REMOVED***def set_fields_mapping(self) -> Self:
***REMOVED***self.fields_mapping = {
***REMOVED******REMOVED***"content_fields": self.content_columns,
***REMOVED******REMOVED***"title_field": self.title_column,
***REMOVED******REMOVED***"url_field": self.url_column,
***REMOVED******REMOVED***"filepath_field": self.filename_column,
***REMOVED******REMOVED***"vector_fields": self.vector_columns
***REMOVED***
***REMOVED***return self
***REMOVED***
***REMOVED***def construct_payload_configuration(
***REMOVED***self,
***REMOVED****args,
***REMOVED*****kwargs
***REMOVED***):
***REMOVED***self.embedding_dependency = \
***REMOVED******REMOVED***self._settings.azure_openai.extract_embedding_dependency()
***REMOVED***parameters = self.model_dump(exclude_none=True, by_alias=True)
***REMOVED***parameters.update(self._settings.search.model_dump(exclude_none=True, by_alias=True))
***REMOVED***return {
***REMOVED******REMOVED***"type": self._type,
***REMOVED******REMOVED***"parameters": parameters
***REMOVED***


class _ElasticsearchSettings(BaseSettings, DatasourcePayloadConstructor):
***REMOVED***model_config = SettingsConfigDict(
***REMOVED***env_prefix="ELASTICSEARCH_",
***REMOVED***env_file=DOTENV_PATH,
***REMOVED***extra="ignore",
***REMOVED***env_ignore_empty=True
***REMOVED***)
***REMOVED***_type: Literal["elasticsearch"] = PrivateAttr(default="elasticsearch")
***REMOVED***top_k: int = Field(default=5, serialization_alias="top_n_documents")
***REMOVED***strictness: int = 3
***REMOVED***enable_in_domain: bool = Field(default=True, serialization_alias="in_scope")
***REMOVED***endpoint: str
***REMOVED***encoded_api_key: str = Field(exclude=True)
***REMOVED***index: str = Field(serialization_alias="index_name")
***REMOVED***query_type: Literal['simple', 'vector'] = "simple"
***REMOVED***content_columns: Optional[List[str]] = Field(default=None, exclude=True)
***REMOVED***vector_columns: Optional[List[str]] = Field(default=None, exclude=True)
***REMOVED***title_column: Optional[str] = Field(default=None, exclude=True)
***REMOVED***url_column: Optional[str] = Field(default=None, exclude=True)
***REMOVED***filename_column: Optional[str] = Field(default=None, exclude=True)
***REMOVED***embedding_model_id: Optional[str] = Field(default=None, exclude=True)
***REMOVED***
***REMOVED***# Constructed fields
***REMOVED***authentication: Optional[dict] = None
***REMOVED***embedding_dependency: Optional[dict] = None
***REMOVED***fields_mapping: Optional[dict] = None
***REMOVED***
***REMOVED***@field_validator('content_columns', 'vector_columns', mode="before")
***REMOVED***@classmethod
***REMOVED***def split_columns(cls, comma_separated_string: str) -> List[str]:
***REMOVED***if isinstance(comma_separated_string, str) and len(comma_separated_string) > 0:
***REMOVED******REMOVED***return parse_multi_columns(comma_separated_string)
***REMOVED***
***REMOVED***return None
***REMOVED***
***REMOVED***@model_validator(mode="after")
***REMOVED***def set_authentication(self) -> Self:
***REMOVED***self.authentication = {
***REMOVED******REMOVED***"type": "encoded_api_key",
***REMOVED******REMOVED***"encoded_api_key": self.encoded_api_key
***REMOVED***
***REMOVED***
***REMOVED***return self
***REMOVED***
***REMOVED***@model_validator(mode="after")
***REMOVED***def set_fields_mapping(self) -> Self:
***REMOVED***self.fields_mapping = {
***REMOVED******REMOVED***"content_fields": self.content_columns,
***REMOVED******REMOVED***"title_field": self.title_column,
***REMOVED******REMOVED***"url_field": self.url_column,
***REMOVED******REMOVED***"filepath_field": self.filename_column,
***REMOVED******REMOVED***"vector_fields": self.vector_columns
***REMOVED***
***REMOVED***return self
***REMOVED***
***REMOVED***def construct_payload_configuration(
***REMOVED***self,
***REMOVED****args,
***REMOVED*****kwargs
***REMOVED***):
***REMOVED***self.embedding_dependency = \
***REMOVED******REMOVED***{"type": "model_id", "model_id": self.embedding_model_id} if self.embedding_model_id else \
***REMOVED******REMOVED***self._settings.azure_openai.extract_embedding_dependency() 
***REMOVED******REMOVED***
***REMOVED***parameters = self.model_dump(exclude_none=True, by_alias=True)
***REMOVED***parameters.update(self._settings.search.model_dump(exclude_none=True, by_alias=True))
***REMOVED******REMOVED***
***REMOVED***return {
***REMOVED******REMOVED***"type": self._type,
***REMOVED******REMOVED***"parameters": parameters
***REMOVED***


class _PineconeSettings(BaseSettings, DatasourcePayloadConstructor):
***REMOVED***model_config = SettingsConfigDict(
***REMOVED***env_prefix="PINECONE_",
***REMOVED***env_file=DOTENV_PATH,
***REMOVED***extra="ignore",
***REMOVED***env_ignore_empty=True
***REMOVED***)
***REMOVED***_type: Literal["pinecone"] = PrivateAttr(default="pinecone")
***REMOVED***top_k: int = Field(default=5, serialization_alias="top_n_documents")
***REMOVED***strictness: int = 3
***REMOVED***enable_in_domain: bool = Field(default=True, serialization_alias="in_scope")
***REMOVED***environment: str
***REMOVED***api_key: str = Field(exclude=True)
***REMOVED***index_name: str
***REMOVED***query_type: Literal["vector"] = "vector"
***REMOVED***content_columns: Optional[List[str]] = Field(default=None, exclude=True)
***REMOVED***vector_columns: Optional[List[str]] = Field(default=None, exclude=True)
***REMOVED***title_column: Optional[str] = Field(default=None, exclude=True)
***REMOVED***url_column: Optional[str] = Field(default=None, exclude=True)
***REMOVED***filename_column: Optional[str] = Field(default=None, exclude=True)
***REMOVED***
***REMOVED***# Constructed fields
***REMOVED***authentication: Optional[dict] = None
***REMOVED***embedding_dependency: Optional[dict] = None
***REMOVED***fields_mapping: Optional[dict] = None
***REMOVED***
***REMOVED***@field_validator('content_columns', 'vector_columns', mode="before")
***REMOVED***@classmethod
***REMOVED***def split_columns(cls, comma_separated_string: str) -> List[str]:
***REMOVED***if isinstance(comma_separated_string, str) and len(comma_separated_string) > 0:
***REMOVED******REMOVED***return parse_multi_columns(comma_separated_string)
***REMOVED***
***REMOVED***return None
***REMOVED***
***REMOVED***@model_validator(mode="after")
***REMOVED***def set_authentication(self) -> Self:
***REMOVED***self.authentication = {
***REMOVED******REMOVED***"type": "api_key",
***REMOVED******REMOVED***"api_key": self.api_key
***REMOVED***
***REMOVED***
***REMOVED***return self
***REMOVED***
***REMOVED***@model_validator(mode="after")
***REMOVED***def set_fields_mapping(self) -> Self:
***REMOVED***self.fields_mapping = {
***REMOVED******REMOVED***"content_fields": self.content_columns,
***REMOVED******REMOVED***"title_field": self.title_column,
***REMOVED******REMOVED***"url_field": self.url_column,
***REMOVED******REMOVED***"filepath_field": self.filename_column,
***REMOVED******REMOVED***"vector_fields": self.vector_columns
***REMOVED***
***REMOVED***return self
***REMOVED***
***REMOVED***def construct_payload_configuration(
***REMOVED***self,
***REMOVED****args,
***REMOVED*****kwargs
***REMOVED***):
***REMOVED***self.embedding_dependency = \
***REMOVED******REMOVED***self._settings.azure_openai.extract_embedding_dependency()
***REMOVED***parameters = self.model_dump(exclude_none=True, by_alias=True)
***REMOVED***parameters.update(self._settings.search.model_dump(exclude_none=True, by_alias=True))
***REMOVED***
***REMOVED***return {
***REMOVED******REMOVED***"type": self._type,
***REMOVED******REMOVED***"parameters": parameters
***REMOVED***


class _AzureMLIndexSettings(BaseSettings, DatasourcePayloadConstructor):
***REMOVED***model_config = SettingsConfigDict(
***REMOVED***env_prefix="AZURE_MLINDEX_",
***REMOVED***env_file=DOTENV_PATH,
***REMOVED***extra="ignore",
***REMOVED***env_ignore_empty=True
***REMOVED***)
***REMOVED***_type: Literal["azure_ml_index"] = PrivateAttr(default="azure_ml_index")
***REMOVED***top_k: int = Field(default=5, serialization_alias="top_n_documents")
***REMOVED***strictness: int = 3
***REMOVED***enable_in_domain: bool = Field(default=True, serialization_alias="in_scope")
***REMOVED***name: str
***REMOVED***version: str
***REMOVED***project_resource_id: str = Field(validation_alias="AZURE_ML_PROJECT_RESOURCE_ID")
***REMOVED***content_columns: Optional[List[str]] = Field(default=None, exclude=True)
***REMOVED***vector_columns: Optional[List[str]] = Field(default=None, exclude=True)
***REMOVED***title_column: Optional[str] = Field(default=None, exclude=True)
***REMOVED***url_column: Optional[str] = Field(default=None, exclude=True)
***REMOVED***filename_column: Optional[str] = Field(default=None, exclude=True)
***REMOVED***
***REMOVED***# Constructed fields
***REMOVED***fields_mapping: Optional[dict] = None
***REMOVED***
***REMOVED***@field_validator('content_columns', 'vector_columns', mode="before")
***REMOVED***@classmethod
***REMOVED***def split_columns(cls, comma_separated_string: str) -> List[str]:
***REMOVED***if isinstance(comma_separated_string, str) and len(comma_separated_string) > 0:
***REMOVED******REMOVED***return parse_multi_columns(comma_separated_string)
***REMOVED***
***REMOVED***return None
***REMOVED***
***REMOVED***@model_validator(mode="after")
***REMOVED***def set_fields_mapping(self) -> Self:
***REMOVED***self.fields_mapping = {
***REMOVED******REMOVED***"content_fields": self.content_columns,
***REMOVED******REMOVED***"title_field": self.title_column,
***REMOVED******REMOVED***"url_field": self.url_column,
***REMOVED******REMOVED***"filepath_field": self.filename_column,
***REMOVED******REMOVED***"vector_fields": self.vector_columns
***REMOVED***
***REMOVED***return self
***REMOVED***
***REMOVED***def construct_payload_configuration(
***REMOVED***self,
***REMOVED****args,
***REMOVED*****kwargs
***REMOVED***):
***REMOVED***parameters = self.model_dump(exclude_none=True, by_alias=True)
***REMOVED***parameters.update(self._settings.search.model_dump(exclude_none=True, by_alias=True))
***REMOVED***
***REMOVED***return {
***REMOVED******REMOVED***"type": self._type,
***REMOVED******REMOVED***"parameters": parameters
***REMOVED***


class _AzureSqlServerSettings(BaseSettings, DatasourcePayloadConstructor):
***REMOVED***model_config = SettingsConfigDict(
***REMOVED***env_prefix="AZURE_SQL_SERVER_",
***REMOVED***env_file=DOTENV_PATH,
***REMOVED***extra="ignore"
***REMOVED***)
***REMOVED***_type: Literal["azure_sql_server"] = PrivateAttr(default="azure_sql_server")
***REMOVED***
***REMOVED***connection_string: str = Field(exclude=True)
***REMOVED***table_schema: str
***REMOVED***schema_max_row: Optional[int] = None
***REMOVED***top_n_results: Optional[int] = None
***REMOVED***
***REMOVED***# Constructed fields
***REMOVED***authentication: Optional[dict] = None
***REMOVED***
***REMOVED***@model_validator(mode="after")
***REMOVED***def construct_authentication(self) -> Self:
***REMOVED***self.authentication = {
***REMOVED******REMOVED***"type": "connection_string",
***REMOVED******REMOVED***"connection_string": self.connection_string
***REMOVED***
***REMOVED***return self
***REMOVED***
***REMOVED***def construct_payload_configuration(
***REMOVED***self,
***REMOVED****args,
***REMOVED*****kwargs
***REMOVED***):
***REMOVED***parameters = self.model_dump(exclude_none=True, by_alias=True)
***REMOVED***#parameters.update(self._settings.search.model_dump(exclude_none=True, by_alias=True))
***REMOVED***
***REMOVED***return {
***REMOVED******REMOVED***"type": self._type,
***REMOVED******REMOVED***"parameters": parameters
***REMOVED***
***REMOVED***
***REMOVED***
class _BaseSettings(BaseSettings):
***REMOVED***model_config = SettingsConfigDict(
***REMOVED***env_file=DOTENV_PATH,
***REMOVED***extra="ignore",
***REMOVED***arbitrary_types_allowed=True,
***REMOVED***env_ignore_empty=True
***REMOVED***)
***REMOVED***datasource_type: Optional[str] = None
***REMOVED***auth_enabled: bool = False
***REMOVED***sanitize_answer: bool = False
***REMOVED***use_promptflow: bool = False


class _AppSettings(BaseModel):
***REMOVED***base_settings: _BaseSettings = _BaseSettings()
***REMOVED***azure_openai: _AzureOpenAISettings = _AzureOpenAISettings()
***REMOVED***search: _SearchCommonSettings = _SearchCommonSettings()
***REMOVED***ui: Optional[_UiSettings] = _UiSettings()
***REMOVED***
***REMOVED***# Constructed properties
***REMOVED***chat_history: Optional[_ChatHistorySettings] = None
***REMOVED***datasource: Optional[DatasourcePayloadConstructor] = None
***REMOVED***promptflow: Optional[_PromptflowSettings] = None

***REMOVED***@model_validator(mode="after")
***REMOVED***def set_promptflow_settings(self) -> Self:
***REMOVED***try:
***REMOVED******REMOVED***self.promptflow = _PromptflowSettings()
***REMOVED******REMOVED***
***REMOVED***except ValidationError:
***REMOVED******REMOVED***self.promptflow = None
***REMOVED******REMOVED***
***REMOVED***return self
***REMOVED***
***REMOVED***@model_validator(mode="after")
***REMOVED***def set_chat_history_settings(self) -> Self:
***REMOVED***try:
***REMOVED******REMOVED***self.chat_history = _ChatHistorySettings()
***REMOVED***
***REMOVED***except ValidationError:
***REMOVED******REMOVED***self.chat_history = None
***REMOVED***
***REMOVED***return self
***REMOVED***
***REMOVED***@model_validator(mode="after")
***REMOVED***def set_datasource_settings(self) -> Self:
***REMOVED***try:
***REMOVED******REMOVED***if self.base_settings.datasource_type == "AzureCognitiveSearch":
***REMOVED******REMOVED***self.datasource = _AzureSearchSettings(settings=self, _env_file=DOTENV_PATH)
***REMOVED******REMOVED***logging.debug("Using Azure Cognitive Search")
***REMOVED******REMOVED***
***REMOVED******REMOVED***elif self.base_settings.datasource_type == "AzureCosmosDB":
***REMOVED******REMOVED***self.datasource = _AzureCosmosDbMongoVcoreSettings(settings=self, _env_file=DOTENV_PATH)
***REMOVED******REMOVED***logging.debug("Using Azure CosmosDB Mongo vcore")
***REMOVED******REMOVED***
***REMOVED******REMOVED***elif self.base_settings.datasource_type == "Elasticsearch":
***REMOVED******REMOVED***self.datasource = _ElasticsearchSettings(settings=self, _env_file=DOTENV_PATH)
***REMOVED******REMOVED***logging.debug("Using Elasticsearch")
***REMOVED******REMOVED***
***REMOVED******REMOVED***elif self.base_settings.datasource_type == "Pinecone":
***REMOVED******REMOVED***self.datasource = _PineconeSettings(settings=self, _env_file=DOTENV_PATH)
***REMOVED******REMOVED***logging.debug("Using Pinecone")
***REMOVED******REMOVED***
***REMOVED******REMOVED***elif self.base_settings.datasource_type == "AzureMLIndex":
***REMOVED******REMOVED***self.datasource = _AzureMLIndexSettings(settings=self, _env_file=DOTENV_PATH)
***REMOVED******REMOVED***logging.debug("Using Azure ML Index")
***REMOVED******REMOVED***
***REMOVED******REMOVED***elif self.base_settings.datasource_type == "AzureSqlServer":
***REMOVED******REMOVED***self.datasource = _AzureSqlServerSettings(settings=self, _env_file=DOTENV_PATH)
***REMOVED******REMOVED***logging.debug("Using SQL Server")
***REMOVED******REMOVED***
***REMOVED******REMOVED***else:
***REMOVED******REMOVED***self.datasource = None
***REMOVED******REMOVED***logging.warning("No datasource configuration found in the environment -- calls will be made to Azure OpenAI without grounding data.")
***REMOVED******REMOVED***
***REMOVED******REMOVED***return self

***REMOVED***except ValidationError:
***REMOVED******REMOVED***logging.warning("No datasource configuration found in the environment -- calls will be made to Azure OpenAI without grounding data.")


app_settings = _AppSettings()
