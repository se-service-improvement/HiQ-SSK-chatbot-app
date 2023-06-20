param name string
param location string = resourceGroup().location
param tags object = {}

@allowed([ 'Hot', 'Cool', 'Premium' ])
param accessTier string = 'Hot'
param allowBlobPublicAccess bool = false
param allowCrossTenantReplication bool = true
param allowSharedKeyAccess bool = true
param defaultToOAuthAuthentication bool = false
param deleteRetentionPolicy object = {}
@allowed([ 'AzureDnsZone', 'Standard' ])
param dnsEndpointType string = 'Standard'
param kind string = 'StorageV2'
param minimumTlsVersion string = 'TLS1_2'
@allowed([ 'Enabled', 'Disabled' ])
param publicNetworkAccess string = 'Disabled'
param sku object = { name: 'Standard_LRS' }

param containers array = []

resource storage 'Microsoft.Storage/storageAccounts@2022-05-01' = {
  name: name
  location: location
  tags: tags
  kind: kind
  sku: sku
  properties: {
***REMOVED***accessTier: accessTier
***REMOVED***allowBlobPublicAccess: allowBlobPublicAccess
***REMOVED***allowCrossTenantReplication: allowCrossTenantReplication
***REMOVED***allowSharedKeyAccess: allowSharedKeyAccess
***REMOVED***defaultToOAuthAuthentication: defaultToOAuthAuthentication
***REMOVED***dnsEndpointType: dnsEndpointType
***REMOVED***minimumTlsVersion: minimumTlsVersion
***REMOVED***networkAcls: {
***REMOVED***  bypass: 'AzureServices'
***REMOVED***  defaultAction: 'Allow'
***REMOVED***
***REMOVED***publicNetworkAccess: publicNetworkAccess
  }

  resource blobServices 'blobServices' = if (!empty(containers)) {
***REMOVED***name: 'default'
***REMOVED***properties: {
***REMOVED***  deleteRetentionPolicy: deleteRetentionPolicy
***REMOVED***
***REMOVED***resource container 'containers' = [for container in containers: {
***REMOVED***  name: container.name
***REMOVED***  properties: {
***REMOVED***publicAccess: contains(container, 'publicAccess') ? container.publicAccess : 'None'
  ***REMOVED***
***REMOVED***]
  }
}

output name string = storage.name
output primaryEndpoints object = storage.properties.primaryEndpoints
