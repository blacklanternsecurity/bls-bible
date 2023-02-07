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
# Hooking
### References

### Background

# AV Hooking

### Process Context
1. Program Starts
1. AV/EDR Inserts Hook
	* Process
		1. Insert `JMP` instruction at the beginning
1. API Call Made
	* Examples
		* `CreateFile`
		* `ReadFile`
		* `OpenProcess`
	* Process
		1. API Call sent by process
1. AV/EDR intercepts API call via hook
	* Overview
	* Process
		1. 
	* User-land Hooks
		* AV/EDR hijack/modifies function definitions (APIs) found in Windows DLLs
			* Examples
				* `kernel32`/`kernelbase`
				* `ntdll`
				1. Program execution flow redirects to EDR inspection module
1. AV/EDR processes action and attempts to filter malicious behavior
	* On Detection
		1. Process fails
	* On Bypass
		1. .

### Tools

* Alternative Unhooking
	* Perun's Fart -<br />[https://github.com/plackyhacker/Peruns-Fart](https://github.com/plackyhacker/Peruns-Fart)
		* A C# application that unhooks AV and EDR to help run malicious code undetected. This differs to this classic unhooking technique because it does not need to load the 'clean' copy of ntdll.dll from disk, it copies it from another process before AV/EDR can hook it.
* Parallel Syscalls (Load `ntdll.dll` from disk into memory for avoiding hooks)
	* mdsec original -<br />[https://github.com/mdsecactivebreach/ParallelSyscalls](https://github.com/mdsecactivebreach/ParallelSyscalls)
		* References
			* mdsec blog: "EDR Parallel-asis through Analysis" -<br />[https://www.mdsec.co.uk/2022/01/edr-parallel-asis-through-analysis/](https://www.mdsec.co.uk/2022/01/edr-parallel-asis-through-analysis/)
		* Overview
			* .
	* C#
		* ParalellSysCalls cube0x0 -<br />[https://github.com/cube0x0/ParallelSyscalls](https://github.com/cube0x0/ParallelSyscalls)
			* References
				* [https://twitter.com/cube0x0/status/1480167424695615491?t=lj-IA1TLH-l3pikTTNwMhA](https://twitter.com/cube0x0/status/1480167424695615491?t=lj-IA1TLH-l3pikTTNwMhA)

