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
# Windows Execution
### From a Linux Machine
* <details><summary>Notes (Click to expand)</summary><p>
	* <details><summary>Remote UAC (Click to expand)</summary><p>
		* If remote execution fails as local admin (e.g., rpc access denied via impacket), you may be blocked by Remote UAC.
		* In order to allow for connections, typically to a non-domain joined system, you need to enable this registry key to allow remote connections:

				HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\

				New Key:

				LocalAccountTokenFilterPolicy DWORD
				Value: 1
* WinRM
	* <details><summary>References (Click to expand)</summary><p>
		* Metasploit -<br />[https://rapid7.com/blog/post/2008/abusing-windows-remote-management-winrm-with-metasploit/](https://rapid7.com/blog/post/2008/abusing-windows-remote-management-winrm-with-metasploit/)
	* <details><summary>evilwinrm (Click to expand) -<br />[https://github.com/Hackplayers/evil-winrm](https://github.com/Hackplayers/evil-winrm)</summary><p>
		* `gem install evil-winrm`
		* OpSec: Submit password after command rather than with the prompt.

				evil-winrm  -i 192.168.1.100 -u Administrator -s '/home/foo/ps1_scripts/' -e '/home/foo/exe_files/'
	* <details><summary>CrackMapExec ([CrackMapExec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md)) (Click to expand)</summary><p>
	* <details><summary>WSMan.Automation COM object (Click to expand)</summary><p>
		* WSMan-WinRM -<br />[https://github.com/bohops/WSMan-WinRM](https://github.com/bohops/WSMan-WinRM)
	* <details><summary>PyWinRM (Click to expand) -<br />[https://pypi.org/project/pywinrm/0.2.2/](https://pypi.org/project/pywinrm/0.2.2/)<br />[https://github.com/diyan/pywinrm](https://github.com/diyan/pywinrm)</summary><p>
* <details><summary>SMB (Server Message Block) (Click to expand)</summary><p>
	* <details><summary>impacket's smbexec.py (Click to expand) ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md))</summary><p>
		* Notes
			* .
		* Process
			* Execute the command according to the credentials you have. 
				* NTLM Hash
				
					python examples/smbexec.py domain.local/username@<target_system_name_or_IP> -hashes :<hash>
	* <details><summary>CrackMapExec (Click to expand)</summary><p>
	* <details><summary>impacket's psexec.py (Click to expand) ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md))</summary><p>
		* Notes
			* Not OpSec friendly
		* Process
			* Execute the command according to the credentials you have. 
				* NTLM Hash
				
						python examples/psexec.py domain.local/username@<target_system_name_or_IP> -hashes :<hash>
* <details><summary>WMI (Windows Management Instrumenetation) (Click to expand) ([`Windows Management Instrumentation` TTP](TTP/T1047_Windows_Management_Instrumentation/T1047.md))</summary><p>
	* <details><summary>impacket: wmiexec.py (Click to expand) ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md))</summary><p>
		* Requirements
			* Port 135 open
	* <details><summary>Alternative wmiexec: wmiexec-RegOut [https://github.com/XiaoliChan/wmiexec-RegOut](https://github.com/XiaoliChan/wmiexec-RegOut) (Click to expand)</summary><p>
* <details><summary>RDP (Click to expand)</summary><p>
	* <details><summary>GUI (Click to expand)</summary><p>
		* Remina
	* <details><summary>Non-GUI (Click to expand)</summary><p>
		* skelsec's asynchronous RDP CLI tool
* <details><summary>WinRM (Click to expand)</summary><p>
	
### Windows
#### Remote Windows
* <details><summary>SMB (Click to expand)</summary><p>
* <details><summary>HTTP (Click to expand)</summary><p>
* <details><summary>WinRM (Click to expand)</summary><p>
	* CSharpWinRM -<br />[https://github.com/mez-0/CSharpWinRM](https://github.com/mez-0/CSharpWinRM)
	* winrs.exe -<br />[https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/winrs](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/winrs)
	* winrm.vbs -<br />[https://docs.microsoft.com/en-us/windows/win32/winrm/scripting-in-windows-remote-management](https://docs.microsoft.com/en-us/windows/win32/winrm/scripting-in-windows-remote-management)
	* winrmdll -<br />[https://github.com/mez-0/winrmdll](https://github.com/mez-0/winrmdll)
* <details><summary>RDP (Click to expand)</summary><p>
		* .

#### Local Windows
* Windows Command Shell ([Redvelations Command Shell Guide](Testaments_and_Books/Redvelations/Windows/002-1_Command_Shell_Execution.md), [TTP](TTP/T1059_Command_and_Scripting_Interpreter/003_Windows_Command_Shell/T1059.003.md))
* Powershell ([Redvelations PowerShell Guide](Testaments_and_Books/Redvelations/Windows/002-2_PowerShell_Execution.md), [TTP](TTP/T1059_Command_and_Scripting_Interpreter/001_PowerShell/T1059.001.md))
* Visual Basic ([VBA/VBS Execution Guide](Testaments_and_Books/Redvelations/Windows/002-3_VBA-VBS_Execution.md), [TTP](TTP/T1059_Command_and_Scripting_Interpreter/005_Visual_Basic/T1059.005.md))
* Native API ([TTP](TTP/T1106_Native_API/T1106.md))

* Event Triggered Execution ([`Event Triggered Execution` TTP](TTP/T1546_Event_Triggered_Execution/T1546.md))
	* Change Default File Association ([`Event Triggered Execution - Change Default File Association` TTP](TTP/T1546_Event_Triggered_Execution/001_Change_Default_File_Association/T1546.001.md))
	* Screensaver ([`Event Triggered Execution - Screensaver` TTP](TTP/T1546_Event_Triggered_Execution/002_Screensaver/T1546.002.md))
	* WMI Event Subscription ([`Event Triggered Execution - Windows Management Instrumentation Event Subscription` TTP](TTP/T1546_Event_Triggered_Execution/003_Windows_Management_Instrumentation_Event_Subscription/T1546.003.md))
	* ([`Event Triggered Execution - Trap` TTP](TTP/T1546_Event_Triggered_Execution/005_Trap/T1546.005.md))
	* ([`Event Triggered Execution - LC LOAD DYLIB Addition` TTP](TTP/T1546_Event_Triggered_Execution/006_LC_LOAD_DYLIB_Addition/T1546.006.md))
	* ([`Event Triggered Execution - Netsh Helper DLL` TTP](TTP/T1546_Event_Triggered_Execution/007_Netsh_Helper_DLL/T1546.007.md))
	* ([`Event Triggered Execution - Accessibility Features` TTP](TTP/T1546_Event_Triggered_Execution/008_Accessibility_Features/T1546.008.md))
	* ([`Event Triggered Execution - AppCert DLLs` TTP](TTP/T1546_Event_Triggered_Execution/009_AppCert_DLLs/T1546.009.md))
	* ([`Event Triggered Execution - AppInit DLLs` TTP](TTP/T1546_Event_Triggered_Execution/010_AppInit_DLLs/T1546.010.md))
	* ([`Event Triggered Execution - Application Shimming` TTP](TTP/T1546_Event_Triggered_Execution/011_Application_Shimming/T1546.011.md))
	* ([`Event Triggered Execution - Image File Execution Options Injection` TTP](TTP/T1546_Event_Triggered_Execution/012_Image_File_Execution_Options_Injection/T1546.012.md))
	* ([`Event Triggered Execution - PowerShell Profile` TTP](TTP/T1546_Event_Triggered_Execution/013_PowerShell_Profile/T1546.013.md))
	* ([`Event Triggered Execution - Emond` TTP](TTP/T1546_Event_Triggered_Execution/014_Emond/T1546.014.md))
	* ([`Event Triggered Execution - Component Object Model Hijacking` TTP](TTP/T1546_Event_Triggered_Execution/015_Component_Object_Model_Hijacking/T1546.015.md))
* Remote Service Session Hijacking ([`Remote Service Session Hijacking` TTP](TTP/T1563_Remote_Service_Session_Hijacking/T1563.md))
	* RDP Hijacking ([`Remote Service Session Hijacking - RDP Hijacking` TTP](TTP/T1563_Remote_Service_Session_Hijacking/002_RDP_Hijacking/T1563.002.md))
	* SSH Hijacking ([`Remote Service Session Hijacking - SSH Hijacking` TTP](TTP/T1563_Remote_Service_Session_Hijacking/001_SSH_Hijacking/T1563.001.md))
