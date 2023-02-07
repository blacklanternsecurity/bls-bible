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

# Azure Persistence

## Tags
<details><summary>Tags</summary><p>

`#@Azure #@AAD #@Token #@AccessToken #@RefreshToken #@Refresh #@Access #@Teams #@Outlook #@Graph #@O365`

</details>

Like any other system, Azure provides many interesting persistence opportunities. Look for persistence, wherever we can modify or create a resource or permission or have an access that is not time limited.

## Hybrid Identity

* On-Prem to Cloud
	* It is recommended by Microsoft to join the Azure AD Connect server to the on-prem AD
	* This means that the persistence mechanisms for on-prem (like Golden Ticket, Silver Ticket, ACL Backdoors and others) that provide us either DA on the on-prem or local admin on the Azure AD connect server will allow usto get GA on Azure AD on demand
		* For PHS, we can extract the credentials
		* For PTA, we can install the agent
		* For Federation, we can extract the certificate from ADFS server using DA
* PTA and PHS
	* If self service password reset is enabled (which allows users to reset their own Azure AD passwords) and the reset is propagated to on-prem AD using password write back, it opens up interesting persistence scenario
	* If we have already compromised on-prem AD, we can provide high permissions (DCSync using AdminSDHolder) to a synced user that we control and can then reset password for the user from Azure AD (where it will not be an administrator). This will give us DA privs on-prem that we can use to get GA on Azure AD
	* Since Azure AD connect does not support resetting passwords of accounts with admincount we need to use attacks like FullControl/DCSync permissions using AdminSDHolder

## Federation Services

* Trusted Domain
	* If we have GA privileges on a tenant, we can add a new domain (must be verified), configure its authentication type to Federated and configure the domain to trust a specific certificate (any.sts in the below command)and issuer. Using AADInternals:
		* `ConvertTo-AADIntBackdoor -DomainName cyberranges.io`
	* Get ImmutableID of the user that we want to impersonate. Using Msol module:
		* `Get-MsolUser | select userPrincipalName,ImmutableID`
	* Access any cloud apps as the user:
		* `Open-AADIntOffice365Portal -ImmutableID ID-HERE -Issuer "http://any.sts/B121241" -UseBuiltInCertificate -ByPassMFA $true`
* Token Signing Certificate
	* With DA privileges on on-prem AD, it is possible to create and import new Token signing and Token Decrypt certificates that have a very long validity
	* This will allow us to log-in as any user whose ImmutableID we know
	* Run the below command as DA on the ADFS server(s) to create new certs (default password 'AADInternals'), add them to ADFS, disable auto rollover and restart the service
		* `New-AADIntADFSSelfSignedCertificates`
	* Update the certificate information with Azure AD
		* `Update-AADIntADFSFederationSettings -Domain cyberranges.io`
	* Previous certificates will remain and still function properly

## Storage Account Access Keys

* We already know that keys provide root equivalent privileges on a storage account
* There are two access keys and they are NOT rotated automatically (unless a key vault is managing the keys)
* This, of course, provides neat persistent access to the storage account
* We can also generate SAS URL (including offline minting) using the access keys

## Applications and Service Principals

* Azure AD Enterprise Applications (service principals) and App Registration (applications) can be used for persistence
* With privileges of Application Administrator, GA or a custom role with `microsoft.directory/applications/credentials/update` permissions, we can add credentials (secret or certificate) to an existing application
* By targeting an application with high permissions this is a very useful persistence mechanism
* It also allows to bypass MFA
* We can also add a new application that has high permissions and then use that for persistence
* If we have GA privileges, we can create an application with the Privileged authentication administrator role - that allows to reset password of Global Administrators
* Would generate an email alert that a privileged role was assigned, unfortunately this is typically lost in the weeds
* Sign in as a service principal using Az PowerShell (Use the application ID as the username, and secret as password)
	* `$passwd = ConvertTo-SecureString "put-secret-in-quotes" -AsPlainText -Force`
	* `$creds = New-Object System.Management.Automation.PSCredential ("put-application-id-in-quotes", $passwd)`
	* `Connect-AzAccount -ServicePrincipal -Credential $creds -Tenant put-tenant-id-here`
* For certificate based authentication
	* `Connect-AzAccount -ServicePrincipal -Tenant tenant-id-here -CertificateThumbprint thumbprint-here -ApplicationId application-id-here`
* We can use az cli too to sign in as a service principal

## Azure VMs and NSGs

* OS level persistence on an Azure VM where we have remote access is very useful
* Azure VMs also support managed identity so persistence on any such VM will allow us access to additional Azure resources
* We can also create snapshot of disk attached to a running VM. This can be used to extract secrets stored on disk (like SAM hive for Windows)
* It is also possible to attach a modified/tampered disk to a turned-off VM. For example, add a local administrator
* Couple this with modification of NSGs to allow access from IPs that we control

## Custom Azure AD Roles

* If we have GA in a tenant, we can modify a custom role and assign that to a user that we control
* Take a look at the permissions of the built-in administrative roles, we can pick individual actions. It is always helpful to go for minimal privileges
	* https://docs.microsoft.com/en-us/azure/active-directory/roles/permissions-reference
* For example, Actions allowed to Application Developer are good enough for a low-privilege persistence as they allow application registration even if - "Users can register applications" setting is set to No

## Deployment Modification

* Recall the Github account that we compromise earlier
* If we have persistent access to external resources like GitHub repos that are a part of deployment chain, it will be possible to persist in the target tenant
* Often, a GitHub account would not have same level of security and monitoring compared to an Azure AD account with similar privileges
* This is just an example, deployment modification has a huge attack surface

## Token Juggling

* It is possible to keep renewing a refresh token before it expires
* This can be mitigated by conditional access policies (Premium P1 subscription)
* [Token Juggling](Testaments_and_Books/Redvelations/Cloud/Azure/005-1_Azure_Access_Token_Manipulation.md)