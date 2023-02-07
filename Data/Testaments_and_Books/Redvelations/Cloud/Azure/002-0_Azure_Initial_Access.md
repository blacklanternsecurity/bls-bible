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

# Initial Access

## Tags
<details><summary>Tags</summary><p>

`#@Azure #@AAD #@Token #@AccessToken #@RefreshToken #@Refresh #@Access #@Teams #@Outlook #@Graph #@O365`

</details>

There are multiple ways to gain access to an Azure environment. The goal is to either compromise some service running as a resource in Azure that is configured to use a managed identity, or phish a target user. Either of these would result in the acquisition of an `access_token`. These tokens can then be used to begin enumerating the tenant information. 

## Generate or Steal an Azure `access_token` from a Compromised Workstation

[API and Auth Access](Testaments_and_Books/Redvelations/Cloud/Azure/002-1_Azure_API_and_Auth_Access.md)

### Az PowerShell

#### Create a Token on a Compromised Machine

```powershell
Get-AzAccessToken
```

```powershell
(Get-AzAccessToken).Token
```

```powershell
Get-AzAccessToken -ResourceTypeName AadGraph
```

```powershell
(Get-AzAccessToken -Resource "https://graph.microsoft.com").Token
```

#### Steal a Token on a Compromised Machine

- `Az` PowerShell module stores access tokens in clear text in `TokenCache.dat` in the directory `C:\Users\[username]\.Azure`
- It also stores `ServicePrincipalSecret` in clear-text in `AzureRmContext.json` if a service principal secret is used to authenticate
- Another interesting method is to take a process dump of PowerShell and looking for tokens in it
- Users can save tokens using `Save-AzContext`, look out for them! Search for `Save-AzContext` in PowerShell console history

### az cli

#### Create a Token on a Compromised Machine

```bash
az account get-access-token
```

```bash
az account get-access-token --resource-type ms-graph
```

#### Steal a Token on a Compromised Machine

- `az cli` stores access tokens in clear text in `accessTokens.json` in the directory `C:\Users\[username]\.Azure`
  - We can read tokens from the file, use them and request new ones too
- `azureProfile.json` in the same directory contains information about subscriptions

## Exploitation of Function Application

[Azure Function Application Exploitation](Testaments_and_Books/Redvelations/Cloud/Azure/002-3_Function_Application_Exploitation.md)

* Function App (also called Azure Functions) is Azure's 'serverless' solution to run code
* Languages like C#, Java, PowerShell, Python and more are supported
* A Function App is supposed to be used to react to an event like:
	* HTTP Trigger
	* Processing a file upload
	* Run code on scheduled time and more

## Exploitation of Web Application

[Azure App Service Exploitation](Testaments_and_Books/Redvelations/Cloud/Azure/002-4_App_Service_Exploitation.md)

- Azure App Service is an HTTP-based service for hosting web applications, REST APIs, and mobile back ends.
- Supports boths Windows and Linux environments
- .NET, .NET Core, Java, Ruby, Node.js, PHP, or Python are supported
- Each app runs inside a sandbox but isolation depends upon App Service plans
	+ Apps in Free and Shared tiers run on shared VMs
	+ Apps in Standard and Premium tiers run on dedicated VMs
- Windows apps (not running in Windows containers) have local drives, UNC shares, outbound network connectivity (unless restricted), read access to Registry and event logs
- In the above case, it is also possible to run a PowerShell script and command shell. But the privileges will be of the low-privliege workers process that uses a random application pool identity

## Illicit Consent Grant Phish

[Illicit Consent Grant Phish](Testaments_and_Books/Redvelations/Cloud/Azure/002-5_Illicit_Consent_Grant.md)

- By default, any user can register an application in Azure AD
- We can register an application (only for the target tenant) that needs high impact permissions with admin consent - like sending mail on a user's behalf, role management, etc.
- This will allow us to execute phishing attacks that would be very fruitful in case of success

## Device Code Authentication Flow Phish

[Device Code Authentication Phish](Testaments_and_Books/Redvelations/Cloud/Azure/002-2_Azure_Device_Code_Phish.md)

- An attacker connects to `/devicecode` endpoint and sends `client_id` and resource
- After receiving `verification_uri` and `user_code`, create an email containing a link to `verification_uri` and `user_code`, and send it to the victim.
- Victim clicks the link, provides the code and completes the sign in.
- The attacker receives `access_token` and `refresh_token` and can now mimic the victim.