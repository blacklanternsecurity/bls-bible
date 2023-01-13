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
# Remote Administration Enumeration
## Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@enum #@enumerate #@enumeration #@remote #@remoteadministration #@administration #@wmi #@windows #@management #@instrumentation #@rdp #@remote #@desktop #@protocol #@winrm

Tools

		#@crackmapexec #@impacket #@rdp #@check #@rdpcheck

</p></details>

## Overview

Several TTPs are referenced in this guide, including cases of multiple TTPs for the same tool

* Remote Service Abuse ([`Remote Services` TTP](TTP/T1021_Remote_Services/T1021.md))
* External Remote Services ([`External Remote Services` TTP](TTP/T1133_External_Remote_Services/T1133.md)))

## Enumeration
### From a Linux Machine


#### RDP

* RDP
	* <details><summary>impacket's rdp_check.py  ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md)) (Click to expand)</summary><p>
		* Examples
			* Example 1: Password-Based

					rdp_check.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$TARGET
				* Example Output

						root@jack-Virtual-Machine:~# rdp_check.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$TARGET
						Impacket v0.10.1.dev1+20220720.103933.3c6713e - Copyright 2022 SecureAuth Corporation

						[*] Access Granted
	* <details><summary>crackmapexec (Click to expand)</summary><p>
		* Examples
			* Example 1: Password-Based, Capture Screenshots

					crackmapexec rdp -u $DOMAIN_USER -p $PASSWORD -d $DOMAIN --screenshot $TARGET
				* Targets can be a subnet or a single system
				* Example Output

						root@jack-Virtual-Machine:~# cme rdp -u $DOMAIN_USER -p $PASSWORD -d $DOMAIN --screenshot 10.0.0.0/24
						RDP         10.0.0.101      3389   WIN11            [*] Windows 10 or Windows Server 2016 Build 22000 (name:WIN11) (domain:microsoftdelivery.com) (nla:True)
						RDP         10.0.0.50       3389   APP              [*] Windows 10 or Windows Server 2016 Build 17763 (name:APP) (domain:microsoftdelivery.com) (nla:True)
						RDP         10.0.0.1        3389   DC01             [*] Windows 10 or Windows Server 2016 Build 17763 (name:DC01) (domain:microsoftdelivery.com) (nla:True)
						RDP         10.0.0.3        3389   CA               [*] Windows 10 or Windows Server 2016 Build 17763 (name:CA) (domain:microsoftdelivery.com) (nla:True)
						RDP         10.0.0.2        3389   DC02             [*] Windows 10 or Windows Server 2016 Build 17763 (name:DC02) (domain:microsoftdelivery.com) (nla:True)
						RDP         10.0.0.101      3389   WIN11            [+] microsoftdelivery.com\domain_admin:P@ssw0rd (Pwn3d!)
						RDP         10.0.0.50       3389   APP              [+] microsoftdelivery.com\domain_admin:P@ssw0rd (Pwn3d!)
						RDP         10.0.0.1        3389   DC01             [+] microsoftdelivery.com\domain_admin:P@ssw0rd (Pwn3d!)
						RDP         10.0.0.3        3389   CA               [+] microsoftdelivery.com\domain_admin:P@ssw0rd (Pwn3d!)
						RDP         10.0.0.101      3389   WIN11            Screenshot saved /root/.cme/screenshots/WIN11_10.0.0.101_2022-08-18_171433.png
						RDP         10.0.0.2        3389   DC02             [+] microsoftdelivery.com\domain_admin:P@ssw0rd (Pwn3d!)
						RDP         10.0.0.50       3389   APP              Screenshot saved /root/.cme/screenshots/APP_10.0.0.50_2022-08-18_171437.png
						RDP         10.0.0.3        3389   CA               Screenshot saved /root/.cme/screenshots/CA_10.0.0.3_2022-08-18_171443.png
						RDP         10.0.0.2        3389   DC02             Screenshot saved /root/.cme/screenshots/DC02_10.0.0.2_2022-08-18_171445.png


#### WinRM



#### WMI


