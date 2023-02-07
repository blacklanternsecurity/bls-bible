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
# Remote Server Administration Tools

## Tags

- <details><summary>(Click to expand)</summary><p>
	- `#@windows #@activedirectory #@active #@directory #@active_directory #@gpo #@blueteam #@blue #@tool #@rsat #@rsop #@policy`

## References

- [https://www.microsoft.com/en-us/download/details.aspx?id=45520](https://www.microsoft.com/en-us/download/details.aspx?id=45520)

## Background

Remote Server Administration Tools for Windows 10 includes Server Manager, Microsoft Management Console (MMC) snap-ins, consoles, Windows PowerShell cmdlets and providers, and command-line tools for managing roles and features that run on Windows Server.

## Commands

It is recommended to pull GPO reports by utilizing something like [`evil-winrm`](/Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/Evil-WinRM.md) to authenticate to a Domain Controller. This will avoid alerts and give you access to a PowerShell like session.

1. <details><summary>Pull GPO Report (PowerShell)</summary><p>


		Get-GPOReport -All -Domain <target-domain> -ReportType HTML -Path <path-to-save-to>