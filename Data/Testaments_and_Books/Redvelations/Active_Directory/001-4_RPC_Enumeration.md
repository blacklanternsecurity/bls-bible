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
# RPC Enumeration
## Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@enum #@enumerate #@enumeration #@dns #@dhcp #@ldap #@smb #@network #@icmp #@ping #@sweep #@cve #@exploit #@vuln #@vulnerability #@vulnerabilities #@vulns

Tools

		#@impacket #@pcaptools #@pcap #@nmap #@zmap #@samrdump #@rpcclient #@crackmapexec #@coercer

</p></details>

## References

## Overview

## Enumeration
### From a Linux Machine
#### No Credentials Required (Usually)
* Broad enumeration
	* <details><summary>impacket's rpcdump.py (Click to expand)</summary><p>

			rpcdump.py -port 135 $TARGET_IP
		* Example Output

				root@jack-Virtual-Machine:~# rpcdump.py -port 135 $TARGET_IP
				Impacket v0.10.1.dev1+20220720.103933.3c6713e - Copyright 2022 SecureAuth Corporation

				[*] Retrieving endpoint list from 10.0.0.60
				Protocol: N/A 
				Provider: N/A 
				UUID    : 51A227AE-825B-41F2-B4A9-1AC9557A1018 v1.0 Ngc Pop Key Service
				Bindings: 
				          ncacn_ip_tcp:10.0.0.60[49669]
				          ncalrpc:[NETLOGON_LRPC]
				          ncacn_ip_tcp:10.0.0.60[49664]
				          ncalrpc:[samss lpc]
				          ncalrpc:[SidKey Local End Point]
				          ncalrpc:[protected_storage]
				          ncalrpc:[lsasspirpc]
				          ncalrpc:[lsapolicylookup]
				          ncalrpc:[LSA_EAS_ENDPOINT]
				          ncalrpc:[LSA_IDPEXT_ENDPOINT]
				          ncalrpc:[lsacap]
				          ncalrpc:[LSARPC_ENDPOINT]
				          ncalrpc:[securityevent]
				          ncalrpc:[audit]
				          ncacn_np:\\WIN11[\pipe\lsass]

				Protocol: N/A 
				Provider: N/A 
				UUID    : 8FB74744-B2FF-4C00-BE0D-9EF9A191FE1B v1.0 Ngc Pop Key Service
				Bindings: 
				          ncacn_ip_tcp:10.0.0.60[49669]
				          ncalrpc:[NETLOGON_LRPC]
				          ncacn_ip_tcp:10.0.0.60[49664]
				          ncalrpc:[samss lpc]
				          ncalrpc:[SidKey Local End Point]
				          ncalrpc:[protected_storage]
				          ncalrpc:[lsasspirpc]
				          ncalrpc:[lsapolicylookup]
				          ncalrpc:[LSA_EAS_ENDPOINT]
				          ncalrpc:[LSA_IDPEXT_ENDPOINT]
				          ncalrpc:[lsacap]
				          ncalrpc:[LSARPC_ENDPOINT]
				          ncalrpc:[securityevent]
				          ncalrpc:[audit]
				          ncacn_np:\\WIN11[\pipe\lsass]

				Protocol: N/A 
				Provider: N/A 
	* <details><summary>enum4linux-ng (Click to expand)</summary><p>

			enum4linux-ng -P -w -u $USER -p $PASSWORD $DOMAIN_CONTROLLER
	* <details><summary>rpcmap.py (impacket) (Click to expand) ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md))</summary><p>
		* <details><summary>Options (Click to expand)</summary><p>

				python examples/rpcmap.py 'ncacn_ip_tcp:10.0.0.1'
			* Required
				* `stringbinding`
					* <details><summary>Examples (Click to expand)</summary><p>
	 	 	 	 	 	* `ncacn_ip_tcp:192.168.0.1[135]`
	 	 	 	 	 	* `ncacn_np:192.168.0.1[\pipe\spoolss]`
	 	 	 	 	 	* `ncacn_http:192.168.0.1[593]`
	 	 	 	 	 	* `ncacn_http:[6001,RpcProxy=exchange.contoso.com:443]`
	 	 	 	 	 	* `ncacn_http:localhost[3388,RpcProxy=rds.contoso:443]`
	* <details><summary>rpcclient (Click to expand)</summary><p>

			rpcclient -c 'command' $TARGET
		* `apt install smbclient` to install rpcclient.
		* Options
			* <details><summary>rpcclient (Click to expand)</summary><p>`lsaquery`: get domain name and SID (Security IDentifier)

					root@kali:/# rpcclient -c 'lsaquery' 10.0.0.1 -U securelab/domain_user
					Enter SECURELAB\domain_user's password: 
					Domain Name: SECURELAB
					Domain Sid: S-1-5-21-1850020582-442782152-1341288763
* Enumerate for forced authentication vulnerabilies (unauthenticated)
	* Multiple
		* <details><summary>coercer.py (Click to expand) -<br />[https://github.com/p0dalirius/Coercer](https://github.com/p0dalirius/Coercer)</summary><p>
			* Overview
				* The tool author has enumerated many potential forced authentication endpoints and produced PoCs for each case. The instances need research, but if you run out of options, it may be worth trying. -<br />[https://github.com/p0dalirius/windows-coerced-authentication-methods](https://github.com/p0dalirius/windows-coerced-authentication-methods)
			* Example 1: Analyze for multiple forced authentication options

					coercer -a -t $TARGET -l $LOCAL_IP
				* Example Output

						root@jack-Virtual-Machine:~# coercer -a  -t $DOMAIN_CONTROLLER -l $LOCAL_IP

						       ______
						      / ____/___  ___  _____________  _____
						     / /   / __ \/ _ \/ ___/ ___/ _ \/ ___/
						    / /___/ /_/ /  __/ /  / /__/  __/ /      v1.6
						    \____/\____/\___/_/   \___/\___/_/       by @podalirius_

						[dc01.microsoftdelivery.com] Analyzing available protocols on the remote machine and interesting calls ...
						   [>] Pipe '\PIPE\Fssagentrpc' is not accessible!
						   [>] Pipe '\PIPE\efsrpc' is not accessible!
						   [>] Pipe '\PIPE\lsarpc' is accessible!
						      [>] MS-EFSR (uuid=c681d488-d850-11d0-8c52-00c04fd90f7e, version=1.0) EfsRpcOpenFileRaw (opnum 0) 
						      [>] MS-EFSR (uuid=c681d488-d850-11d0-8c52-00c04fd90f7e, version=1.0) EfsRpcEncryptFileSrv (opnum 4) 
						      [>] MS-EFSR (uuid=c681d488-d850-11d0-8c52-00c04fd90f7e, version=1.0) EfsRpcDecryptFileSrv (opnum 5) 
						      [>] MS-EFSR (uuid=c681d488-d850-11d0-8c52-00c04fd90f7e, version=1.0) EfsRpcQueryUsersOnFile (opnum 6) 
						      [>] MS-EFSR (uuid=c681d488-d850-11d0-8c52-00c04fd90f7e, version=1.0) EfsRpcQueryRecoveryAgents (opnum 7) 
						      [>] MS-EFSR (uuid=c681d488-d850-11d0-8c52-00c04fd90f7e, version=1.0) EfsRpcFileKeyInfo (opnum 12) 
						   [>] Pipe '\PIPE\netdfs' is not accessible!
						   [>] Pipe '\PIPE\spoolss' is not accessible!

						[+] All done!

#### Credentials Required (Usually)
* Broad enumerations
	* <details><summary>impacket's samrdump.py (Click to expand)</summary><p>
		* Example

				samrdump.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$DOMAIN_CONTROLLER
			* Example Output

					root@jack-Virtual-Machine:~# samrdump.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$DOMAIN_CONTROLLER
					Impacket v0.10.1.dev1+20220720.103933.3c6713e - Copyright 2022 SecureAuth Corporation

					[*] Retrieving endpoint list from dc01.microsoftdelivery.com
					Found domain(s):
					 . MICROSOFTDELIVE
					 . Builtin
					[*] Looking up users in domain MICROSOFTDELIVE
					Found user: Administrator, uid = 500
					Found user: Guest, uid = 501
					Found user: krbtgt, uid = 502
					Found user: domain_admin, uid = 1105
					Found user: domain_user, uid = 1106
					Found user: MSOL_acade27cae4b, uid = 1107
					Found user: Domain_User_ADCS, uid = 1114
					Found user: domain_user_writer, uid = 1115
					Found user: domain_user_target, uid = 1116
					Found user: kerberoastable, uid = 1120
					Found user: domain_user_builtin, uid = 1121
					Found user: backup_operator, uid = 1122
					Found user: account_operator, uid = 1123
					Found user: dns_admin, uid = 1124
					Found user: server_operator, uid = 1125
					Found user: schema_admin, uid = 1126
					Found user: asreproastable, uid = 1127
					Administrator (500)/FullName:
					Administrator (500)/UserComment:
					Administrator (500)/PrimaryGroupId: 513
					Administrator (500)/BadPasswordCount: 0
					Administrator (500)/LogonCount: 15
					Administrator (500)/PasswordLastSet: 2022-06-24 11:39:39.613339
					Administrator (500)/PasswordDoesNotExpire: False
					Administrator (500)/AccountIsDisabled: False
					Administrator (500)/ScriptPath:
					Guest (501)/FullName: 
					<TRUNCATED>
* Enumerate users
	* <details><summary>impacket's lookupsid.py ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md)) (Click to expand)</summary><p>
		* Examples
			* Example 1: Enumerate users, default max RID 4000

					lookupsid.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$TARGET 0
			* Example 2: Enumerate Users, higher max RID

					lookupsid.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$TARGET 10000000
	* <details><summary>RID_ENUM (Click to expand) -<br />[https://github.com/trustedsec/ridenum](https://github.com/trustedsec/ridenum)</summary><p>

			python ridenum.py $DOMAIN_CONTROLLER <start_rid> <end_rid> $DOMAIN_USER $PASSWORD $PASSWORD_FILE $USERNAME_FILE
		* Optional Flags: Username/Password, Username File/Pasword File
		* <details><summary>Example output (Click to expand)</summary><p>

				python ridenum.py 10.0.0.1 0 10000000 domain_user 'Passw0rd'
				[*] Attempting lsaquery first...This will enumerate the base domain SID
				[*] Successfully enumerated base domain SID. Printing information: 
				Domain Name: SECURELAB
				Domain Sid: S-1-5-21-1850020582-442782152-1341288763
				[*] Moving on to extract via RID cycling attack.. 
				[*] Enumerating user accounts.. This could take a little while.
				Account name: SECURELAB\Administrator
				Account name: SECURELAB\Guest
				Account name: SECURELAB\krbtgt
				Account name: SECURELAB\DC01$
				Account name: SECURELAB\CA$
				Account name: SECURELAB\EXCHANGE$
				Account name: SECURELAB\DC02$
				Account name: SECURELAB\domain_admin
				Account name: SECURELAB\domain_user
				Account name: SECURELAB\WIN10-1$
				Account name: SECURELAB\WIN11-1$
				[*] RIDENUM has finished enumerating user accounts...
	* <details><summary>rpcclient `enumdomusers` (Click to expand)</summary><p>
		* Example

				rpcclient -U $DOMAIN_NETBIOS/$DOMAIN_USER -c 'enumdomusers' $DOMAIN_CONTROLLER
			* Example Output
			
					root@ubuntu:/# rpcclient -U $DOMAIN_NETBIOS/$DOMAIN_USER -c 'enumdomusers' $DOMAIN_CONTROLLER
					user:[Administrator] rid:[0x1f4]
					user:[Guest] rid:[0x1f5]
					user:[krbtgt] rid:[0x1f6]
					user:[domain_admin] rid:[0x454]
					user:[domain_user] rid:[0x455]
* Enumerate Domain SID
	* <details><summary>impacket's lookupsid.py ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md)) (Click to expand)</summary><p>
		* Example 1: Set Max RID value to 0

				lookupsid.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$TARGET 0
* Enumerate groups
	* Enumerate Domain groups
		* <details><summary>rpcclient `enumdomgroups` (Click to expand)</summary><p>

				root@ubuntu:/# rpcclient -U securelab/domain_user -c 'enumdomgroups' 10.0.0.1
				Enter SECURELAB\domain_user's password: 
				group:[Enterprise Read-only Domain Controllers] rid:[0x1f2]
				group:[Domain Admins] rid:[0x200]
				group:[Domain Users] rid:[0x201]
				group:[Domain Guests] rid:[0x202]
				group:[Domain Computers] rid:[0x203]
				group:[Domain Controllers] rid:[0x204]
				group:[Schema Admins] rid:[0x206]
				group:[Enterprise Admins] rid:[0x207]
				group:[Group Policy Creator Owners] rid:[0x208]
				group:[Read-only Domain Controllers] rid:[0x209]
				group:[Cloneable Domain Controllers] rid:[0x20a]
				group:[Protected Users] rid:[0x20d]
				group:[Key Admins] rid:[0x20e]
				group:[Enterprise Key Admins] rid:[0x20f]
				group:[DnsUpdateProxy] rid:[0x44e]
	* Built-in
		* <details><summary>rpcclient `enumalsgroups builtin`, returns local groups and RIDs (Relative IDs) (Click to expand)</summary><p>
			* Examples
				* Example 1: Password Authentication, Built-in Group

						rpcclient -U $DOMAIN_NETBIOS/$DOMAIN_USER$PASSWORD $TARGET -c 'enumalsgroups builtin'
					* <details><summary>Example Output (Click to expand)</summary><p>

							group:[Server Operators] rid:[0x225]
							group:[Account Operators] rid:[0x224]
							group:[Pre-Windows 2000 Compatible Access] rid:[0x22a]
							group:[Incoming Forest Trust Builders] rid:[0x22d]
							group:[Windows Authorization Access Group] rid:[0x230]
							group:[Terminal Server License Servers] rid:[0x231]
							group:[Administrators] rid:[0x220]
							group:[Users] rid:[0x221]
							group:[Guests] rid:[0x222]
							group:[Print Operators] rid:[0x226]
							group:[Backup Operators] rid:[0x227]
							group:[Replicator] rid:[0x228]
							group:[Remote Desktop Users] rid:[0x22b]
							group:[Network Configuration Operators] rid:[0x22c]
							group:[Performance Monitor Users] rid:[0x22e]
							group:[Performance Log Users] rid:[0x22f]
							group:[Distributed COM Users] rid:[0x232]
							group:[IIS_IUSRS] rid:[0x238]
							group:[Cryptographic Operators] rid:[0x239]
							group:[Event Log Readers] rid:[0x23d]
							group:[Certificate Service DCOM Access] rid:[0x23e]
							group:[RDS Remote Access Servers] rid:[0x23f]
							group:[RDS Endpoint Servers] rid:[0x240]
							group:[RDS Management Servers] rid:[0x241]
							group:[Hyper-V Administrators] rid:[0x242]
							group:[Access Control Assistance Operators] rid:[0x243]
							group:[Remote Management Users] rid:[0x244]
							group:[Storage Replica Administrators] rid:[0x246]
* Enumerate group members
	* <details><summary>rpcclient `queryaliasmem <RID>`: list local group members, returns SIDs (Click to expand)</summary><p>

			root@ubuntu:/# rpcclient -U securelab/domain_user -c 'queryaliasmem builtin 0x220' 10.0.0.1
			Enter SECURELAB\domain_user's password: 
				 	 sid:[S-1-5-21-1850020582-442782152-1341288763-500]
				 	 sid:[S-1-5-21-1850020582-442782152-1341288763-519]
				 	 sid:[S-1-5-21-1850020582-442782152-1341288763-512]
* Lookup SID for a username
	* <details><summary>rpcclient `lookupnames <NAME>`: resolve name to SID (Click to expand)</summary><p>

			root@ubuntu:/# rpcclient -U securelab/domain_user -c 'lookupnames domain_admin' 10.0.0.1
			Enter SECURELAB\domain_user's password: 
			domain_admin S-1-5-21-1850020582-442782152-1341288763-1108 (User: 1)
* Collect user information
	* <details><summary>rpcclient `queryuser <rid/name>`: obtain info on a user (Click to expand)</summary><p>

			root@ubuntu:/# rpcclient -U securelab/domain_user -c 'queryuser domain_admin' 10.0.0.1
			Enter SECURELAB\domain_user's password: 
				 	 User Name   :   domain_admin
				 	 Full Name   :   Domain Admin
				 	 Home Drive  :
				 	 Dir Drive   :
				 	 Profile Path:
				 	 Logon Script:
				 	 Description :
				 	 Workstations:
				 	 Comment	  :
				 	 Remote Dial :
				 	 Logon Time	 	 	    :	   Sat, 06 Nov 2021 20:11:16 PDT
				 	 Logoff Time	 	 	   :	   Wed, 31 Dec 1969 16:00:00 PST
				 	 Kickoff Time	 	 	  :	   Wed, 13 Sep 30828 19:48:05 PDT
				 	 Password last set Time   :	   Thu, 04 Nov 2021 00:19:56 PDT
				 	 Password can change Time :	   Fri, 05 Nov 2021 00:19:56 PDT
				 	 Password must change Time:	   Wed, 13 Sep 30828 19:48:05 PDT
				 	 unknown_2[0..31]...
				 	 user_rid :	   0x454
				 	 group_rid:	   0x201
				 	 acb_info :	   0x00000210
				 	 fields_present: 0x00ffffff
				 	 logon_divs:	  168
				 	 bad_password_count:	  0x00000000
				 	 logon_count:	 0x00000015
				 	 padding1[0..7]...
				 	 logon_hrs[0..21]...
* List members of a group
	* <details><summary>rpcclient `querygroupmem <rid>`: obtain group members, equivalent to `net group <group> /domain` (Click to expand)</summary><p>
		* Examples
			* Example 1:

					rpcclient -U $DOMAIN_NETBIOS/$DOMAIN_USER%$PASSWORD -c 'querygroupmem 0x200' $DOMAIN_CONTROLLER
				* Example Output

						root@ubuntu:/# rpcclient -U securelab/domain_user -c 'querygroupmem 0x200' 10.0.0.1
						Enter SECURELAB\domain_user's password: 
							 	 rid:[0x1f4] attr:[0x7]
							 	 rid:[0x454] attr:[0x7]
* List a user's privileges
 	* <details><summary>rpcclient `enumprivs`: list user privileges (Click to expand)</summary><p>
		* Examples
			* Example 1

					rpcclient -U $DOMAIN_NETBIOS/$DOMAIN_USER%$PASSWORD -c 'enumprivs' $DOMAIN_CONTROLLER
				* Example Output

						rpcclient $> enumprivs
						found 35 privileges

						SeCreateTokenPrivilege	 	   0:2 (0x0:0x2)
						SeAssignPrimaryTokenPrivilege	 	    0:3 (0x0:0x3)
						SeLockMemoryPrivilege	 	    0:4 (0x0:0x4)
						SeIncreaseQuotaPrivilege	 	 	 	 0:5 (0x0:0x5)
						SeMachineAccountPrivilege	 	 	    0:6 (0x0:0x6)
						SeTcbPrivilege	 	   0:7 (0x0:0x7)
						SeSecurityPrivilege	 	 	  0:8 (0x0:0x8)
						SeTakeOwnershipPrivilege	 	 	 	 0:9 (0x0:0x9)
						SeLoadDriverPrivilege	 	    0:10 (0x0:0xa)
						SeSystemProfilePrivilege	 	 	 	 0:11 (0x0:0xb)
						SeSystemtimePrivilege	 	    0:12 (0x0:0xc)
						SeProfileSingleProcessPrivilege	 	 	 	  0:13 (0x0:0xd)
						SeIncreaseBasePriorityPrivilege	 	 	 	  0:14 (0x0:0xe)
						SeCreatePagefilePrivilege	 	 	    0:15 (0x0:0xf)
						SeCreatePermanentPrivilege	 	 	   0:16 (0x0:0x10)
						SeBackupPrivilege	 	 	    0:17 (0x0:0x11)
						SeRestorePrivilege	 	 	   0:18 (0x0:0x12)
						SeShutdownPrivilege	 	 	  0:19 (0x0:0x13)
						SeDebugPrivilege	 	 	 	 0:20 (0x0:0x14)
						SeAuditPrivilege	 	 	 	 0:21 (0x0:0x15)
						SeSystemEnvironmentPrivilege	 	 	 0:22 (0x0:0x16)
						SeChangeNotifyPrivilege	 	 	 	  0:23 (0x0:0x17)
						SeRemoteShutdownPrivilege	 	 	    0:24 (0x0:0x18)
						SeUndockPrivilege	 	 	    0:25 (0x0:0x19)
						SeSyncAgentPrivilege	 	 	 0:26 (0x0:0x1a)
						SeEnableDelegationPrivilege	 	 	  0:27 (0x0:0x1b)
						SeManageVolumePrivilege	 	 	 	  0:28 (0x0:0x1c)
						SeImpersonatePrivilege	 	   0:29 (0x0:0x1d)
						SeCreateGlobalPrivilege	 	 	 	  0:30 (0x0:0x1e)
						SeTrustedCredManAccessPrivilege	 	 	 	  0:31 (0x0:0x1f)
						SeRelabelPrivilege	 	 	   0:32 (0x0:0x20)
						SeIncreaseWorkingSetPrivilege	 	    0:33 (0x0:0x21)
						SeTimeZonePrivilege	 	 	  0:34 (0x0:0x22)
						SeCreateSymbolicLinkPrivilege	 	    0:35 (0x0:0x23)
						SeDelegateSessionUserImpersonatePrivilege	 	 	    0:36 (0x0:0x24)
* Enumerate drivers
	* <details><summary>rpcclient `enumdrivers` (Click to expand)</summary><p>
		* Examples
			* Example 1

					rpcclient -U $DOMAIN_NETBIOS/$DOMAIN_USER%$PASSWORD -c 'enumdrivers' $DOMAIN_CONTROLLER
				* Example Output

						rpcclient $> enumdrivers

						[Windows NT x86]
						Printer Driver Info 1:
							 	 Driver Name: [Microsoft enhanced Point and Print compatibility driver]

						Server does not support environment [Windows NT R4000]
						Server does not support environment [Windows NT Alpha_AXP]
						Server does not support environment [Windows NT PowerPC]

						[Windows x64]
						Printer Driver Info 1:
							 	 Driver Name: [Microsoft XPS Document Writer v4]

						Printer Driver Info 1:
							 	 Driver Name: [Microsoft Print To PDF]

						Printer Driver Info 1:
							 	 Driver Name: [Microsoft enhanced Point and Print compatibility driver]
* Enumerate connected printers
	* <details><summary>`enumprinters` (Click to expand)</summary><p>
		* Examples
			* Example 1

					rpcclient -U $DOMAIN_NETBIOS/$DOMAIN_USER%$PASSWORD -c 'getdompwinfo' $DOMAIN_CONTROLLER
				* Example Output

						rpcclient $> enumprinters
						No printers returned.
* Enumerate exposed RPC ports
	* <details><summary>rpcclient `enumports` (Click to expand)</summary><p>
		* Examples
			* Example 1

					rpcclient -U $DOMAIN_NETBIOS/$DOMAIN_USER%$PASSWORD -c 'enumports' $DOMAIN_CONTROLLER
				* Example Output

						rpcclient $> enumports
					 	 Port Name:	   [COM1:]
					 	 Port Name:	   [COM2:]
					 	 Port Name:	   [COM3:]
					 	 Port Name:	   [COM4:]
					 	 Port Name:	   [FILE:]
					 	 Port Name:	   [LPT1:]
					 	 Port Name:	   [LPT2:]
					 	 Port Name:	   [LPT3:]
					 	 Port Name:	   [PORTPROMPT:]
* Password Policy
	* <details><summary>rpcclient `getdompwinfo`: get password policy (Click to expand)</summary><p>
		* Examples
			* Example 1

					rpcclient -U $DOMAIN_NETBIOS/$DOMAIN_USER%$PASSWORD -c 'getdompwinfo' $DOMAIN_CONTROLLER
				* Example Output

						root@ubuntu:/# rpcclient -U securelab/domain_user -c 'getdompwinfo' 10.0.0.1
						Enter SECURELAB\domain_user's password: 
						min_password_length: 7
						password_properties: 0x00000001
							 	 DOMAIN_PASSWORD_COMPLEX
	* <details><summary>polenum (Click to expand)</summary><p>

			polenum -d $DOMAIN -u $USER -p $PASSWORD -d $DOMAIN
	* <details><summary>CrackMapExec (Click to expand) ([crackmapexec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md))</summary><p>

			cme smb $DOMAIN_CONTROLLER -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD --pass-pol
		* <details><summary>Example Output (Click to expand)</summary><p>

				./CME smb dc01 -u 'domain_user' -p 'P@ssw0rd' -d securelab.local --pass-pol
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:securelab.local) (signing:True) (SMBv1:False)
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  [+] securelab.local\domain_user:P@ssw0rd 
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  [+] Dumping password info for domain: SECURELAB
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  Minimum password length: 7
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  Password history length: 24
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  Maximum password age: 41 days 23 hours 53 minutes 
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  Password Complexity Flags: 000001
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	 	  Domain Refuse Password Change: 0
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	 	  Domain Password Store Cleartext: 0
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	 	  Domain Password Lockout Admins: 0
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	 	  Domain Password No Clear Change: 0
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	 	  Domain Password No Anon Change: 0
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	 	  Domain Password Complex: 1
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  Minimum password age: 1 day 4 minutes 
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  Reset Account Lockout Counter: 30 minutes 
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  Locked Account Duration: 30 minutes 
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  Account Lockout Threshold: None
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  Forced Log off Time: Not Set
* Enumerate for forced authentication vulnerabilies
	* Multiple
		* <details><summary>coercer.py (Click to expand) -<br />[https://github.com/p0dalirius/Coercer](https://github.com/p0dalirius/Coercer)</summary><p>
			* Overview
				* The tool author has enumerated many potential forced authentication endpoints and produced PoCs for each case. The instances need research, but if you run out of options, it may be worth trying. -<br />[https://github.com/p0dalirius/windows-coerced-authentication-methods](https://github.com/p0dalirius/windows-coerced-authentication-methods)
			* Example 1: Analyze for multiple forced authentication options

					coercer -a -u $DOMAIN_USER -p $PASSWORD -d $DOMAIN -t $TARGET -l $LOCAL_IP
				* Example Output

						root@jack-Virtual-Machine:~# coercer -a -u $DOMAIN_USER -p $PASSWORD -d $DOMAIN -t $TARGET -l 10.0.0.100

						       ______
						      / ____/___  ___  _____________  _____
						     / /   / __ \/ _ \/ ___/ ___/ _ \/ ___/
						    / /___/ /_/ /  __/ /  / /__/  __/ /      v1.6
						    \____/\____/\___/_/   \___/\___/_/       by @podalirius_

						[dc01.microsoftdelivery.com] Analyzing available protocols on the remote machine and interesting calls ...
						   [>] Pipe '\PIPE\Fssagentrpc' is not accessible!
						   [>] Pipe '\PIPE\efsrpc' is not accessible!
						   [>] Pipe '\PIPE\lsarpc' is accessible!
						      [>] MS-EFSR (uuid=c681d488-d850-11d0-8c52-00c04fd90f7e, version=1.0) EfsRpcOpenFileRaw (opnum 0) 
						      [>] MS-EFSR (uuid=c681d488-d850-11d0-8c52-00c04fd90f7e, version=1.0) EfsRpcEncryptFileSrv (opnum 4) 
						      [>] MS-EFSR (uuid=c681d488-d850-11d0-8c52-00c04fd90f7e, version=1.0) EfsRpcDecryptFileSrv (opnum 5) 
						      [>] MS-EFSR (uuid=c681d488-d850-11d0-8c52-00c04fd90f7e, version=1.0) EfsRpcQueryUsersOnFile (opnum 6) 
						      [>] MS-EFSR (uuid=c681d488-d850-11d0-8c52-00c04fd90f7e, version=1.0) EfsRpcQueryRecoveryAgents (opnum 7) 
						      [>] MS-EFSR (uuid=c681d488-d850-11d0-8c52-00c04fd90f7e, version=1.0) EfsRpcFileKeyInfo (opnum 12) 
						   [>] Pipe '\PIPE\netdfs' is accessible!
						      [>] MS-DFSNM (uuid=4fc742e0-4a10-11cf-8273-00aa004ae673, version=3.0) NetrDfsAddStdRoot (opnum 12) 
						      [>] MS-DFSNM (uuid=4fc742e0-4a10-11cf-8273-00aa004ae673, version=3.0) NetrDfsRemoveStdRoot (opnum 13) 
						   [>] Pipe '\PIPE\spoolss' is accessible!
						      [>] MS-RPRN (uuid=12345678-1234-ABCD-EF00-0123456789AB, version=1.0) RpcRemoteFindFirstPrinterChangeNotificationEx (opnum 65) 

						[+] All done!
			* Example 2: Analyze for multiple forced authentication options and use webdav

					coercer -a -u $DOMAIN_USER -p $PASSWORD -d $DOMAIN -t $DOMAIN_CONTROLLER -wh $TARGET
				* Example Output

						root@jack-Virtual-Machine:~# coercer -a -u $DOMAIN_USER -p $PASSWORD -d $DOMAIN -t $DOMAIN_CONTROLLER -wh $TARGET 

						       ______
						      / ____/___  ___  _____________  _____
						     / /   / __ \/ _ \/ ___/ ___/ _ \/ ___/
						    / /___/ /_/ /  __/ /  / /__/  __/ /      v1.6
						    \____/\____/\___/_/   \___/\___/_/       by @podalirius_

						[dc01.microsoftdelivery.com] Analyzing available protocols on the remote machine and interesting calls ...
						   [>] Pipe '\PIPE\Fssagentrpc' is not accessible!
						   [>] Pipe '\PIPE\efsrpc' is not accessible!
						   [>] Pipe '\PIPE\lsarpc' is accessible!
						      [>] MS-EFSR (uuid=c681d488-d850-11d0-8c52-00c04fd90f7e, version=1.0) EfsRpcOpenFileRaw (opnum 0) 
						      [>] MS-EFSR (uuid=c681d488-d850-11d0-8c52-00c04fd90f7e, version=1.0) EfsRpcEncryptFileSrv (opnum 4) 
						      [>] MS-EFSR (uuid=c681d488-d850-11d0-8c52-00c04fd90f7e, version=1.0) EfsRpcDecryptFileSrv (opnum 5) 
						      [>] MS-EFSR (uuid=c681d488-d850-11d0-8c52-00c04fd90f7e, version=1.0) EfsRpcQueryUsersOnFile (opnum 6) 
						      [>] MS-EFSR (uuid=c681d488-d850-11d0-8c52-00c04fd90f7e, version=1.0) EfsRpcQueryRecoveryAgents (opnum 7) 
						      [>] MS-EFSR (uuid=c681d488-d850-11d0-8c52-00c04fd90f7e, version=1.0) EfsRpcFileKeyInfo (opnum 12) 
						   [>] Pipe '\PIPE\netdfs' is accessible!
						      [>] MS-DFSNM (uuid=4fc742e0-4a10-11cf-8273-00aa004ae673, version=3.0) NetrDfsAddStdRoot (opnum 12) 
						      [>] MS-DFSNM (uuid=4fc742e0-4a10-11cf-8273-00aa004ae673, version=3.0) NetrDfsRemoveStdRoot (opnum 13) 
						   [>] Pipe '\PIPE\spoolss' is accessible!
						      [>] MS-RPRN (uuid=12345678-1234-ABCD-EF00-0123456789AB, version=1.0) RpcRemoteFindFirstPrinterChangeNotificationEx (opnum 65) 

						[+] All done!






### Windows

* <details><summary>Internal (Click to expand)</summary><p>
	* Domain-Joined

			net accounts
			net accounts /domain
	* Non-Domain-Joined
* <details><summary>Domain Users (Click to expand)</summary><p>

		net user /domain
* <details><summary>Domain Groups (Click to expand)</summary><p>

		net group /domain
* <details><summary>Collect Specific User Info (Click to expand)</summary><p>

		net user <user> /domain
