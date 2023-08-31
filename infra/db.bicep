param accountName string
param location string = resourceGroup().location
param tags object = {}

param databaseName string = 'db_conversation_history'
param collectionName string = 'conversations'
param principalIds array = []

param containers array = [
  {
***REMOVED***name: collectionName
***REMOVED***id: collectionName
***REMOVED***partitionKey: '/id'
  }
]

module cosmos 'core/database/cosmos/sql/cosmos-sql-db.bicep' = {
  name: 'cosmos-sql'
  params: {
***REMOVED***accountName: accountName
***REMOVED***databaseName: databaseName
***REMOVED***location: location
***REMOVED***containers: containers
***REMOVED***tags: tags
***REMOVED***principalIds: principalIds
  }
}


output databaseName string = cosmos.outputs.databaseName
output containerName string = containers[0].name
output accountName string = cosmos.outputs.accountName
output endpoint string = cosmos.outputs.endpoint
