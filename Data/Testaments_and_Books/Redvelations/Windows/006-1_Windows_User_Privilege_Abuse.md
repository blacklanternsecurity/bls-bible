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
# Windows Privilege Abuse
### References
* [https://github.com/gtworek/Priv2Admin](https://github.com/gtworek/Priv2Admin)

### Privileges
* Privilege
	* Impact
	* Tool
	* Execution path
	* Remarks

* <details><summary> `SeAssignPrimaryTokenPrivilege` (Click to expand)</summary><p>
	* RogueWinRM -<br />[https://github.com/antonioCoco/RogueWinRM](https://github.com/antonioCoco/RogueWinRM)
		* References
			* [https://twitter.com/splinter_code/status/1479118236922748932](https://twitter.com/splinter_code/status/1479118236922748932)
		* Overview
			* Escalate to SYSTEM, even from a Medium IL process
		* Process
			* .
* <details><summary> `SeImpersonate`, `SeAssignPrimaryToken` (Click to expand)</summary><p>
	* `SeAssignPrimaryToken`
		* Admin
		* 3rd party tool
		* "It would allow a user to impersonate tokens and privesc to nt system using tools such as potato.exe, rottenpotato.exe and juicypotato.exe"
		* Thank you Aurélien Chalot for the update. I will try to re-phrase it to something more recipe-like soon.
		* "It would allow a user to impersonate tokens and privesc to `nt system`
		* Tools
			* `potato.exe`
			* `rottenpotato.exe`
			* `juicypotato.exe`
	* `SeImpersonate`
		* Overview
			* Admin
			* 3rd party tool
			* Tools from the Potato family (potato.exe, RottenPotato, RottenPotatoNG, Juicy Potato, SweetPotato, RemotePotato0), RogueWinRM, PrintSpoofer, etc.
			* Similarly to SeAssignPrimaryToken, allows by design to create a process under the security context of another user (using a handle to a token of said user).
			* Multiple tools and techniques may be used to obtain the required token.
			* Similarly to SeAssignPrimaryToken, allows by design to create a process under the security context of another user (using a handle to a token of said user). 
		* MultiPotato -<br />[https://github.com/S3cur3Th1sSh1t/MultiPotato](https://github.com/S3cur3Th1sSh1t/MultiPotato)
			* Overview
				* Improvements over RoguePotato
					* It doesn't contain any SYSTEM auth trigger for weaponization. Instead the code can be used to integrate your favorite trigger by yourself.
					* It's not only using CreateProcessWithTokenW to spawn a new process. Instead you can choose between CreateProcessWithTokenW, CreateProcessAsUserW, CreateUser and BindShell.
			* Examples
				* CreateUser with modified PetitPotam trigger

						c:\temp\MultiPotato> MultiPotato.exe -t CreateUser
					* You have by default value 60 secconds (changable via THEAD_TIMEOUT) to let the SYSTEM account or any other account authenticate. This can be done for example via an unpatched MS-EFSRPC function. By default MultiPotato listens on the pipename \\.\pipe\pwned/pipe/srvsvc which is meant to be used in combination with MS-EFSRPC. For other SYSTEM auth triggers you can adjust this value via the -p parameter.

							c:\temp\MultiPotato> PetitPotamModified.exe localhost/pipe/pwned localhost
					* Using PetitPotam.py as trigger from a remote system with a valid low privileged user is of course also possible.
				* CreateProcessAsUserW with SpoolSample trigger:

					c:\temp\MultiPotato> MultiPotato.exe -t CreateProcessAsUserW -p "pwned\pipe\spoolss" -e "C:\temp\stage2.exe"
				* And trigger it via

						c:\temp\MultiPotato>MS-RPRN.exe \\192.168.100.150 \\192.168.100.150/pipe/pwned
				* Important: In my testings for MS-RPRN I could not use localhost or 127.0.0.1 as target, this has to be the network IP-Adress or FQDN. In addition the Printer Service needs to be enabled for this to work.

					    BindShell with SpoolSample PipeName

						c:\temp\MultiPotato> MultiPotato.exe -t BindShell -p "pwned\pipe\spoolss"
		* RemotePotato0 -<br >[https://github.com/antonioCoco/RemotePotato0](https://github.com/antonioCoco/RemotePotato0)
			* Overview
				* DCOM Activation Service
				* [CLSID List Guide](Testaments_and_Books/Redvelations/)
				* "It abuses the DCOM activation service and trigger an NTLM authentication of any user currently logged on in the target machine. It is required that a privileged user is logged on the same machine (e.g. a Domain Admin user). Once the NTLM type1 is triggered we setup a cross protocol relay server that receive the privileged type1 message and relay it to a third resource by unpacking the RPC protocol and packing the authentication over HTTP. On the receiving end you can setup a further relay node (eg. ntlmrelayx) or relay directly to a privileged resource. RemotePotato0 also allows to grab and steal NTLMv2 hashes of every users logged on a machine."
				* Why: I recently had a penetrationtest, where I was able to pwn a MSSQL Server via SQL-Injection and XP_CMDShell. But all public Potatoes failed on this target system to elevate privileges from service-account to SYSTEM. The System auth trigger was not the problem - instead CreateProcessWithTokenW failed all the time with NTSTATUS Code 5 - access forbidden. This didn't really makes sense for me and may be an edge case. One reason for that could be the local endpoint protection which may have blocked the process creation after impersonating SYSTEM.
				* Therefore I searched for alternatives - and asked some people on Twitter about it. Again Credit to @splinter_code for explaining me how to do it via CreateProcessAsUserW which worked fine on the pwned MSSQL server to get a SYSTEM C2-Callback.
		* RoguePotato
			* Overview
	* Candy Potato ("Caramelized Juicy Potato")
		* References
		* Overview
			* "Version 0.2 of JuicyPotato. In comparison with version 0.1 (JuicyPotato), this version offers some improvements, such as automating the exploitation."
			* "This tool has been made on top of the original JuicyPotato, with the main focus on improving/adding some functionalities which was lacking. It is known to work against both Windows Workstation and Server versions up to 8.1 and Server 2016, respectively."
			* JuicyPotato leverages the privilege escalation chain based on certain COM Servers, using a MiTM listener hosted on 127.0.0.1, and it works when you have SeImpersonate or SeAssignPrimaryToken privileges. By default, JuicyPotato uses the BITS service CLSID, and provides other tools (a set of PowerShell and Batch scripts), to enumerate and test other CLSIDs.
			* JuicyPotato Drawbacks
				* Upload Multiple executables
				* Create Multiple data files during CLSID gathering
				* Low speed because of multistep process
				* The "weakest" point is that different Windows Versions, as well as different configurations often requires to enumerate available CLSID over the target machine and that "try" them, one by one.
		* Example

				T:\>CandyPotato.exe
				CandyPotato v0.2
		* Parameters
			* Mandatory args
				* `-t` createprocess call: `<t>` CreateProcessWithTokenW, `<u>` CreateProcessAsUser, `<*>` try both
				* `-p` `<program>`: program to launch
			* Optional args
				* `-l` - `<port>`: COM server listen port (default 10000)
				* `-m` - `<ip>`: COM server listen address (default 127.0.0.1)
				* `-a` -` <argument>`: command line argument to pass to program (default NULL)
				* `-k` - `<ip>`: RPC server ip address (default 127.0.0.1)
				* `-n` - `<port>`: RPC server listen port (default 135)
				* `-c` - <{clsid}>: CLSID (default BITS:{4991d34b-80a1-4291-83b6-3328366b9097})
				* `-z` - only test CLSID and print token's user
				* `-x` - automatically identifies suitable CLSIDs and attempt exploitation
				* `-s` - `<start-type>` `[1-4](default 3:[MANUAL])`
				* `-Q` - print available CLSIDs and exit
	* JuicyPotato -<br />[https://github.com/ohpe/juicy-potato]
		* References
			* .
* <details><summary> `SeAudit` (Click to expand)</summary><p>
	* Threat
	* 3rd party tool
	* Write events to the Security event log to fool auditing or to overwrite old events.
	* Writing own events is possible with Authz Report Security Event API.
* <details><summary> `SeBackup` (Click to expand)</summary><p>
	* Admin
	* 3rd party tool
	* Notes
		* Backup the HKLM\SAM and HKLM\SYSTEM registry hives
		* Extract the local accounts hashes from the SAM database
		* Pass-the-Hash as a member of the local Administrators group
		* Alternatively, can be used to read sensitive files.
	* For more information, refer to the SeBackupPrivilege file.
* <details><summary> `SeChangeNotify` (Click to expand)</summary><p>
	* None
	* -
	* -
	* Privilege held by everyone. Revoking it may make the OS (Windows Server 2019) unbootable.
* <details><summary> `SeCreateGlobal` (Click to expand)</summary><p>
	* ?
	* ?
	* ?
	* 
* <details><summary> `SeCreatePagefile` (Click to expand)</summary><p>`
	* None
	* Built-in commands
	* Create hiberfil.sys, read it offline, look for sensitive data.
	* Requires offline access, which leads to admin rights anyway.
* <details><summary> `SeCreatePermanent` (Click to expand)</summary><p>
	* ?
	* ?
	* ?
	* 
* <details><summary> `SeCreateSymbolicLink` (Click to expand)</summary><p>
	* ?
	* ?
	* ?
	* 
* <details><summary> `SeCreateToken` (Click to expand)</summary><p>
	* Admin
	* 3rd party tool
	* Create arbitrary token including local admin rights with NtCreateToken.
	* 
* <details><summary> `SeDebug` (Click to expand)</summary><p>
	* Admin
	* PowerShell
	* Duplicate the lsass.exe token.
	* Script to be found at FuzzySecurity
* <details><summary> `SeDelegateSession-UserImpersonate` (Click to expand)</summary><p>
	* ?
	* ?
	* ?
	* Privilege name broken to make the column narrow.
* <details><summary> `SeEnableDelegation` (Click to expand)</summary><p>
	* None
	* -
	* -
	* The privilege is not used in the Windows OS.
* <details><summary> `SeIncreaseBasePriority` (Click to expand)</summary><p>
	* Availability
	* Built-in commands
	* start /realtime SomeCpuIntensiveApp.exe
	* May be more interesting on servers.
* <details><summary> `SeIncreaseQuota` (Click to expand)</summary><p>
	* Availability
	* 3rd party tool
	* Change cpu, memory, and cache limits to some values making the OS unbootable.
		* Quotas are not checked in the safe mode, which makes repair relatively easy.
		* The same privilege is used for managing registry quotas.
* <details><summary> `SeIncreaseWorkingSet` (Click to expand)</summary><p>
	* None
	* -
	* -
	* Privilege held by everyone. Checked when calling fine-tuning memory management functions.
* <details><summary> `SeLoadDriver` (Click to expand)</summary><p>
	* Admin
	* 3rd party tool
		1. Load buggy kernel driver such as szkg64.sys
		2. Exploit the driver vulnerability
			* Alternatively, the privilege may be used to unload security-related drivers with fltMC builtin command. i.e.: fltMC sysmondrv
	* Notes
		* The szkg64 vulnerability is listed as CVE-2018-15732
		* The szkg64 exploit code was created by Parvez Anwar
* <details><summary> `SeLockMemory` (Click to expand)</summary><p>
	* Availability
	* 3rd party tool
	* Starve System memory partition by moving pages.
	* PoC published by Walied Assar (@waleedassar)
* <details><summary> `SeMachineAccount` (Click to expand)</summary><p>
	* None
	* -
	* -
	* The privilege is not used in the Windows OS.
* <details><summary> `SeManageVolume` (Click to expand)</summary><p>
	* Admin
	* 3rd party tool
	* 1. Enable the privilege in the token
	2. Create handle to \.\C: with SYNCHRONIZE | FILE_TRAVERSE
	3. Send the FSCTL_SD_GLOBAL_CHANGE to replace S-1-5-32-544 with S-1-5-32-545
	4. Overwrite utilman.exe etc.
	* FSCTL_SD_GLOBAL_CHANGE can be made with this piece of code.
* <details><summary> `SeProfileSingleProcess` (Click to expand)</summary><p>
	* None
	* -
	* -
	* The privilege is checked before changing (and in very limited set of commands, before querying) parameters of Prefetch, SuperFetch, and ReadyBoost. The impact may be adjusted, as the real effect is not known.
* <details><summary> `SeRelabel` (Click to expand)</summary><p>
	* Threat
	* 3rd party tool
	* Modification of system files by a legitimate administrator
	* See: MIC documentation
		* Integrity labels provide additional protection, on top of well-known ACLs. Two main scenarios include:
			* protection against attacks using exploitable applications such as browsers, PDF readers etc.
			* protection of OS files.
			* present in the token will allow to use `WRITE_OWNER` access to a resource, including files and folders.
	* Unfortunately, the token with IL less than High will have SeRelabel privilege disabled, making it useless for anyone not being an admin already.
	* See great blog post by @tiraniddo for details.
* <details><summary> `SeRemoteShutdown` (Click to expand)</summary><p>
	* Availability
	* Built-in commands
	
			shutdown /s /f /m \\server1 /d P:5:19
	* The privilege is verified when shutdown/restart request comes from the network. 127.0.0.1 scenario to be investigated.
* <details><summary> `SeReserveProcessor` (Click to expand)</summary><p>
	* None
	* -
	* -
	* It looks like the privilege is no longer used and it appeared only in a couple of versions of winnt.h. You can see it listed i.e. in the source code published by Microsoft here.
* <details><summary> `SeRestore` (Click to expand)</summary><p>
	* Admin
	* PowerShell
	* Notes
		1. Launch PowerShell/ISE with the SeRestore privilege present.
		2. Enable the privilege with Enable-SeRestorePrivilege).
		3. Rename utilman.exe to utilman.old
		4. Rename cmd.exe to utilman.exe
		5. Lock the console and press Win+U
	* Attack may be detected by some AV software.
	* Alternative method relies on replacing service binaries stored in "Program Files" using the same privilege.
* <details><summary> `SeSecurity` (Click to expand)</summary><p>
	* Threat
	* Built-in commands
		* Clear Security event log

				wevtutil cl Security
		* Shrink the Security log to 20MB to make events flushed soon

				wevtutil sl Security /ms:0
		* Read Security event log to have knowledge about processes, access and actions of other users within the system.
		* Knowing what is logged to act under the radar.
		* Knowing what is logged to generate large number of events effectively purging old ones without leaving obvious evidence of cleaning.
* <details><summary> `SeShutdown` (Click to expand)</summary><p>
	* Availability
	* Built-in commands
	
			shutdown.exe /s /f /t 1
	* Allows to call most of NtPowerInformation() levels. To be investigated.
* <details><summary> `SeSyncAgent` (Click to expand)</summary><p>
	* None
	* -
	* -
	* The privilege is not used in the Windows OS.
* <details><summary> `SeSystemEnvironment` (Click to expand)</summary><p>
	* Unknown
	* 3rd party tool
	* The privilege permits to use NtSetSystemEnvironmentValue, NtModifyDriverEntry and some other syscalls to manipulate UEFI variables.
	* The privilege is required to run sysprep.exe.
	* Additionally:
		* Firmware environment variables were commonly used on non-Intel platforms in the past, and now slowly return to UEFI world.
		* The area is highly undocumented.
		* The potential may be huge (i.e. breaking Secure Boot) but raising the impact level requires at least PoC.
* <details><summary> `SeSystemProfile` (Click to expand)</summary><p>
	* ?
	* ?
	* ?
	* 
* <details><summary> `SeSystemtime` (Click to expand)</summary><p>
	* Threat
	* Built-in commands
	
			cmd.exe /c date 01-01-01
			cmd.exe /c time 00:00
	* The privilege allows to change the system time, potentially leading to audit trail integrity issues, as events will be stored with wrong date/time.
	* Be careful with date/time formats. Use always-safe values if not sure.
	* Sometimes the name of the privilege uses uppercase "T" and is referred as SeSystemTime.
* <details><summary> `SeTakeOwnership` (Click to expand)</summary><p>
	* Admin
	* Built-in commands

			takeown.exe /f "%windir%\system32"
			icalcs.exe "%windir%\system32" /grant "%username%":F
		* Rename cmd.exe to utilman.exe
		* Lock the console and press Win+U
	* Attack may be detected by some AV software.
	* Alternative method relies on replacing service binaries stored in "Program Files" using the same privilege.
* <details><summary> `SeTcb` (Click to expand)</summary><p>
	* Admin
	* 3rd party tool
	* Manipulate tokens to have local admin rights included.
	* Sample code+exe creating arbitrary tokens to be found at PsBits.
* <details><summary> `SeTimeZone` (Click to expand)</summary><p>
	* Mess
	* Built-in commands
	* Change the timezone. tzutil /s "Chatham Islands Standard Time"
	* 
* <details><summary> `SeTrustedCredManAccess` (Click to expand)</summary><p>
	* Threat
	* 3rd party tool
	* Dumping credentials from Credential Manager
	* Great blog post by @tiraniddo
* <details><summary> `SeUndock` (Click to expand)</summary><p>
	* None
	* -
	* -
	* The privilege is enabled when undocking, but never observed it checked to grant/deny access. In practice it means it is actually unused and cannot lead to any escalation.
* <details><summary> `SeUnsolicitedInput` (Click to expand)</summary><p>
	* None
	* -
	* -
	* The privilege is not used in the Windows OS.