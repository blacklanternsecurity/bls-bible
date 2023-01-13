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
# DHCP
## Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@enum #@enumerate #@enumeration #@dns #@dhcp

Tools

		#@impacket #@pcaptools #@pcap #@nmap #@zmap #@ldapsearch #@ldapsearch-ad #@rpcclient #@smbmap #@crackmapexec #@manspider #@adidnsdump #@dnsrecon #@enum4linux #@nopac

</p></details>

## Enumeration
### From a Linux Machine
* <details><summary>nmap (Click to expand) ([nmap tool guide](Testaments_and_Books/Redvelations/Tools/Port_and_Service_Enumeration/nmap.md))</summary><p>

		nmap --script broadcast-dhcp-discover
	* Expected output

			Starting Nmap 7.80 ( https://nmap.org ) at 2021-11-06 16:22 PDT
			Pre-scan script results:
			| broadcast-dhcp-discover: 
			|   Response 1 of 1: 
			|	  IP Offered: 10.0.0.4
			|	  DHCP Message Type: DHCPOFFER
			|	  Subnet Mask: 255.255.255.0
			|	  Renewal Time Value: 4d00h00m00s
			|	  Rebinding Time Value: 7d00h00m00s
			|	  IP Address Lease Time: 8d00h00m00s
			|	  Server Identifier: 10.0.0.1
			|	  Domain Name Server: 10.0.0.1, 10.0.0.10
			|_	 Domain Name: securelab.local\x00

# DNS ([`Gather Victim Network Information - DNS` TTP](TTP/T1590_Gather_Victim_Network_Information/002_DNS/T1590.002.md))
## Overview
The tools need to know the domain name and which nameservers to query, which is often discoverable through the DHCP enumeration. Otherwise, the information may be stored in (For Linux):

* `/etc/resolv.conf`
* `/run/systemd/resolve/resolv.conf`

## Enumeration
* Check if LLMNR, NBT-NS, or mDNS broadcasts are present
	* <details><summary>Responder (Click to expand)</summary><p>
		* Examples

				python Responder.py -I $NETWORK_INTERFACE -A
* Domain Controller Enumeration
	* PDC (Primary Domain Controller)
		* <details><summary>dnsutils' nslookup (Click to expand)</summary><p>

				nslookup -type=srv _ldap._tcp.pdc._msdcs.$DOMAIN
			* Example Output

					Server:         127.0.0.53
					Address:        127.0.0.53#53

					Non-authoritative answer:
					_ldap._tcp.pdc._msdcs.microsoftdelivery.com     service = 0 100 389 DC01.microsoftdelivery.com.
	* All DCs
		* <details><summary>dnsutils' nslookup (Click to expand)</summary><p>

				nslookup -type=srv _ldap._tcp.dc._msdcs.$DOMAIN
			* Example Output

					root@jack-Virtual-Machine:~# nslookup -type=srv _ldap._tcp.dc._msdcs.$DOMAIN
					Server:         127.0.0.53
					Address:        127.0.0.53#53

					Non-authoritative answer:
					_ldap._tcp.dc._msdcs.microsoftdelivery.com      service = 0 100 389 DC01.microsoftdelivery.com.
					_ldap._tcp.dc._msdcs.microsoftdelivery.com      service = 0 100 389 DC02.microsoftdelivery.com.
	* GC (Global Catalog, or DC with greater data like trust information)
		* <details><summary>dnsutils' nslookup (Click to expand)</summary><p>

				nslookup -type=srv gc._msdcs.$DOMAIN
			* Example Output

					root@jack-Virtual-Machine:~# nslookup -type=any gc._msdcs.$DOMAIN
					Server:         127.0.0.53
					Address:        127.0.0.53#53

					Non-authoritative answer:
					Name:   gc._msdcs.microsoftdelivery.com
					Address: 10.0.0.1
					Name:   gc._msdcs.microsoftdelivery.com
					Address: 10.0.0.2
	* Kerberos Servers
		* <details><summary>dnsutils' nslookup (Click to expand)</summary><p>

				nslookup -type=srv _kerberos._tcp.$DOMAIN
			* Example Output

					root@jack-Virtual-Machine:~# nslookup -type=srv _kerberos._tcp.$DOMAIN
					Server:         127.0.0.53
					Address:        127.0.0.53#53

					Non-authoritative answer:
					_kerberos._tcp.microsoftdelivery.com    service = 0 100 88 DC01.microsoftdelivery.com.
					_kerberos._tcp.microsoftdelivery.com    service = 0 100 88 DC02.microsoftdelivery.com.
	* Kerberos "passwd" servers
		* <details><summary>dnsutils' nslookup (Click to expand)</summary><p>

				nslookup -type=srv _kpasswd._tcp.$DOMAIN
			* Example Output

					root@jack-Virtual-Machine:~# nslookup -type=srv _kpasswd._tcp.$DOMAIN
					Server:         127.0.0.53
					Address:        127.0.0.53#53

					Non-authoritative answer:
					_kpasswd._tcp.microsoftdelivery.com     service = 0 100 464 DC01.microsoftdelivery.com.
					_kpasswd._tcp.microsoftdelivery.com     service = 0 100 464 DC02.microsoftdelivery.com.
	* LDAP Servers
		* <details><summary>dnsutils' nslookup (Click to expand)</summary><p>

				nslookup -type=srv _ldap._tcp.$DOMAIN
			* Example Output

					root@jack-Virtual-Machine:~#     nslookup -type=srv _ldap._tcp.$DOMAIN
					Server:         127.0.0.53
					Address:        127.0.0.53#53

					Non-authoritative answer:
					_ldap._tcp.microsoftdelivery.com        service = 0 100 389 DC01.microsoftdelivery.com.
					_ldap._tcp.microsoftdelivery.com        service = 0 100 389 DC02.microsoftdelivery.com.
* List DNS Records ([`Gather Victim Network Information - Domain Properties` TTP](TTP/T1590_Gather_Victim_Network_Information/001_Domain_Properties/T1590.001.md))
	* <details><summary>adidnsdump (Click to expand) -<br />[https://github.com/dirkjanm/adidnsdump](https://github.com/dirkjanm/adidnsdump)</summary><p>
		* <details><summary>References (Click to expand)</summary><p>
			* dirkjanm's blog: Getting in the Zone: dumping Active Directory DNS using adidnsdump -<br />[https://dirkjanm.io/getting-in-the-zone-dumping-active-directory-dns-with-adidnsdump/](https://dirkjanm.io/getting-in-the-zone-dumping-active-directory-dns-with-adidnsdump/)
		* <details><summary>Notes (Click to expand)</summary><p>
			* Enumerates all DNS records in the Domain or Forest DNS zones.
			* The enumeration initially performs a request over **LDAP** to retrieve records, then validates the records over **DNS** requests.
		* <details><summary>Requirements (Click to expand)</summary><p>
			* impacket ([Impacket Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/impacket.md))
			* dnspython
			* "If using proxychains, make sure to specify the `--dns-tcp` option."
		* Examples
			* Example 1: 

					adidnsdump -u $DOMAIN\\$DOMAIN_USER -p $PASSWORD ldap://$DOMAIN_CONTROLLER
				* Command Output

						(adidnsdump-qqqTMx5t) root@ubuntu:~/Tools/adidnsdump# adidnsdump -u securelab.local\\domain_user -p 'P@ssw0rd' ldap://10.0.0.1
						[-] Connecting to host...
						[-] Binding to host
						[+] Bind OK
						[-] Querying zone for records
						[+] Found 15 records
			* Example 2

					adidnsdump -r -u $DOMAIN\\$DOMAIN_USER -p $PASSWORD $DOMAIN_CONTROLLER
				* Output

						(adidnsdump-qqqTMx5t) root@ubuntu:~/Tools/adidnsdump# adidnsdump -r -u securelab.local\\domain_user -p 'P@ssw0rd' ldap://10.0.0.1
						[-] Connecting to host...
						[-] Binding to host
						[+] Bind OK
						[-] Querying zone for records
						[-] Could not resolve node _gc._tcp (probably no A record assigned to name)
						[-] Could not resolve node * (probably no A record assigned to name)
						[+] Found 15 records
			* Report Output

					root@ubuntu:~/Tools/adidnsdump# cat records.csv 
					type,name,value
					A,Win11-1,10.0.0.3
					A,Win10-1,10.0.0.30
					A,ForestDnsZones,10.0.0.10
					A,Exchange,10.0.0.3
					A,DomainDnsZones,10.0.0.1
					A,DC02,10.0.0.10
					A,dc01,10.0.0.1
					A,CA,10.0.0.2
					NS,_msdcs,dc01.securelab.local.
					?,_gc._tcp,?
					NS,@,dc02.securelab.local.
					NS,@,dc01.securelab.local.
					A,@,10.0.0.1
					A,@,10.0.0.10
					?,*,?
* Outline subnets following adidnsdump data collect
	* <details><summary>References (Click to expand)</summary><p>
		* snovvcrash twitter status outlining this method -<br />[https://twitter.com/snovvcrash/status/1550518555438891009](https://twitter.com/snovvcrash/status/1550518555438891009)
	* <details><summary>Requirements (Click to expand)</summary><p>
		* records.csv must exist following adidnsdump
		* projectdiscovery's mapcidr tool -<br />[https://github.com/projectdiscovery/mapcidr](https://github.com/projectdiscovery/mapcidr)
	* <details><summary>Example 1: Aggregate IPs/CIDRs into minimum subnet (Click to expand)</summary><p>

			cat records.csv | awk -F, '{print $3}' | egrep '^[0-9]' | mapcidr -a -silent | mapcidr -s -silent
		* Example Output

				root@jack-Virtual-Machine:~# cat records.csv | awk -F, '{print $3}' | egrep '^[0-9]' | mapcidr -a -silent | mapcidr -s -silent
				10.0.0.1/32
				10.0.0.2/31
				10.0.0.50/32
				10.0.0.60/32
				10.0.0.100/32
	* <details><summary>Example 2: Aggregate sparce IPs/CIDRs into minimum approximated subnet (Click to expand)</summary><p>

			cat records.csv | awk -F, '{print $3}' | egrep '^[0-9]' | mapcidr -aa -silent | mapcidr -s -silent
		* Example Output

				10.0.0.0/31
* General DNS Enumeration
	* <details><summary>nmap (Click to expand) ([nmap tool guide](Testaments_and_Books/Redvelations/Tools/Port_and_Service_Enumeration/nmap.md))</summary><p>

			nmap --script dns-srv-enum --script-args dns-srv-enum.domain=$DOMAIN
		* Example Output

				root@ubuntu:/# nmap --script dns-srv-enum --script-args dns-srv-enum.domain=securelab.local
				Starting Nmap 7.80 ( https://nmap.org ) at 2021-11-06 21:44 PDT
				Pre-scan script results:
				| dns-srv-enum: 
				|   Active Directory Global Catalog
				|	  service   prio  weight  host
				|	  3268/tcp  0	  100	  DC02.securelab.local
				|	  3268/tcp  0	  100	  DC01.securelab.local
				|   Kerberos KDC Service
				|	  service  prio  weight  host
				|	  88/tcp   0	  100	  DC02.securelab.local
				|	  88/tcp   0	  100	  DC01.securelab.local
				|	  88/udp   0	  100	  DC02.securelab.local
				|	  88/udp   0	  100	  DC01.securelab.local
				|   Kerberos Password Change Service
				|	  service  prio  weight  host
				|	  464/tcp  0	  100	  DC02.securelab.local
				|	  464/tcp  0	  100	  DC01.securelab.local
				|	  464/udp  0	  100	  DC02.securelab.local
				|	  464/udp  0	  100	  DC01.securelab.local
				|   LDAP
				|	  service  prio  weight  host
				|	  389/tcp  0	  100	  DC02.securelab.local
				|_	 389/tcp  0	  100	  DC01.securelab.local
				WARNING: No targets were specified, so 0 hosts scanned.
				Nmap done: 0 IP addresses (0 hosts up) scanned in 0.17 seconds
* DNZ Zone Transfer
	* <details><summary>dig (Click to expand)</summary><p>
		* Example

				dig axfr zonetransfer.me @$DNS
			* Example Output 1: Transfer Failed

					root@jack-Virtual-Machine:~# dig axfr zonetransfer.me @$DNS

					; <<>> DiG 9.16.1-Ubuntu <<>> axfr zonetransfer.me @dc01.microsoftdelivery.com
					;; global options: +cmd
					; Transfer failed.