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
# File Share
## Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@file #@share #@files #@shares #@smb #@ftp

Tools

		#@manspider

</p></details>

## References

## Overview
## Enumeration
### From a Linux Machine
* SYSVOL Review ([`Credentials from Password Stores` TTP](TTP/T1555_Credentials_from_Password_Stores/T1555.md))
	* References
		* [https://twitter.com/Oddvarmoe/status/1428102443922075652](https://twitter.com/Oddvarmoe/status/1428102443922075652)
		* [https://twitter.com/Oddvarmoe/status/1428102445557817348](https://twitter.com/Oddvarmoe/status/1428102445557817348)
		* [https://podalirius.net/en/articles/exploiting-windows-group-policy-preferences/](https://podalirius.net/en/articles/exploiting-windows-group-policy-preferences/)
	* Overview
		* Group Policy Preferences (GPP) File
			* crackmapexec
		* The preferences files
			* `scripts.ini`
			* `psscripts.ini`
			* Reveals paths, configurations, hidden file servers hosting scripts 
		* Stored Scripts
			* Filetypes to look out for: `.bat`, `.ps1`, `.vbs`
			* `.cmtx` - can contain GPO admins comments
* Services
	* Microsoft Active Directory or Windows Specific
		* SMB ([SMB Guide](Testaments_and_Books/Redvelations/Active_Directory/005-3_SMB.md))
	* General Network File Share Services
		* FTP ([FTP Guide](Testaments_and_Books/Redvelations/Network/005-1_FTP.md))

### From a Windows Machine
#### Locally

#### Remote
