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
# Network Traffic Collections
## Overview
* Augmented greatly when positioned as MitM.

## Collect Network Traffic Data
* Generate a pcap
	* <details><summary>tcpdump (Click to expand)</summary><p>

			tcpdump -i <interface> -w <outfile.pcap>
	* <details><summary>Eavesarp (Click to expand) -<br />[https://github.com/arch4ngel/eavesarp](https://github.com/arch4ngel/eavesarp)</summary><p>

			python eavesarp.py capture -i <interface>
* Repositories
	* <details><summary>tcpdump (Click to expand)</summary><p>Awesome PCAPTools -<br />[https://github.com/caesar0301/awesome-pcaptools](https://github.com/caesar0301/awesome-pcaptools)

## Analyze Network Traffic Data

* `.pcap` data
	* Map Network Topology
		* Linux
			* ???
		* Windows
			* <details><summary>BruteShark <br />[https://github.com/odedshimon/BruteShark](https://github.com/odedshimon/BruteShark) (Click to expand)</summary><p>
	* Credential, PCI Checking
		* PCredz -<br />[https://github.com/lgandx/PCredz](https://github.com/lgandx/PCredz)
		* BruteShark -<br />[https://github.com/odedshimon/BruteShark](https://github.com/odedshimon/BruteShark)
		* [PCI Impact Guide](Testaments_and_Books/Purplippians/Impact/Impact.md)
