metadata description = 'Creates a SQL role definition under an Azure Cosmos DB account.'
param accountName string

resource roleDefinition 'Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions@2022-08-15' = {
  parent: cosmos
  name: guid(cosmos.id, accountName, 'sql-role')
  properties: {
***REMOVED***assignableScopes: [
***REMOVED***  cosmos.id
***REMOVED***]
***REMOVED***permissions: [
***REMOVED***  {
***REMOVED***dataActions: [
***REMOVED***  'Microsoft.DocumentDB/databaseAccounts/readMetadata'
***REMOVED***  'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/*'
***REMOVED***  'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*'
***REMOVED***]
***REMOVED***notDataActions: []
  ***REMOVED***
***REMOVED***]
***REMOVED***roleName: 'Reader Writer'
***REMOVED***type: 'CustomRole'
  }
}

resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2022-08-15' existing = {
  name: accountName
}

output id string = roleDefinition.id
