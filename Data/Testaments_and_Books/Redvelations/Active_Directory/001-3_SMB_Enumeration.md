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
# SMB
## Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@enum #@enumerate #@enumeration #@smb

Tools

		#@impacket #@pcaptools #@pcap #@nmap #@zmap #@ldapsearch #@ldapsearch-ad #@rpcclient #@smbmap #@crackmapexec #@manspider

</p></details>

## Enumeration
### From a Linux Machine
#### No Credentials Required (Usually)
* Systems Using Legacy SMBv1
	* <details><summary>crackmapexec (Click to expand)</summary><p>

			crackmapexec smb $TARGET_SUBNET
		* Example Output

				root@jack-Virtual-Machine:~/ldapsearch-ad# crackmapexec smb  10.0.0.0/24
				SMB         10.0.0.1        445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
				SMB         10.0.0.101      445    WIN11            [*] Windows 10.0 Build 22000 x64 (name:WIN11) (domain:microsoftdelivery.com) (signing:False) (SMBv1:False)
				SMB         10.0.0.3        445    CA               [*] Windows 10.0 Build 17763 x64 (name:CA) (domain:microsoftdelivery.com) (signing:False) (SMBv1:False)
				SMB         10.0.0.50       445    APP              [*] Windows 10.0 Build 17763 x64 (name:APP) (domain:microsoftdelivery.com) (signing:False) (SMBv1:False)
				SMB         10.0.0.2        445    DC02             [*] Windows 10.0 Build 17763 x64 (name:DC02) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
* Systems Missing SMB Signing
	* <details><summary>crackmapexec (Click to expand)</summary><p>

			crackmapexec smb $TARGET_SUBNET --gen-relay-list $WORKING_DIR/outfile.txt
		* Example Output

				root@jack-Virtual-Machine:~/ldapsearch-ad# crackmapexec smb  10.0.0.0/24
				SMB         10.0.0.1        445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
				SMB         10.0.0.101      445    WIN11            [*] Windows 10.0 Build 22000 x64 (name:WIN11) (domain:microsoftdelivery.com) (signing:False) (SMBv1:False)
				SMB         10.0.0.3        445    CA               [*] Windows 10.0 Build 17763 x64 (name:CA) (domain:microsoftdelivery.com) (signing:False) (SMBv1:False)
				SMB         10.0.0.50       445    APP              [*] Windows 10.0 Build 17763 x64 (name:APP) (domain:microsoftdelivery.com) (signing:False) (SMBv1:False)
				SMB         10.0.0.2        445    DC02             [*] Windows 10.0 Build 17763 x64 (name:DC02) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
	* <details><summary>Runfinger.py (Click to expand)</summary><p>

			python runfinger.py $TARGET_SUBNET
* Test for Null Authentication
	* <details><summary>crackmapexec (Click to expand) ([crackmapexec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md))</summary><p>
		* Examples
			* Example 1: Pure Null Authentication

					crackmapexec smb -u '' -p '' $TARGET
* Enumerate Users (Null Authentication)
	* <details><summary>crackmapexec (Click to expand) ([crackmapexec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md))</summary><p>
		* Examples

				crackmapexec smb -u '' -p '' --users $TARGET
* Group Enumeration (Null Authentication)
	* <details><summary>crackmapexec (Click to expand) ([crackmapexec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md))</summary><p>
		* Examples

				crackmapexec smb -u '' -p '' --groups $TARGET
* Password Policy (Null Authentication)
	* <details><summary>crackmapexec (Click to expand) ([crackmapexec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md))</summary><p>
		* Examples

				crackmapexec smb -u '' -p '' --pass-pol $TARGET
			* <details><summary>Example Output (Click to expand)</summary><p>

					crackmapexec smb 10.0.0.0/24 -u '' -p '' 
					SMB	 	  10.0.0.2	 	 445	 CA	 	 	    [*] Windows 10.0 Build 17763 x64 (name:CA) (domain:securelab.local) (signing:False) (SMBv1:False)
					SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:securelab.local) (signing:True) (SMBv1:False)
					SMB	 	  10.0.0.10	    445	 DC02	 	 	  [*] Windows 10.0 Build 17763 x64 (name:DC02) (domain:securelab.local) (signing:True) (SMBv1:False)
					SMB	 	  10.0.0.2	 	 445	 CA	 	 	    [-] securelab.local\: STATUS_ACCESS_DENIED 
					SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  [-] securelab.local\: STATUS_ACCESS_DENIED 
					SMB	 	  10.0.0.22	    445	 NONE	 	 	  [*]  (name:) (domain:) (signing:False) (SMBv1:True)
					SMB	 	  10.0.0.10	    445	 DC02	 	 	  [-] securelab.local\: STATUS_ACCESS_DENIED 
					SMB	 	  10.0.0.22	    445	 NONE	 	 	  [-] \: STATUS_ACCOUNT_DISABLED 
* Shares ([File Share Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-7_File_Share_Enumeration.md))

#### Credentials Required (Usually)
* Password Policy
	* <details><summary>crackmapexec (Click to expand) ([crackmapexec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md))</summary><p>
		* Example

				crackmapexec smb -u $DOMAIN_USER -p $PASSWORD -d $DOMAIN --pass-pol $DOMAIN_CONTROLLER
			* Example Output

					root@jack-Virtual-Machine:~/ldapsearch-ad# crackmapexec smb -u $DOMAIN_USER -p $PASSWORD -d $DOMAIN --pass-pol $DOMAIN_CONTROLLER
					SMB         dc01.microsoftdelivery.com 445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
					SMB         dc01.microsoftdelivery.com 445    DC01             [+] microsoftdelivery.com\domain_user:P@ssw0rd 
					SMB         dc01.microsoftdelivery.com 445    DC01             [+] Dumping password info for domain: MICROSOFTDELIVE
					SMB         dc01.microsoftdelivery.com 445    DC01             Minimum password length: 7
					SMB         dc01.microsoftdelivery.com 445    DC01             Password history length: 24
					SMB         dc01.microsoftdelivery.com 445    DC01             Maximum password age: Not Set
					SMB         dc01.microsoftdelivery.com 445    DC01             
					SMB         dc01.microsoftdelivery.com 445    DC01             Password Complexity Flags: 000001
					SMB         dc01.microsoftdelivery.com 445    DC01              Domain Refuse Password Change: 0
					SMB         dc01.microsoftdelivery.com 445    DC01              Domain Password Store Cleartext: 0
					SMB         dc01.microsoftdelivery.com 445    DC01              Domain Password Lockout Admins: 0
					SMB         dc01.microsoftdelivery.com 445    DC01              Domain Password No Clear Change: 0
					SMB         dc01.microsoftdelivery.com 445    DC01              Domain Password No Anon Change: 0
					SMB         dc01.microsoftdelivery.com 445    DC01              Domain Password Complex: 1
					SMB         dc01.microsoftdelivery.com 445    DC01             
					SMB         dc01.microsoftdelivery.com 445    DC01             Minimum password age: None
					SMB         dc01.microsoftdelivery.com 445    DC01             Reset Account Lockout Counter: 30 minutes 
					SMB         dc01.microsoftdelivery.com 445    DC01             Locked Account Duration: 30 minutes 
					SMB         dc01.microsoftdelivery.com 445    DC01             Account Lockout Threshold: None
					SMB         dc01.microsoftdelivery.com 445    DC01             Forced Log off Time: Not Set
* Users
	* <details><summary>crackmapexec (Click to expand) ([crackmapexec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md))</summary><p>
		* Example

				crackmapexec smb $DOMAIN_CONTROLLER -u $DOMAIN_USER -p $PASSWORD -d $DOMAIN --users
			* Example Output

					root@jack-Virtual-Machine:~/ldapsearch-ad# crackmapexec smb $DOMAIN_CONTROLLER -u $DOMAIN_USER -p $PASSWORD -d $DOMAIN --users
					SMB         dc01.microsoftdelivery.com 445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
					SMB         dc01.microsoftdelivery.com 445    DC01             [+] microsoftdelivery.com\domain_user:P@ssw0rd 
					SMB         dc01.microsoftdelivery.com 445    DC01             [+] Enumerated domain user(s)
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\asreproastable                 badpwdcount: 0 desc: 
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\schema_admin                   badpwdcount: 0 desc: 
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\server_operator                badpwdcount: 0 desc: 
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\dns_admin                      badpwdcount: 0 desc: 
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\account_operator               badpwdcount: 0 desc: 
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\backup_operator                badpwdcount: 0 desc: 
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\domain_user_builtin            badpwdcount: 0 desc: 
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\kerberoastable                 badpwdcount: 0 desc: 
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\domain_user_target             badpwdcount: 0 desc: 
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\domain_user_writer             badpwdcount: 0 desc: 
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\Domain_User_ADCS               badpwdcount: 0 desc: 
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\MSOL_acade27cae4b              badpwdcount: 4 desc: Account created by Microsoft Azure Active Directory Connect with installation identifier acade27cae4b4e0b9a480eb4cd822638 running on computer AAD configured to synchronize to tenant microsoftdelivery.onmicrosoft.com. This account must have directory replication permissions in the local Active Directory and write permission on certain attributes to enable Hybrid Deployment.                                                                                                                                                                    
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\domain_user                    badpwdcount: 0 desc: 
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\domain_admin                   badpwdcount: 0 desc: 
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\krbtgt                         badpwdcount: 0 desc: Key Distribution Center Service Account                                                                                                                                                                  
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\Guest                          badpwdcount: 0 desc: Built-in account for guest access to the computer/domain                                                                                                                                                 
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\Administrator                  badpwdcount: 0 desc: Built-in account for administering the computer/domain
* Computers
	* <details><summary>crackmapexec (Click to expand) ([crackmapexec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md))</summary><p>
		* Example

				crackmapexec smb $DOMAIN_CONTROLLER -u $DOMAIN_USER -p $PASSWORD -d $DOMAIN --pass-pol
			* Example Output

					root@jack-Virtual-Machine:~/ldapsearch-ad# crackmapexec smb $DOMAIN_CONTROLLER -u $DOMAIN_USER -p $PASSWORD -d $DOMAIN --computers
					SMB         dc01.microsoftdelivery.com 445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
					SMB         dc01.microsoftdelivery.com 445    DC01             [+] microsoftdelivery.com\domain_user:P@ssw0rd 
					SMB         dc01.microsoftdelivery.com 445    DC01             [+] Enumerated domain computer(s)
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\Win11$                        
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\App$                          
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\Exchange$                     
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\CA$                           
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\DC02$                         
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\DC01$
* Groups
	* <details><summary>crackmapexec (Click to expand) ([crackmapexec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md))</summary><p>
		* Example

				crackmapexec smb $DOMAIN_CONTROLLER -u $DOMAIN_USER -p $PASSWORD -d $DOMAIN --groups
			* Example Output

					root@jack-Virtual-Machine:~/ldapsearch-ad# crackmapexec smb $DOMAIN_CONTROLLER -u $DOMAIN_USER -p $PASSWORD -d $DOMAIN --groups
					SMB         dc01.microsoftdelivery.com 445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
					SMB         dc01.microsoftdelivery.com 445    DC01             [+] microsoftdelivery.com\domain_user:P@ssw0rd 
					SMB         dc01.microsoftdelivery.com 445    DC01             [+] Enumerated domain group(s)
					SMB         dc01.microsoftdelivery.com 445    DC01             VulnComputers                            membercount: 1
					SMB         dc01.microsoftdelivery.com 445    DC01             writeable                                membercount: 1
					SMB         dc01.microsoftdelivery.com 445    DC01             DnsUpdateProxy                           membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             DnsAdmins                                membercount: 1
					SMB         dc01.microsoftdelivery.com 445    DC01             Enterprise Key Admins                    membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Key Admins                               membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Protected Users                          membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Cloneable Domain Controllers             membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Enterprise Read-only Domain Controllers  membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Read-only Domain Controllers             membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Denied RODC Password Replication Group   membercount: 8
					SMB         dc01.microsoftdelivery.com 445    DC01             Allowed RODC Password Replication Group  membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Terminal Server License Servers          membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Windows Authorization Access Group       membercount: 1
					SMB         dc01.microsoftdelivery.com 445    DC01             Incoming Forest Trust Builders           membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Pre-Windows 2000 Compatible Access       membercount: 2
					SMB         dc01.microsoftdelivery.com 445    DC01             Account Operators                        membercount: 1
					SMB         dc01.microsoftdelivery.com 445    DC01             Server Operators                         membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             RAS and IAS Servers                      membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Group Policy Creator Owners              membercount: 1
					SMB         dc01.microsoftdelivery.com 445    DC01             Domain Guests                            membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Domain Users                             membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Domain Admins                            membercount: 2
					SMB         dc01.microsoftdelivery.com 445    DC01             Cert Publishers                          membercount: 1
					SMB         dc01.microsoftdelivery.com 445    DC01             Enterprise Admins                        membercount: 2
					SMB         dc01.microsoftdelivery.com 445    DC01             Schema Admins                            membercount: 1
					SMB         dc01.microsoftdelivery.com 445    DC01             Domain Controllers                       membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Domain Computers                         membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Storage Replica Administrators           membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Remote Management Users                  membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Access Control Assistance Operators      membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Hyper-V Administrators                   membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             RDS Management Servers                   membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             RDS Endpoint Servers                     membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             RDS Remote Access Servers                membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Certificate Service DCOM Access          membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Event Log Readers                        membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Cryptographic Operators                  membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             IIS_IUSRS                                membercount: 1
					SMB         dc01.microsoftdelivery.com 445    DC01             Distributed COM Users                    membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Performance Log Users                    membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Performance Monitor Users                membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Network Configuration Operators          membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Remote Desktop Users                     membercount: 1
					SMB         dc01.microsoftdelivery.com 445    DC01             Replicator                               membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Backup Operators                         membercount: 2
					SMB         dc01.microsoftdelivery.com 445    DC01             Print Operators                          membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             Guests                                   membercount: 2
					SMB         dc01.microsoftdelivery.com 445    DC01             Users                                    membercount: 3
					SMB         dc01.microsoftdelivery.com 445    DC01             Administrators                           membercount: 3
					SMB         dc01.microsoftdelivery.com 445    DC01             DHCP Administrators                      membercount: 0
					SMB         dc01.microsoftdelivery.com 445    DC01             DHCP Users                               membercount: 0
* Group Members
	* <details><summary>crackmapexec (Click to expand) ([crackmapexec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md))</summary><p>
		* Example

				crackmapexec smb $DOMAIN_CONTROLLER -u $DOMAIN_USER -p $PASSWORD -d $DOMAIN --groups <GROUP_NAME>
			* Example Output

					root@jack-Virtual-Machine:~/ldapsearch-ad# crackmapexec smb $DOMAIN_CONTROLLER -u $DOMAIN_USER -p $PASSWORD -d $DOMAIN --groups 'Administrators'
					SMB         dc01.microsoftdelivery.com 445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
					SMB         dc01.microsoftdelivery.com 445    DC01             [+] microsoftdelivery.com\domain_user:P@ssw0rd 
					SMB         dc01.microsoftdelivery.com 445    DC01             [+] Enumerated members of domain group
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\Domain Admins
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\Enterprise Admins
					SMB         dc01.microsoftdelivery.com 445    DC01             microsoftdelivery.com\Administrator
* Systems with WebClientService/WebDEV Running
	* <details><summary>WebClient Service Scanner (Click to expand) -<br />[https://github.com/Hackndo/WebclientServiceScanner](https://github.com/Hackndo/WebclientServiceScanner)</summary><p>
		* Example
		
				webclientservicescanner $DOMAIN/$DOMAIN_USER:$PASSWORD@$SUBNET_CIDR
			* Creds validated against DC before scanning so typos won't lock out account. Use `-no-validation` to bypass.
			* Example Output

					(WebclientServiceScanner) root@jack-Virtual-Machine:~/WebclientServiceScanner# webclientservicescanner $DOMAIN/$DOMAIN_USER:$PASSWORD@$SUBNET_CIDR
					WebClient Service Scanner v0.1.0 - pixis (@hackanddo) - Based on @tifkin_ idea

					[Errno Connection error (10.0.0.100:445)] [Errno 111] Connection refused
					[10.0.0.1] STOPPED
					[10.0.0.101] RUNNING
					[10.0.0.3] STOPPED
					[10.0.0.2] STOPPED
					[10.0.0.50] STOPPED
	* <details><summary>crackmapexec (Click to expand)</summary><p>
		* Example

				cme smb -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -M webdav $SUBNET_CIDR
			* Example Output

					root@jack-Virtual-Machine:~# cme smb -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -M webdav $SUBNET_CIDR
					SMB         10.0.0.101      445    WIN11            [*] Windows 10.0 Build 22000 x64 (name:WIN11) (domain:microsoftdelivery.com) (signing:False) (SMBv1:False)
					SMB         10.0.0.1        445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
					SMB         10.0.0.2        445    DC02             [*] Windows 10.0 Build 17763 x64 (name:DC02) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
					SMB         10.0.0.3        445    CA               [*] Windows 10.0 Build 17763 x64 (name:CA) (domain:microsoftdelivery.com) (signing:False) (SMBv1:False)
					SMB         10.0.0.101      445    WIN11            [+] microsoftdelivery.com\domain_user:P@ssw0rd 
					WEBDAV      10.0.0.101      445    WIN11            WebClient Service enabled on: 10.0.0.101
					SMB         10.0.0.1        445    DC01             [+] microsoftdelivery.com\domain_user:P@ssw0rd 
					SMB         10.0.0.2        445    DC02             [+] microsoftdelivery.com\domain_user:P@ssw0rd 
					SMB         10.0.0.50       445    APP              [*] Windows 10.0 Build 17763 x64 (name:APP) (domain:microsoftdelivery.com) (signing:False) (SMBv1:False)
					SMB         10.0.0.3        445    CA               [+] microsoftdelivery.com\domain_user:P@ssw0rd 
					SMB         10.0.0.50       445    APP              [-] Connection Error: The NETBIOS connection with the remote host timed out.
* Shares ([File Share Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-7_File_Share_Enumeration.md))

#### Local Administrator Credentials Required (Usually)
* Authentication/Session Data
	* Logged On Users (Recommended over session, see notes)
		* <details><summary>Notes (Click to expand)</summary><p>
			* Session enumeration can have issues, particularly in heavily virtualized environments like Citrix environments
			* Requires local admin
		* <details><summary>bloodhound.py (Click to expand) ([bloodhound.py Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/Bloodhound/002-0_Ingestors.md))</summary><p>

				python bloodhound.py --zip -c LoggedOn option
		* <details><summary>crackmapexec ([crackmapexec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md)) (Click to expand)</summary><p>

				crackmapexec smb -u $LOCAL_ADMIN -p $PASSWORD --loggedon $TARGET
	* Session Data
		* <details><summary>Recommended: BloodHound.py (Click to expand) ([bloodhound.py Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/Bloodhound/002-0_Ingestors.md)) </summary><p>

				python BloodHound.py -c Session
		* <details><summary>crackmapexec (Click to expand) ([crackmapexec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md))</summary><p>

				crackmapexec smb -u $LOCAL_ADMIN -p $PASSWORD --loggedon --sessions $TARGET
			* Expected output

					crackmapexec smb 10.0.0.0/24 -u 'domain_admin' -p 'Passw0rd' -d securelab.local --sessions
					SMB	 	  10.0.0.10	    445	 DC02	 	 	  [*] Windows 10.0 Build 17763 x64 (name:DC02) (domain:securelab.local) (signing:True) (SMBv1:False)
					SMB	 	  10.0.0.2	 	 445	 CA	 	 	    [*] Windows 10.0 Build 17763 x64 (name:CA) (domain:securelab.local) (signing:False) (SMBv1:False)
					SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:securelab.local) (signing:True) (SMBv1:False)
					SMB	 	  10.0.0.22	    445	 NONE	 	 	  [*]  (name:) (domain:securelab.local) (signing:False) (SMBv1:True)
					SMB	 	  10.0.0.10	    445	 DC02	 	 	  [+] securelab.local\domain_admin:Passw0rd (Pwn3d!)
					SMB	 	  10.0.0.2	 	 445	 CA	 	 	    [+] securelab.local\domain_admin:Passw0rd (Pwn3d!)
					SMB	 	  10.0.0.10	    445	 DC02	 	 	  [+] Enumerated sessions
					SMB	 	  10.0.0.2	 	 445	 CA	 	 	    [+] Enumerated sessions
					SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  [+] securelab.local\domain_admin:Passw0rd (Pwn3d!)
					SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  [+] Enumerated sessions

#### From a Windows Machine

* <details><summary>Recommended: Sharphound (Click to expand)</summary><p>

		.\Sharphound.exe --CollectionMethod Session --Loop --Loopduration <HH:MM:SS>
* <details><summary>PowerSploit (Click to expand)</summary><p>

		Invoke-UserHunter -showall -Credential $cred -ComputerName workstation04 | Format-Table -Property userdomain, username,computername, ipaddress