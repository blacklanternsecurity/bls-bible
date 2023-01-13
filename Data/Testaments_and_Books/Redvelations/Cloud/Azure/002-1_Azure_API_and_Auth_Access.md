<!--
 -------------------------------------------------------------------------------
 Copyright: (c) BLS OPS LLC.
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, version 3.
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.
 You should have received a copy of the GNU General Public License
 along with this program. If not, see <https://www.gnu.org/licenses/>.
 -------------------------------------------------------------------------------
-->

# Azure API and Auth Access

## Tags
<details><summary>Tags</summary><p>

`#@Azure #@AAD #@Token #@AccessToken #@RefreshToken #@Refresh #@Access #@AzureAD #@Stealing #@Theft`

</details>

## Token With CLI Tools

### Az PowerShell

* Both Az PowerShell and AzureAD modules allow the use of Access tokens for authentication
* Usually, tokens contain all the claims (**including that for MFA and Conditional Access etc**) so they are useful in bypassing such security controls
* If you are already connected to a tenant, request an access token for resource manager (ARM)
	* `Get-AzAccessToken`
	* `(Get-AzAccessToken).Token`
* Request an access token for AAD Graph to access Azure AD. Supported tokens - AadGraph, AnalysisServices, Arm, Attestation, Batch, DataLake, KeyVault, OperationalInsights, ResourceManager, Synapse
	* `Get-AzAccessToken -ResourceTypeName AadGraph`
* For Microsoft Graph
	* `(Get-AzAccessToken -Resource "https://graph.microsoft.com").Token`
* Use the access token
	* `Connect-AzAccount -AccoundId test@defcorphq.onmicrosoft.com -AccessToken put-token-here`
* Use other access tokens. In the below command, use the one for AAD Graph (access token is still required) for accessing Azure AD
	* `Connect-AzAccount -AccountId test@defcorphq.onmicrosoft.com -AccessToken put-token-here -GraphAccessToken put-graph-token-here`

### az cli

* az cli can request a token but cannot use it
* Request an access token (ARM)
	* `az account get-access-token`
* Request an access token for aad-graph. Supported tokens: aad-graph, arm, batch, data-lake, media, ms-graph, oss-rdbms
	* `az account get-access-token --resource-type ms-graph`

## Stealing Tokens 

### az cli

* az cli stores access tokens in clear text in `accessTokens.json` in the directory `C:\Users\[username]\.Azure`
* We can read tokens from the file, use them and request new ones too
* `azureProfile.json` in the same directory contains information about subscriptions
* You can modify accessTokens.json to use access tokens with az cli but better to use with Az PowerShell or the Azure AD module
* To clear the access tokens, always use `az logout`

### Az PowerShell

* Az PowerShell stores access tokens in clear text in `TokenCache.dat` in the directory `C:\Users\[username]\.Azure`
* It also stores ServicePrincipalSecret in clear-text in `AzureRmContext.json` if a service principal secret is used to authenticate
* Another interesting method is to take a process dump of PowerShell and looking for tokens in it
* Users can save tokens using `Save-AzContext`, look out for them! Search for `Save-AzContext` in PowerShell console history
* Always use `Disconnect-AzAccount`!