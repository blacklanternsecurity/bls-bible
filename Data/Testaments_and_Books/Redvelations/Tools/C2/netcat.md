<!---------------------------------------------------------------------------------
Copyright: (c) BLS OPS LLC.
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
--------------------------------------------------------------------------------->
# netcat
### References
### Overview

* Examples
	* Example 1
		1. Listener

				nc -lvnp <port>
		1. Target

				netcat.exe
	* Tips: Include line wrapping in connection
		* rlwrap

				rlwrap nc -lvnp

### Shellcode
#### Windows

* nishang windows shells

### Target System Commands
#### Windows

* PowerShell IEX cradle