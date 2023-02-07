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
# Java
### References

### Overview
* JNDI Exploit Kit
	* Original -<br />[https://github.com/welk1n/JNDI-Injection-Exploit](https://github.com/welk1n/JNDI-Injection-Exploit)
	* Fork -<br />[https://github.com/pimps/JNDI-Exploit-Kit](https://github.com/pimps/JNDI-Exploit-Kit)
		* Features over original
			* `exec_global` - Default Ysoserial execution via Runtime.exec(command);
			* `exec_win` - Execute command using Runtime.exec(["cmd.exe", "/c", command]);
			* `exec_unix` - Execute command using Runtime.exec(["/bin/sh", "/c", command]);
			* `java_reverse_shell` - Native java reverse shell payload to avoid the use of Runtime.exec() and potentially bypass some protections;
			* `sleep` - Native java sleep payload. Its useful to detect if a gadged was executed when you don't have network exfiltration.
			* `dns` - Native java dns request. Its useful to detect if a gadget was executed.
* Broad Exploit Suites
	* Remote Method Guesser -<br />[https://github.com/qtc-de/remote-method-guesser](https://github.com/qtc-de/remote-method-guesser)
		* Overview