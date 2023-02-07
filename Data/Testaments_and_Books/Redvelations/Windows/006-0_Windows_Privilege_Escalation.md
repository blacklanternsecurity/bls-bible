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
# Windows Workstation - Execution and Privilege Escalation

		#@WINDOWS #@Execution #@PrivEsc

## References
* <details><summary>References (Click to expand)</summary><p>
	* swisskyrepo's [Windows Privesc Guide](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md)
	* gtworek's [Privileges Abuse Cheat Sheet](https://github.com/gtworek/Priv2Admin)

### Attacks

* <details><summary>Exploitation for Privilege Escalation ([TTP](TTP/T1068_Exploitation_for_Privilege_Escalation/T1068.md)) (Click to expand)</summary><p>

* Scheduled Task/Job `at.exe` ([TTP](TTP/T1053_Scheduled_Task-Job/002_At_Windows/T1053.002.md))
* Abuse Elevation Control Mechanism: Bypass User Account Control ([TTP](TTP/T1548_Abuse_Elevation_Control_Mechanism/002_Bypass_User_Account_Control/T1548.002.md))
* <details><summary>Access Token Manipulation (Click to expand)</summary><p>
	* Windows uses access tokens to determine the ownership of a running process.
	* Token Impersonation/Theft ([`Access Token Maniupulaton - Token Impersonation/Theft` TTP](TTP/T1134_Access_Token_Manipulation/001_Token_Impersonation-Theft/T1134.001.md))
	* Create Process with Token ([TTP](TTP/T1134_Access_Token_Manipulation/002_Create_Process_with_Token/T1134.002.md))
	* Make and Impersonate Token ([TTP](TTP/T1134_Access_Token_Manipulation/003_Make_and_Impersonate_Token/T1134.003.md))
	* Parent PID Spoofing ([TTP](TTP/T1134_Access_Token_Manipulation/004_Parent_PID_Spoofing/T1134.004.md))
	* SID/History Injection ([TTP](TTP/T1134_Access_Token_Manipulation/005_SID-History_Injection/T1134.005.md))
* <details><summary>Create or Modify System Process (Click to expand)</summary><p>
	* Create or Modify System Process: Windows Service ([TTP](TTP/T1543_Create_or_Modify_System_Process/003_Windows_Service/T1543.003.md))
* <details><summary>Domain Policy Modification (Click to expand)</summary><p>
	* Group Policy Modification ([TTP](TTP/T1484_Domain_Policy_Modification/001_Group_Policy_Modification/T1484.001.md))
	* Domain Trust Modification ([TTP](TTP/T1484_Domain_Policy_Modification/002_Domain_Trust_Modification/T1484.002.md))
* <details><summary>Event Triggered Execution (Click to expand)</summary><p>
	* Change Default File Association ([TTP](TTP/T1546_Event_Triggered_Execution/001_Change_Default_File_Association/T1546.001.md))
		* When a file is opened, the default program used to open the file (also called the file association or handler) is checked.
	* Screensaver ([TTP](TTP/T1546_Event_Triggered_Execution/002_Screensaver/T1546.002.md))
	* Windows Management Instrumentation Event Subscription ([TTP](TTP/T1546_Event_Triggered_Execution/003_Windows_Management_Instrumentation_Event_Subscription/T1546.003.md))
	* Netsh Helper DLL ([TTP](TTP/T1546_Event_Triggered_Execution/007_Netsh_Helper_DLL/T1546.007.md))
		* `netsh` can be used as a persistence proxy technique to execute a helper DLL when netsh.exe is executed.
	* Accessibility Features ([TTP](TTP/T1546_Event_Triggered_Execution/008_Accessibility_Features/T1546.008.md))
	* AppCert DLLs ([TTP](TTP/T1546_Event_Triggered_Execution/009_AppCert_DLLs/T1546.009.md))
	* AppInit DLLs ([TTP](TTP/T1546_Event_Triggered_Execution/010_AppInit_DLLs/T1546.010.md))
	* Application Shimming ([TTP](TTP/T1546_Event_Triggered_Execution/011_Application_Shimming/T1546.011.md))
	* Image File Execution Options Injection ([TTP](TTP/T1546_Event_Triggered_Execution/012_Image_File_Execution_Options_Injection/T1546.012.md))
	* PowerShell Profile ([TTP](TTP/T1546_Event_Triggered_Execution/013_PowerShell_Profile/T1546.013.md))
	* Component Object Model Hijacking ([TTP](TTP/T1546_Event_Triggered_Execution/015_Component_Object_Model_Hijacking/T1546.015.md))
* <details><summary>Hijack Execution Flow (Click to expand)</summary><p>
	* DLL Search Order Hijacking ([TTP](TTP/T1574_Hijack_Execution_Flow/001_DLL_Search_Order_Hijacking/T1574.001.md))
	* DLL Side-Loading ([TTP](TTP/T1574_Hijack_Execution_Flow/002_DLL_Side-Loading/T1574.002.md))
	* Executable Installer File Permissions Weakness ([TTP](TTP/T1574_Hijack_Execution_Flow/005_Executable_Installer_File_Permissions_Weakness/T1574.005.md))
	* Path Interception by PATH Environment Variable ([TTP](TTP/T1574_Hijack_Execution_Flow/007_Path_Interception_by_PATH_Environment_Variable/T1574.007.md))
	* Path Interception by Search Order Hijacking ([TTP](TTP/T1574_Hijack_Execution_Flow/008_Path_Interception_by_Search_Order_Hijacking/T1574.008.md))
	* Path Interception by Unquoted Path ([TTP](TTP/T1574_Hijack_Execution_Flow/009_Path_Interception_by_Unquoted_Path/T1574.009.md))
	* Services File Permissions Weakness([TTP](TTP/T1574_Hijack_Execution_Flow/010_Services_File_Permissions_Weakness/T1574.010.md))
	* Services Registry Permissions Weakness ([TTP](TTP/T1574_Hijack_Execution_Flow/011_Services_Registry_Permissions_Weakness/T1574.011.md))
	* COR_PROFILER ([TTP](TTP/T1574_Hijack_Execution_Flow/012_COR_PROFILER/T1574.012.md))
* <details><summary>Process Injection (Click to expand)</summary><p>
	* Dynamic-link Library Injection ([TTP](TTP/T1055_Process_Injection/001_Dynamic-link_Library_Injection/T1055.001.md))
	* Portable Executable Injection ([TTP](TTP/T1055_Process_Injection/002_Portable_Executable_Injection/T1055.002.md))
	* Thread Execution Hijacking ([TTP](TTP/T1055_Process_Injection/003_Thread_Execution_Hijacking/T1055.003.md))
	* Asynchronous Procedure Call ([TTP](TTP/T1055_Process_Injection/004_Asynchronous_Procedure_Call/T1055.004.md))
	* Thread Local Storage ([TTP](TTP/T1055_Process_Injection/005_Thread_Local_Storage/T1055.005.md))
	* Extra Window Memory Injection ([TTP](TTP/T1055_Process_Injection/011_Extra_Window_Memory_Injection/T1055.011.md))
	* Process Hollowing ([TTP](TTP/T1055_Process_Injection/012_Process_Hollowing/T1055.012.md))
	* Process Doppelgänging ([TTP](TTP/T1055_Process_Injection/013_Process_Doppelgänging/T1055.013.md))
* <details><summary>Credential-Oriented (Click to expand)</summary><p>
	* <details><summary>LSASS Memory Dump (e.g. Procdump, Mimikatz) (Click to expand) ([TTP](TTP/T1003_OS_Credential_Dumping/001_LSASS_Memory/T1003.001.md))</summary><p>
		* LPE
			* CVE-2021-40449: Callback Hell
				* References
					* [https://www.kaspersky.com/blog/mysterysnail-cve-2021-40449/42448/](https://www.kaspersky.com/blog/mysterysnail-cve-2021-40449/42448/)
					* [https://github.com/ly4k/CallbackHell](https://github.com/ly4k/CallbackHell)
				* CVE-2021-40449 is a use-after-free in Win32k that allows for local privilege escalation
		* Word Exploits
			* cve-2021-40444 -<br />[https://twitter.com/0x09AL/status/1436072416791437312](https://twitter.com/0x09AL/status/1436072416791437312)
		* Unhooking
			* "Full DLL Unhooking"
				* [https://www.ired.team/offensive-security/defense-evasion/how-to-unhook-a-dll-using-c++](https://www.ired.team/offensive-security/defense-evasion/how-to-unhook-a-dll-using-c++)
			* PEzor

					PEzor -unhook -sgn shellcode.bin

Abuse service, stop/start


* `AlwaysInstallElevated` Enabled
		* <details><summary>Metasploit payloads (Click to expand)</summary><p>
			* No uac format

					msfvenom -p windows/adduser USER=rottenadmin PASS=P@ssword123! -f msi-nouac -o alwe.msi
			* Using the msiexec the uac wont be prompted

					msfvenom -p windows/adduser USER=rottenadmin PASS=P@ssword123! -f msi -o alwe.msi
			* If you have a meterpreter session you can automate this technique using the module `exploit/windows/local/always_install_elevated`
		* <details><summary>PowerUP (Click to expand)</summary><p>
			* Use the Write-UserAddMSI command from power-up to create inside the current directory a Windows MSI binary to escalate privileges. This script writes out a precompiled MSI installer that prompts for a user/group addition (so you will need GIU access):
		* <details><summary>Write-UserAddMSI (Click to expand)</summary><p>
			* Just execute the created binary to escalate privileges.
		* <details><summary>MSI Wrapper (Click to expand)</summary><p>
			* References
				* HackTricks: MSI Wrapper -<br />[https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/msi-wrapper](https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/msi-wrapper)
		* <details><summary>Create MSI with WIX (Click to expand)</summary><p>
			* References
				HackTricks: Create MSI with wix -<br />[https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/create-msi-with-wix](https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/create-msi-with-wix)
		* <details><summary>MSI Installation (Click to expand)</summary><p>
			* To execute the installation of the malicious .msi file in background:

					msiexec /quiet /qn /i C:\Users\Steve.INFERNO\Downloads\alwe.msi
			* To exploit this vulnerability you can use: `exploit/windows/local/always_install_elevated`
* <details><summary>From Administrator Medium to High Integrity Level / UAC Bypass (Click to expand)</summary><p>
	* <details><summary>References (Click to expand)</summary><p>
		* HackTricks: Integrity Levels -<br />[https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/integrity-levels](https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/integrity-levels)
		* HackTricks: What is UAC, How to Bypass -<br />[https://book.hacktricks.xyz/windows/authentication-credentials-uac-and-efs#uac](https://book.hacktricks.xyz/windows/authentication-credentials-uac-and-efs#uac)
* <details><summary>From High Integrity to System (Click to expand)</summary><p>
	* New service
		* If you are already running on a High Integrity process, the pass to SYSTEM can be easy just creating and executing a new service:

				sc create newservicename binPath= "C:\windows\system32\notepad.exe"
				sc start newservicename
	* `AlwaysInstallElevated`
		* References
			* HackTricks: AlwaysInstallElevated -<br />[https://book.hacktricks.xyz/windows/windows-local-privilege-escalation#alwaysinstallelevated](https://book.hacktricks.xyz/windows/windows-local-privilege-escalation#alwaysinstallelevated)
		* Overview
			* From a High Integrity process you could try to enable the AlwaysInstallElevated registry entries and install a reverse shell using a `.msi` wrapper. 
	* High + `SeImpersonate` privilege to System
		* References
			* HackTricks: SeImpersonate from High To System, including code -<br />[https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/seimpersonate-from-high-to-system](https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/seimpersonate-from-high-to-system)
	* From SeDebug + SeImpersonate to Full Token privileges
		* References
			* HackTricks: SeDebug + SeImpersonate copy token -<br />[https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/sedebug-+-seimpersonate-copy-token](https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/sedebug-+-seimpersonate-copy-token)
		* Overview
			* If you have those token privileges (probably you will find this in an already High Integrity process), you will be able to open almost any process (not protected processes) with the SeDebug privilege, copy the token of the process, and create an arbitrary process with that token.
			* Using this technique is usually selected any process running as SYSTEM with all the token privileges (yes, you can find SYSTEM processes without all the token privileges).
	* Named Pipes
		* References
			* [https://book.hacktricks.xyz/windows/windows-local-privilege-escalation#named-pipe-client-impersonation](https://book.hacktricks.xyz/windows/windows-local-privilege-escalation#named-pipe-client-impersonation)
		* Overview
			* This technique is used by meterpreter to escalate in getsystem. The technique consists on creating a pipe and then create/abuse a service to write on that pipe. Then, the server that created the pipe using the SeImpersonate privilege will be able to impersonate the token of the pipe client (the service) obtaining SYSTEM privileges.
	* Dll Hijacking
		* References
			* HackTricks: DLL Hijacking -<br />[https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/dll-hijacking](https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/dll-hijacking)
		* Overview
			* If you manages to hijack a dll being loaded by a process running as SYSTEM you will be able to execute arbitrary code with those permissions. Therefore Dll Hijacking is also useful to this kind of privilege escalation, and, moreover, if far more easy to achieve from a high integrity process as it will have write permissions on the folders used to load dlls.
	* From Administrator or Network Service to System
		* References
			* sailay1996 GitHub: RpcSsImpersonator -<br />[https://github.com/sailay1996/RpcSsImpersonator](https://github.com/sailay1996/RpcSsImpersonator)