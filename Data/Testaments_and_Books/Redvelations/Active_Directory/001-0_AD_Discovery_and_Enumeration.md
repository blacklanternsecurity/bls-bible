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
# Active Directory Discovery and Enumeration (Internal) ([`Gather Victim Network Information - Domain Properties` TTP](TTP/T1590_Gather_Victim_Network_Information/001_Domain_Properties/T1590.001.md))
## Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@enum #@enumerate #@enumeration

Tools

		#@checklist

</p></details>

## References

## AD Ports and Services List
* <details><summary>References (Click to expand)</summary><p>
	* [https://docs.microsoft.com/en-us/troubleshoot/windows-server/networking/service-overview-and-network-port-requirements#system-services-ports](https://docs.microsoft.com/en-us/troubleshoot/windows-server/networking/service-overview-and-network-port-requirements#system-services-ports)
* <details><summary>Overview (Click to expand)</summary><p>
	* Active Directory Web Services (ADWS)
		* TCP 9389
	* Active Directory Management Gateway Service
		* TCP 9389
	* Global Catalog
		* TCP 3269
	* Global Catalog
		* TCP 3268
	* ICMP
		* No port number
	* Lightweight Directory Access Protocol (LDAP) Server 	
		* TCP 389
	* LDAP Server
		* UDP 389
	* LDAP SSL
		* TCP 636
	* IPsec ISAKMP
		* UDP 500
	* NAT-T
		* UDP 4500
	* RPC
		* TCP 135
	* RPC randomly allocated high TCP ports
		* TCP
			* 1024 - 5000
			* 49152 - 65535
	* SMB
		* TCP 445

## Overview

What makes this guide different from the [Active Directory Attack Guide](Testaments_and_Books/Redvelations/Active_Directory/000-0_AD_Attack_Guide.md) is that it's intended to solve two objectives:

* Provide a well-rounded situational awareness. This is essential knowledge to knowing if you can complete an attack.
* Additional attack vector discovery

Note that there is a distinction between Active Directory and Networking.

* Active Directory, in short, provides a particular set of benefits for managing a network.
* Separately, all networks have certain aspect in common at the base level that do not require active directory to be present, covered by the [Network Enumeration Guide](Testaments_and_Books/Redvelations/Network/001-0_Network_Enumeration.md).


## Checklist
### No domain credentials required (usually)
* Key Server Hostnames and IP Address Collection
	* [ ] - DHCP Server
		* Enumeration: [AD DHCP Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-1_AD_DNS_and_DHCP_Enumeration.md)
	* [ ] - DNS Server
		* Enumeration: [AD DNS Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-1_AD_DNS_and_DHCP_Enumeration.md)
	* [ ] - Domain Controller(s)
		* [ ] - Primary Domain Controller (AD FSMO Roles' PDC)
			* Responsible for tracking failed login attempts
	* [ ] - Exchange Servers
		* Enumeration: [AD DHCP Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-1_AD_DNS_and_DHCP_Enumeration.md)
	* [ ] - Any other servers that should be considered "Microsoft Tier 1" in AD Structure
	* [ ] - ADCS Server
* Network Information
	* [ ] - [Network Enumeration Checklist](Testaments_and_Books/Redvelations/Network/001-0_Network_Enumeration.md)
		* Checklist includes vulnerability checks and network design
* Domain Properties
	* DNS ([AD DNS Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-1_AD_DNS_and_DHCP_Enumeration.md))
		* [ ] - Are NBT-NS, LLMNR, or mDNS enabled?
		* [ ] - Does a DNS zone transfer reveal any information? (Not OpSec friendly)
	* LDAP ([LDAP Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-2_LDAP_Enumeration.md))
		* [ ] - Does the domain require LDAP signing/binding?
		* [ ] - What is the domain functional level?
		* [ ] - Does the domain utilize LDAP or LDAPS?
			* Retrievable information from DNS ([AD DNS Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-1_AD_DNS_and_DHCP_Enumeration.md))
		* [ ] - Can user information be enumerated from LDAP anonymously?
	* SMB ([SMB Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-3_SMB_Enumeration.md))
		* [ ] - What hosts are using legacy SMB protocol (SMBv1)?
		* [ ] - What hosts do not require SMB signing?
		* [ ] - What useful information can be retrieved from null authentications?
			* Password Policy, Group Information, Users
	* RPC ([RPC Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-4_RPC_Enumeration.md))
		* [ ] - Can any interesting RPC handles be accessed anonymously?
		* [ ] - Can user information be enumerated from RPC anonymously?
		* [ ] - Are forced authentication misconfigurations present?
	* File Shares ([File Share Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-7_File_Share_Enumeration.md))
		* [ ] - Can any shares be anonymously accessed?
		* [ ] - What data is available on file shares?
	* (Unuathenticated) AD Vulnerabilities and Misconfigurations
		* [ ] - What vulnerabilities does AD have directly?
			* Enumeration: [AD CVE Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-6_AD_CVE_Enumeration.md)

### Domain User Credentials Required (Usually)
* Key Server Hostnames and IP Address Collection
    * [ ] - ADCS Server (if not identifiable anonymously)
* Domain Properties
	* LDAP ([LDAP Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-2_LDAP_Enumeration.md))
		* [ ] - What AD Trusts are present?
		* [ ] - Are there accounts (user *or* computer!) that have never logged on?
			* [ ] - Are there computer accounts that additionally do not require a password?
				* [ ] - Do any of the computer accounts meeting the above two criteria produce the following message when you attempt to logon with the username as the password (lowercase, no `$` included in password)? `STATUS_NOLOGON_WORKSTATION_TRUST_ACCOUNT`
		* [ ] - Who are the members of privileged groups?
		* [ ] - Have passwords not been reset recently on any potentially high-value targets?
		* [ ] - What information does LDAP reveal about the currently compromised accounts?
		* [ ] - Does broad LDAP enumeration (e.g., ADExplorer, BloodHound, Adalanche) reveal anything interesting?
		* [ ] - What differences are there between standard domain user password policies and privileged domain users?
		* [ ] - What information is stored in account descriptions?
	* SMB ([SMB Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-3_SMB_Enumeration.md))
		* [ ] - What systems have the WebDAV service running?
		* [ ] - Who are the domain users?
		* [ ] - Who are the domain computers?
		* [ ] - What are the domain groups?
		* [ ] - Who are members of sensitive groups?
	* RPC ([RPC Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-4_RPC_Enumeration.md))
		* [ ] - Who are the domain's users/computers?
		* [ ] - What is the domain's SID?
		* [ ] - What are the domain groups and their members?
		* [ ] - Is there any interesting user information for the compromised users?
		* [ ] - What is the domain password policy?
		* [ ] - Are forced authentication misconfigurations present?
* Network Information
	* Subnet information
		* [ ] - What subnets contain the systems managed by the domain controller?
			* [LDAP Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-2_LDAP_Enumeration.md)
			* [ ] - What systems/subnets are revealed through LDAP queries supplemented by DNS validation?
				* [DNS Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-1_AD_DNS_and_DHCP_Enumeration.md)
* File Shares ([File Share Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-7_File_Share_Enumeration.md))
	* [ ] - Can any shares be accessed?
	* [ ] - What data is available on file shares?
* AD Vulnerabilities and Misconfigurations ([AD CVE Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-6_AD_CVE_Enumeration.md))
	* [ ] - What vulnerabilities does AD have directly?
* ADCS ([ADCS Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-5_ADCS_Enumeration.md))
	* [ ] - What certificate templates can be used for authentication?
	* [ ] - Are certificate templates vulnerable to abuse?
	* [ ] - Does broad ADCS enumeration reveal anything interesting?

### Local Administrator Credentials Required (Usually)
* SMB ([SMB Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-3_SMB_Enumeration.md))
	* [ ] - What accounts have sessions on a systems where you have local administrator privileges?
	* [ ] - What accounts are logged on to systems where you have local administrator privileges?

### Privileged Domain User Account is Compromised
* RPC ([RPC Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-4_RPC_Enumeration.md))
	* [ ] - What differences are there in authentication requirements for privileged users (e.g., different password policies)?


## CLICK-TO-COPY CHECKLIST

```
## Checklist
### No domain credentials required (usually)
* Key Server Hostnames and IP Address Collection
	* [ ] - DHCP Server
			* [ ] - DNS Server
			* [ ] - Domain Controller(s)
		* [ ] - Primary Domain Controller (AD FSMO Roles' PDC)
			* Responsible for tracking failed login attempts
	* [ ] - Exchange Servers
			* [ ] - Any other servers that should be considered "Microsoft Tier 1" in AD Structure
	* [ ] - ADCS Server
* Network Information
	* [ ] - Network Enumeration Checklist
		* Checklist includes vulnerability checks and network design
* Domain Properties
	* DNS
		* [ ] - Are NBT-NS, LLMNR, or mDNS enabled?
		* [ ] - Does a DNS zone transfer reveal any information? (Not OpSec friendly)
	* LDAP
		* [ ] - Does the domain require LDAP signing/binding?
		* [ ] - What is the domain functional level?
		* [ ] - Does the domain utilize LDAP or LDAPS?
			* Retrievable information from DNS
		* [ ] - Can user information be enumerated from LDAP anonymously?
	* SMB
		* [ ] - What hosts are using legacy SMB protocol (SMBv1)?
		* [ ] - What hosts do not require SMB signing?
		* [ ] - What useful information can be retrieved from null authentications?
			* Password Policy, Group Information, Users
	* RPC
		* [ ] - Can any interesting RPC handles be accessed anonymously?
		* [ ] - Can user information be enumerated from RPC anonymously?
		* [ ] - Are forced authentication misconfigurations present?
	* File Shares
		* [ ] - Can any shares be anonymously accessed?
		* [ ] - What data is available on file shares?
	* (Unuathenticated) AD Vulnerabilities and Misconfigurations
		* [ ] - What vulnerabilities does AD have directly?
			
### Domain User Credentials Required (Usually)
* Key Server Hostnames and IP Address Collection
    * [ ] - ADCS Server (if not identifiable anonymously)
* Domain Properties
	* LDAP
		* [ ] - What AD Trusts are present?
		* [ ] - Are there accounts (user *or* computer!) that have never logged on?
			* [ ] - Are there computer accounts that additionally do not require a password?
				* [ ] - Do any of the computer accounts meeting the above two criteria produce the following message when you attempt to logon with the username as the password (lowercase, no `$` included in password)? `STATUS_NOLOGON_WORKSTATION_TRUST_ACCOUNT`
		* [ ] - Who are the members of privileged groups?
		* [ ] - Have passwords not been reset recently on any potentially high-value targets?
		* [ ] - What information does LDAP reveal about the currently compromised accounts?
		* [ ] - Does broad LDAP enumeration (e.g., ADExplorer, BloodHound, Adalanche) reveal anything interesting?
		* [ ] - What differences are there between standard domain user password policies and privileged domain users?
		* [ ] - What information is stored in account descriptions?
	* SMB
		* [ ] - What systems have the WebDAV service running?
		* [ ] - Who are the domain users?
		* [ ] - Who are the domain computers?
		* [ ] - What are the domain groups?
		* [ ] - Who are members of sensitive groups?
	* RPC
		* [ ] - Who are the domain's users/computers?
		* [ ] - What is the domain's SID?
		* [ ] - What are the domain groups and their members?
		* [ ] - Is there any interesting user information for the compromised users?
		* [ ] - What is the domain password policy?
		* [ ] - Are forced authentication misconfigurations present?
* Network Information
	* Subnet information
		* [ ] - What subnets contain the systems managed by the domain controller?
			* [ ] - What systems/subnets are revealed through LDAP queries supplemented by DNS validation?
* File Shares
	* [ ] - Can any shares be accessed?
	* [ ] - What data is available on file shares?
* AD Vulnerabilities and Misconfigurations
	* [ ] - What vulnerabilities does AD have directly?
* ADCS
	* [ ] - What certificate templates can be used for authentication?
	* [ ] - Are certificate templates vulnerable to abuse?
	* [ ] - Does broad ADCS enumeration reveal anything interesting?

### Local Administrator Credentials Required (Usually)
* SMB
	* [ ] - What accounts have sessions on a systems where you have local administrator privileges?
	* [ ] - What accounts are logged on to systems where you have local administrator privileges?

### Privileged Domain User Account is Compromised
* RPC
	* [ ] - What differences are there in authentication requirements for privileged users (e.g., different password policies)?
```