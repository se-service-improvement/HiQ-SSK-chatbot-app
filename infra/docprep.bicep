targetScope = 'subscription'

param resourceGroupName string
param location string
param tags object = {}
param principalId string
param resourceToken string

// Storage and form recognizer: Used by document uploader / extractor
param storageAccountName string = ''
param storageResourceGroupName string = ''
param storageResourceGroupLocation string = location
param storageContainerName string = 'content'

param formRecognizerServiceName string = ''
param formRecognizerResourceGroupName string = ''
param formRecognizerResourceGroupLocation string = location
param formRecognizerSkuName string = 'S0'

var abbrs = loadJsonContent('abbreviations.json')

resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' existing = {
  name: resourceGroupName
}

resource storageResourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' existing = if (!empty(storageResourceGroupName)) {
  name: !empty(storageResourceGroupName) ? storageResourceGroupName : resourceGroup.name
}

resource formRecognizerResourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' existing = if (!empty(formRecognizerResourceGroupName)) {
  name: !empty(formRecognizerResourceGroupName) ? formRecognizerResourceGroupName : resourceGroup.name
}

module storage 'core/storage/storage-account.bicep' = {
  name: 'storage'
  scope: storageResourceGroup
  params: {
***REMOVED***name: !empty(storageAccountName) ? storageAccountName : '${abbrs.storageStorageAccounts}${resourceToken}'
***REMOVED***location: storageResourceGroupLocation
***REMOVED***tags: tags
***REMOVED***publicNetworkAccess: 'Enabled'
***REMOVED***sku: {
***REMOVED***  name: 'Standard_ZRS'
***REMOVED***
***REMOVED***deleteRetentionPolicy: {
***REMOVED***  enabled: true
***REMOVED***  days: 2
***REMOVED***
***REMOVED***containers: [
***REMOVED***  {
***REMOVED***name: storageContainerName
***REMOVED***publicAccess: 'None'
  ***REMOVED***
***REMOVED***]
  }
}

module formRecognizer 'core/ai/cognitiveservices.bicep' = {
  name: 'formrecognizer'
  scope: formRecognizerResourceGroup
  params: {
***REMOVED***name: !empty(formRecognizerServiceName) ? formRecognizerServiceName : '${abbrs.cognitiveServicesFormRecognizer}${resourceToken}'
***REMOVED***kind: 'FormRecognizer'
***REMOVED***location: formRecognizerResourceGroupLocation
***REMOVED***tags: tags
***REMOVED***sku: {
***REMOVED***  name: formRecognizerSkuName
***REMOVED***
  }
}

module storageRoleUser 'core/security/role.bicep' = {
  scope: storageResourceGroup
  name: 'storage-role-user'
  params: {
***REMOVED***principalId: principalId
***REMOVED***roleDefinitionId: '2a2b9908-6ea1-4ae2-8e65-a410df84e7d1'
***REMOVED***principalType: 'User'
  }
}

module storageContribRoleUser 'core/security/role.bicep' = {
  scope: storageResourceGroup
  name: 'storage-contribrole-user'
  params: {
***REMOVED***principalId: principalId
***REMOVED***roleDefinitionId: 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
***REMOVED***principalType: 'User'
  }
}

module formRecognizerRoleUser 'core/security/role.bicep' = {
  scope: formRecognizerResourceGroup
  name: 'formrecognizer-role-user'
  params: {
***REMOVED***principalId: principalId
***REMOVED***roleDefinitionId: 'a97b65f3-24c7-4388-baec-2e87135dc908'
***REMOVED***principalType: 'User'
  }
}

// Used by prepdocs
// Form recognizer
output AZURE_FORMRECOGNIZER_SERVICE string = formRecognizer.outputs.name
output AZURE_FORMRECOGNIZER_RESOURCE_GROUP string = formRecognizerResourceGroup.name
output AZURE_FORMRECOGNIZER_SKU_NAME string = formRecognizerSkuName

// Storage
output AZURE_STORAGE_ACCOUNT string = storage.outputs.name
output AZURE_STORAGE_CONTAINER string = storageContainerName
output AZURE_STORAGE_RESOURCE_GROUP string = storageResourceGroup.name
