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
# Windows Easy Wins
* Reverse shell, Remote Code Execution ([Reverse Shell Guide](Testaments_and_Books/Redvelations/Windows/004-1_Windows_Reverse_Shells.md))

1. Setup C2, Generate Shellcode
	* Splinternet ([Splinternet Tool Guide](Testaments_and_Books/Redvelations/Tools/C2/Splinternet/000_Splinternet.md))
	* Metasploit  ([Metasploit Tool Guide](Testaments_and_Books/Redvelations/Tools/C2/Metasploit/000_Metasploit.md))
1. Use shellcode in payloads
	* MSBuild [Folder, including TTP and payloads](TTP/T1127_Trusted_Developer_Utilities_Proxy_Execution/001_MSBuild/)
	* (/TTP/T1218_Sign_Binary_Proxy_Execution/T1218.md)
1. Upload the payload using `smbclient.py`, or host a local Python HTTP server and download it using `certutil.exe`
1. Execute the payload using impacket's `wmiexec.py`
