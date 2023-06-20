param name string
param location string = resourceGroup().location
param tags object = {}

param sku object = {
  name: 'standard'
}

param authOptions object = {}
param semanticSearch string = 'disabled'

resource search 'Microsoft.Search/searchServices@2021-04-01-preview' = {
  name: name
  location: location
  tags: tags
  identity: {
***REMOVED***type: 'SystemAssigned'
  }
  properties: {
***REMOVED***authOptions: authOptions
***REMOVED***disableLocalAuth: false
***REMOVED***disabledDataExfiltrationOptions: []
***REMOVED***encryptionWithCmk: {
***REMOVED***  enforcement: 'Unspecified'
***REMOVED***
***REMOVED***hostingMode: 'default'
***REMOVED***networkRuleSet: {
***REMOVED***  bypass: 'None'
***REMOVED***  ipRules: []
***REMOVED***
***REMOVED***partitionCount: 1
***REMOVED***publicNetworkAccess: 'Enabled'
***REMOVED***replicaCount: 1
***REMOVED***semanticSearch: semanticSearch
  }
  sku: sku
}

output id string = search.id
output endpoint string = 'https://${name}.search.windows.net/'
output name string = search.name
output skuName string = sku.name
output adminKey string = search.listAdminKeys().primaryKey
