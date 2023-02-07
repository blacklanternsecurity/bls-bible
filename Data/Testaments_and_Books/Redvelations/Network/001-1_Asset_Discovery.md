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
# Network Asset Discovery
## Enumeration
* Active Scans ([`Active Scanning` TTP](TTP/T1595_Active_Scanning/T1595.md))
* Asset Discovery
	* Broad Asset Discovery
	* ICMP (e.g., "ping sweep") ([`Active Scanning - Scanning IP Blocks` TTP](TTP/T1595_Active_Scanning/001_Scanning_IP_Blocks/T1595.001.md), [`Gather Victim Network Information - IP Addresses` TTP](TTP/T1590_Gather_Victim_Network_Information/005_IP_Addresses/T1590.005.md))
* Subnet Enumeration ([`Gather Victim Network Information - Network Topology` TTP](TTP/T1590_Gather_Victim_Network_Information/004_Network_Topology/T1590.004.md))
1. ICMP ([`Network IP Discovery` TTP](TTP/T1590_Gather_Victim_Network_Information/005_IP_Addresses/T1590.005.md))
	* <details><summary>References (Click to expand)</summary><p>
		* [https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Network%20Discovery.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Network%20Discovery.md)
		* MITRE Techniques: [Remote System Discovery](TTP/T1018_Remote_System_Discovery/T1018.md), [Run host discovery](TTP/T1592_Gather_Victim_Host_Information/T1592.md)
	* Ping Sweep
		* <details><summary>nmap (Click to expand) -<br />[nmap tool guide](Testaments_and_Books/Redvelations/Tools/Port_and_Service_Enumeration/nmap.md)</summary><p>

				nmap -oA <outfile> <CIDR>
		* <details><summary>BLS zmap Asset Inventory Script (Click to expand) -<br />[https://github.com/blacklanternsecurity/zmap-asset-inventory](https://github.com/blacklanternsecurity/zmap-asset-inventory)</summary><p>
			* Produce an asset inventory
				1. Enter the docker container

						docker run -it -v /root/inventory/asset_inventory:/root/.asset_inventory zmap-assets
				1. Run the inventory

						./asset_inventory.py -t 10.0.0.0/8
			* Print just the IPs (for use with other tools)
				* Example

						root@VM:~# awk -F, '{print $1}' ~/inventory/asset_inventory/asset_inventory_2022-08-15_20-04-03.csv | tail -n+2
					* Example Output

							10.0.0.1
							10.0.0.2
							10.0.0.60
							10.0.0.100
* Network Appliances ([`Gather Victim Network Information - Network Security Appliances` TTP](TTP/T1590_Gather_Victim_Network_Information/006_Network_Security_Appliances/T1590.006.md))
	* Network Firewall Solutions, etc.
