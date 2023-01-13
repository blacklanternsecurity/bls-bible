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
# Responder

1. Responder Toolset
Check for machines on the subnet with SMB signing not enabled
	`RunFinger.py`
		Command
			```
			python RunFinger.py -i 10.0.2.0/24
			```

		* `-w` will enable the wpad proxy answering such requests
			* Be aware that the client will afterwards route all his browser HTTP traffic to your attacker machine which might break stuff on the network.
		* `-b` - force WebDAV browser to use basic authentication (plaintext creds)