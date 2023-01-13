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
# ADCS Enumeration
## Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@enum #@enumerate #@enumeration #@dns #@dhcp #@ldap #@smb #@rpc

Tools

		#@impacket #@certipy #@pcaptools #@pcap #@nmap #@zmap #@ldapsearch #@curl #@crackmapexec #@certify

</p></details>

## References

* hideandsec: Active Directory Certificate Services -<br />[https://hideandsec.sh/books/cheatsheets-82c/page/active-directory-certificate-services](https://hideandsec.sh/books/cheatsheets-82c/page/active-directory-certificate-services)

## Overview
Note that ADCS is not present in every environment

## Enumeration
### From a Linux Machine

* Broad ADCS Enumeration (Templates, Servers, More) * Enumerate Vulnerable Certificates ([`Active Scanning - Vulnerability Scanning` TTP](TTP/T1595_Active_Scanning/002_Vulnerability_Scanning/T1595.002.md))
	* <details><summary>Recommended: certipy (Click to expand) </summary><p>
		* At the time of this writing (2022.08), a forked version of BloodHound must be used for certipy data.
		* Example

				certipy find -u $DOMAIN_USER@$DOMAIN -p $PASSWORD
			* Example Output

					Certipy v4.0.0 - by Oliver Lyak (ly4k)

					[*] Finding certificate templates
					[*] Found 37 certificate templates
					[*] Finding certificate authorities
					[*] Found 1 certificate authority
					[*] Found 15 enabled certificate templates
					[*] Trying to get CA configuration for 'microsoftdelivery-CA-CA' via CSRA
					[!] Got error while trying to get CA configuration for 'microsoftdelivery-CA-CA' via CSRA: CASessionError: code: 0x80070005 - E_ACCESSDENIED - General access denied error.
					[*] Trying to get CA configuration for 'microsoftdelivery-CA-CA' via RRP
					[!] Failed to connect to remote registry. Service should be starting now. Trying again...
					[*] Got CA configuration for 'microsoftdelivery-CA-CA'
					[*] Saved BloodHound data to '20220810094458_Certipy.zip'. Drag and drop the file into the BloodHound GUI from @ly4k
					[*] Saved text output to '20220810094458_Certipy.txt'
					[*] Saved JSON output to '20220810094458_Certipy.json'
* Identify Certificate Authorities
	* RPC
		* <details><summary>rpc tools (Click to expand)</summary><p>
			* Examples
				* Example 1: Identify "Cert Publishers"

						rpc net group members "Cert Publishers" -U $DOMAIN/$DOMAIN_USER%$PASSWORD -S "DomainController"
	* LDAP
		* <details><summary>ldapsearch (from ldap-utils package) (Click to expand)</summary><p>
			* Examples
				* Example 1 (Needs testing)

						ldapsearch -H ldap://dc_IP -x -LLL -D 'CN=<user>,OU=Users,DC=domain,DC=local' -w '<password>' -b "CN=Enrollment Services,CN=Public Key Services,CN=Services,CN=CONFIGURATION,DC=domain,DC=local" dNSHostName
		* <details><summary>crackmapexec (Click to expand)</summary><p>
			* Example

					crackmapexec ldap $DOMAIN_CONTROLLER -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -M adcs
				* Example Output

						root@jack-Virtual-Machine:~# crackmapexec ldap $DOMAIN_CONTROLLER -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -M adcs
						SMB         dc01.microsoftdelivery.com 445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
						LDAP        dc01.microsoftdelivery.com 389    DC01             [+] microsoftdelivery.com\domain_user:P@ssw0rd 
						ADCS    Found PKI Enrollment Server: CA.microsoftdelivery.com
						ADCS    Found CN: microsoftdelivery-CA-CA
						ADCS    Found PKI Enrollment WebService: https://ca.microsoftdelivery.com/microsoftdelivery-CA-CA_CES_Kerberos/service.svc/CES
	* HTTP
		* <details><summary>curl known endpoints (Click to expand)</summary><p>
			* Certificate Authorities have known endpoints exposed that can confirm if ADCS is in effect.

					curl http://<CA>/certsrv/
				* **401 unauthorized** - The target is the CA.

### From a Windows Machine

* <details><summary>Note (Click to expand)</summary><p>
	* Untested with `runas /netonly` but may still work 2021.09.30
* Enumerate Certificate Authority
	* Net commands
		* Example

			net group "Cert Publishers" /domain
	* <details><summary>Recommended: Certify.exe (Click to expand)</summary><p>
		* Commands
			* **Top Alternative:** Find information about all registered CAs:

					Certify.exe cas [/ca:SERVER\ca-name | /domain:domain.local | /path:CN=Configuration,DC=domain,DC=local] [/hideAdmins] [/showAllPermissions] [/skipWebServiceChecks] [/quiet]
	* <details><summary>LOLBIN: Certutil on a domain-joined Windows machine (Click to expand)</summary><p>
		1. Confirm Certificate Services is active and identify Certificate Authority.

				Certutil.exe -CA
* Enumerate all vulnerable certificates
		* <details><summary>certify (Click to expand)</summary><p>

				Certify.exe find /vulnerable [/ca:SERVER\ca-name | /domain:domain.local | /path:CN=Configuration,DC=domain,DC=local] [/quiet]
			* <details><summary>Example Output (Click to expand)</summary><p>

					PS C:\users\lab_user\downloads\group> .\Certify.exe find /vulnerable

					   _____          _   _  __
					  / ____|        | | (_)/ _|
					 | |     ___ _ __| |_ _| |_ _   _
					 | |    / _ \ '__| __| |  _| | | |
					 | |___|  __/ |  | |_| | | | |_| |
					  \_____\___|_|   \__|_|_|  \__, |
					                             __/ |
					                            |___./
					  v1.0.0

					[*] Action: Find certificate templates
					[*] Using the search base 'CN=Configuration,DC=lab,DC=local'

					[*] Listing info about the Enterprise CA 'lab-CA-CA'

					    Enterprise CA Name            : lab-CA-CA
					    DNS Hostname                  : CA.lab.local
					    FullName                      : CA.lab.local\lab-CA-CA
					    Flags                         : SUPPORTS_NT_AUTHENTICATION, CA_SERVERTYPE_ADVANCED
					    Cert SubjectName              : CN=lab-CA-CA, DC=lab, DC=local
					    Cert Thumbprint               : FD65809936943E86F43428FF43E73D1A6CBE4273
					    Cert Serial                   : 70ED422FDD30DFAF4856C1DA3DE37A7F
					    Cert Start Date               : 8/6/2021 1:13:25 AM
					    Cert End Date                 : 8/6/2026 1:23:23 AM
					    Cert Chain                    : CN=lab-CA-CA,DC=lab,DC=local
					    [!] UserSpecifiedSAN : EDITF_ATTRIBUTESUBJECTALTNAME2 set, enrollees can specify Subject Alternative Names!
					    CA Permissions                :
					      Owner: BUILTIN\Administrators        S-1-5-32-544

					      Access Rights                                     Principal

					      Allow  ManageCA, ManageCertificates, Enroll       NT AUTHORITY\Authenticated UsersS-1-5-11
					        [!] Low-privileged principal has ManageCA rights!
					      Allow  Enroll                                     NT AUTHORITY\Authenticated UsersS-1-5-11
					      Allow  ManageCA, ManageCertificates               BUILTIN\Administrators        S-1-5-32-544
					      Allow  ManageCA, ManageCertificates               LAB\Domain Admins             S-1-5-21-1578223589-3704162669-771149463-512
					      Allow  ManageCA, ManageCertificates               LAB\Enterprise Admins         S-1-5-21-1578223589-3704162669-771149463-519
					    Enrollment Agent Restrictions : None

					[!] Vulnerable Certificates Templates :

					    CA Name                         : CA.lab.local\lab-CA-CA
					    Template Name                   : vuln_CA_template
					    Schema Version                  : 2
					    Validity Period                 : 1 year
					    Renewal Period                  : 6 weeks
					    msPKI-Certificates-Name-Flag    : ENROLLEE_SUPPLIES_SUBJECT
					    mspki-enrollment-flag           : INCLUDE_SYMMETRIC_ALGORITHMS, PUBLISH_TO_DS
					    Authorized Signatures Required  : 0
					    pkiextendedkeyusage             : Client Authentication, Encrypting File System, Secure Email
					    Permissions
					      Enrollment Permissions
					        Enrollment Rights           : LAB\Domain Admins             S-1-5-21-1578223589-3704162669-771149463-512
					                                      LAB\Domain Users              S-1-5-21-1578223589-3704162669-771149463-513
					                                      LAB\Enterprise Admins         S-1-5-21-1578223589-3704162669-771149463-519
					                                      LAB\lab_user                  S-1-5-21-1578223589-3704162669-771149463-500
					                                      NT AUTHORITY\Authenticated UsersS-1-5-11
					      Object Control Permissions
					        Owner                       : LAB\lab_user                  S-1-5-21-1578223589-3704162669-771149463-500
					        WriteOwner Principals       : LAB\Domain Admins             S-1-5-21-1578223589-3704162669-771149463-512
					                                      LAB\Enterprise Admins         S-1-5-21-1578223589-3704162669-771149463-519
					                                      LAB\lab_user                  S-1-5-21-1578223589-3704162669-771149463-500
					        WriteDacl Principals        : LAB\Domain Admins             S-1-5-21-1578223589-3704162669-771149463-512
					                                      LAB\Enterprise Admins         S-1-5-21-1578223589-3704162669-771149463-519
					                                      LAB\lab_user                  S-1-5-21-1578223589-3704162669-771149463-500
					        WriteProperty Principals    : LAB\Domain Admins             S-1-5-21-1578223589-3704162669-771149463-512
					                                      LAB\Enterprise Admins         S-1-5-21-1578223589-3704162669-771149463-519
					                                      LAB\lab_user                  S-1-5-21-1578223589-3704162669-771149463-500

					    CA Name                         : CA.lab.local\lab-CA-CA
					    Template Name                   : vuln_CA_template_2
					    Schema Version                  : 2
					    Validity Period                 : 1 year
					    Renewal Period                  : 6 weeks
					    msPKI-Certificates-Name-Flag    : ENROLLEE_SUPPLIES_SUBJECT
					    mspki-enrollment-flag           : INCLUDE_SYMMETRIC_ALGORITHMS, PUBLISH_TO_DS
					    Authorized Signatures Required  : 0
					    pkiextendedkeyusage             : Any Purpose, Client Authentication, Encrypting File System, Secure Email
					    Permissions
					      Enrollment Permissions
					        Enrollment Rights           : LAB\Domain Admins             S-1-5-21-1578223589-3704162669-771149463-512
					                                      LAB\Domain Users              S-1-5-21-1578223589-3704162669-771149463-513
					                                      LAB\Enterprise Admins         S-1-5-21-1578223589-3704162669-771149463-519
					                                      LAB\lab_user                  S-1-5-21-1578223589-3704162669-771149463-500
					                                      NT AUTHORITY\Authenticated UsersS-1-5-11
					      Object Control Permissions
					        Owner                       : LAB\lab_user                  S-1-5-21-1578223589-3704162669-771149463-500
					        WriteOwner Principals       : LAB\Domain Admins             S-1-5-21-1578223589-3704162669-771149463-512
					                                      LAB\Enterprise Admins         S-1-5-21-1578223589-3704162669-771149463-519
					                                      LAB\lab_user                  S-1-5-21-1578223589-3704162669-771149463-500
					        WriteDacl Principals        : LAB\Domain Admins             S-1-5-21-1578223589-3704162669-771149463-512
					                                      LAB\Enterprise Admins         S-1-5-21-1578223589-3704162669-771149463-519
					                                      LAB\lab_user                  S-1-5-21-1578223589-3704162669-771149463-500
					        WriteProperty Principals    : LAB\Domain Admins             S-1-5-21-1578223589-3704162669-771149463-512
					                                      LAB\Enterprise Admins         S-1-5-21-1578223589-3704162669-771149463-519
					                                      LAB\lab_user                  S-1-5-21-1578223589-3704162669-771149463-500

					    CA Name                         : CA.lab.local\lab-CA-CA
					    Template Name                   : vuln_CA_template_3
					    Schema Version                  : 2
					    Validity Period                 : 1 year
					    Renewal Period                  : 6 weeks
					    msPKI-Certificates-Name-Flag    : ENROLLEE_SUPPLIES_SUBJECT
					    mspki-enrollment-flag           : INCLUDE_SYMMETRIC_ALGORITHMS, PUBLISH_TO_DS
					    Authorized Signatures Required  : 0
					    pkiextendedkeyusage             : Any Purpose, Certificate Request Agent, Client Authentication, Encrypting File System, Secure Email
					    Permissions
					      Enrollment Permissions
					        Enrollment Rights           : LAB\Domain Admins             S-1-5-21-1578223589-3704162669-771149463-512
					                                      LAB\Domain Users              S-1-5-21-1578223589-3704162669-771149463-513
					                                      LAB\Enterprise Admins         S-1-5-21-1578223589-3704162669-771149463-519
					                                      LAB\lab_user                  S-1-5-21-1578223589-3704162669-771149463-500
					        All Extended Rights         : NT AUTHORITY\Authenticated UsersS-1-5-11
					      Object Control Permissions
					        Owner                       : LAB\lab_user                  S-1-5-21-1578223589-3704162669-771149463-500
					        Full Control Principals     : NT AUTHORITY\Authenticated UsersS-1-5-11
					        WriteOwner Principals       : LAB\Domain Admins             S-1-5-21-1578223589-3704162669-771149463-512
					                                      LAB\Enterprise Admins         S-1-5-21-1578223589-3704162669-771149463-519
					                                      LAB\lab_user                  S-1-5-21-1578223589-3704162669-771149463-500
					                                      NT AUTHORITY\Authenticated UsersS-1-5-11
					        WriteDacl Principals        : LAB\Domain Admins             S-1-5-21-1578223589-3704162669-771149463-512
					                                      LAB\Enterprise Admins         S-1-5-21-1578223589-3704162669-771149463-519
					                                      LAB\lab_user                  S-1-5-21-1578223589-3704162669-771149463-500
					                                      NT AUTHORITY\Authenticated UsersS-1-5-11
					        WriteProperty Principals    : LAB\Domain Admins             S-1-5-21-1578223589-3704162669-771149463-512
					                                      LAB\Enterprise Admins         S-1-5-21-1578223589-3704162669-771149463-519
					                                      LAB\lab_user                  S-1-5-21-1578223589-3704162669-771149463-500
					                                      NT AUTHORITY\Authenticated UsersS-1-5-11



					Certify completed in 00:00:03.3111981
