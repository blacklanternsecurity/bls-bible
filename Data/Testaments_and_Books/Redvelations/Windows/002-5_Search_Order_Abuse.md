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
# Search Order Abuse
### References
<details><summary>References (Click to expand)</summary><p>

* Red Canary Blog: System32 Binaries -<br />[https://redcanary.com/blog/system32-binaries/](https://redcanary.com/blog/system32-binaries/)

</p></details>

### Tags

<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@Windows #@microsoft

Context

		#@lolbin #@lolbas #@lolbins #@lol #@download #@execute #@execution #@exec #@bypass #@EDR #@av #@search #@order #@abuse #@lolbin #@lolbins #@arbitrary #@dll #@execution #@download

Tools

		#@cloudnotifications #@credwiz #@CompMgmtLauncher.exe #@CompMgmtLauncher #@computerdefaults.exe #@computerdefaults #@dccw.exe #@dccw #@devicepairingwizard.exe #@devicepairingwizard #@dialer.exe #@dialer #@dism.exe #@dism #@dxpserver.exe #@dxpserver #@filehistory.exe #@filehistory #@gamepanel.exe #@gamepanel #@genvalobj.exe #@genvalobj #@isoburn.exe #@isoburn #@lpksetup.exe #@lpksetup #@mdeserver.exe #@mdeserver #@mdmagent.exe #@mdmagent #@mdmappinstaller.exe #@mdmappinstaller #@mfpmp.exe #@mfpmp #@MoUsoCoreWorker.exe #@MoUsoCoreWorker #@msdt.exe #@msdt #@musnotificationux.exe #@musnotificationux #@netplwiz.exe #@netplwiz #@odbcad32.exe #@odbcad32 #@optionalfeatures.exe #@optionalfeatures #@printfilterpipelinesvc.exe #@printfilterpipelinesvc #@ProximityUxHost.exe #@ProximityUxHost #@quickassist.exe #@quickassist #@rasphone.exe #@rasphone #@regedt32.exe #@regedt32 #@shrpubw.exe #@shrpubw #@tabcal.exe #@tabcal #@usocoreworker.exe #@usocoreworker #@wfs.exe #@wfs 


</p></details>

### Overview

This guide is a subsection of the Windows ([LOLBAS Guide](Testaments_and_Books/Redvelations/Windows/002-4_LOLBAS.md)).

<details><summary>Overview (Click to expand)</summary><p>

* Search Order Abuse takes advantage of Windows binaries searching for a target file name across multiple locations according to a specific order. Included in the specific order is the file path wherever the binary is being presently executed. Microsoft signed binaries fom system32 can be copied to a user-controlled folder to execute malicious files matching the expected file name.
* Microsoft signed binaries
	* Trusted binaries that do not require a user prompt for elevated execution.
	* Portable between systems and can either be copied from the local system32 directory or from a remote machine's system32 directory.
* Evasion, Obfuscation
	* Although it is simple to copy the file over, EDR can detect this behavior.
	* EDR also searches according to file hashes. The binary can be obfuscated by adding a simple null byte to change the file hash and bypass EDRs, provided the binary still properly executes the shellcode

			echo x00 >> <binary.exe>
* Identify vulnerable binaries
	* Sysinternals Process Explorer ([Sysinternals Process Explorer Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/Sysinternals/Process_Explorer.md))
* Additionally, environment variables can be manipulated to alter where the expected locations are for DLLs and load arbitrary DLLs.
	* [https://www.wietzebeukema.nl/blog/save-the-environment-variables](https://www.wietzebeukema.nl/blog/save-the-environment-variables)


</p></details>

### Process
* Phishing
	1. Remotely host affected obfuscated Microsoft-signed binary
	1. Use COM Object to remotely pull the binary and shellcode with expected name for binary to a user-controlled folder.
	1. Execute the obfuscated signed binary command.

### Arbitrary DLLs ([DLL Search Order Hijacking TTP](TTP/T1574_Hijack_Execution_Flow/001_DLL_Search_Order_Hijacking/T1574.001.md))

* <details><summary>CloudNotifications.exe</summary><p>
	* Expected DLL filename
		* `vm3dum64_loader.dll`
	* Command

			.\CloudNotifications.exe
* <details><summary>credwiz.exe</summary><p>
	* Expected DLL filename
		* `DUser.dll`
	* Command

			.\credwiz.exe
* <details><summary>CompMgmtLauncher.exe (Click to expand)</summary><p>
	* Expected DLL filename (any of these)
		* `apphelp.dll`
		* `profapi.dll`
	* Command

			.\CompMgmtLauncher.exe
* <details><summary>ComputerDefaults.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `PROPSYS.dll`
	* Command

			.\computerfdefaults.exe
* <details><summary>dccw.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `duser.dll`
	* Command

			.\dccw.exe
* <details><summary>DevicePairingWizard.exe (Click to expand)</summary><p>
	* Expected DLL filename (any of these)
		* `dwmapi.dll`
		* `textshaping.dll`
	* Command

			.\DevicePairingWizard.exe
* <details><summary>dialer.exe (Click to expand)</summary><p>
	* Expected DLL filename (any of these)
		* `rtutils.dll`
		* `SspiCli.dll`
		* `textshaping.dll`
	* Command

			.\dialer.exe
* <details><summary>Dism.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `dismcore.dll`
	* Command

			.\Dism.exe
* <details><summary>Dxpserver.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `MSASN1.dll`
	* Command

			.\Dxpserver.exe
* <details><summary>FileHistory.exe (Click to expand)</summary><p>
	* Expected DLL filename (any of these)
		* `CRYPTBASE.dll`
		* `CRYPTSP.dll`
	* Command

			.\FileHistory.exe
* <details><summary>GamePanel.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `UMPDC.dll`
	* Command

			.\GamePanel.exe
* <details><summary>GenValObj.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `MSASN1.dll`
	* Command

			.\GenValObj.exe
* <details><summary>isoburn.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `textshaping.dll`
	* Command

			.\isoburn.exe
* <details><summary>lpksetup.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `CRYPTBASE.dll`
	* Command

			.\lpksetup.exe
* <details><summary>mdeserver.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `MFPlat.dll`
	* Command

			.\MDEServer.exe
* <details><summary>MDMAgent.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `UMPDC.dll`
	* Command

			.\MDMAgent.exe
* <details><summary>MDMAppInstaller.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `UMPDC.dll`
	* Command

			.\MDMAppInstaller.exe
* <details><summary>mfpmp.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `UMPDC.dll`
	* Command

			.\mfpmp.exe
* <details><summary>MoUsoCoreWorker.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `MSASN1.dll`
	* Command

			.\MoUsoCoreWorker.exe
* <details><summary>msdt.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `MASN1.dll`
	* Command

			.\msdt.exe
* <details><summary>MusNotificationUx.exe (Click to expand)</summary><p>
	* Expected DLL filename (any of these)
		* `MSASN1.dll`
		* `UMPDC.dll`
	* Command

			.\MusNotificationUx.exe
* <details><summary>Netplwiz.exe (Click to expand)</summary><p>
	* Expected DLL filename (any of these)
		* `DSROLE.dll`
		* `netutils.dll`
		* `samcli.dll`
		* `SAMLIB.dll`
		* `textshaping.dll`
		* `wkscli.dll`
	* Command

			.\Netplwiz.exe
* <details><summary>odbcad32.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `textshaping.dll`
	* Command

			.\odbcad32.exe
* <details><summary>OptionalFeatures.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `textshaping.dll`
	* Command

			.\OptionalFeatures.exe
* <details><summary>printfilterpipelinesvc.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `UMPDC.dll`
	* Command

			.\printfilterpipelinesvc.exe
* <details><summary>ProximityUxHost.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `UMPDC.dll`
	* Command

			.\ProximityUxHost.exe
* <details><summary>quickassist.exe (Click to expand)</summary><p>
	* Expected DLL filename (any of these)
		* `msIso.dll`
		* `srpapi.dll`
	* Command

			.\quickassist.exe
* <details><summary>rasphone.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `textshaping.dll`
	* Command

			.\rasphone.exe
* <details><summary>regedt32.exe (Click to expand)</summary><p>
	* Expected DLL filename (any of these)
		* `edputil.dll`
		* `profapi.dll`
		* `PROPSYS.dll`
		* `urlmon.dll`
	* Command

			.\regedt32.exe
* <details><summary>shrpubw.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `ACLUI.dll`
	* Command

			.\shrpubw.exe
* <details><summary>tabcal.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `MSASN1.dll`
	* Command

			.\tabcal.exe
* <details><summary>usocoreworker.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `MSASN1.dll`
	* Command

			.\usocoreworker.exe
* <details><summary>WFS.exe (Click to expand)</summary><p>
	* Expected DLL filename
		* `FxsCompose.dll`
	* Command

			.\WFS.exe