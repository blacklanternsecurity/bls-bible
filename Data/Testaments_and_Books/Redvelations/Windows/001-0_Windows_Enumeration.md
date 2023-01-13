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
# Windows Enumeration ([`Gather Victim Host Information` TTP](TTP/T1592_Gather_Victim_Host_Information/T1592.md))
### References
* <details><summary>References (Click to expand)</summary><p>

### External Enumeration
#### From Linux
* Scanning or Automated Tools ([`Active Scanning - Vulnerability Scanning` TTP](TTP/T1595_Active_Scanning/002_Vulnerability_Scanning/T1595.002.md))
* User Account Permissions
	* <details><summary>Local Administrator Status (Click to expand)</summary><p>
		* SMB
		* crackmapexec ([crackmapexec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md))

				crackmapexec smb <target> -u '<username>' -p '<password'
			* `pwned` indicates the user has local adminstrator access through this method.
		* WinRM
			* crackmapexec ([crackmapexec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md))

					crackmapexec winrm <target>
				* `pwned` indicates the user has local adminstrator access through this method.
	* AD User Privileges ([AD Access Control Abuse Guide](Testaments_and_Books/Redvelations/Active_Directory/004-0_AD_Access_Control_Abuse.md))
* SMB
	* <details><summary>Domain name (Click to expand)</summary><p>
		* crackmapexec ([crackmapexec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md))

				crackmapexec smb <target>
	* <details><summary>Shares (Click to expand)</summary><p>
		* <details><summary>Null Authentication (Click to expand)</summary><p>
			* crackmapexec ([crackmapexec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md))

					crackmapexec smb <target> -u '' -p '' --shares
					crackmapexec smb <target> --shares
				* Also collects domain name information
			* smbmap

					smbmap -H <target> -u '' -p ''
		* <details><summary>With Credentials (Click to expand)</summary><p>
			* crackmapexec ([crackmapexec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md))

					crackmapexec smb <target> -u '<username>' -p '<password>' --shares
* RPC ([RPC Service Guide](Testaments_and_Books/Redvelations/Apps_and_Services/RPC.md))
	* <details><summary>rpcclient ([rpcclient tool guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/rpcclient.md)) (Click to expand)</summary><p>

			rpcclient <IP> -U '' -P ''
		* Launches interactive command line, unless you select the flag for submitting a single command
		* Example commands for enumeration

				enumdomusers
				enumdomgroups
				enumdomains

#### From Windows
##### Remote Windows System
* Scanning or Automated Tools ([`Active Scanning - Vulnerability Scanning` TTP](TTP/T1595_Active_Scanning/002_Vulnerability_Scanning/T1595.002.md))

##### Local Enumeration
* [Windows Local Enumeration Guide](Testaments_and_Books/Redvelations/Windows/001-1_Windows_Local_Enumeration.md)


([`Gather Victim Host Information - Firmware` TTP](TTP/T1592_Gather_Victim_Host_Information/003_Firmware/T1592.003.md))
([`Gather Victim Host Information - Hardware` TTP](TTP/T1592_Gather_Victim_Host_Information/001_Hardware/T1592.001.md))
([`Gather Victim Host Information - Software` TTP](TTP/T1592_Gather_Victim_Host_Information/002_Software/T1592.002.md))
([`Gather Victim Host Information` TTP](TTP/T1592_Gather_Victim_Host_Information/T1592.md))