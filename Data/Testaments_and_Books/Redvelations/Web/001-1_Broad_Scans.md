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
# Enumeration - Broad Scans


### Automated
* Enumerate Ports
	* Host Information Collection ([TTP](TTP/T1592_Gather_Victim_Host_Information/T1592.md))
	* Ports and Services
* Crawl Websites
	* Search Victim-Owned Websites ([TTP](TTP/T1594_Search_Victim-Owned_Websites/T1594.md))
* Tip: Often a good idea to run automated while performing manual
* <details><summary>Wordlists (Click to expand)</summary><p>
	* `SecLists/Discovery/Web-Content/`
* subdomain enumeration
	* <details><summary>gobuster (Click to expand)</summary><p>
		* Examples Brute force with 50 threads and only list status code 200

				gobuster dir -u <url> -w <wordlist> -t 50 -fw -s 20
		* Require Parameters
			* `-u` - targeturl
		* Other Popular Parameters
			* `-x` - extensions
			* `-o` - outfile
			* `-t` - threads
			* `-w` - wordlist
	* <details><summary>Sublist3r (Click to expand)</summary><p>
		1. .

				mkdir domains
				for i in $(cat domains.txt); do sublist3r -v -d $i -o domains/$i.txt; done
				cd domains
				cat * | tr '[:upper:]' '[:lower:]' | sort -u > all.txt
		1. resolved IPs

				for domain in $(cat domains.txt); do ip=$(host $domain | grep 'has address' | egrep -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | tail -n 1); echo -e "$ip\t$domain"; done | tee resolved.txt
		1. deduplicate by IP

				cat resolved.txt | sort -u -t$'\t' -k1,1 | sort -nr
	* <details><summary>dirb (Click to expand)</summary><p>
		* Brute force with dirb and ignore 404 reponses

				dirb http://<url> <wordlist> -w -N 404
* <details><summary>crt.sh (Click to expand)</summary><p>
	* [https://crt.sh/?q=evilcorp.com](https://crt.sh/?q=evilcorp.com)
* <details><summary>historical dns data (Click to expand)</summary><p>
	* securitytrails.com
	* dnsdumpster.com
* <details><summary>Amass (Click to expand)</summary><p>
	1. Run Amass
		1. Initial Scan

				amass db -dir uap_domains_1_graph -d domain.com -enum 1 -names
		1. Perform subdomain enumeration

				amass enum -active -src -ip -dir amass/<client> -config your-config.ini -o amass/<client>.txt
		1. Optional: Review database

				amass db -dir amass/<client> -d <client>.com -enum 1 -names
	1. Run nuclei templates on resulting data.
		* Requirements
			* Nuclei API key
		* Process
			1. Export collected domains
			1. Run nuclei on the exported domains.

					nuclei -t your-templates-dir/ -l LIST_OF_TARGETS -rl 100 -c 5 -no-color -tags security-survey -stats -iserver 'http://interactsh-server.com/' -itoken 'your-interactsh-token' | tee outfile.txt
				* `-iserver` and `-itoken` may not be correct in latest versions
