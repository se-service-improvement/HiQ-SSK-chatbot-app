metadata description = 'Creates an Azure Cosmos DB for NoSQL account with a database.'
param accountName string
param databaseName string
param location string = resourceGroup().location
param tags object = {}

param containers array = []
param principalIds array = []

module cosmos 'cosmos-sql-account.bicep' = {
  name: 'cosmos-sql-account'
  params: {
***REMOVED***name: accountName
***REMOVED***location: location
***REMOVED***tags: tags
  }
}

resource database 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2022-05-15' = {
  name: '${accountName}/${databaseName}'
  properties: {
***REMOVED***resource: { id: databaseName }
  }

  resource list 'containers' = [for container in containers: {
***REMOVED***name: container.name
***REMOVED***properties: {
***REMOVED***  resource: {
***REMOVED***id: container.id
***REMOVED***partitionKey: { paths: [ container.partitionKey ] }
  ***REMOVED***
***REMOVED***  options: {}
***REMOVED***
  }]

  dependsOn: [
***REMOVED***cosmos
  ]
}

module roleDefinition 'cosmos-sql-role-def.bicep' = {
  name: 'cosmos-sql-role-definition'
  params: {
***REMOVED***accountName: accountName
  }
  dependsOn: [
***REMOVED***cosmos
***REMOVED***database
  ]
}

// We need batchSize(1) here because sql role assignments have to be done sequentially
@batchSize(1)
module userRole 'cosmos-sql-role-assign.bicep' = [for principalId in principalIds: if (!empty(principalId)) {
  name: 'cosmos-sql-user-role-${uniqueString(principalId)}'
  params: {
***REMOVED***accountName: accountName
***REMOVED***roleDefinitionId: roleDefinition.outputs.id
***REMOVED***principalId: principalId
  }
  dependsOn: [
***REMOVED***cosmos
***REMOVED***database
  ]
}]

output accountId string = cosmos.outputs.id
output accountName string = cosmos.outputs.name
output databaseName string = databaseName
output endpoint string = cosmos.outputs.endpoint
output roleDefinitionId string = roleDefinition.outputs.id
