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
# SIP Port 5060

* SIP Enumeration
	* netcat

			nc IP_Address Port
	* sipflanker

			python sipflanker.py 192.168.1-254
	* Sipscan
	* smap

			smap IP_Address/Subnet_Mask
			smap -o IP_Address/Subnet_Mask
			smap -l IP_Address
* SIP Packet Crafting etc.
	* sipsak
		* Tracing paths:

				sipsak -T -s sip:usernaem@domain
		* Options request:

				sipsak -vv -s sip:username@domain
		* Query registered bindings:

				sipsak -I -C empty -a password -s sip:username@domain
	* siprogue
* SIP Vulnerability Scanning/ Brute Force
	* tftp bruteforcer
		* Default dictionary file
		
			./tftpbrute.pl IP_Address Dictionary_file Maximum_Processes
	* VoIPaudit
	* SiVuS
* Examine Configuration Files
	* `SIPDefault.cnf`
	* `asterisk.conf`
	* `sip.conf`
	* `phone.conf`
	* `sip_notify.conf`
	* `<Ethernet address>.cfg`
	* `000000000000.cfg`
	* `phone1.cfg`
	* `sip.cfg etc. etc.`
