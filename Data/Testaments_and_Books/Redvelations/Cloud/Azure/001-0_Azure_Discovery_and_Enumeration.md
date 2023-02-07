<!---------------------------------------------------------------------------------
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
--------------------------------------------------------------------------------->
# Azure Discovery and Enumeration

### References

### Process

* We only know the domain name or email addresses of the target organization
	* DefCorpHQ
* We can extract some interesting information
	* If the target organization uses Azure tenant
	* Tenant ID
	* Tenant name
	* Authentication type (Federation or not)
	* Domains
	* Azure Services used by the target organization
	* Guess email IDs

### Azure Portal

* The Azure Portal (https://portal.azure.com/) is a web console that can be used to manage Azure account and its resources
* It is a GUI alternative to tools like PowerShell modules and Azure cli

### Default User Permissions

* A normal user has many interesting permissions in Azure AD
	* Read all users, Groups, Applications, Devices, Roles, Subscriptions, and their public repositories
	* Invite Guests
	* Create Security groups
	* Read non-hidden Group memberships
	* Add guests to Owned groups
	* Create new application
	* Add up to 50 devices to Azure

### AzureAD Module

* AzureAD is a PowerShell module from Microsoft for managing Azure AD
* Does not show all the properties of Azure AD objects and the documentation is not good. Still useful to some extent
* Can be used only to interact with Azure AD, no access to Azure resources
* Note that if the module is not present on your machine, you can use `Install-Module AzureAD` command or:
	* Download it from PowerShell Gallery:
		* https://www.powershellgallery.com/packages/AzureAD
		* Rename the .nupkg to .zip and extract it
		* `Import-Module C:\AzAD\Tools\AzureAD\AzureAD.psd1`
* To be able to use PowerShell module, we must connect to Azure AD first:
	* `Connect-AzureAD`
* Using credentials from command line (PSCredential object can be used too)
	* Option 1

			$creds = Get-Credential
			Connect-AzureAD -Credential $creds
	* Option 2

			$passwd = ConvertTo-SecureString "SuperVeryEasytoGuessPassword@1234" -AsPlainText -Force
			$creds = New-Object System.Management.Automation.PSCredential("test@defcorphq.onmicrosoft.com", $passwd)
			Connect-AzureAD -Credential $creds
* Get the current session state
	* `Get-AzureADCurrentSessionInfo`
* Get details of the current tenant
	* `Get-AzureADTenantDetail`

#### Users

* Enumerate all users
	* `Get-AzureADUser -All $true`
* Enumerate a specific user
	* `Get-AzureADUser -ObjectId test@defcorphq.onmicrosoft.com`
* Search for a user based on a string in first characters of `DisplayName` or `userPrincipalName` (wildcard not supported)
	* `Get-AzureADUser -SearchString "admin"`
* Search for users who contain the word "admin" in their Display name:
	* `Get-AzureADUser -All $true |?{$_.DisplayName -match "admin"}`
* List all the attributes for a user
	* `Get-AzureADUser -ObjectId test@defcorphq.onmicrosoft.com | fl *`
	* `Get-AzureADUser -ObjectId test@defcorphq.onmicrosoft.com | %{$_.PSObject.Properties.Name}`
* Search attributes for all users that contain the string "password"
	* `Get-AzureADUser |%{$Properties = $_;$Properties.PSObject.Properties.Name | % {if ($Properties.$_ -match 'password') {"$($Properties.UserPrincipalName) - $_ - $($Properties.$_)"}}}`
* All users who are synced from on-prem
	* `Get-AzureADUser -All $true | ?{$_.OnPremisesSecurityIdentifier -ne $null}`
* All users who are from Azure AD
	* `Get-AzureADUser -All $true | ?{$_.OnPremisesSecurityIdentifier -eq $null}`
* Objects created by any user (use-ObjectId for a specific user)
	* `Get-AzureADUser | Get-AzureADUserCreatedObject`
* Objects owned by a specific user
	* `Get-AzureADUserOwnedObject -ObjectId test@defcorphq.onmicrosoft.com`

#### Groups

* List all groups
	* `Get-AzureADGroup -All $true`
* Enumerate a specific group
	* `Get-AzureADGroup -ObjectId put-the-object-id-here`
* Search for a group based on string in first characters of DisplayName (wildcard not supported)
	* `Get-AzureADGroup -SearchString "admin" | fl *`
* To search for groups which contain the word "admin" in their name:
	* `Get-AzureADGroup -All $true | ?{$_.DisplayName -match "admin"}`
* Get groups that allow dynamic membership (note the cmdlet name)
	* `Get-AzureADMSGroup | ?{$_.GroupTypes -eq 'DynamicMembership'}`
* All groups that are synced from on-prem (note that security groups are not synced)
	* `Get-AzureADGroup -All $true | ?{$_.OnPremisesSecurityIdentifier -ne $null}`
* All groups that are from Azure AD
	* `Get-AzureADGroup -All $true | ?{$_.OnPremisesSecurityIdentifier -eq $null}`
* Get members of a group
	* `Get-AzureADGroupMember -ObjectId put-object-id-here`
* Get groups and roles where the specified user is a member
	* `Get-AzureADUser -SearchString 'test' | Get-AzureADUserMembership`
	* `Get-AzureADUserMembership -ObjectId test@defcorphq.onmicrosoft.com`

#### Roles

* Get all available role templates
	* `Get-AzureADDirectoryRoleTemplate`
* Get all roles
	* `Get-AzureADDirectoryRole`
* Enumerate users to whom roles are assigned
	* `Get-AzureADDirectoryRole -Filter "DisplayName eq 'Global Administrator'" | Get-AzureADDirectoryRoleMember`

#### Devices

* Get all Azure joined and registered devices
	* `Get-AzureADDevice -All $true | fl *`
* Get the device configuration object (note the RegistrationQuota in the output)
	* `Get-AzureADDeviceConfiguration | fl *`
* List Registered owners of all the devices
	* `Get-AzureADDevice -All $true | Get-AzureADDeviceRegisteredOwner`
	* **The device's registered owner is automatically added to the local administrators group for that device**
* List Registered users of all the devices
	* `Get-AzureADDevice -All $true | Get-AzureADDeviceRegisteredUser`
* List devices owned by a user
	* `Get-AzureADUserOwnedDevice - ObjectId michaelmbarron@defcorphq.onmicrosoft.com`
* List devices registered by a user
	* `Get-AzureADUserRegisteredDevice -ObjectId michaelmbarron@defcorphq.onmicrosoft.com`
* List devices managed using Intune
	* `Get-AzureADDevice -All $true | ?{$_.IsCompliant -eq "True"}`

#### Apps

* Get all the application (visible as **application registrations in Azure Portal**) objects registered with the current tenant (visible in App Registrations in Azure portal). An application object is the global representation of an app
	* `Get-AzureADApplication -All $true`
* Get all details about an application (application registrations)
	* `Get-AzureADApplication -ObjectId put-object-id-here | fl *`
* Get an application based on the display name (application registrations)
	* `Get-AzureADApplication -All $true | ?{$_.DisplayName -match "app"}`
* The `Get-AzureADApplicationPasswordCredential` will show the applications with an application password but password value is not shown
* Get owner of an application
	* `Get-AzureADApplication -ObjectId put-object-id-here | Get-AzureADApplicationOwner | fl *`
* Get Apps where a User has a role (exact role is not shown)
	* `Get-AzureADUser -ObjectId roygcain@defcorphq.onmicrosoft.com | Get-AzureADUserAppRoleAssignment | fl *`
* Get Apps where a group has a role (exact role is not shown)
	* `Get-AzureADGroup -ObjectId put-object-id-here | Get-AzureADGroupAppRoleAssignment | fl *`

#### Service Principals

* Enumerate Service Principals (visible as **Enterprise Applications in Azure Portal**). Service principal is local representation for an app in a specific tenant and it is the security object that has privileges. This is the 'service account'
* Service principals can be assigned Azure roles
* Get all service principals
	* `Get-AzureADServicePrincipal -All $true`
* Get all details about a service principal
	* `Get-AzureADServicePrincipal - ObjectId put-object-id-here | fl *`
* Get a service principal based on the display name
	* `Get-AzureADServicePrincipal -All $true | ?{$_.DisplayName -match "app"}`
* Get owner of a service principal
	* `Get-AzureADServicePrincipal -ObjectId put-object-id-here | Get-AzureADServicePrincipalOwner | fl *`
* Get objects owned by a service principal
	* `Get-AzureADServicePrincipal -ObjectId put-object-id-here | Get-AzureADServicePrincipalOwnedObject`
* Get objects created by a service principal
	* `Get-AzureADServicePrincipal -ObjectId put-object-id-here | Get-AzureADServicePrincipalCreatedObject`
* Get group and role membersips of a service principal
	* `Get-AzureADServicePrincipal -ObjectId put-object-id-here | Get-AzureADServicePrincipalMembership | fl *`
	* `Get-AzureADServicePrincipal | Get-AzureADServicePrincipalMembership`

### Az PowerShell

* Az PowerShell is a module from Microsoft for managing Azure resources
* Please note that if the module is not present on your machine, you can use `Install-Module Az` command
* "The Azure Az PowerShell module is a rollup module. Installing it downloads the generally available Az PowerShell modules, and makes their cmdlets available for use."
* To be able to use PowerShell module, we must connect to Azure AD first:
	* `Connect-AzAccount`
* Using credentials from command line (PSCredential object and access tokens can be used too)
	* `$creds = Get-Credential`
	* `Connect-AzAccount -Credential $creds`
	* or
	* `$passwd = ConvertTo-SecureString "SuperVeryEasytoGuessPassword@1234" -AsPlainText -Force`
	* `$creds = New-Object System.Management.Automation.PSCredential("test@defcorphq.onmicrosoft.com", $passwd)`
	* `Connect-AzAccount -Credential $creds`
* Az PowerShell can enumerate both Azure AD and Azure Resources
* All the Azure AD cmdlets have the format `*-AzAD*`
	* `Get-Command *azad*`
	* `Get-AzADUser`
* Cmdlets for other Azure resources have the format `*Az*`
	* `Get-Command *az*`
	* `Get-AzResource`
* Find cmdlets for a particular resource. For example, VMs:
	* `Get-Command *azvm*`
	* `Get-Command -Noun *vm* -Verg Get`
	* `Get-Command *vm*`
* Get the information about the current context (Account, Tenant, Subscription, etc)
	* `Get-AzContext`
* List all available context
	* `Get-AzContext -ListAvailable`
* Enumerate subscriptions accessible by the current user
	* `Get-AzSubscription`
* Enumerate all resources visible to the current user
	* `Get-AzResource`
* Enumerate all Azure RBAC role assignments
	* `Get-AzRoleAssignment`

#### AAD Users

* Enumerate all users
	* `Get-AzADUser`
* Enumerate a specific user
	* `Get-AzADUser -UserPrincipalName test@defcorphq.onmicrosoft.com`
* Search for a user based on string in first characer of DisplayName (wildcard not supported)
	* `Get-AzADUser -SearchString "admin"`
* Search for users who contain the word "admin" in their display name
	* `Get-AzADUser | ?{$_.DisplayName -match "admin"}`

#### AAD Groups

* List all groups
	* `Get-AzADGroup`
* Enumerate a specific group
	* `Get-AzADGroup -ObjectId put-object-id-here`
* Search for a group based on string in first characters of DisplayName (wildcard not supported)
	* `Get-AzADGroup -SearchString "admin" | fl *`
* To search for groups which contain the word "admin" in their name
	* `Get-AzADGroup | ?{$_.DisplayName -match "admin"}`
* Get members of a group
	* `Get-AzADGroupMember -ObjectId put-object-id-here`

#### AAD Apps

* Get all the application objects registered with the current tenant (visible in App Registrations in Azure portal). An application object is the global representation of an app
	* `Get-AzADApplication`
* Get all details about an application
	* `Get-AzADApplication -ObjectId put-object-id-here`
* Get an application based on the display name
	* `Get-AzADApplication | ?{$_.DisplayName -match "app"}`
* The `Get-AzADAppCredential` will show the applications with an application password but password value is not shown

#### AAD Service Principals

* Enumerate Service Principals (visible as Enterprise Applications in Azure Portal). Service Principal is local representation for an app in a specific tenant and it is the security object that has privileges. This is the 'service account'
* Service principals can be assigned Azure roles
* Get all service principals
	* `Get-AzADServicePrincipal`
* Get all details about a service principal
	* `Get-AzADServicePrincipal -ObjectId put-object-id-here`
* Get a service principal based on the display name
	* `Get-AzADServicePrincipal | ?{$_.DisplayName -match "app"}`

### Azure CLI (az cli)

* "A set of commands used to create and manage Azure resources"
* Can be installed on multiple platforms and can be used with multiple clouds
* Available in Cloud Shell too
* Install using MSI - https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
* To be able to use az cli, we must connect to Azure AD first (opens up a login page using Default browser)
	* `az login`
* Using credentials from command line (service principals and managed identity for VMs is also supported)
	* `az login -u test@defcorphq.onmicrosoft.com -p SuperVeryEasytoGuessPassword@1234`
* If the user has no permissions on the subscription
	* `az login -u test@defcorphq.onmicrosoft.com -p SuperVeryEasytoGuessPassword@1234 --allow-no-subscriptions`
* You can configure az cli to set some default behavior (output type, location, resource group etc)
	* `az configure`
* We can search for popular commands (based on user telemetry) on a particular topic
* To find popular commands for VMs
	* `az find "vm"`
* To find popular commands within "az vm"
	* `az find "az vm"`
* To find popular subcommands and parameters within "az vm list"
	* `az find "az vm list"`
* We can format output using the `--output` parameter. The default format is JSON. You can change the default as discussed already
* List all the users in Azure AD and format output in table
	* `az ad user list --output table`
* List only the userPrincipalName and givenName (case sensitive) for all the users in Azure AD and format output in table. az cli uses JMESPath (pronounced 'James path') query
	* `az ad user list --query "[].[userPrincipalName,displayName]" --output table`
* List only the userPrincipalName and givenName (case sensitive) for all the users in Azure AD, rename the properties and format output in table
	* `az ad user list --query "[].{UPN:userPrincipalName, Name:displayName}" --output table`
* We can use JMESPath query on the results of JSON output. Add `--query-examples` at the end of any command to see examples
	* `az ad user show list --query-examples`
* We will cover additional options of az cli as and when required
* Get details of the current tenant (uses the account extension)
	* `az account tenant list`
* Get details of the current subscription (uses the account extension)
	* `az account subscription list`
* List the current signed-in user
	* `az ad signed-in-user show`

#### AAD Users

* Enumerate all users
	* `az ad user list`
	* `az ad user list --query "[].[displayName]" -o table`
* Enumerate a specific user (lists all attributes)
	* `az ad user show --id test@defcorphq.onmicrosoft.com`
* Search for users who contain the word "admin" in their Display name (case sensitive)
	* `az ad user list --query "[?Contains(displayName, 'admin')].displayName"`
* When using PowerShell, search for users who contain the word "admin" in their Display name. This is NOT case-sensitive
	* `az ad user list | ConvertFrom-Json | %{$_.displayName -match "admin"}`
* All users who are synced from on-prem
	* `az ad user list | --query "[?onPremisesSecurityIdentifier!=null].displayName"`
* All users who are from Azure AD
	* `az ad user list --query "[?onPremisesSecurityIdentifer==null].displayName"`

#### AAD Groups

* List all groups
	* `az ad group list`
	* `az ad group list --query "[].[displayName]" -o table`
* Enumerate a specific group using display name or object id
	* `az ad group show -g "VM Admins"`
	* `az ad group show -g put-object-id-here`
* Search for groups that contain the word "admin" in their Display name (case sensitive) - run from cmd:
	* `az ad group list --query "[?contains(displayName,'admin')].displayName"`
* When using PowerShell, search for groups that contain the word "admin" in their display name. This is NOT case sensitive
	* `az ad group list | ConvertFrom-Json | %{$_.displayName -match "admin"}`
* All groups that are synced from on-prem
	* `az ad group list --query "[?onPremisesSecurityIdentifier!=null].displayName"`
* All groups that are from Azure AD
	* `az ad group list --query "[?onPremisesSecurityIdentifier==null].displayName"`
* Get members of a group
	* `az ad group member list -g "VM Admins" --query "[].[displayName]" -o table`
* Check if a user is member of the specified group
	* `az ad group member check --group "VM Admins" --member-id put-object-id-here`
* Get the object IDs of the groups of which the specified group is a member
	* `az ad group get-member-groups -g "VM Admins"`

#### AAD Apps

* Get all the application objects registered with the current tenant (visible in App Registrations in Azure portal). An application object is the global representation of an app.
	* `az ad app list`
	* `az ad app list --query "[].[displayName]" -o table`
* Get all details about an application using identifier uri, application id or object id
	* `az ad app show --id put-id-here`
* Get an application based on the display name (Run from cmd)
	* `az ad app list --query "[?contains(displayName,'app')].displayName"`
* When using PowerShell, search for apps that contain the word "slack" in their Display name. This is NOT case sensitive
	* `az ad app list | ConvertFrom-Json | %{$_.displayName -match "app"}`

### ROADTools

* RoadRecon (https://github.com/dirkjanm/ROADTools) is a tool for enumerating Azure AD environments
* RoadRecon uses a different version '1.61-internal' of Azure AD Graph API that provides more information
* Enumeration using RoadRecon includes three steps
	* Authentication
	* Data Gathering
	* Data Exploration
* roadrecon supports username/password, access and refresh tokens, device code flow (sign-in from another device) and PRT cookie
	* `cd C:\AzAD\Tools\ROADTools`
	* `pipenv shell`
	* `roadrecon auth -u test@defcorphq.onmicrosoft.com -p SuperVeryEasytoGuessPassword@1234`
	* If you are in the situation where you only have access to an account that has MFA enabled, you can auth using the `roadrecon auth --device-code` option
	  * This will present you with a device code to use in order to authenticate your roadlib script
* Once authentication is done, use the below command to gather data (ignore the errors)
	* `roadrecon gather`
* Use roadrecon GUI to analyse the gathered information (starts a web server on port 5000)
	* `roadrecon gui`

### Azure Tenant

* Get if Azure tenant is in use, tenant name and Federation
	* `https://login.microsoftonline.com/getuserrealm.srf?login=[USERNAME@DOMAIN]&xml=1`
	* `login.microsoftonline.com/getuserrealm.srf?login=something@defcorphq.onmicrosoft.com&xml=1`
		* Will return an XML file with useful information
* Get the Tenant ID
	* `https://login.microsoftonline.com/[DOMAIN]/.well-known/openid-configuration`
* Validate Email ID by sending requests to:\
	* `https://login.microsoftonline.com/common/GetCredentialType`
* Easier to just use some tools eh?
* We can use the AADInternals tool
	* https://github.com/Gerenios/AADInternals
		* PowerShell module that we will use for multiple attacks against AzureAD
	* `Import-Module C:\AzAD\Tools\AADInternals\AADInternals.psd1 -Verbose`
	* Get tenant name, authentication, brand name (usually same as directory name) and domain name
		* `Get-AADIntLoginInformation -UserName root@defcorphq.onmicrosoft.com`
	* Get tenant ID
		* `Get-AADIntTenantID -Domain defcorphq.onmicrosoft.com`
	* Get tenant domains
		* `Get-AADIntTenantDomains -Domain defcorphq.onmicrosoft.com`
		* `Get-AADIntTenantDomains -Domain deffin.onmicrosoft.com`
	* Get all the information
		* `Invoke-AADIntReconAsOutsider -DomainName defcorphq.onmicrosoft.com`

### Email IDs

* We can use o365creeper (https://github.com/LMGsec/o365creeper) to check if an email ID belongs to a tenant
* It makes requests to the GetCredentialType API that we saw earlier
	* `C:\Python27\python.exe`
	* `C:\AzAD\Tools\o365creeper\o365creeper.py -f`
	* `C:\AzAD\Tools\emails.txt -o`
	* `C:\AzAD\Tools\validemails.txt`

### Azure Services

* Azure services are available at specific domains and subdomains
* We can enumerate if the target organization is using any of the services by looking for such subdomains
* The tool that we will use for this is MicroBurst
	* https://github.com/NetSPI/MicroBurst
* MicroBurst is a useful tool for security assessment of Azure
	* Uses Az, AzureAD, AzurRM and MSOL tools and additional REST API calls
	* `Import-Module C:\AzAD\Tools\MicroBurst\MicroBurst.psm1 -Verbose`
* Enumerate all subdomains for an organization specified using the `-Base` parameter:
	* `Invoke-EnumerateAzureSubDomains -Base defcorphq -Verbose`


PASSWORD SPRAY
* We can use MSOLSpray (https://github.com/dafthack/MSOLSpray) for password spray against the accounts that we discovered
* The tool supports fireprox (https://github.com/ustayready/fireprox) to rotate source IP address on auth request
	* `C:\AzAD\Tools\MSOLSpray\MSOLSpray.ps1`
	* `Invoke-MSOLSpray -UserList C:\AzAD\Tools\validemails.txt -Password SuperVeryEasytoGuessPassword@1234 -Verbose`
* Overview
	* We will use a single password against multiple users that we have enumerated
	* This is definitely noisy and may lead to detection
	* For Azure, password spray attack can be done against different API endpoints like Azure AD Graph, Microsoft Graph, Office 365 Reporting webservice etc

* (Potentially) No Credentials Required
	* Azure - IP Ranges
		* Bash one liner to grab current Azure IP ranges

				download=$(curl -s https://www.microsoft.com/en-us/download/confirmation.aspx?id=41653 | grep '{base_0:{url:"' | cut -d ':' -f3,4 | cut -d '"' -f2) && curl -s $download | cut -d '"' -f2 | grep [0-9] | grep -v [a-zA-Z]
	* Search Microsoft Azure Active Directory for Vulnerable User Attributes (Powershell MSoL)
		* References
			* [https://twitter.com/dafthack/status/1248688920315002887](https://twitter.com/dafthack/status/1248688920315002887)
		* Comand

				import-module MSOnline
				Connect-MsolService
				$x=Get-MsolUser;foreach($u in $x){$p = @();$u|gm|%{$p+=$_.Name};ForEach($s in $p){if($u.$s -like "*passw*"){Write("[*]"+$u.UserPrincipalName+"["+$s+"]"+" : "+$u.$s)}}}
	* References
		* @dafthack, @ustayready -<br />[https://sans.org/cyber-security-summit/archives/file/summit-archive-1542324182.pdf](https://sans.org/cyber-security-summit/archives/file/summit-archive-1542324182.pdf)

* Blob Storage
	* Searching for Azure blob storage (Name must be between 3-24 characters)

			https://<name>.blob.core.windows.net
	* Discover blob storage account name (from Blue Cloud of Death by Bryce Kunz)

			gobuster -m dns -u "blob.core.windows.net" -i -t 100 -fw -w <wordlist>
	* Discover container names and blobs (from Blue Cloud of Death by Bryce Kunz)

			gobuster -m dir -u "https://<storage_account_name>.blob.core.windows.net/<container_name>/<blobname>" -i -t 100 -e -s 200,204 -w <wordlist>

* ROADtools
	* Resources
		* Tool [https://github.com/dirkjanm/ROADtools](https://github.com/dirkjanm/ROADtools)
		* blog/video -<br >[https://dirkjanm.io/introducing-roadtools-and-roadrecon-azure-ad-exploration-framework/](https://dirkjanm.io/introducing-roadtools-and-roadrecon-azure-ad-exploration-framework/)
	* Overview
		* Interacts with Microsoft's "internal" AzureAD API to pull information that's not available in other tools

* Credentials Required
	* Credentials Required
		* External Access Capabilities
			* References
				* [https://www.blackhillsinfosec.com/red-teaming-microsoft-part-1-active-directory-leaks-via-azure/](https://www.blackhillsinfosec.com/red-teaming-microsoft-part-1-active-directory-leaks-via-azure/)
			* Add guest users
			* Pull info
				* Users
				* Groups
				* Group Membership
				* Service Principles
				* Applications
	* Azure - CLI
		* Search .azure file on users system for .azureprofiles.json or accessToken.json(Can be used to login to Azure acount)

				az login
		* Login with Azure CLI (This also generates a cookie in the browser for .login.microsoftonline.com called ESTSAUTHPERSISTENT

				az account show
		* List account information includes subscription ID:

				az account set --subscription "<subname>"
		* Set subscription

				169.254.169.254
		* Querying Azure Metadata service:

				curl http://169.254.169.254/metadata/v1/InstanceInfo
		* Example usage(Get instance info):

				az vm extension
		* Run custom scripts
			* References
				* [https://docs.microsoft.com/en-us/azure/virtual-machines/extensions/custom-script-linux](https://docs.microsoft.com/en-us/azure/virtual-machines/extensions/custom-script-linux)
			* Command

					az storage blob list --account-name <account_name> --container <container_name>