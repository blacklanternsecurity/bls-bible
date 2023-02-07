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
# Credential Dump Processing
### From a Linux Machine

* lsass dump
	* pypykatz
	* <details><summary>lsassy (Click to expand) -<br />[https://github.com/Hackndo/lsassy](https://github.com/Hackndo/lsassy)</summary><p>
	* Impacket's secretsdump.py
* NTDS.dit
	* pypykatz
	* <details><summary>lsassy (Click to expand) -<br />[https://github.com/Hackndo/lsassy](https://github.com/Hackndo/lsassy)</summary><p>
	* Impacket's secretsdump.py

			secretsdump.py -ntds ntds.dit -system system.bak LOCAL
* SAM Hive
	* pypykatz
	* <details><summary>lsassy (Click to expand) -<br />[https://github.com/Hackndo/lsassy](https://github.com/Hackndo/lsassy)</summary><p>
	* Impacket's secretsdump.py


secretsdump.py -sam sam.save -security security.save -system system.save LOCAL

### From a Windows Machine
#### Remote

#### Local (Domain-Joined)