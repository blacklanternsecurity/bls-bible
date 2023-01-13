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
# Evil-WinRM

## Tags

* <details><summary>(Click to expand)</summary><p>
	* `#@tool #@activedirectory #@active #@directory #@active_directory #@windows #@winrm`

## References

* Download - [https://github.com/Hackplayers/evil-winrm](https://github.com/Hackplayers/evil-winrm)

## Background

WinRM (Windows Remote Management) is the Microsoft implementation of WS-Management Protocol. A standard SOAP based protocol that allows hardware and operating systems from different vendors to interoperate. Microsoft included it in their Operating Systems in order to make life easier to system administrators.

This program can be used on any Microsoft Windows Servers with this feature enabled (usually at port 5985), of course only if you have credentials and permissions to use it. So we can say that it could be used in a post-exploitation hacking/pentesting phase. The purpose of this program is to provide nice and easy-to-use features for hacking. It can be used with legitimate purposes by system administrators as well but the most of its features are focused on hacking/pentesting stuff.

It is based mainly in the WinRM Ruby library which changed its way to work since its version 2.0. Now instead of using WinRM protocol, it is using PSRP (Powershell Remoting Protocol) for initializing runspace pools as well as creating and processing pipelines.

## Commands

1. <details><summary>Connect with user/pass</summary><p>
	1. You may omit `-p <password>` to avoid dropping the password into the bash history
	1. You will then be prompted for it	
			
			evil-winrm -i <target> -u <user> -p <password>
1. <details><summary>Connect with user/hash</summary><p>
				
		evil-winrm -i <target> -u <user> -H <hash>
1. <details><summary>In Evil-WinRM Shell Commands</summary><p>
	- `menu`
		- Displays the available `PowerShell` modules and other commands relevant to `evil-winrm`
	- `download`
		- Downloads the remote file to your working directory
		- Relative paths are not allowed to use on download
		- Use filenames on current directory or absolute path
	- `upload`
		- Uploads the local file to the remote destination
		- Relative paths are not allowed to use on upload
		- Use filenames on current directory or absolute path