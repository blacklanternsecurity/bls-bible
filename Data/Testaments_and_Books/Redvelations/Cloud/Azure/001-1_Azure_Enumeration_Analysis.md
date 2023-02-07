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
# Azure Enumeration Analysis

### Overview

### Process

### StormSpotter

* StormSpotter (https://github.com/Azure/StormSpotter) is a tool from Microsoft for creating attack graphs of Azure resources
* It uses the Neo4j graph database to create graphs for relationships in Azure and Azure AD
* It has following modules
	* Backend - Used for ingesting the data in the Neo4j database
	* Frontend (WebApp) - UI used for visualizing the data
	* Collector - Used to collect the data from Azure
* Start the backend service
	* `cd C:\AzAD\Tools\stormspotter\backend\`
	* `pipenv shell`
	* `python ssbackend.pyz`
* In a new process, Start the frontend webserver
	* `cd C:\AzAD\Tools\stormspotter\frontend\dist\spa\`
	* `quasar.cmd server -p 9091 --history`
* Use Stormcollector to collect the data
	* `cd C:\AzAD\Tools\stormspotter\stormcollector\`
	* `pipenv shell`
	* `az login -u test@defcorphq.onmicrosoft.com -p SuperVeryEasytoGuessPassword@1234`
	* `python C:\AzAD\Tools\stormspotter\stormcollector\sscollector.pyz cli`
* Log-on to the webserver at http://localhost:9091 using the following:
	* Username: neo4j
	* Password: BloodHound
	* Server: bolt://localhost:7687
* After login, upload the ZIP archive created by the collector
* Use the built-in queries to visualize the data

### BloodHound

* BloodHound's AzureHound (https://github.com/BloodHoundAD/AzureHound) supports Azure and Azure AD too to map attack paths
* It uses Azure AD and Az PowerShell modules for gathering the data through its collectors
	* If you do not have them installed already, in a adminstrative powershell session run the following and accept all requests
		* `Install-Module Az`
		* `Install-Module AzureAD`
* Run the collector to gather data:
* You can also find this (more up to date) in the normal BloodHound repository under `/Collectors`
* A neat thing to do if possible, run both `SharpHound.ps1` and `AzureHound.ps1`. Their results can both be imported into the same neo4j database and analyzed together

		$passwd = ConvertTo-SecureString "SuperVeryEasytoGuessPassword@1234" -AsPlainText -Force
		$creds = New-Object System.Management.Automation.PSCredential("test@defcorphq.onmicrosoft.com", $passwd)
		Connect-AzAccount -Credential $creds
		Connect-AzureAD -Credential $creds
		C:\AzAD\Tools\AzureHound\AzureHound.ps1
		Invoke-AzureHound -Verbose


* Open the BloodHound application (`C:\AzAD\Tools\BloodHound-win32-x64\BloodHound-win32-x64\BloodHound.exe`) and login using the following details
	* Username: neo4j
	* Password: BloodHound
* Upload the ZIP archive to BloodHound UI (drag and drop) and use built-in or custom Cypher queries to query the data. Some examples are below:
	* Find all users who have the Global Administrator role:
		* `MATCH p = (n)-[r:AZGlobalAdmin*1..]->(m) RETURN p`
	* Find all paths to an Azure VM
		* `MATCH p = (n)-[r]->(g:AZVM) RETURN p`
	* Find all paths to an Azure KeyVault
		* `MATCH p = (n)-[r]->(g:AZKeyVault) RETURN p`
	* Find all paths to an Azure Resource Group
		* `MATCH p = (n)-[r]->(g:AZResrouceGroup) RETURN p`
	* Find Owners of Azure Groups
		* `MATCH p = (n)-[r:AZOwns]->(g:AZGroup) RETURN p`
	* Return All Azure Users and their Groups
	* `MATCH p=(m:AZUser)-[r:MemberOf]->(n) WHERE NOT m.objectid CONTAINS 'S-1-5' RETURN p`
	* Return All Azure AD Groups that are synchronized with On-Premise AD
	* `MATCH (n:Group) WHERE n.objectid CONTAINS 'S-1-5' AND n.azsyncid IS NOT NULL RETURN n`
	* Find all Privileged Service Principals
	* `MATCH p = (g:AZServicePrincipal)-[r]->(n) RETURN p`
	* Find all Owners of Azure Applications
	* `MATCH p = (n)-[r:AZOwns]->(g:AZApp) RETURN p`
* Neo4j console (usually located at http://localhost:7474)
	* Return All Azure Users
	* `MATCH (n:AZUser) return n.name`
	* Return All Azure Applications
	* `MATCH (n:AZApp) return n.objectid`
	* Return All Azure Devices
	* `MATCH (n:AZDevice) return n.name`
	* Return All Azure Groups
	* `MATCH (n:AZGroup) return n.name`
	* Return all Azure Key Vaults
	* `MATCH (n:AZKeyVault) return n.name`
	* Return all Azure Resource Groups
	* `MATCH (n:AZResourceGroup) return n.name`
	* Return all Azure Service Principals
	* `MATCH (n:AZServicePrincipal) return n.objectid`
	* Return all Azure Virtual Machines
	* `MATCH (n:AZVM) return n.name`
	* Find All Principals with the ‘Contributor’ role
	* `MATCH p = (n)-[r:AZContributor]->(g) RETURN p`
* https://github.com/hausec/Bloodhound-Custom-Queries
* AzureHound/BloodHound does not play well with very large organizations
	* AzureHound Considerations
		* With very large organizations, running AzureHound on a VM with 2-4GB of RAM will likely not be sufficient
	* Success has been had only using the host Dell XPS system
	* BloodHound Considerations
	* With very large JSON result files, in the >2GB range, BloodHound will not be able to handle the size.
	* You can chunk the JSON file with the following python script:
		* [script](Testaments_and_Books/Redvelations/Cloud/Azure/scripts/Azurehound-Bloodhound-JSON-Chunking.py)

## Azure Blob Storage

* Blob storage is used to store unstructured data (like files, videos, audio, etc)
* Three types of resources in blob storage
	* Storage account - unique namespace across Azure. Can be accessed over HTTP or HTTPs
	* Container in the storage account - 'Folders' in the storage account
	* Blob in a container - Stores data. Three types of blobs
* A storage account has globally unique endpoints
* Very useful in enumeration too by guessing the storage account names
	* Blob Storage
		* `https://<storage-account>.blob.core.windows.net`
	* Azure Data Lake Storage Gen2
		* `https://<storage-account>.dfs.core.windows.net`
	* Azure Files
		* `https://<storage-account>.file.core.windows.net`
	* Queue Storage
		* `https://<storage-account>.queue.core.windows.net`
	* Table Storage
		* `https://<storage-account>.table.core.windows.net`

### Storage Account

#### Authorization

* There are multiple ways to control access to a storage account
	* Use Azure AD credentials - Authorize user, group or other identities based on Azure AD authentication. RBAC roles supported
	* Share Key - Use access keys of the storage account. This provides full access to the storage account
	* Shared Access Signature (SAS) - Time limited and specific permissions

#### Anonymous Access

* By default, anonymous access is not allowed for storage accounts
* If 'Allow Blob public access' is allowed on the storage account, it is possible to configure anonymous/public read access to:
	* Only the blobs inside containers. Listing of container content not allowed
	* Contents of container and blobs

##### Abuse

* The knowledge that Storage accounts have globally unique endpoints and can allow public read access comes handy
* Let's try to find out insecure storage blobs in the defcorphq tenant
* We can add permutations like common, backup, code to the `permutations.txt` in `C:\AzAD\Tools\Microburst\Misc` to tune it for defcorphq
* We can then use the below command from MicroBurst:
	* `Invoke-EnumerateAzureBlobs -Base defcorp`

#### Storage Explorer

* Storage explorer is a standalone desktop app to work with Azure storage accounts
* It is possible to connect using access keys, SAS urls, etc