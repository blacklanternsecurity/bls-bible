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
# Windows Payload Obfuscation
### References

### Process

1. Generate a payload ([Payload Generation Guide](Testaments_and_Books/Redvelations/Windows/004-2_Windows_Payload_Generation.md))
1. <details><summary>Execution (Click to expand)</summary><p>Apply obfuscation techniques
	* Notes
		* Splinternet payloads
	* Options
		* Tools
			* nimcognito ([Nimcognito Tool Guide](Testaments_and_Books/Redvelations/Tools/Malware/nimcognito.md))
				* Accepts raw shellcode
					* UPX packing to reduce size (EXE)
					* Self-deleting (EXE)
					* Rundll32-compatible (DLL)
				* Notes
					* nimcognito is a command-line tool that automates implant generation based on byt3bl33d3r's OffensiveNim repository and ajpc500's NimlineWhispers. Using user-supplied shellcode, a 64-bit executable/DLL shellcode loader is created. The loader starts a given process and injects shellcode into memory while bypassing userland AV hooking.
		* Manual Obfuscation
			* base64 encoding