param name string
param location string = resourceGroup().location
param tags object = {}

// Reference Properties
param applicationInsightsName string = ''
param appServicePlanId string
param keyVaultName string = ''
param managedIdentity bool = !empty(keyVaultName)

// Runtime Properties
@allowed([
  'dotnet', 'dotnetcore', 'dotnet-isolated', 'node', 'python', 'java', 'powershell', 'custom'
])
param runtimeName string
param runtimeNameAndVersion string = '${runtimeName}|${runtimeVersion}'
param runtimeVersion string

// Microsoft.Web/sites Properties
param kind string = 'app,linux'

// Microsoft.Web/sites/config
param allowedOrigins array = []
param alwaysOn bool = true
param appCommandLine string = ''
param appSettings object = {}
param authClientId string
@secure()
param authClientSecret string
param authIssuerUri string
param clientAffinityEnabled bool = false
param enableOryxBuild bool = contains(kind, 'linux')
param functionAppScaleLimit int = -1
param linuxFxVersion string = runtimeNameAndVersion
param minimumElasticInstanceCount int = -1
param numberOfWorkers int = -1
param scmDoBuildDuringDeployment bool = false
param use32BitWorkerProcess bool = false
param ftpsState string = 'FtpsOnly'
param healthCheckPath string = ''

resource appService 'Microsoft.Web/sites@2022-03-01' = {
  name: name
  location: location
  tags: tags
  kind: kind
  properties: {
***REMOVED***serverFarmId: appServicePlanId
***REMOVED***siteConfig: {
***REMOVED***  linuxFxVersion: linuxFxVersion
***REMOVED***  alwaysOn: alwaysOn
***REMOVED***  ftpsState: ftpsState
***REMOVED***  appCommandLine: appCommandLine
***REMOVED***  numberOfWorkers: numberOfWorkers != -1 ? numberOfWorkers : null
***REMOVED***  minimumElasticInstanceCount: minimumElasticInstanceCount != -1 ? minimumElasticInstanceCount : null
***REMOVED***  use32BitWorkerProcess: use32BitWorkerProcess
***REMOVED***  functionAppScaleLimit: functionAppScaleLimit != -1 ? functionAppScaleLimit : null
***REMOVED***  healthCheckPath: healthCheckPath
***REMOVED***  cors: {
***REMOVED***allowedOrigins: union([ 'https://portal.azure.com', 'https://ms.portal.azure.com' ], allowedOrigins)
  ***REMOVED***
***REMOVED***
***REMOVED***clientAffinityEnabled: clientAffinityEnabled
***REMOVED***httpsOnly: true
  }

  identity: { type: managedIdentity ? 'SystemAssigned' : 'None' }

  resource configAppSettings 'config' = {
***REMOVED***name: 'appsettings'
***REMOVED***properties: union(appSettings,
***REMOVED***  {
***REMOVED***SCM_DO_BUILD_DURING_DEPLOYMENT: string(scmDoBuildDuringDeployment)
***REMOVED***ENABLE_ORYX_BUILD: string(enableOryxBuild)
  ***REMOVED***,
***REMOVED***  !empty(applicationInsightsName) ? { APPLICATIONINSIGHTS_CONNECTION_STRING: applicationInsights.properties.ConnectionString } : {},
***REMOVED***  !empty(keyVaultName) ? { AZURE_KEY_VAULT_ENDPOINT: keyVault.properties.vaultUri } : {},
***REMOVED***  !empty(authClientSecret) ? { AUTH_CLIENT_SECRET: authClientSecret } : {}
***REMOVED***)
  }

  resource configLogs 'config' = {
***REMOVED***name: 'logs'
***REMOVED***properties: {
***REMOVED***  applicationLogs: { fileSystem: { level: 'Verbose' } }
***REMOVED***  detailedErrorMessages: { enabled: true }
***REMOVED***  failedRequestsTracing: { enabled: true }
***REMOVED***  httpLogs: { fileSystem: { enabled: true, retentionInDays: 1, retentionInMb: 35 } }
***REMOVED***
***REMOVED***dependsOn: [
***REMOVED***  configAppSettings
***REMOVED***]
  }

  resource configAuth 'config' = if (!(empty(authClientId))) {
***REMOVED***name: 'authsettingsV2'
***REMOVED***properties: {
***REMOVED***  globalValidation: {
***REMOVED***requireAuthentication: true
***REMOVED***unauthenticatedClientAction: 'RedirectToLoginPage'
***REMOVED***redirectToProvider: 'azureactivedirectory'
  ***REMOVED***
***REMOVED***  identityProviders: {
***REMOVED***azureActiveDirectory: {
***REMOVED***  enabled: true
***REMOVED***  registration: {
***REMOVED******REMOVED***clientId: authClientId
***REMOVED******REMOVED***clientSecretSettingName: 'AUTH_CLIENT_SECRET'
***REMOVED******REMOVED***openIdIssuer: authIssuerUri
  ***REMOVED***
***REMOVED***  validation: {
***REMOVED******REMOVED***defaultAuthorizationPolicy: {
***REMOVED******REMOVED***  allowedApplications: []
***REMOVED***
  ***REMOVED***
***REMOVED***
  ***REMOVED***
***REMOVED***  login: {
***REMOVED***tokenStore: {
***REMOVED***  enabled: true
***REMOVED***
  ***REMOVED***
***REMOVED***
  }
}

resource keyVault 'Microsoft.KeyVault/vaults@2022-07-01' existing = if (!(empty(keyVaultName))) {
  name: keyVaultName
}

resource applicationInsights 'Microsoft.Insights/components@2020-02-02' existing = if (!empty(applicationInsightsName)) {
  name: applicationInsightsName
}

output identityPrincipalId string = managedIdentity ? appService.identity.principalId : ''
output name string = appService.name
output uri string = 'https://${appService.properties.defaultHostName}'
