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
# Azure Overview
### References
### Terminology

* Tenant
	* An instance of Azure AD, represents single organization
* Azure AD Directory
	* Each tenant has a dedicated directory.
	* Used to perform identity and access management functions for resources
* Subscriptions
	* Used to pay for services
	* Can have multiple per directory
* Core Domain
	* Initial domain name `<tenant>.onmicrosoft.com` is the core domain
	* Can define custom domain names

### Azure Architecture

* Resources are divided into levels
	* Management Groups
	* Subscriptions
	* Resource Groups
	* Resources
* Management Groups
	* Used to manage multiple subscriptions
	* Subsciptions inherit conditions applied to the management group
	* Subscriptions within a single management group belong to same Azure tenant
	* Management group can be placed in a lower hierarchy of another management group
	* Single top-level management group - **Root management group** - for each directory in Azure
	* Note: Global administration can always elevate their privileges to the Root management group
* Subscriptions
	* Logical unit of Azure services that links to an Azure account
	* Billing and/or access control boundary in an Azure AD Directory
	* Azure AD Directory may have multiple subscriptions but each subscription can only trust a single directory
	* Azure role applied at the subscription level applies to all the resources within the subscription
* Resource Groups and Resources
	* Resources are deployable items in Azure like VMs, App Services, Storage Accounts etc.
	* Resource Groups act as containers for resources
	* All resources must be inside a resource group and can belong only to a group
	* If a group is deleted, the resources inside are also deleted
	* groups have their own identity and access management settings for providing RBAC.
		* An Azure role applied to the resource group is applied to the resources within
* Managed Identity
	* Azure provides ability to assign Managed Identities to resources like app service, function apps, VMs, etc.
	* Managed Identity uses Azure AD tokens to access other resources (like key vaults, storage accounts) that support Azure AD authentication
	* It is a service principal of special type that can be used with Azure resources
	* Managed Identity can be system-assigned (tied to a resource and cannot be shared with other resources) or user-assigned (independent life cycle and can be shared across resources)
* Azure Resource Manager (ARM)
	* The client neutral deployment and management service for Azure that is used for lifecycle management (creating, updating and deleting) and access control of resources
	* ARM templates can be used for consistent and dependency-defined redeployment of resources

### Azure AD vs Azure

* Azure AD is not Azure
* Azure AD is a product offering within Azure
* Azure is Microsoft's cloud platform whereas Azure AD is enterprise identity service in Azure

### Azure AD vs On-Prem AD
* References
	* Microsoft Official Comparison of AAD vs. AD -<br />[https://docs.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-compare-azure-ad-to-ad](https://docs.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-compare-azure-ad-to-ad)
* Overview
	* The only similarity between the two is both are identity and access management solutions
	* Both may have some similar terms but NOT trying to look at Azure AD from the lens of on-prem AD concepts will be very useful
	* Azure AD is NOT directory services in the cloud. That one is Azure Active Directory Domain Services which provides 'domain controller as a service'
	* It is possible to integrate on-prem AD with Azure AD for a hybrid identity

## Azure RBAC Roles

* Azure RBAC Roles (simply Azure roles)
* There are over 70 built-in roles and we can define custom roles too
* There are four fundamental Azure roles
	* Owner
		* Permissions
			* Full access to all resources
			* Can manage access for other users
		* Applies On
			* All resource types
	* Contributor
		* Permissions
			* Full access to all resources
			* Cannot manage access
		* Applies On
			* All resource types
	* Reader
		* Permissions
			* View all resources
		* Applies On
			* All resource types
	* User Access Administrator
		* Permissions
			* View all resources
			* Can manage access for other users
		* Applies on
			* All resource types
* Azure AD roles are applicable on Azure AD resources like users, groups, domains, licenses etc
* There are many Administrator roles in Azure AD (see the slide note). We can also define custom roles.
* Global administrator is teh most well-known and all powerful administrator role
* Global administrator has the ability to 'elevate' to User Access Administrator Azure role to the root management group

### Tools

* Microsoft's Tools
	* az cli - To manage Azure resources
	* Az PowerShell module (Replaced the AzureRM and Azure module) - To manage Azure resources
	* AzureAD PowerShell module - To manage Azure AD
	* Some Microsoft portals (A comprehensive list is at https://msportals.io/)
* Open source PowerShell, .NET and C++ tools

### Needs Research

* [https://gist.github.com/xpn/f12b145dba16c2eebdd1c6829267b90c](https://gist.github.com/xpn/f12b145dba16c2eebdd1c6829267b90c)
* [https://github.com/dafthack/m365_groups_enum](https://github.com/dafthack/m365_groups_enum)
* MSOLSpray
	* PowerShell -<br />[https://github.com/dafthack/MSOLSpray](https://github.com/dafthack/MSOLSpray)
	* Python Rewrite -<br />[https://github.com/MartinIngesen/MSOLSpray](https://github.com/MartinIngesen/MSOLSpray)
* [https://github.com/0xZDH/o365spray](https://github.com/0xZDH/o365spray)
* [https://github.com/dafthack/MFASweep](https://github.com/dafthack/MFASweep)
