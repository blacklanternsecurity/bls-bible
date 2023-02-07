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
# Network Application and Service Enumeration
## References

## Overview

* Several TTPs are used across most of the steps below, including:
	* Software Discovery ([`Software Discovery` TTP](TTP/T1518_Software_Discovery/T1518.md))
	*  Network Service Scanning ([`Network Service Scanning` TTP](TTP/T1046_Network_Service_Scanning/T1046.md)
	* System Service Discovery ([System Service Discovery TTP](TTP/T1007_System_Service_Discovery/T1007.md))
* Some common follow-ups after performing discovery:
	* Identify if a domain controller is present
		* <details><summary>Example Domain Controller Ports (Click to expand)</summary><p>

				Starting Nmap 7.80 ( https://nmap.org ) at 2021-11-06 21:30 PDT
				Nmap scan report for dc01 (10.0.0.1)
				Host is up (0.00097s latency).
				Not shown: 65509 closed ports
				PORT	   STATE SERVICE
				53/tcp	 open  domain
				88/tcp	 open  kerberos-sec
				135/tcp   open  msrpc
				139/tcp   open  netbios-ssn
				389/tcp   open  ldap
				445/tcp   open  microsoft-ds
				464/tcp   open  kpasswd5
				593/tcp   open  http-rpc-epmap
				636/tcp   open  ldapssl
				3268/tcp  open  globalcatLDAP
				3269/tcp  open  globalcatLDAPssl
				5985/tcp  open  wsman
				9389/tcp  open  adws
				47001/tcp open  winrm
				49664/tcp open  unknown
				49665/tcp open  unknown
				49666/tcp open  unknown
				49667/tcp open  unknown
				49669/tcp open  unknown
				49670/tcp open  unknown
				49671/tcp open  unknown
				49672/tcp open  unknown
				49679/tcp open  unknown
				49681/tcp open  unknown
				49687/tcp open  unknown
				49703/tcp open  unknown

## Enumeration
### Port and Service Scanning
* <details><summary>SpooNMAP (Click to expand) -<br />[https://github.com/trustedsec/spoonmap](https://github.com/trustedsec/spoonmap)</summary><p>
	* "This script is simply a wrapper for NMAP and Masscan."
* <details><summary>nmap ([nmap tool guide](Testaments_and_Books/Redvelations/Tools/Port_and_Service_Enumeration/nmap.md)) (Click to expand)</summary><p>

		nmap -sC -sV -T4 -oA <outfile_name> $SUBNET_CIDR
	* Select Parameters
		* `-sC` - Run scripts on identified ports
		* `-sV` - Enumerate version information of ports
		* `-T` - Speed, 1-5. Faster speeds risk greater chance of inaccurate results.
		* Output
			* `-oA` - Output all formats
		* `-Pn` - Assume host is up. Often necessary for Windows targets.
* <details><summary>zmap (Click to expand)</summary><p>
	* Example

			zmap .
* <details><summary>BLS zmap Asset Inventory Script (Click to expand) -<br />[https://github.com/blacklanternsecurity/zmap-asset-inventory](https://github.com/blacklanternsecurity/zmap-asset-inventory)</summary><p>


### Applications
#### Web
* Exposed Web Services
	* <details><summary>Project Discovery's httpx (Click to expand)</summary><p>
		* Enumerate http addresses from a target IP list
			* Command

					httpx -l TARGETS.txt -o nuclei-targets.txt
				* Example Output

						   / /_  / /_/ /_____ | |/ /
						  / __ \/ __/ __/ __ \|   /
						 / / / / /_/ /_/ /_/ /   |
						/_/ /_/\__/\__/ .___/_/|_|
						             /_/              v1.2.4

								projectdiscovery.io

						Use with caution. You are responsible for your actions.
						Developers assume no liability and are not responsible for any misuse or damage.
						https://10.0.0.100
						http://10.0.0.50
	* Auto-Screenshot
		* <details><summary>Recommended: witness me (Click to expand) -<br />[https://github.com/byt3bl33d3r/WitnessMe](https://github.com/byt3bl33d3r/WitnessMe)</summary><p>

				witnessme screenshot 10.0.1.0/24 192.168.0.1-20 ~/my_nessus_scan.nessus ~/my_nmap_scan.xml
		* <details><summary>gowitness (Click to expand) -<br />[https://github.com/sensepost/gowitness](https://github.com/sensepost/gowitness)</summary><p>

				gowitness scan --cidr <cidr> --threads <threads>
		* <details><summary>eyewitness -<br />[https://github.com/FortyNorthSecurity/EyeWitness](https://github.com/FortyNorthSecurity/EyeWitness) (Click to expand)</summary><p>

				python EyeWitness.py -f urls.txt --web --proxy-ip 127.0.0.1 --proxy-port 8080 --proxy-type socks5 --timeout 120

### CVE and Misconfiguration Discovery ([`Active Scanning - Vulnerability Scanning` TTP](TTP/T1595_Active_Scanning/002_Vulnerability_Scanning/T1595.002.md))

* Several
	* <details><summary>BLS zmap Asset Inventory Script (Click to expand) -<br />[https://github.com/blacklanternsecurity/zmap-asset-inventory](https://github.com/blacklanternsecurity/zmap-asset-inventory)</summary><p>

		    ./asset_inventory.py -M all
	* <details><summary>nmap scripts (Click to expand)</summary><p>
		* `-sC` - 
		* <details><summary>`--script` - Top recommendations (Click to expand)</summary><p>
			* .
* Default Credentials
	* SSH
		* <details><summary>BLS zmap Asset Inventory Script (Click to expand) -<br />[https://github.com/blacklanternsecurity/zmap-asset-inventory](https://github.com/blacklanternsecurity/zmap-asset-inventory)</summary><p>

				./asset_inventory.py -M default-ssh
* BlueKeep
	* <details><summary>aconite33: Detect Bluekeep -<br />[https://github.com/aconite33/detect_bluekeep.py](https://github.com/aconite33/detect_bluekeep.py) (Click to expand)</summary><p>
* Windows
	* Eternal Blue
		* <details><summary>BLS zmap Asset Inventory Script (Click to expand) -<br />[https://github.com/blacklanternsecurity/zmap-asset-inventory](https://github.com/blacklanternsecurity/zmap-asset-inventory)</summary><p>

				./asset_inventory.py -M eternalblue
* Remove Management Services
	* Default open VNC
		* <details><summary>BLS zmap Asset Inventory Script (Click to expand) -<br />[https://github.com/blacklanternsecurity/zmap-asset-inventory](https://github.com/blacklanternsecurity/zmap-asset-inventory)</summary><p>

				./asset_inventory.py -M open-vnc
* File Shares
	* All types (SMB, FTP, and NFS)
		* <details><summary>BLS zmap Asset Inventory Script (Click to expand) -<br />[https://github.com/blacklanternsecurity/zmap-asset-inventory](https://github.com/blacklanternsecurity/zmap-asset-inventory)</summary><p>

			    ./asset_inventory.py -M open-shares
* Application
	* Web
		* Project Discovery One-Liner
			* Tools used (must be installed)
				* httpx
				* nuclei
				* nabuu
			* Example

					echo evilcorp.com | subfinder -silent  | sudo nabuu -retries 1 -c 256 -top-ports 1000 -silent | httpx -t 256 -silent | nuclei -rl 500 -t nuclei-templates-bls -tags security-survey -stats
		* Project Discovery's nuclei
			* <details><summary>References (Click to expand)</summary><p>
				* [https://nuclei.projectdiscovery.io/nuclei/get-started/](https://nuclei.projectdiscovery.io/nuclei/get-started/)
			* Notes
				* The examples describe disabling the use of an interactsh server. However, you can stand one up on your own workstation to test DNS.
			* Examples
				* Example 1: Generally Safe Internal Network Nuclei Test (needs testing to confirm safety)

						nuclei -rl 500 -t cves/ -tags <TAGS> -stats -duc -ni -sr
					* `-duc` - Disable version update check  
					* `-ni` - Disable the public interactsh server
					* `-sr` - Use system resolver to resolve your internal hosts
					* Optional: `-r` flag to provider internal dns server to resolve internal hosts.
					* Recommended Tags (separated in command line by ?)
						* cve
						* panel
						* exposure
						* rce
						* tech
				* Example 2: Exclude By Multiple Tags, Exclude By Multiple Templates

						nuclei -l urls.txt -t cves/ -etags sqli,rce -exclude-templates exposed-panels/ -exclude-templates technologies/

### Discovered Application Follow-up Quick Reference
* Note that dedicated guides for applications are maintained in the applications directory of Redvelations (`Testaments_and_Books/Redvelations/Applications/`).

* Java
	* Java RMI
		* Ports
			* 1090, 1098, 1099, 4444, 11099, 47001, 47002, 10999
		* <details><summary>References (Click to expand)</summary><p>
			* [https://www.rapid7.com/db/modules/exploit/multi/misc/java_rmi_server](https://www.rapid7.com/db/modules/exploit/multi/misc/java_rmi_server)
			* [https://medium.com/@afinepl/java-rmi-for-pentesters-structure-recon-and-communication-non-jmx-registries-a10d5c996a79](https://medium.com/@afinepl/java-rmi-for-pentesters-structure-recon-and-communication-non-jmx-registries-a10d5c996a79)
			* [https://medium.com/@afinepl/java-rmi-for-pentesters-part-two-reconnaissance-attack-against-non-jmx-registries-187a6561314d](https://medium.com/@afinepl/java-rmi-for-pentesters-part-two-reconnaissance-attack-against-non-jmx-registries-187a6561314d)
		* Tools
	* WebLogic
		* Ports
			* 7000-7004, 8000-8003, 9000-9003, 9503, 7070, 7071
		* <details><summary>References (Click to expand)</summary><p>
			* [https://www.exploit-db.com/search?q=weblogic](https://www.exploit-db.com/search?q=weblogic)
	* JDWP
		* Ports
			* 45000, 45001
		* <details><summary>References (Click to expand)</summary><p>
			* [https://www.rapid7.com/db/modules/exploit/multi/misc/java_jdwp_debugger](https://www.rapid7.com/db/modules/exploit/multi/misc/java_jdwp_debugger)
			* [https://github.com/IOActive/jdwp-shellifier](https://github.com/IOActive/jdwp-shellifier)
	* JMX
		* Ports
			* 8686, 9012, 50500
		* <details><summary>References (Click to expand)</summary><p>
			* [https://www.rapid7.com/db/modules/exploit/multi/misc/java_jmx_server](https://www.rapid7.com/db/modules/exploit/multi/misc/java_jmx_server)
	* GlassFish
		* Ports
			* 4848
			* [https://www.rapid7.com/db/modules/auxiliary/scanner/http/glassfish_traversal](https://www.rapid7.com/db/modules/auxiliary/scanner/http/glassfish_traversal)
	* JBoss
		* Ports
			* 11111, 4444, 4445
		* <details><summary>References (Click to expand)</summary><p>
			[https://www.rapid7.com/db/modules/auxiliary/scanner/http/jboss_vulnscan](https://www.rapid7.com/db/modules/auxiliary/scanner/http/jboss_vulnscan)
			[https://github.com/joaomatosf/jexboss](https://github.com/joaomatosf/jexboss)
	* Cisco Smart Install
		* Ports
			* 4786
		* <details><summary>References (Click to expand)</summary><p>
			* [https://www.rapid7.com/db/modules/auxiliary/scanner/misc/cisco_smart_install](https://www.rapid7.com/db/modules/auxiliary/scanner/misc/cisco_smart_install)
			* [https://github.com/Sab0tag3d/SIET](https://github.com/Sab0tag3d/SIET)

	* HP Data Protector
		* Ports
			* 5555, 5556
		* <details><summary>References (Click to expand)</summary><p>
			* [https://www.rapid7.com/db/modules/exploit/multi/misc/hp_data_protector_exec_integutil](https://www.rapid7.com/db/modules/exploit/multi/misc/hp_data_protector_exec_integutil)
			* [https://www.rapid7.com/db/modules/exploit/windows/misc/hp_dataprotector_cmd_exec](https://www.rapid7.com/db/modules/exploit/windows/misc/hp_dataprotector_cmd_exec)
	* SAP
		* Ports
			* 3300
		* <details><summary>References (Click to expand)</summary><p>
			* [https://github.com/chipik/SAP_GW_RCE_exploit](https://github.com/chipik/SAP_GW_RCE_exploit)
	* Dameware
		* Ports
			* 6129
		* <details><summary>References (Click to expand)</summary><p>
			* [https://www.tenable.com/security/research/tra-2019-43](https://www.tenable.com/security/research/tra-2019-43)
			* [https://github.com/tenable/poc/blob/master/Solarwinds/Dameware/dwrcs_dwDrvInst_rce.py](https://github.com/tenable/poc/blob/master/Solarwinds/Dameware/dwrcs_dwDrvInst_rce.py)
	* Redis
		* Ports
			* 6379
		* <details><summary>References (Click to expand)</summary><p>
			* [https://www.rapid7.com/db/modules/exploit/linux/redis/redis_replication_cmd_exec](https://www.rapid7.com/db/modules/exploit/linux/redis/redis_replication_cmd_exec)
	* Cisco Unified Communications Manager
		* Ports
			* 6970
		* <details><summary>References (Click to expand)</summary><p>
			* [http://[CUCM IP Address]:6970/ConfigFileCacheList.txt](http://[CUCM IP Address]:6970/ConfigFileCacheList.txt)
	* Adobe CodFusion BlazeDS
		* Ports
			* 8080
		* <details><summary>References (Click to expand)</summary><p>
			* [https://www.tenable.com/plugins/nessus/99731](https://www.tenable.com/plugins/nessus/99731)