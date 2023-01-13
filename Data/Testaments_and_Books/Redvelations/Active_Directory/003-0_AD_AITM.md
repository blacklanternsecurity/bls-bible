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
# AD AITM
### Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@pcap #@packet #@capture #@poison #@arp #@traficc #@collect #@collection #@pcaptools

Tools

		#@tcpdump #@eavesarp #@eavesarp.py

</p></details>

### References
### Overview
* Cleartext protocols common to AD
	* FTP (tcp port 20, 21)
	* Telnet (tcp port 23)
	* SMTP (tcp port 25)
	* HTTP (tcp port 80)
	* POP3 (tcp port 110)
	* IMAP4 (tcp port 143)
	* SNMP (udp port 161, 162)
	* LDAP (tcp port 389)
	* SOCKS (tcp port 1080)
	* MSSQL (tcp port 1433)
	* XMPP (tcp port 5222)
	* PostgreSQL (tcp port 5432)
	* IRC (tcp port 6667)


* ([`Adversary-in-the-Middle - LLMNR-NBT-NS Poisoning and SMB Relay By responding to LLMNR-NBT-NS network traffic` TTP](TTP/T1557_Adversary-in-the-Middle/001_LLMNR-NBT-NS_Poisoning_and_SMB_Relay_By_responding_to_LLMNR-NBT-NS_network_traffic/T1557.001.md))


### Process to MITM Network Traffic ([`Adversary-in-the-Middle` TTP](TTP/T1557_Adversary-in-the-Middle/T1557.md))

* ([`Adversary-in-the-Middle - ARP Cache Poisoning` TTP](TTP/T1557_Adversary-in-the-Middle/002_ARP_Cache_Poisoning/T1557.002.md))
* [`Network Sniffing` TTP](TTP/T1040_Network_Sniffing/T1040.md)

1. Passive Network Traffic Collection
	* <details><summary>Generate a pcap (Click to expand)</summary><p>
		* tcpdump

				tcpdump -i <interface> -w <outfile.pcap>
	* <details><summary>Repositories (Click to expand)</summary><p>
		* Awesome PCAPTools -<br />[https://github.com/caesar0301/awesome-pcaptools](https://github.com/caesar0301/awesome-pcaptools)
	* <details><summary>Eavesarp (Click to expand) -<br />[https://github.com/arch4ngel/eavesarp](https://github.com/arch4ngel/eavesarp)</summary><p>

			python eavesarp.py capture -i <interface>
