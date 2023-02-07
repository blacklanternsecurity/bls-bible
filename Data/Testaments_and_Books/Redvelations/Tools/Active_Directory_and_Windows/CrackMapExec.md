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
# CrackMapExec

## Tags

- <details><summary>(Click to expand)</summary><p>
	- `#@windows #@smb #@winrm #@crackmapexec #@tool #@enumeration #@password`

## References
* [MITRE](https://attack.mitre.org/software/S0488/)
* Download - [https://github.com/byt3bl33d3r/CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec)
* Wiki - [https://github.com/byt3bl33d3r/CrackMapExec/wiki](https://github.com/byt3bl33d3r/CrackMapExec/wiki)

## Background

Crack Map Exec (cme) is a tool that is used to verify and get access to a Windows Domain. This can be used in conjuction with Responder/Impacker/Metasploit attack where you get a NTLM hash or a Password. It can quickly map out the Windows Network using Null Sessions, along with checking where a user has admin on a machine. A great tool to finding ways to escalate using Bloodhound and CME.
* BE CAREFUL WHEN USING CRACKMAPEXEC. IT CAN QUICKLY LOCK OUT ACCOUNTS IF INCORRECT CREDENTIALS ARE SUPPLIED.

## Commands

1. <details><summary>Enumerate Hosts (Null Session Connection) ([TTP](TTP/T1087_Account_Discovery/002_Domain_Account/T1087.002.md))</summary><p>
	1. SMB
 
			crackmapexec smb <targets>
	1. WinRM

			crackmapexec winrm <targets>
1. <details><summary>Authenticate</summary><p>
	1. <details><summary>Using Credentials</summary><p>
		1. SMB

				crackmapexec smb <ip_address>/24 -u <username> -p '<password>' -t 500
		1. WinRM
				
				crackmapexec winrm <ip_address>/24 -u <username> -p '<password>' -t 500
	1. <details><summary>Using Hashes ([TTP](TTP/T1550_Use_Alternate_Authentication_Material/002_Pass_the_Hash/T1550.002.md) - Defense Evasion), ([TTP](TTP/T1550_Use_Alternate_Authentication_Material/002_Pass_the_Hash/T1550.002.md) - Lateral Movement)</summary><p>
		1. SMB

				crackmapexec smb -u <user> -H <hash>:<hash> <target>
		1. WinRM

				crackmapexec winrm -u <user> -H <hash>:<hash> <target> 
1. Identifies shares ([TTP](TTP/T1135_Network_Share_Discovery/T1135.md))
1. Spidering looking for pattern ([TTP](TTP/T1083_File_and_Directory_Discovery/T1083.md))
1. <details><summary>Checking for host-based security controls</summary><p>
	1. Windows

			cme smb <host_list> -u <username> -p <password> -x 'sc query | findstr "Symantec Altiris Snare BES FireAMP"'
	1. Linux

			cme smb <host_list> -u <username> -p <password> -x 'ps -ef | grep "Symantec Altiris Snare BES FireAMP"'

## Additional Tool Commands

- `cmedb`
- `hosts`
- `creds`