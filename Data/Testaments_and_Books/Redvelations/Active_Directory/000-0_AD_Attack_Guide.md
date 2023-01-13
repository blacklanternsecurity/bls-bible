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
# Active Directory Attack Guide
## Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@attack #@checklist #@mindmap #@mind #@map

Tools

		#@impacket #@pcaptools #@pcap #@nmap #@zmap #@ldapsearch #@ldapsearch-ad #@rpcclient #@smbmap #@crackmapexec #@manspider #@adidnsdump #@dnsrecon #@enum4linux #@nopac

</p></details>

## References

<details><summary>References</summary><p>

* Microsoft Won't Fix List
	* [https://github.com/cfalta/MicrosoftWontFixList](https://github.com/cfalta/MicrosoftWontFixList)
* [https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Active%20Directory%20Attack.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Active%20Directory%20Attack.md)
* "AD Pentest mindmap upgrade" -<br />[https://twitter.com/M4yFly/status/1440060656871374853](https://twitter.com/M4yFly/status/1440060656871374853)
	* [https://twitter.com/M4yFly/status/1440060656871374853/photo/1](https://twitter.com/M4yFly/status/1440060656871374853/photo/1)
	* [https://owasp.org/www-pdf-archive/OWASP_FFM_41_OffensiveActiveDirectory_101_MichaelRitter.pdf](https://owasp.org/www-pdf-archive/OWASP_FFM_41_OffensiveActiveDirectory_101_MichaelRitter.pdf)
* swisskyrepo's [Network Pivoting Techniques](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Network%20Pivoting%20Techniques.md)

</details>

## Tools
* <details><summary>Linux (Click to expand)</summary><p>
	* General
		* crackmapexec -<br />[https://github.com/Porchetta-Industries/CrackMapExec](https://github.com/Porchetta-Industries/CrackMapExec)
		* Impacket
	* Broad Enumeration
		* bloodhound.py -<br />[https://github.com/fox-it/BloodHound.py](https://github.com/fox-it/BloodHound.py)
		* adidnsdump -<br />[https://github.com/dirkjanm/adidnsdump](https://github.com/dirkjanm/adidnsdump)
	* Relay, Forced Authentication, AITM
		* coercer.py -<br />[https://github.com/p0dalirius/Coercer](https://github.com/p0dalirius/Coercer)
		* mitm6 -<br />[https://github.com/dirkjanm/mitm6](https://github.com/dirkjanm/mitm6)
		* Responder (by lgandx) -<br />[https://github.com/lgandx/Responder](https://github.com/lgandx/Responder)
		* krbrelayx -<br />[https://github.com/dirkjanm/krbrelayx](https://github.com/dirkjanm/krbrelayx)
	* ADCS
		* certipy -<br />[https://github.com/ly4k/certipy](https://github.com/ly4k/certipy)
	* File Shares
		* manspider -<br />[https://github.com/blacklanternsecurity/MANSPIDER](https://github.com/blacklanternsecurity/MANSPIDER)
	* AD CVE Exploit Tools
		* pachine -<br />[https://github.com/ly4k/Pachine](https://github.com/ly4k/Pachine)
	* Windows and AD Credential Dumping Tools
		* lsassy -<br />[https://github.com/hackndo/lsassy](https://github.com/hackndo/lsassy)
		* Donpapi -<br />[https://github.com/login-securite/DonPAPI/](https://github.com/login-securite/DonPAPI/)
* Analysis Tools
	* bloodhound (GUI)

* Other broad tool packs that may provide value
	<details><summary>Needs Research</summary><p>
		* [https://github.com/S3cur3Th1sSh1t/PowerSharpPack](https://github.com/S3cur3Th1sSh1t/PowerSharpPack)

### Quick Install Recommended Tools (Linux)
<details><summary>Linux Tool Installation</summary><p>

1. Use pipx to installs tools into virtual environments with self-contained dependencies
	1. Install pre-requisites. **python3.9** is included, as some tools rely on python newer than the current debian distributions produce.
		1. apt package installation

				sudo apt install python3 python3-venv python3-pip python3.9 python3.9-venv -y
		1. pipx installation

				sudo python3.9 -m pip install --user pipx
				python3.9 -m pipx ensurepath
	1. Close the terminal and open a new one so that the path variables are updated
	1. Create a file with desired tools compatible with the command `pip install .`, which relies on either `setup.py`  or `pyproject.toml` to be present in the Git repository.

			https://github.com/Porchetta-Industries/CrackMapExec
			https://github.com/SecureAuthCorp/impacket
			https://github.com/fox-it/BloodHound.py
			https://github.com/ly4k/certipy
			https://github.com/hackndo/lsassy
			https://github.com/blacklanternsecurity/MANSPIDER
			https://github.com/dirkjanm/adidnsdump
	1. Install desired tools compatible with pipx. This format uses python3.9 for installation, but you may separate tools between python versions if you have alternative python needs.

			while read -r line; do pipx install --python python3.9 git+$line; done < pipx.txt
	1. Test that the tools work with tab-complete, and that the tool successfully produces a help dialogue.

			secretsdump.py
1. Download remaining tools not compatible with pip
	1. Install pre-requisites.
		1. apt package installation

				sudo apt install git
		1. pip installation 

				python3 -m pip install pipenv
	1. Create a file with desired tools compatible with `git clone`.

			https://github.com/lgandx/Responder
			https://github.com/p0dalirius/Coercer
			https://github.com/dirkjanm/mitm6
			https://github.com/dirkjanm/krbrelayx
			https://github.com/login-securite/DonPAPI
			https://github.com/ly4k/Pachine
	1. Install desired tools compatible with pipx. This format uses python3.9 for installation, but you may separate tools between python versions if you have alternative python needs.

			while read -r line; do git clone $line; done < git.txt
	1. Update path for pipx

			pipx ensurepath
1. Install golang
	1. Retrieve golang (set for v1.19, although if there's a way to target "latest," please let me know)-<br />[https://go.dev/doc/install](https://go.dev/doc/install)

			wget https://go.dev/dl/go1.19.linux-amd64.tar.gz
	1. Remove any existing golang and extract the downloaded files

			rm -rf /usr/local/go && tar -C /usr/local -xzf go1.19.linux-amd64.tar.gz
	1. Set your path variable so that the installed go binary and retrieved tools can easily be referenced. The format of the two commands are designed to support an installation of go tools as the root user.

			echo 'export PATH=$PATH:/usr/local/go/bin' >> /etc/profile
			echo 'export PATH=$PATH:/root/go/bin/' >> /etc/profile
1. Install helpful go tools
	* subnet mapping
		* mapcidr

				go install -v github.com/projectdiscovery/mapcidr/cmd/mapcidr@latest
	* LDAP Enumeration
		* adalanche

				go install -v github.com/lkarlslund/adalanche  /cmd/mapcidr@latest 

</p></details>

## MindMaps, Images

Orange Cyberdefense's GitHub - Arsenal - Mindmap -<br />[https://github.com/orangecyberdefense/arsenal](https://github.com/orangecyberdefense/arsenal)


<img src="https://raw.githubusercontent.com/Orange-Cyberdefense/arsenal/master/mindmap/pentest_ad_dark.png" style="float": left; width="1200" />


## Example Attacks
* PetitPotam, Responder, Silver Ticket
	* References
		* [https://blog.zsec.uk/chasing-the-silver-petit-potam/](https://blog.zsec.uk/chasing-the-silver-petit-potam/)

## Checklist

### Step 1: Enumerate (**Recommended** for achieving situational awareness before attempting attacks)
* [ ] - Follow the [AD Enumeration Guide's](Testaments_and_Books/Redvelations/Active_Directory/001-0_AD_Discovery_and_Enumeration.md) checklist.
* [ ] - Follow the [Network Enumeration Guide's](Testaments_and_Books/Redvelations/Network/001-0_Network_Enumeration.md) checklist.

### Attacks without credentials (No User Context)
* Account Takeover
	* [ ] - Spray for accounts with weak/guessable passwords
		* Requirements (`*`), Recommendations
			* Knowledge of password policy requirements
	* [ ] - Pre-created computer account compromise
		* Requirements (`*`), Recommendations
			* (`*`) Identified computer accounts that have never logged on and do not require a password
		* Abuse:
			1. Attempt to logon with the accounts using the username as the password (lowercase, not `$`)
			1. Change the password of the account so it can be used.
* Abuse: [Active Directory Password Spraying Guide](Testaments_and_Books/Redvelations/Active_Directory/002-6_AD_Password_Spraying.md)
* Relay or Capture Attacks
	* Requirements (`*`), recommendations
		* (`*`)Inbound authentication (coerced or otherwise)
		* (`*`)The potential for directing the authentication into abuse.
	* [ ] - Abuse the network according to information revealed by broadcasts
		* Requirements (`*`), Recommendations
			* Usually need to be on the same subnet at targets 
		* Network Poisoning Options
			* [ ] - ADIDNS Poisoning
			* [ ] - WPAD Spoofing
			* [ ] - LLMNR Poisoning
			* [ ] - NBT-NS Poisoning
			* [ ] - mDNS Poisoning
			* [ ] - IPv6/DHCPv6 Abuse
		* Abuse: [Forced Authentication Guide](Testaments_and_Books/Redvelations/Active_Directory/003-3_AD_Forced_Authentication.md)
	* Capture Attacks
		* Requirements (`*`), Recommendations
			* (`*`)Capturable authentication use in environment (e.g., NTLM)
			* (`*`)Machine account hashes must be downgraded to be crackable
			* (`*`)A functional forced authentication technique
			* Hashes can be trivially cracked if authentication can be downgraded to NTLMv1
		* Capture Authentication
			* [ ] - Capture Authentication
			* [ ] - Crack authentication
			* Abuse: [AD NTLM Capture and Relay Attacks Guide](Testaments_and_Books/Redvelations/Active_Directory/003-1_AD_NTLM_Capture_and_Relay_Attacks.md)
		* Note: Pass-the-Hash will not work for these captured hashes. The hash must instead be cracked.
			* Abuse: [Cracking Guide](Testaments_and_Books/Redvelations/Accounts/003_Cracking.md)
	* Relay Attacks
		* [ ] - Perform an SMB Relay Attack
			* Requirements (`*`), Recommendations
				* (`*`)SMB Signing must be disabled between multiple targets, or use HTTP
				* (`*`)A functional forced authentication technique
				* Extended Protection for Authentication (EPA) not enforced
			* Abuse: [AD NTLM Capture and Relay Attacks Guide](Testaments_and_Books/Redvelations/Active_Directory/003-1_AD_NTLM_Capture_and_Relay_Attacks.md)
				* [ ] - Dump credentials on a target
				  * Relayed authentication must have local administrator privileges on the target
				* [ ] - Execute commands or a file on a target
				* [ ] - Perform the Zerologon exploit without changing passwords
				  * DC must be vulnerable to Zerologon
				* [ ] - Enumerate local administrator accounts
		* [ ] - Perform an LDAP relay attack
			* Requirements (`*`), Recommendations
				* (`*`) LDAP Signing/Channel Binding must be disabled, or use HTTP
				* (`*`)A functional forced authentication technique
				* Extended Protection for Authentication (EPA) not enforced
			* Abuse: [AD NTLM Capture and Relay Attacks Guide](Testaments_and_Books/Redvelations/Active_Directory/003-1_AD_NTLM_Capture_and_Relay_Attacks.md)
				* Requirements (`*`), Recommendations
					* (`*`) LDAP signing must not be enabled
						* Special CVE vulnerabilities can remove signing
				* [ ] - Dump broad LDAP information
				* [ ] - Escalate existing user privileges
				  * (`*`)Relayed authentication must have sufficient domain permissions to elevate privileges of another user 
				* [ ] - Abuse RBCD to obtain local administrator privileges on a coerced system
					* (`*`)If a machine account is not already compromised, attack requires a machine account quota greater than 0.
		* [ ] - Abuse WebDav/HTTP to circumvent SMB/LDAP protections
			* Requirements (`*`), Recommendations
				* (`*`) WebDav must be present on targets
					* Enable WebDav on target systems to enable HTTP relays
						* [SMB Guide, WebDav Section](Testaments_and_Books/Redvelations/Active_Directory/005-3_SMB.md)
						* [Forced Authentication Guide](Testaments_and_Books/Redvelations/Active_Directory/003-3_AD_Forced_Authentication.md); [AD NTLM Capture and Relay Attacks Guide](Testaments_and_Books/Redvelations/Active_Directory/003-1_AD_NTLM_Capture_and_Relay_Attacks.md); If HTTP is exposed in ADCS, [ADCS Attack Guide](Testaments_and_Books/Redvelations/Active_Directory/002-3_ADCS_Abuse.md)
			* Enumeration:
				* [AD NTLM Capture and Relay Attacks Guide](Testaments_and_Books/Redvelations/Active_Directory/003-1_AD_NTLM_Capture_and_Relay_Attacks.md)
				* [ADCS Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-5_ADCS_Enumeration.md)
			* Abuse:
				* [AD NTLM Capture and Relay Attacks Guide](Testaments_and_Books/Redvelations/Active_Directory/003-1_AD_NTLM_Capture_and_Relay_Attacks.md))
* Active Directory Vulnerabilities (Enumeration: [AD CVE Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-6_AD_CVE_Enumeration.md), Abuse: [AD CVEs Guide](Testaments_and_Books/Redvelations/Active_Directory/006-0_AD_CVEs.md))
	* [ ] - ZeroLogon
* File Share Abuse
	* [ ] - Do any shares accept null or guest authentication?
		* Enumeration: [File Share Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-7_File_Share_Enumeration.md)
		* Abuse: [File Share Attack Guide](Testaments_and_Books/Redvelations/Active_Directory/005-5_File_Share.md)
	* [ ] - Does the data of any file shares contain any credential information?
		* Enumeration: [File Share Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-7_File_Share_Enumeration.md)
		* Abuse:
			* [Forced Authentication Guide, Social Engineering](Testaments_and_Books/Redvelations/Active_Directory/003-3_AD_Forced_Authentication.md)
			* [File Share Attack Guide](Testaments_and_Books/Redvelations/Active_Directory/005-5_File_Share.md)
	* [ ] - Are any shares writeable?
		* Enumeration: [File Share Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-7_File_Share_Enumeration.md)
		* Abuse:
			* [Forced Authentication Guide, Social Engineering](Testaments_and_Books/Redvelations/Active_Directory/003-3_AD_Forced_Authentication.md)
			* [File Share Attack Guide](Testaments_and_Books/Redvelations/Active_Directory/005-5_File_Share.md)
	* [ ] - Are the decryptable Group Policy Preferences (GPP) Passwords present?
		* Enumeration: [File Share Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-7_File_Share_Enumeration.md)
		* Abuse: [File Share Attack Guide](Testaments_and_Books/Redvelations/Active_Directory/005-5_File_Share.md)
* Network Attacks
	* [ ] - Attempt attacks from the network attack guide
		* Enumeration: [Network Enumeration Guide](Testaments_and_Books/Redvelations/Network/001-0_Network_Enumeration.md)
		* Abuse: [Network Attack Guide](Testaments_and_Books/Redvelations/Network/000-0_Network_Attacks.md)
			* Application (e.g., Web) Attacks
			* CVE Exploitation

### Attacks without credentials (User Context)

* [ ] - Attempt to retrieve the domain user hash or credentials
	* Abuse: [Forced Authentication Guide (such as the LOLBAS section)](Testaments_and_Books/Redvelations/Active_Directory/003-3_AD_Forced_Authentication.md), [AD NTLM Capture and Relay Attacks Guide](Testaments_and_Books/Redvelations/Active_Directory/003-1_AD_NTLM_Capture_and_Relay_Attacks.md))
* [ ] - Attempt a local privilege escalation
	* Windows-Based
		* Enumeration: [Windows Enumeration Guide](Testaments_and_Books/Redvelations/Windows/001-0_Windows_Enumeration.md)
		* Abuse: [Windows Privilege Escalation Guide](Testaments_and_Books/Redvelations/Windows/006-0_Windows_Privilege_Escalation.md)

### Attacks with domain user credentials

* Accounts and Authentication Abuse
	* [ ] - Spray for weak passwords
		* Requirements (`*`), Recommendations
			* Preferred: Knowledge of the Password Policy (Password Requirements, Lockout Enforcement/Restrictions)
		* Abuse: [Active Directory Password Spraying Guide](Testaments_and_Books/Redvelations/Active_Directory/002-6_AD_Password_Spraying.md)
	* [ ] - Spray for accounts with passwords pre-dating the current password policy
		* Abuse: [Active Directory Password Spraying Guide](Testaments_and_Books/Redvelations/Active_Directory/002-6_AD_Password_Spraying.md)
	* Active Directory Vulnerabilities (CVEs) Requiring Credentials
		* [ ] - NTLM tampering vulnerabilities
			* Abuse: NTLM relay attacks ([AD Capture and Relay Attacks Guide](Testaments_and_Books/Redvelations/Active_Directory/003-1_AD_NTLM_Capture_and_Relay_Attacks.md))
	* Kerberos (Unless noted, Enumeration and Abuse: [Kerberos Abuse Guide](Testaments_and_Books/Redvelations/Active_Directory/002-2_Kerberos_Abuse.md))
		* [ ] - As-Rep-Roastable Accounts (Accounts do not require Kerberos Pre-Authentication)
		* [ ] - Kerberoastable accounts (user accounts with at least one `ServicePrincipalName`)
		* [ ] - Kerberos Unconstrained Delegation
		* [ ] - Kerberos Constrained Delegation
		* [ ] - Kerberos Resource Based Constrained Delegation
		* [ ] - Has `krbtgt`'s password been changed recently?
			* Abuse: Golden Ticket persistence attacks ([Domain Persistence Guide](Testaments_and_Books/Redvelations/Active_Directory/007-0_AD_Domain_Persistence.md))
				* Requires knowledge of the Domain SID
	* Forced Authentication Abuses (Initiates Impact to Relay Attack Abuses)
		* [ ] - RPC Forced Authentication misconfigurations
			* [ ] - Print spooler
			* [ ] - Petitpotam
			* [ ] - ShadowCoerce
			* [ ] - MS-FSVRP
			* [ ] - Social Engineering
* Active Directory Vulnerabilities (Enumeration: [AD CVE Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-6_AD_CVE_Enumeration.md), Abuse: [AD CVEs Guide](Testaments_and_Books/Redvelations/Active_Directory/006-0_AD_CVEs.md))
	* [ ] - Exploit No-Pac
		* Requires a Machine Account Quota greater than 0 for the domain user (Enumeration: [LDAP Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-2_LDAP_Enumeration.md))
	* [ ] - Exploit Kerberos sAMAccountName spoofing
		* Requires a Machine Account Quota greater than 0 for the domain user (Enumeration: [LDAP Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-2_LDAP_Enumeration.md))
* Active Directory Services
	* ADCS ([ADCS Abuse Guide](Testaments_and_Books/Redvelations/Active_Directory/002-3_ADCS_Abuse.md))
		* [ ] - Certificate Authority Misconfigurations (e.g., `EDITF_ATTRIBUTESUBJECTALTNAME2` flag)
		* [ ] - Poorly configured certificate templates
		* [ ] - Vulnerable Certificate Authority Web Endpoints exposed
			* Relay attacks ([AD Capture and Relay Attacks Guide](Testaments_and_Books/Redvelations/Active_Directory/003-1_AD_NTLM_Capture_and_Relay_Attacks.md))
		* Abuse: [ADCS Attack Guide](Testaments_and_Books/Redvelations/Active_Directory/002-3_ADCS_Abuse.md)
	* File Sharing ([File Share Attacks Guide](Testaments_and_Books/Redvelations/Active_Directory/005-5_File_Share.md))
		* [ ] - SYSVOL storage of sensitive information, often from administrators attempting to make workstation deployment easier
		* [ ] - No saved credentials (e.g., passwords or certificates) on shares
	* Exchange ([Exchange Guide](Testaments_and_Books/Redvelations/Active_Directory/005-6_Exchange.md))
		* [ ] - PrivExchange
			* Forced authentication (PushSubscription API)
			* ACE abuse attacks relying on the `EXCHANGE WINDOWS PERMISSION` group having `WriteDacl` permissions against the domain object
				* DCSync ([Domain Persistence Guide](Testaments_and_Books/Redvelations/Active_Directory/007-0_AD_Domain_Persistence.md))

### Attacks with Local Administrator credentials

* [ ] - Dump Windows credentials stored in memory
	* Requirements (`*`), Recommendations
		* (`*`) LSA protections not enabled
	* [Windows Credential Dumping Guide](Testaments_and_Books/Redvelations/Windows/007-0_Windows_Credential_Dumping.md)
		* LSASS dumping
* [ ] - Authenticate to other systems with the same local adminsitrator account ([Active Directory Password Spraying Guide](Testaments_and_Books/Redvelations/Active_Directory/002-6_AD_Password_Spraying.md))
	* Enumeration: Password Spraying (to see where your credentials are valid)
	* Abuse: Credential stuffing, [Active Directory Password Spraying Guide](Testaments_and_Books/Redvelations/Active_Directory/002-6_AD_Password_Spraying.md)
* [ ] - Privileged User Sessions on Compromised Systems
* [ ] - Abuse computer accounts with local admin privileges over others

### Attacks with Privileged Domain User credentials
* [ ] - Abuse special group privileges (e.g., built-in groups)
	* Enumerate: [LDAP Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-2_LDAP_Enumeration.md)
	* Abuse: [Built-In Groups Attack Guide](Testaments_and_Books/Redvelations/Active_Directory/004-1_AD_Built-In_Groups.md)
* [ ] - Dump Credentials from domain password stores
	* [AD Credential Dumping Guide](Testaments_and_Books/Redvelations/Active_Directory/007-1_AD_Credential_Dumping.md)
* [ ] - Establish domain persistence
	* Abuse: [Domain Persistence Guide](Testaments_and_Books/Redvelations/Active_Directory/007-0_AD_Domain_Persistence.md)

### Compromised "Non-Password" Authentication Material

* "Convert" your authentication material to a password by cracking it ([Cracking Guide](Testaments_and_Books/Redvelations/Accounts/003_Cracking.md))
	* Weak Encryption (\~All possibilities can be guessed/predicted trivially)
		* LM Hashes: The entire keyspace for the 8 character limitation can be guessed rapidly
		* NetNTLMv1 Hashes: When the challenge used is `112233445566778899`, the hash can be cracked into an NTLM hash.
	* Stronger encryption requiring effective password guessed
		* Kerberoasted Hashes
		* Asreproasted Hashes
		* NetNTLMv2 Hashes
* [ ] - Attempt to use the alternate authentication material directly (Abuse: [AD Authenticaiton and Movement Guide](Testaments_and_Books/Redvelations/Active_Directory/002-0_AD_Authentication_and_Movement.md))
	* NTLM: Pass-The-Hash
	* LM: Pass-The-Hash
	* Kerberos Ticket: Pass-The-Ticket
	* Certificate: Pass-The-Certificate
* [ ] - Convert the collected authentication material to something more accepted (Abuse: [AD Authenticaiton and Movement Guide](Testaments_and_Books/Redvelations/Active_Directory/002-0_AD_Authentication_and_Movement.md))
	* NTLM to Kerberos
	* NTLM to Certificates
	* Kerberos to NTLM
		* Requires the RC4 `etype` enabled
	* Kerberos to Certificates
	* Certificates to NTLM
	* Certificates to Kerberos

### Other Abuses
* Network
	* [ ] - Inadequate Network Segmentation
		* Missing sufficient firewall rules for reaching other systems
* Impact
	* [ ] - Does any of the collected data reveal potential impact to the organization?
		* [Impact Guide](Testaments_and_Books/Purplippians/Impact/Impact.md)

## Supplemental Guide Recommendations
* Network Attacking
	* [Network Attack Guide](Testaments_and_Books/Redvelations/Network/000-0_Network_Attacks.md)
* OS Attack Guides
	* [Windows Attacks Guide](Testaments_and_Books/Redvelations/Windows/000-0_Windows_Attacks.md)
	* [Linux Attacks Guide](Testaments_and_Books/Redvelations/Linux/000-0_Linux_Attack_Guide.md)
	* [Mac Attacks Guide](Testaments_and_Books/Redvelations/MacOS/Mac_Situational_Awareness.md)
* Application Attacks
	* [Web App Attack Guide](Testaments_and_Books/Redvelations/Web/000_Web_App_Attack_Guide.md)


## CLICK-TO-COPY CHECKLIST

```
## Checklist

### Step 1: Enumerate (**Recommended** for achieving situational awareness before attempting attacks)
* [ ] - Follow the AD Enumeration Guide's checklist.
* [ ] - Follow the Network Enumeration Guide's checklist.

### Attacks without credentials (No User Context)
* Account Takeover
	* [ ] - Spray for accounts with weak/guessable passwords
		* Requirements (`*`), Recommendations
			* Knowledge of password policy requirements
	* [ ] - Pre-created computer account compromise
		* Requirements (`*`), Recommendations
			* (`*`) Identified computer accounts that have never logged on and do not require a password
		* Abuse:
			1. Attempt to logon with the accounts using the username as the password (lowercase, not `$`)
			1. Change the password of the account so it can be used.
* Relay or Capture Attacks
	* Requirements (`*`), recommendations
		* (`*`)Inbound authentication (coerced or otherwise)
		* (`*`)The potential for directing the authentication into abuse.
	* [ ] - Abuse the network according to information revealed by broadcasts
		* Requirements (`*`), Recommendations
			* Usually need to be on the same subnet at targets 
		* Network Poisoning Options
			* [ ] - ADIDNS Poisoning
			* [ ] - WPAD Spoofing
			* [ ] - LLMNR Poisoning
			* [ ] - NBT-NS Poisoning
			* [ ] - mDNS Poisoning
			* [ ] - IPv6/DHCPv6 Abuse
			* Capture Attacks
		* Requirements (`*`), Recommendations
			* (`*`)Capturable authentication use in environment (e.g., NTLM)
			* (`*`)Machine account hashes must be downgraded to be crackable
			* (`*`)A functional forced authentication technique
			* Hashes can be trivially cracked if authentication can be downgraded to NTLMv1
		* Capture Authentication
			* [ ] - Capture Authentication
			* [ ] - Crack authentication
					* Note: Pass-the-Hash will not work for these captured hashes. The hash must instead be cracked.
				* Relay Attacks
		* [ ] - Perform an SMB Relay Attack
			* Requirements
				* (`*`)SMB Signing must be disabled between multiple targets, or use HTTP
				* (`*`)A functional forced authentication technique
				* Extended Protection for Authentication (EPA) not enforced
							* [ ] - Dump credentials on a target
				  * Relayed authentication must have local administrator privileges on the target
				* [ ] - Execute commands or a file on a target
				* [ ] - Perform the Zerologon exploit without changing passwords
				  * DC must be vulnerable to Zerologon
				* [ ] - Enumerate local administrator accounts
		* [ ] - Perform an LDAP relay attack
			* Requirements
				* (`*`) LDAP Signing/Channel Binding must be disabled, or use HTTP
				* (`*`)A functional forced authentication technique
				* Extended Protection for Authentication (EPA) not enforced
							* Requirements
					* (`*`) LDAP signing must not be enabled
						* Special CVE vulnerabilities can remove signing
				* [ ] - Dump broad LDAP information
				* [ ] - Escalate existing user privileges
				  * (`*`)Relayed authentication must have sufficient domain permissions to elevate privileges of another user 
				* [ ] - Abuse RBCD to obtain local administrator privileges on a coerced system
					* (`*`)If a machine account is not already compromised, attack requires a machine account quota greater than 0.
		* [ ] - Abuse WebDav/HTTP to circumvent SMB/LDAP protections
			* Requirements
				* (`*`) WebDav must be present on targets
					* Enable WebDav on target systems to enable HTTP relays
															* Enumeration:
											* Abuse:
				* Active Directory Vulnerabilities
	* [ ] - ZeroLogon
* File Share Abuse
	* [ ] - Do any shares accept null or guest authentication?
	* [ ] - Does the data of any file shares contain any credential information?
	* [ ] - Are any shares writeable?
	* [ ] - Are the decryptable Group Policy Preferences (GPP) Passwords present?
* Network Attacks
	* [ ] - Are any of the attacks in the network attack guide applicable and possible?
* Application (e.g., Web) Attacks
* CVE Exploitation


### Attacks without credentials (User Context)

* [ ] - Can you retrieve the domain user credentials (hash)?
	* [ ] - Can your privileges be escalated to local administrator status?
		
### Attacks with domain user credentials

* [ ] - Does the domain user have local administrator privileges anywhere?
	* Abuse: Move to section below for local administrator rights (instead of domain user rights).
* Accounts and Authentication Abuse
	* Password Policy
		* [ ] - Is the user password policy inadequate? (Minimum password requirements allow weak accounts, account lockout restrictions too lax)
					* [ ] - Are there accounts with passwords that have not been set since the existing password policy has been put in place, or at least for an extended period of time?
				* Active Directory Vulnerabilities (CVEs) Requiring Credentials
		* [ ] - NTLM tampering vulnerabilities
	* Kerberos
		* [ ] - Are there As-Rep-Roastable Accounts (Accounts do not require Kerberos Pre-Authentication)?
		* [ ] - Are there kerberoastable accounts (user accounts with at least one `ServicePrincipalName`)
		* [ ] - Do any accounts have Kerberos Unconstrained Delegation?
		* [ ] - Do any accounts have Kerberos Constrained Delegation?
		* [ ] - Do any accounts have Kerberos Resource Based Constrained Delegation?
		* [ ] - Has `krbtgt`'s password been changed recently?
			* Golden Ticket persistence attacks
				* Requires knowledge of the Domain SID
	* Forced Authentication Abuses (Initiates Impact to Relay Attack Abuses)
		* [ ] - RPC Forced Authentication misconfigurations
			* [ ] - Print spooler
			* [ ] - Petitpotam
			* [ ] - ShadowCoerce
			* [ ] - MS-FSVRP
			* [ ] - Social Engineering
* Active Directory Vulnerabilities
	* [ ] - Is the domain controller vulnerable to No-Pac?
		* Requires a Machine Account Quota greater than 0 for the domain user
	* [ ] - Kerberos sAMAccountName spoofing
		* Requires a Machine Account Quota greater than 0 for the domain user
* Active Directory Services
	* ADCS
		* [ ] - Certificate Authority Misconfigurations (e.g., `EDITF_ATTRIBUTESUBJECTALTNAME2` flag)
		* [ ] - Poorly configured certificate templates
		* [ ] - Vulnerable Certificate Authority Web Endpoints exposed
			* Relay attacks
			* File Sharing
		* [ ] - SYSVOL storage of sensitive information, often from administrators attempting to make workstation deployment easier
		* [ ] - No saved credentials (e.g., passwords or certificates) on shares
	* Exchange
		* [ ] - PrivExchange
			* Forced authentication (PushSubscription API)
			* ACE abuse attacks relying on the `EXCHANGE WINDOWS PERMISSION` group having `WriteDacl` permissions against the domain object
				* DCSync
	* [ ] - Machine Account Quota Restrictions
		* Many Attacks

### Attacks with Local Administrator credentials

* [ ] - Dump Windows credentials stored in memory
	* Are there active sessions of other domain users that are worth retrieving?
	* Credential dumping
		* [ ] - Are LSA protections not enabled?
		* LSASS dumping
* [ ] - Is the local administrator password re-used between systems?
* [ ] - Privileged User Sessions on Compromised Systems
* [ ] - Computer accounts with local admin privileges over others

### Attacks with Privileged Domain User credentials
* [ ] - Is the user account part of any special AD groups (e.g., built-in groups)?
	* [ ] - Can you achieve domain persistence?
	* Enumeration:
	
### Compromised "Non-Password" Authentication Material

* Can your authentication be trivially cracked because of the hashing algorithm?
	* LM Hashes: The entire keyspace for the 8 character limitation can be guessed rapidly
			* NetNTLMv1 Hashes: When the challenge used is `112233445566778899`, the hash can be cracked into an NTLM hash.
		* [ ] - Is your authentication material a suitable replacement to password-based authentication?
	* NTLM: Pass-The-Hash
	* LM: Pass-The-Hash
	* Kerberos Ticket: Pass-The-Ticket
	* Certificate: Pass-The-Certificate
* [ ] - If the domain does not accept the collected authentication, can it be converted?
	* NTLM to Kerberos: 
		* [ ] - Is the RC4 `etype` is enabled?
			* Overpass-the-hash
			* NTLMv1 capture attacks
			* Silver Ticket attacks
	* NTLM to Certificates: 
	* Kerberos to NTLM: 
	* Kerberos to Certificates: 
	* Certificates to NTLM: 
	* Certificates to Kerberos: 
* [ ] - If your collected hash doesn't apply to the above, is the password guessable?
	* Examples of Affected Authentication
		* Kerberoasted Hashes
		* Asreproasted Hashes
		* NetNTLMv2 Hashes
	
### Other Abuses
* Network
	* [ ] - Inadequate Network Segmentation
		* Missing sufficient firewall rules for reaching other systems
* Impact
	* [ ] - Does any of the collected data reveal potential impact to the organization?
		
## Supplemental Guide Recommendations
* Network Attacking
	* OS Attack Guides
			* Application Attacks
```