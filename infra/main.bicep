targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the the environment which is used to generate a short unique hash used in all resources.')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

param appServicePlanName string = ''
param backendServiceName string = ''
param resourceGroupName string = ''

param searchServiceName string = ''
param searchServiceResourceGroupName string = ''
param searchServiceResourceGroupLocation string = location
param searchServiceSkuName string = ''
param searchIndexName string = 'gptkbindex'
param searchUseSemanticSearch bool = false
param searchSemanticSearchConfig string = 'default'
param searchTopK int = 5
param searchEnableInDomain bool = true
param searchContentColumns string = 'content'
param searchFilenameColumn string = 'filepath'
param searchTitleColumn string = 'title'
param searchUrlColumn string = 'url'

param openAiResourceName string = ''
param openAiResourceGroupName string = ''
param openAiResourceGroupLocation string = location
param openAiSkuName string = ''
param openAIModel string = 'chat'
param openAIModelName string = 'gpt-35-turbo'
param openAITemperature int = 0
param openAITopP int = 1
param openAIMaxTokens int = 1000
param openAIStopSequence string = '\n'
param openAISystemMessage string = 'You are an AI assistant that helps people find information.'
param openAIApiVersion string = '2023-06-01-preview'
param openAIStream bool = true

// Used by prepdocs.py: Form recognizer
param formRecognizerServiceName string = ''
param formRecognizerResourceGroupName string = ''
param formRecognizerResourceGroupLocation string = location
param formRecognizerSkuName string = ''

// Used for the Azure AD application
param authClientId string
@secure()
param authClientSecret string

@description('Id of the user or app to assign application roles')
param principalId string = ''

var abbrs = loadJsonContent('abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var tags = { 'azd-env-name': environmentName }

// Organize resources in a resource group
resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: !empty(resourceGroupName) ? resourceGroupName : '${abbrs.resourcesResourceGroups}${environmentName}'
  location: location
  tags: tags
}

resource openAiResourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' existing = if (!empty(openAiResourceGroupName)) {
  name: !empty(openAiResourceGroupName) ? openAiResourceGroupName : resourceGroup.name
}

resource searchServiceResourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' existing = if (!empty(searchServiceResourceGroupName)) {
  name: !empty(searchServiceResourceGroupName) ? searchServiceResourceGroupName : resourceGroup.name
}


// Create an App Service Plan to group applications under the same payment plan and SKU
module appServicePlan 'core/host/appserviceplan.bicep' = {
  name: 'appserviceplan'
  scope: resourceGroup
  params: {
***REMOVED***name: !empty(appServicePlanName) ? appServicePlanName : '${abbrs.webServerFarms}${resourceToken}'
***REMOVED***location: location
***REMOVED***tags: tags
***REMOVED***sku: {
***REMOVED***  name: 'B1'
***REMOVED***  capacity: 1
***REMOVED***
***REMOVED***kind: 'linux'
  }
}

// The application frontend
var appServiceName = !empty(backendServiceName) ? backendServiceName : '${abbrs.webSitesAppService}backend-${resourceToken}'
module backend 'core/host/appservice.bicep' = {
  name: 'web'
  scope: resourceGroup
  params: {
***REMOVED***name: appServiceName
***REMOVED***location: location
***REMOVED***tags: union(tags, { 'azd-service-name': 'backend' })
***REMOVED***appServicePlanId: appServicePlan.outputs.id
***REMOVED***runtimeName: 'python'
***REMOVED***runtimeVersion: '3.10'
***REMOVED***scmDoBuildDuringDeployment: true
***REMOVED***managedIdentity: true
***REMOVED***authClientSecret: authClientSecret
***REMOVED***authClientId: authClientId
***REMOVED***appSettings: {
***REMOVED***  // search
***REMOVED***  AZURE_SEARCH_INDEX: searchIndexName
***REMOVED***  AZURE_SEARCH_SERVICE: searchService.outputs.name
***REMOVED***  AZURE_SEARCH_KEY: searchService.outputs.adminKey
***REMOVED***  AZURE_SEARCH_USE_SEMANTIC_SEARCH: searchUseSemanticSearch
***REMOVED***  AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG: searchSemanticSearchConfig
***REMOVED***  AZURE_SEARCH_TOP_K: searchTopK
***REMOVED***  AZURE_SEARCH_ENABLE_IN_DOMAIN: searchEnableInDomain
***REMOVED***  AZURE_SEARCH_CONTENT_COLUMNS: searchContentColumns
***REMOVED***  AZURE_SEARCH_FILENAME_COLUMN: searchFilenameColumn
***REMOVED***  AZURE_SEARCH_TITLE_COLUMN: searchTitleColumn
***REMOVED***  AZURE_SEARCH_URL_COLUMN: searchUrlColumn
***REMOVED***  // openai
***REMOVED***  AZURE_OPENAI_RESOURCE: openAi.outputs.name
***REMOVED***  AZURE_OPENAI_MODEL: openAIModel
***REMOVED***  AZURE_OPENAI_MODEL_NAME: openAIModelName
***REMOVED***  AZURE_OPENAI_KEY: openAi.outputs.key
***REMOVED***  AZURE_OPENAI_TEMPERATURE: openAITemperature
***REMOVED***  AZURE_OPENAI_TOP_P: openAITopP
***REMOVED***  AZURE_OPENAI_MAX_TOKENS: openAIMaxTokens
***REMOVED***  AZURE_OPENAI_STOP_SEQUENCE: openAIStopSequence
***REMOVED***  AZURE_OPENAI_SYSTEM_MESSAGE: openAISystemMessage
***REMOVED***  AZURE_OPENAI_PREVIEW_API_VERSION: openAIApiVersion
***REMOVED***  AZURE_OPENAI_STREAM: openAIStream
***REMOVED***
  }
}


module openAi 'core/ai/cognitiveservices.bicep' = {
  name: 'openai'
  scope: openAiResourceGroup
  params: {
***REMOVED***name: !empty(openAiResourceName) ? openAiResourceName : '${abbrs.cognitiveServicesAccounts}${resourceToken}'
***REMOVED***location: openAiResourceGroupLocation
***REMOVED***tags: tags
***REMOVED***sku: {
***REMOVED***  name: !empty(openAiSkuName) ? openAiSkuName : 'S0'
***REMOVED***
***REMOVED***deployments: [
***REMOVED***  {
***REMOVED***name: openAIModel
***REMOVED***model: {
***REMOVED***  format: 'OpenAI'
***REMOVED***  name: openAIModelName
***REMOVED***  version: '0301'
***REMOVED***
***REMOVED***scaleSettings: {
***REMOVED***  scaleType: 'Standard'
***REMOVED***
  ***REMOVED***
***REMOVED***]
  }
}

module searchService 'core/search/search-services.bicep' = {
  name: 'search-service'
  scope: searchServiceResourceGroup
  params: {
***REMOVED***name: !empty(searchServiceName) ? searchServiceName : 'gptkb-${resourceToken}'
***REMOVED***location: searchServiceResourceGroupLocation
***REMOVED***tags: tags
***REMOVED***authOptions: {
***REMOVED***  aadOrApiKey: {
***REMOVED***aadAuthFailureMode: 'http401WithBearerChallenge'
  ***REMOVED***
***REMOVED***
***REMOVED***sku: {
***REMOVED***  name: !empty(searchServiceSkuName) ? searchServiceSkuName : 'standard'
***REMOVED***
***REMOVED***semanticSearch: 'free'
  }
}



// USER ROLES
module openAiRoleUser 'core/security/role.bicep' = {
  scope: openAiResourceGroup
  name: 'openai-role-user'
  params: {
***REMOVED***principalId: principalId
***REMOVED***roleDefinitionId: '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd'
***REMOVED***principalType: 'User'
  }
}

module searchRoleUser 'core/security/role.bicep' = {
  scope: searchServiceResourceGroup
  name: 'search-role-user'
  params: {
***REMOVED***principalId: principalId
***REMOVED***roleDefinitionId: '1407120a-92aa-4202-b7e9-c0e197c71c8f'
***REMOVED***principalType: 'User'
  }
}

module searchIndexDataContribRoleUser 'core/security/role.bicep' = {
  scope: searchServiceResourceGroup
  name: 'search-index-data-contrib-role-user'
  params: {
***REMOVED***principalId: principalId
***REMOVED***roleDefinitionId: '8ebe5a00-799e-43f5-93ac-243d3dce84a7'
***REMOVED***principalType: 'User'
  }
}

module searchServiceContribRoleUser 'core/security/role.bicep' = {
  scope: searchServiceResourceGroup
  name: 'search-service-contrib-role-user'
  params: {
***REMOVED***principalId: principalId
***REMOVED***roleDefinitionId: '7ca78c08-252a-4471-8644-bb5ff32d4ba0'
***REMOVED***principalType: 'User'
  }
}

// SYSTEM IDENTITIES
module openAiRoleBackend 'core/security/role.bicep' = {
  scope: openAiResourceGroup
  name: 'openai-role-backend'
  params: {
***REMOVED***principalId: backend.outputs.identityPrincipalId
***REMOVED***roleDefinitionId: '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd'
***REMOVED***principalType: 'ServicePrincipal'
  }
}

module searchRoleBackend 'core/security/role.bicep' = {
  scope: searchServiceResourceGroup
  name: 'search-role-backend'
  params: {
***REMOVED***principalId: backend.outputs.identityPrincipalId
***REMOVED***roleDefinitionId: '1407120a-92aa-4202-b7e9-c0e197c71c8f'
***REMOVED***principalType: 'ServicePrincipal'
  }
}


// For doc prep

module docPrepResources 'docprep.bicep' = {
  name: 'docprep-resources'
  params: {
***REMOVED***location: location
***REMOVED***resourceToken: resourceToken
***REMOVED***tags: tags
***REMOVED***principalId: principalId
***REMOVED***resourceGroupName: resourceGroup.name
***REMOVED***formRecognizerServiceName: formRecognizerServiceName
***REMOVED***formRecognizerResourceGroupName: formRecognizerResourceGroupName
***REMOVED***formRecognizerResourceGroupLocation: formRecognizerResourceGroupLocation
***REMOVED***formRecognizerSkuName: !empty(formRecognizerSkuName) ? formRecognizerSkuName : 'S0'
  }
}
output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenant().tenantId
output AZURE_RESOURCE_GROUP string = resourceGroup.name

output BACKEND_URI string = backend.outputs.uri

// search
output AZURE_SEARCH_INDEX string = searchIndexName
output AZURE_SEARCH_SERVICE string = searchService.outputs.name
output AZURE_SEARCH_SERVICE_RESOURCE_GROUP string = searchServiceResourceGroup.name
output AZURE_SEARCH_SKU_NAME string = searchService.outputs.skuName
output AZURE_SEARCH_KEY string = searchService.outputs.adminKey
output AZURE_SEARCH_USE_SEMANTIC_SEARCH bool = searchUseSemanticSearch
output AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG string = searchSemanticSearchConfig
output AZURE_SEARCH_TOP_K int = searchTopK
output AZURE_SEARCH_ENABLE_IN_DOMAIN bool = searchEnableInDomain
output AZURE_SEARCH_CONTENT_COLUMNS string = searchContentColumns
output AZURE_SEARCH_FILENAME_COLUMN string = searchFilenameColumn
output AZURE_SEARCH_TITLE_COLUMN string = searchTitleColumn
output AZURE_SEARCH_URL_COLUMN string = searchUrlColumn

// openai
output AZURE_OPENAI_RESOURCE string = openAi.outputs.name
output AZURE_OPENAI_RESOURCE_GROUP string = openAiResourceGroup.name
output AZURE_OPENAI_MODEL string = openAIModel
output AZURE_OPENAI_MODEL_NAME string = openAIModelName
output AZURE_OPENAI_SKU_NAME string = openAi.outputs.skuName
output AZURE_OPENAI_KEY string = openAi.outputs.key
output AZURE_OPENAI_TEMPERATURE int = openAITemperature
output AZURE_OPENAI_TOP_P int = openAITopP
output AZURE_OPENAI_MAX_TOKENS int = openAIMaxTokens
output AZURE_OPENAI_STOP_SEQUENCE string = openAIStopSequence
output AZURE_OPENAI_SYSTEM_MESSAGE string = openAISystemMessage
output AZURE_OPENAI_PREVIEW_API_VERSION string = openAIApiVersion
output AZURE_OPENAI_STREAM bool = openAIStream

// Used by prepdocs.py:
output AZURE_FORMRECOGNIZER_SERVICE string = docPrepResources.outputs.AZURE_FORMRECOGNIZER_SERVICE
output AZURE_FORMRECOGNIZER_RESOURCE_GROUP string = docPrepResources.outputs.AZURE_FORMRECOGNIZER_RESOURCE_GROUP
output AZURE_FORMRECOGNIZER_SKU_NAME string = docPrepResources.outputs.AZURE_FORMRECOGNIZER_SKU_NAME

output AUTH_ISSUER_URI string = environment().authentication.loginEndpoint
