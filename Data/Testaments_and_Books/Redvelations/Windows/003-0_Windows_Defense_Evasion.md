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
# Windows Defense Evasion
### References
### TTPs

* Evasion during Execution
	* <details><summary>DLL Hijacking (Click to expand)</summary><p>
		* [DLL Search Order Hijacking](TTP/T1574_Hijack_Execution_Flow/001_DLL_Search_Order_Hijacking/T1574.001.md)
		* [DLL Side-Loading](TTP/T1574_Hijack_Execution_Flow/002_DLL_Side-Loading/T1574.002.md)
	* <details><summary>Trusted Developer Utilities (Click to expand)</summary><p>
		* Trusted Developer Utilities 
		* Trusted Developer Utilities: MSBuild
	* <details><summary>AMSI Bypass (Click to expand)</summary><p>
		* []()
	* <details><summary>UAC Bypass (Click to expand) ([`Abuse Elevation Control Mechanism - Bypass User Account Control` TTP](TTP/T1548_Abuse_Elevation_Control_Mechanism/002_Bypass_User_Account_Control/T1548.002.md))</summary><p>
		* chryzsh's "PowerShell UAC Always Notify Bypass" - Elevate command shell when already local admin
			* References
				* [https://gist.github.com/chryzsh/5dd33c2cd85f50fae5f1f08637086c48](https://gist.github.com/chryzsh/5dd33c2cd85f50fae5f1f08637086c48)
			* Requirements
				* Local Admin
			* Process
				1. Copy the described payload
				1. Optional: modify line 30 

						key.SetValue("C:\Windows\Microsoft.Net\Framework\v4.0.30319\msbuild.exe C:\users\public\output.txt " + " & ", RegistryValueKind.String);
					* Parameters
						* `msbuild.exe` - Used to abuse the trusted developer utility for execution.
						* `output.txt` - Often shellcode in the format that is compatible with msbuild.
				1. .
		* Example 2 (TODO: Research)
			[bypass uac payload](Testaments_and_Books/Redvelations/Windows/Payloads/bypass_uac_1.ps1)
* <details><summary>Shellcode Obfuscation (Click to expand)</summary><p>
	* 
* <details><summary>File obfuscation (Click to expand)</summary><p>
	* Microsoft Office
		* [VBA](Testaments_and_Books/Redvelations/Windows/003-1_VBA-VBS_Obfuscation.md)
	* donut
	* .NET Binaries
		* Dotfuscator Community
			 * **NOTE** Dotfuscator has a community (CE) and a professional (Pro) edition. The Community edition is licensed for free with Visual Studio 2017 and 2019. As of this writing Code is not supported.
		* References
			 * [https://www.preemptive.com/dotfuscator/ce/docs/help/index.html](https://www.preemptive.com/dotfuscator/ce/docs/help/index.html)
		* Install
			1. Open Visual Studio (2017 or 2019)
			1. In the **Quick Launch** (Ctrl+Q), search for **dotfuscator**
			1. In the search results under `Components`, select **Install PreEmptive Protection - Dotfuscator Community**
			1. The visual studio installer will launch and prompt for install
			1. Once added to visual studio, select **Tools -> PreEmptive Protextion - Dotfuscator** to access
		* Notes
			* Binary obfuscation in CE can be performed via the GUI or CLI. CLI access requires registration to enable.
			* Binary obfuscation with CE is performed post compilation. Pro allows for obfuscation during compile time. Supports assemblies (`.dll` or `.exe`) and packages (`.appx`)
		* Process
			1. Open your project in Visual Studio as normal
			1. Set the project to **release** and build as usual
			1. Open Dotfuscator, select **Tools -> PreEmptive Protection - Dotfuscator Community**
			1. Select **Inputs** and click the green plus (Add Inputs) to select your compiled binary
			1. Your binary will appear as an input in the list (Multiple inputs can be compiled at once)
			1. Select **Build** to run the obfuscation against your binary. The completed assembly will be located in a new folder under `\Release\Dotfuscated\binary.exe`
			1. You will be prompted to save your Dotfuscator config file as an `.xml` file
		* Obfuscation Options
			* `Library Mode` - Disabling this allows for more aggressive renaming, but will not include assemblies that are not part of the dotfuscator config
		* Viewing Results
			* Selecting the **Results** tab upon completion of the build process will display the structure of the output assembly. Drilling down into the nodes and look for altered elements, marked with a Dotfuscator icon.
			* Additionally, if you'd like to can use the built in .NET dissassembler `ildasm` located in `c:\Program Files (x86)\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.8 Tools\ildasm.exe`

### Unicode for Defense Evasion

* U+2012, U+2013, U+2014, or U+2015 - Can be used in Command Line for the similar-looking character

### Test Execution Against Defenses
* <details><summary>Test Execution Against Defenses (Click to expand)</summary><p>
	* Process
		1. Collect information on the target environment and replicate with a test environment
			* Operating System
			* AV, EDR
				* Not all EDRs offer a free trial or testing of their product
			* NDR
		1. Optional: In the test, consider disabling any sample submission options in your AV/EDR
		1. Test the file within the test environment. Modify until successful within the test environment.
		1. Download API Monitor for monitoring calls to **NTDLL** ([https://rohitab.com])
			* Recommended: Portable version
			* This tool has been tested on the latest version of Windows 10
		1. Get the list of hooked functions for the AV/EDR you're trying to evade (GitHub - Mr-Un1k0d3r/EDRs) -<br />[https://github.com/Mr-Un1k0d3r/EDRs](https://github.com/Mr-Un1k0d3r/EDRs)
			* Example: For Carbon Black, download `EDRs/carbonblack.txt` from **GitHub - Mr-Un1k0d3r/EDRs**
		1. Turn the list into a monitoring filter

				awk -F' ' '{print "<Filter Field=\"API Name\" Relation=\"is\" Value=\""$1"\" Action=\"Show\" Enabled=\"True\"/>"}' carbonblack.txt
			* Replace `carbonblack.txt` with whatever text file you downloaded from the aforementioned github.
		1. Input your results into the following file which you then save as `filter.xml`:
			* [filter.xml](Testaments_and_Books/Redvelations/Windows/Payloads/filter.xml)
		1. Prepare API Monitor for usage
			1. In the API Filter pane (left side of the application), select **Ntdll.dll** from the dropdown list of modules.
			1. Check all the boxes for API categories that pop up below.
				* Examples: Additional Resources, NT Native
			1. Import the filter
				1. Opening the API Monitor application
				1. Select the Load Filter button that looks like a folder on the left side of the application under API Filter
				1. Select the `filter.xml` file that you created
		1. Execute the command in API Monitor
			1. Execute your payload by pressing "Ctrl + M" and entering the command to launch your payload.
				* Example 1
					* Ex. Process:
						* `C:Windows\System32\wuauclt.exe`
					* Arguments:
						* `/UpdateDeploymentProvider C:\Users\Public\Downloads\backup.dll /RunHandlerComServer`
					* StartIn:
						* `C:\Windows\System32 and then press OK.`
				* Example 2
					* Ex. Process:
						* `C:\Windows\Microsoft.NET\Framework64\v4.0.30319\MSBuild.exe`
					* Arguments:
						* `C:\Users\Public\Downloads\payload.txt`
					* StartIn
						* `C:\Windows\Microsoft.NET\Framework64\v4.0.30319`
		1. Look at the displayed API calls for what will be detected
			* Now **API Monitor** will display the API calls that are both being used to get execution and monitored by AV/EDR.
				* If no results show up then that means your execution should be opsec safe.
				* If results show up then tread carefully, AV/EDR will be monitoring what you're doing and could flag it as malicious


* Abuse Elevation Control Mechanism ([`Abuse Elevation Control Mechanism` TTP](TTP/T1548_Abuse_Elevation_Control_Mechanism/T1548.md))
	* Perform Elevated Execution with prompt ([`Abuse Elevation Control Mechanism - Elevated Execution with Prompt` TTP](TTP/T1548_Abuse_Elevation_Control_Mechanism/004_Elevated_Execution_with_Prompt/T1548.004.md))
* Access Token Manipulation ([`Access Token Manipulation` TTP](TTP/T1134_Access_Token_Manipulation/T1134.md)
	* Create a Process ([`Access Token Manipulation - Create Process with Token` TTP](TTP/T1134_Access_Token_Manipulation/002_Create_Process_with_Token/T1134.002.md))
	* Make/Impersonate Token ([`Access Token Manipulation - Make and Impersonate Token` TTP](TTP/T1134_Access_Token_Manipulation/003_Make_and_Impersonate_Token/T1134.003.md))
	* Parent PID Spoofing ([`Access Token Manipulation - Parent PID Spoofing` TTP](TTP/T1134_Access_Token_Manipulation/004_Parent_PID_Spoofing/T1134.004.md))
	* SID History Injection ([`Access Token Manipulation - SID-History Injection` TTP](TTP/T1134_Access_Token_Manipulation/005_SID-History_Injection/T1134.005.md))
	* Impersonation/Theft ([`Access Token Manipulation - Token Impersonation-Theft` TTP](TTP/T1134_Access_Token_Manipulation/001_Token_Impersonation-Theft/T1134.001.md))
* Process Injection ([`Process Injection` TTP](TTP/T1055_Process_Injection/T1055.md))
	* DLL ([`Process Injection - Dynamic-link Library Injection` TTP](TTP/T1055_Process_Injection/001_Dynamic-link_Library_Injection/T1055.001.md))
	* (Portable) Executable ([`Process Injection - Portable Executable Injection` TTP](TTP/T1055_Process_Injection/002_Portable_Executable_Injection/T1055.002.md))
	* Thread Execution Hijacking ([`Process Injection - Thread Execution Hijacking` TTP](TTP/T1055_Process_Injection/003_Thread_Execution_Hijacking/T1055.003.md))
	* Asynchronous Procedure Call ([`Process Injection - Asynchronous Procedure Call` TTP](TTP/T1055_Process_Injection/004_Asynchronous_Procedure_Call/T1055.004.md))
	* Thread Local Storage ([`Process Injection - Thread Local Storage` TTP](TTP/T1055_Process_Injection/005_Thread_Local_Storage/T1055.005.md))
	* Ptrace System Calls ([`Process Injection - Ptrace System Calls` TTP](TTP/T1055_Process_Injection/008_Ptrace_System_Calls/T1055.008.md))
	* Proc Memory ([`Process Injection - Proc Memory` TTP](TTP/T1055_Process_Injection/009_Proc_Memory/T1055.009.md))
	* Extra Window Memory Injection ([`Process Injection - Extra Window Memory Injection` TTP](TTP/T1055_Process_Injection/011_Extra_Window_Memory_Injection/T1055.011.md))
	* Process Hollowing ([`Process Injection - Process Hollowing` TTP](TTP/T1055_Process_Injection/012_Process_Hollowing/T1055.012.md))
	* Process Doppelgänging ([`Process Injection - Process Doppelgänging` TTP](TTP/T1055_Process_Injection/013_Process_Doppelgänging/T1055.013.md))
	* VDSO Hijacking ([`Process Injection - VDSO Hijacking` TTP](TTP/T1055_Process_Injection/014_VDSO_Hijacking/T1055.014.md))
* Hiding Artifacts ([`Hide Artifacts` TTP](TTP/T1564_Hide_Artifacts/T1564.md))
	* Hidden Files/Directories ([`Hide Artifacts - Hidden Files and Directories` TTP](TTP/T1564_Hide_Artifacts/001_Hidden_Files_and_Directories/T1564.001.md))
	* Hidden Users([`Hide Artifacts - Hidden Users` TTP](TTP/T1564_Hide_Artifacts/002_Hidden_Users/T1564.002.md))
	* Hidden Window([`Hide Artifacts - Hidden Window` TTP](TTP/T1564_Hide_Artifacts/003_Hidden_Window/T1564.003.md))
	* NTFS File Attributes ([`Hide Artifacts - NTFS File Attributes` TTP](TTP/T1564_Hide_Artifacts/004_NTFS_File_Attributes/T1564.004.md))
	* Hidden File System ([`Hide Artifacts - Hidden File System` TTP](TTP/T1564_Hide_Artifacts/005_Hidden_File_System/T1564.005.md))
	* Run Virtual Instance ([`Hide Artifacts - Run Virtual Instance` TTP](TTP/T1564_Hide_Artifacts/006_Run_Virtual_Instance/T1564.006.md))
	* VBA Stomping ([`Hide Artifacts - VBA Stomping` TTP](TTP/T1564_Hide_Artifacts/007_VBA_Stomping/T1564.007.md))

	* <details><summary>MalSecLogon (Click to expand)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* [https://github.com/antonioCoco/MalSeclogon](https://github.com/antonioCoco/MalSeclogon)
		* <details><summary>Overview (Click to expand)</summary><p>
			* .
		* Examples

				.