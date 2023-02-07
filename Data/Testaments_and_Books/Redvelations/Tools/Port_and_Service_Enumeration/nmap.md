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
# nmap
### References

### Example Commands
* Example 1

		nmap -sC -sV -T4 -oA <outfile_name> <target/CIDR>

### Parameter Guidance

* `-sC` - Run scripts on identified ports
* `-sV` - Enumerate version information of ports
* `-T` - Speed, 1-5. Faster speeds risk greater chance of inaccurate results.
* Output
	* `-oA` - Output all formats
* `-Pn` - Assume host is up. Often necessary for Windows targets.

