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
# Windows COM Objects
### Tags
		#@CLSID #@Windows #@Defense #@Evasion

### References
* <details><summary>References (Click to expand)</summary><p>
	* Complete List of Windows 10 CLSID Key (GUID) Shortcuts -<br />[https://www.tenforums.com/tutorials/3123-clsid-key-guid-shortcuts-list-windows-10-a.html](https://www.tenforums.com/tutorials/3123-clsid-key-guid-shortcuts-list-windows-10-a.html)
	* Mandiant: Hunting COM Objects -<br />[https://www.mandiant.com/resources/hunting-com-objects](https://www.mandiant.com/resources/hunting-com-objects)
	* Mirosoft Documentation: OLE-COM Object Viewer -<br />[https://docs.microsoft.com/en-us/windows/win32/com/ole-com-object-viewer](https://docs.microsoft.com/en-us/windows/win32/com/ole-com-object-viewer)
	* [http://ohpe.it/juicy-potato/CLSID/](http://ohpe.it/juicy-potato/CLSID/)
	* [https://labs.sentinelone.com/relaying-potatoes-dce-rpc-ntlm-relay-eop/](https://labs.sentinelone.com/relaying-potatoes-dce-rpc-ntlm-relay-eop/)
	* [https://www.tiraniddo.dev/2021/04/standard-activating-yourself-to.html](https://www.tiraniddo.dev/2021/04/standard-activating-yourself-to.html)

### TTP Links

* Windows COM Objects ([`Inter-Process Communication - Component Object Model` TTP](TTP/T1559_Inter-Process_Communication/001_Component_Object_Model/T1559.001.md))


### CLSID List


### Process to Test CLSID Effectiveness

1. Collect CLSIDs on a local test system
	* Powershell

			New-PSDrive -PSProvider registry -Root HKEY_CLASSES_ROOT -Name HKCR Get-ChildItem -Path HKCR:\CLSID -Name | Select -Skip 1 > clsids.txt
1. Collect properties of CLSIDs as an unprivileged user
	* PowerShell

			$Position  = 1
			$Filename = "win10-clsid-members.txt"
			$inputFilename = "clsids.txt"
			ForEach($CLSID in Get-Content $inputFilename) {
			      Write-Output "$($Position) - $($CLSID)"
			      Write-Output "------------------------" | Out-File $Filename -Append
			      Write-Output $($CLSID) | Out-File $Filename -Append
			      $handle = [activator]::CreateInstance([type]::GetTypeFromCLSID($CLSID))
			      $handle | Get-Member | Out-File $Filename -Append
			      $Position += 1
			}

