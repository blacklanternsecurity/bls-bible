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
# AD Services
### Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@services #@service #@exchange #@file #@files #@share #@shares

Tools

		#@certi #@certipy #@certify #@rubeus

</p></details>

### References


### AD Ports and Services List
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

### Services

* [DNS and DHCP](Testaments_and_Books/Redvelations/Active_Directory/005-1_AD_DNS_and_DHCP.md)
* [File Share](Testaments_and_Books/Redvelations/Active_Directory/005-5_File_Share.md)
* [Exchange](Testaments_and_Books/Redvelations/Active_Directory/005-6_Exchange.md)