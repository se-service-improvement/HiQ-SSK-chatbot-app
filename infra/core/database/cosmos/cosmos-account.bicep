metadata description = 'Creates an Azure Cosmos DB account.'
param name string
param location string = resourceGroup().location
param tags object = {}

@allowed([ 'GlobalDocumentDB', 'MongoDB', 'Parse' ])
param kind string

resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2022-08-15' = {
  name: name
  kind: kind
  location: location
  tags: tags
  properties: {
***REMOVED***consistencyPolicy: { defaultConsistencyLevel: 'Session' }
***REMOVED***locations: [
***REMOVED***  {
***REMOVED***locationName: location
***REMOVED***failoverPriority: 0
***REMOVED***isZoneRedundant: false
  ***REMOVED***
***REMOVED***]
***REMOVED***databaseAccountOfferType: 'Standard'
***REMOVED***enableAutomaticFailover: false
***REMOVED***enableMultipleWriteLocations: false
***REMOVED***apiProperties: (kind == 'MongoDB') ? { serverVersion: '4.0' } : {}
***REMOVED***capabilities: [ { name: 'EnableServerless' } ]
  }
}

output endpoint string = cosmos.properties.documentEndpoint
output id string = cosmos.id
output name string = cosmos.name
