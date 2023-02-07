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
# Unhooking Background
### Assembly Code, Machine Code

* Tools that first produce assembler code, then translate to Machine Code
	* gcc
* Assembler instructions have 1:1 mapping with machine code

# Windows OS Architecture
* Basic functions are imported from existing libraries
	* Examples
		* `printf()` is imported from the library `stdio.h` in `C`. Windows developers use an API which can be imported to a program. The Win32 API is well-documented and consists of several library files (DLLs, located in `C:\Windows\system32`) like `kernel32.dll`, `User32.dll`, etc.
* References
	* [https://docs.microsoft.com/en-us/windows/win32/api/](https://docs.microsoft.com/en-us/windows/win32/api/)

# Windows User-mode/Kernel Mode

* User-mode
	* All applications
	* Cannot access or manipulate memory sections in Kernel-mode
	* AV/EDR systemscan only monitor application behavior in User-mode
		* Kernel Patch Protection (https://en.wikipedia.org/wiki/Kernel_Patch_Protection)
	* The last instance in User-mode is the Windows API functions from NTDLL.dll.
		* If any function from `NTDLL.dll` is called, the CPU switches to Kernel-mode next, which cannot be monitored by AV/EDR vendors anymore
* Kernel-mode
	* kernel
	* device drivers

## NTDLL
* Individual functions are called Syscalls

# Using the Windows API for Offsec
* Windows API functions can be useful for writing shellcode
	* In this case, the function `WriteProcessMemory` can be imported from `kernel32.dll`.
		* Example
			* [https://github.com/S3cur3Th1sSh1t/Creds/blob/master/Csharp/CreateRemoteThread.cs](https://github.com/S3cur3Th1sSh1t/Creds/blob/master/Csharp/CreateRemoteThread.cs)
* PE-Loaders
	* C-based tools (e.g., mimikatz) must be loaded in memory pre-PE-Loaders to remain in memory for as long as possible
	* Tools
		* PowerShell
			* [Invoke-ReflectivePEInjection](https://github.com/S3cur3Th1sSh1t/Creds/blob/master/PowershellScripts/Invoke-ReflectivePEInjection.ps1)
			* C# [PE-Loader](https://github.com/S3cur3Th1sSh1t/Creds/blob/master/Csharp/PEloader.cs)
	* Make heavy use of `kernel32.dll`'s Windows API functions like
		* `CreateRemoteThread`
		* `GetProcAddress`
		* `CreateThread`
* Win32 API files
	* Example files used to import functions
		* `kernel32.dll`
		* `User32.dll`
	* Not 1:1 mapped with Machine Code
		* Instead, these user-land functions are mapped to `NTDLL.dll`
			* The native API that interacts with the kernel
	* Example
		* `kernel32.dll`'s `WriteProcessMemory` resolves to `NTDLL.dll`'s' `NtProtectVirtualMemory > NtWriteVirtualMemory > NtProtectVirtualMemory`.
			* Syscall Order/Process
				1. `NtProtectVirtualMemory`
					* Unsets protection for the process, making it writable.
				1. `NtWriteVirtualMemory`
					* Writes the bytes.
				1. `NtProtectVirtualMemory`
					* Restores protection to the process’ memory.
* `NTDLL.dll` functions are the last step that can be monitored before kernel-mode.
	* AV/EDRs focus here
		* Vendors inject a custom DLL-file into every new process.
			* You can find the DLL files using something like `procexp64.exe` from SysInternals. Use the Lower Pane option in the View menu.
* If a program loads a function like `NtWriteVirtualMemory` from `kernel32.dll`, a copy of `kernel32.dll` is placed into memory.
	* Vendors typically manipulate the in-memory copy and add their own code into specific functions like `NtWriteVirtualMemory`. 
		* When the function is called by the program, the AV/EDR’s additional code is executed first, which analyzes the bytes. By using this technique, it is possible to see the cleartext shellcode bytes.
		* AV/EDR’s technique of embedding their own code in memory by patching API functions is called Userland Hooking.

Bypass Methods
* Unhooking
* Re-patch DLL in memory
* Patch AV/EDR’s DLL
* Avoid loading Win32 API, using direct Syscalls instead

* If your implant or tool loads some functions from `kernel32.dll` or `NTDLL.dll`, a copy of the library file is loaded into memory. The AV/EDR vendors typically patch some functions from the in-memory copy and place a `JMP` assembler instruction at the beginning of the bode to redirect the Windows API function to some inspecting code.
	* Therefore, before calling the real Windows API function code, an analysis is done. If this analysis results in no suspicious/malicious behavior and returns a clean result, the original Windows API function is called afterwards. If something malicious is found, the API call is blocked, or the process is killed.

1. AV/EDR Inserts Hook at the the beginning of specific files
	* Hook: `JMP` instruction at the beginning; redirects to EDR inspection module
		* "detour/trampoline"
	* 
1. file.exe begins
1. Code Executes
1. Process Starts
	* Vendors inject a custom DLL-file into every new process.
		* You can find the DLL files using something like `procexp64.exe` from SysInternals. Use the Lower Pane option in the View menu.
1. API Call Begins
	* Examples
		* `CreateFile`
		* `ReadFile`
		* `OpenProcess`
1. AV/EDR intercepts API call via hook
	* User-land Hooks
		* AV/EDR hijack/modifies function definitions (APIs) found in Windows DLLs
			* Examples
				* `kernel32`/`kernelbase`
				* `ntdll`
					* Last step that can be monitored before kernel-mode.
				* If a program (or tool) loads functions from `kernel32.dll` or `NTDLL.dll`, a copy of the library file is loaded into memory
		* Bypass Methods
			* Unhooking
			* Re-patch DLL in memory
			* Patch AV/EDR’s DLL
			* Avoid loading Win32 API, using direct Syscalls instead
1. AV/EDR processes action and attempts to filter malicious behavior
	* On Detection, process fails
	* `NTDLL.dll` 
1. On bypass, proceed to kernel-land