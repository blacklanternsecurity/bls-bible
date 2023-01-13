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
# Network Attacks
### Tags


### References

### Tools
* <details><summary>Linux (Click to expand)</summary><p>
	* Zmap asset inventory script -<br />[https://github.com/blacklanternsecurity/zmap-asset-inventory](https://github.com/blacklanternsecurity/zmap-asset-inventory)

### Quick Install Recommended Tools (Linux)

<details><summary>Linux Tool Installation</summary><p>

1. Install pipx
1. Install tools with pipx
1. Git clone remaining tools not compatible with pipx
	* BLS zmap Asset Inventory Script -<br />[https://github.com/blacklanternsecurity/zmap-asset-inventory](https://github.com/blacklanternsecurity/zmap-asset-inventory)
1. Install golang (See Red Team Field Manual Linux Installation)
1. Install helpful go tools
	* subnet mapping
		* mapcidr

				go install -v github.com/projectdiscovery/mapcidr/cmd/mapcidr@latest
	* Web Discovery and Analysis
		* nuclei

				go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
		* httpx

				go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
		* naabu

				go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
		* gowitness

				go install -v github.com/sensepost/gowitness@latest
		* ffuf

				go install -v github.com/ffuf/ffuf@latest


1. Packages requiring compiling
	* masscan
		1. Install pre-requisite packages
				sudo apt-get --assume-yes install git make gcc
		1. Git clone the package
				git clone https://github.com/robertdavidgraham/masscan; cd masscan
		1. Make the package

				make
		1. Install the package
				make install
	* zmap
		* Installation
			1. Install prerequisite packages
			
					sudo apt-get install build-essential cmake libgmp3-dev gengetopt libpcap-dev flex byacc libjson-c-dev pkg-config libunistring-dev -y
			1. Git clone the package

					git clone https://github.com/zmap/zmap.git; cd zmap
			1. Build the package with cmake

					cmake .
			1. Make the package

					make -j4
			1. Install the package

					make install
1. Packages requiring docker builds
	* BLS zmap Asset Inventory Script -<br />[https://github.com/blacklanternsecurity/zmap-asset-inventory](https://github.com/blacklanternsecurity/zmap-asset-inventory)
		1. Git clone the package

				git clone https://github.com/blacklanternsecurity/zmap-asset-inventory.git; cd zmap-asset-inventory
		1. Build the docker image

					docker build -t zmap-assets .
		1. Start container (making sure to remap the script's working directory to the host) 

				docker run -it -v /root/inventory/asset_inventory:/root/.asset_inventory zmap-assets
		1. Start scan with desired options. NOTE: you may need to ping 8.8.8.8 (or any IP) so the MAC of the gateway is populated in the ARP cache.

				./asset_inventory.py -t 10.0.0.0/8
		1. (Optional) Change the default Docker network if it overlaps with any of your target subnets. It's 172.16.0.1/16 by default.

				ip addr
				...
				1: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default 
				    link/ether 02:44:73:ff:35:93 brd ff:ff:ff:ff:ff:ff
				    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
				       valid_lft forever preferred_lft forever
				...
		1. Edit `/etc/docker/daemon.json`

				$ sudo vim /etc/docker/daemon.json
				{
				    "bip": "172.16.99.1/24",
				}
		1. Restart dockerd

				sudo systemctl restart docker

</p></details>

### Process

1. [Network Enumeration](Testaments_and_Books/Redvelations/Network/001-0_Network_Enumeration.md)


### #@TODO

* ([`Network Boundary Bridging - Network Address Translation Traversal` TTP](TTP/T1599_Network_Boundary_Bridging/001_Network_Address_Translation_Traversal/T1599.001.md))
* ([`Network Boundary Bridging` TTP](TTP/T1599_Network_Boundary_Bridging/T1599.md))
* ([`Command and Scripting Interpreter - Network Device CLI` TTP](TTP/T1059_Command_and_Scripting_Interpreter/008_Network_Device_CLI/T1059.008.md))