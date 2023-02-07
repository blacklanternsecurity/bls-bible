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

# Azure Attack Guide

## Tags
<details><summary>Tags</summary><p>

`#@Azure #@AAD #@Token #@AccessToken #@RefreshToken #@Refresh #@Access #@Teams #@Outlook #@Graph #@O365`

</details>

## References

## Overview

## Attack Process

1. [Initial Access](Testaments_and_Books/Redvelations/Cloud/Azure/002-0_Azure_Initial_Access.md)
	- [Device Code Phish](Testaments_and_Books/Redvelations/Cloud/Azure/002-2_Azure_Device_Code_Phish.md)
	- [API and Auth Access](Testaments_and_Books/Redvelations/Cloud/Azure/002-1_Azure_API_and_Auth_Access.md)
	- [Azure Function Application Exploitation](Testaments_and_Books/Redvelations/Cloud/Azure/002-3_Function_Application_Exploitation.md)
	- [Azure App Service Exploitation](Testaments_and_Books/Redvelations/Cloud/Azure/002-4_App_Service_Exploitation.md)
	- [Illicit Consent Grant Phish](Testaments_and_Books/Redvelations/Cloud/Azure/002-5_Illicit_Consent_Grant.md)
1. Enumerate
1. Identify misconfigurations
1. Abuse misconfigurations
	- Azure Managed Identities
		- Basically the same as AWS IAM roles
		- [https://blog.netspi.com/azure-privilege-escalation-using-managed-identities/](https://blog.netspi.com/azure-privilege-escalation-using-managed-identities/)
1. [Persistence](Testaments_and_Books/Redvelations/Cloud/Azure/005-0_Azure_Persistence.md)
	- [Token Juggling](Testaments_and_Books/Redvelations/Cloud/Azure/005-1_Azure_Access_Token_Manipulation.md)

## Todo

- [https://github.com/boku7/azureOutlookC2](https://github.com/boku7/azureOutlookC2)
- [https://hub.steampipe.io/mods/turbot/azure_compliance/controls/benchmark.nist_sp_800_53_rev_5](https://hub.steampipe.io/mods/turbot/azure_compliance/controls/benchmark.nist_sp_800_53_rev_5)
- [https://github.com/darkquasar/AzureHunter](https://github.com/darkquasar/AzureHunter)
- [https://www.trustedsec.com/blog/creating-a-malicious-azure-ad-oauth2-application/](https://www.trustedsec.com/blog/creating-a-malicious-azure-ad-oauth2-application/)