targetScope = 'subscription'

param resourceGroupName string
param location string
param tags object = {}
param principalId string
param resourceToken string

param formRecognizerServiceName string = ''
param formRecognizerResourceGroupName string = ''
param formRecognizerResourceGroupLocation string = location
param formRecognizerSkuName string = 'S0'

var abbrs = loadJsonContent('abbreviations.json')

resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' existing = {
  name: resourceGroupName
}

resource formRecognizerResourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' existing = if (!empty(formRecognizerResourceGroupName)) {
  name: !empty(formRecognizerResourceGroupName) ? formRecognizerResourceGroupName : resourceGroup.name
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
