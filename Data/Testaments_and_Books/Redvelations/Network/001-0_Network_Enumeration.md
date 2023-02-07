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
# Network Enumeration ([`Gather Victim Network Information` TTP](TTP/T1590_Gather_Victim_Network_Information/T1590.md))
## References

## Checklist

* DMZ Network
	* What systems can be accessed from the DMZ network?
		* [ ] - DMZ Network Systems
		* [ ] - Internal Network Systems
		* [ ] - External Network Systems
	* [ ] - What segmentation exists within the DMZ network?
* Internal Network
	* Access
		* [ ] - How can network access be achieved?
			* [ ] - Direct cable connection
			* Wi-Fi
				* [ ] - Public/Guest Wi-Fi Access
				* [ ] - Employee
	* Subnets
		* [ ] - What is the IP scheme of the subnet?
		* [ ] - How many subnets are visible?
	* Segmentation
		* [ ] - Is there evidence of firewall rule restrictions preventing activity?
		* [ ] - Do external-facing servers (e.g., web servers) reside in the internal network?
	* Systems
		* [ ] - How many systems are visible 
		* Is there a pattern in format for system hostnames?
			* [ ] - Servers
			* [ ] - Workstations
			* [ ] - Other Devices
	* Outbound Connections
		* [ ] - Are outbound protocols restricted in any way?
			* [ ] - DNS
			* [ ] - HTTP/s
			* [ ] - Direct requests for external IP addresses

## CLICK-TO-COPY CHECKLIST

```
* DMZ Network
	* What systems can be accessed from the DMZ network?
		* [ ] - DMZ Network Systems
		* [ ] - Internal Network Systems
		* [ ] - External Network Systems
	* [ ] - What segmentation exists within the DMZ network?
* Internal Network
	* Access
		* [ ] - How can network access be achieved?
			* [ ] - Direct cable connection
			* Wi-Fi
				* [ ] - Public/Guest Wi-Fi Access
				* [ ] - Employee
	* Subnets
		* [ ] - What is the IP scheme of the subnet?
		* [ ] - How many subnets are visible?
	* Segmentation
		* [ ] - Is there evidence of firewall rule restrictions preventing activity?
		* [ ] - Do external-facing servers (e.g., web servers) reside in the internal network?
	* Systems
		* [ ] - How many systems are visible 
		* Is there a pattern in format for system hostnames?
			* [ ] - Servers
			* [ ] - Workstations
			* [ ] - Other Devices
	* Outbound Connections
		* [ ] - Are outbound protocols restricted in any way?
			* [ ] - DNS
			* [ ] - HTTP/s
			* [ ] - Direct requests for external IP addresses
```