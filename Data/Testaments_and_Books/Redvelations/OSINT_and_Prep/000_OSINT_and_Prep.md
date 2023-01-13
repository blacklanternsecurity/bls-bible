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
# Recon and OSINT
## Overview

Common TTPs used between the tools essential for Recon and OSINT processes:

* Collect information about the organization ([TTP](TTP/T1591_Gather_Victim_Org_Information/T1591.md))
	* ([`Gather Victim Org Information - Determine Physical Locations` TTP](TTP/T1591_Gather_Victim_Org_Information/001_Determine_Physical_Locations/T1591.001.md))
	* ([`Gather Victim Org Information - Business Relationships` TTP](TTP/T1591_Gather_Victim_Org_Information/002_Business_Relationships/T1591.002.md))
	* ([`Gather Victim Org Information - Identify Business Tempo` TTP](TTP/T1591_Gather_Victim_Org_Information/003_Identify_Business_Tempo/T1591.003.md))
	* ([`Gather Victim Org Information - Identify Roles` TTP](TTP/T1591_Gather_Victim_Org_Information/004_Identify_Roles/T1591.004.md))
* Collect information about the organization's employees ([TTP](TTP/T1589_Gather_Victim_Identity_Information/T1589.md))
	* Credential Reconnaissance ([TTP](TTP/T1589_Gather_Victim_Identity_Information/001_Credentials/T1589.001.md))
	* ([`Gather Victim Identity Information - Email Addresses` TTP](TTP/T1589_Gather_Victim_Identity_Information/002_Email_Addresses/T1589.002.md))
	* ([`Gather Victim Identity Information -  Employee Names` TTP](TTP/T1589_Gather_Victim_Identity_Information/003_Employee_Names/T1589.003.md))
* Review the organizations external asset presence ([TTP](TTP/T1593_Search_Open_Websites-Domains/T1593.md))
	* ([`Search Open Websites/Domains - Social Media` TTP](TTP/T1593_Search_Open_Websites-Domains/001_Social_Media/T1593.001.md))
	* ([`Search Open Websites/Domains - Search Engines` TTP](TTP/T1593_Search_Open_Websites-Domains/002_Search_Engines/T1593.002.md))
* Search the victim-owned websites ([TTP](TTP/T1594_Search_Victim-Owned_Websites/T1594.md))
	* Search Engine Crafting, Google Dorks ([`Search Open Websites/Domains - Search Engines`TTP](TTP/T1593_Search_Open_Websites-Domains/002_Search_Engines/T1593.002.md))
* Gather employee and credential information
	* Phishing ([`Phishing for Information` TTP](TTP/T1598_Phishing_for_Information/T1598.md), [`Spearphishing Service` TTP](TTP/T1598_Phishing_for_Information/001_Spearphishing_Service/T1598.001.md), [`Spearphishing Attachment` TTP](TTP/T1598_Phishing_for_Information/002_Spearphishing_Attachment/T1598.002.md), [`Spearphishing Link` TTP](TTP/T1598_Phishing_for_Information/003_Spearphishing_Link/T1598.003.md))
	* ([`Gather Victim Identity Information - Credentials` TTP](TTP/T1589_Gather_Victim_Identity_Information/001_Credentials/T1589.001.md))
* Network Trust Dependencies ([`Gather Victim Network Information - Network Trust Dependencies` TTP](TTP/T1590_Gather_Victim_Network_Information/003_Network_Trust_Dependencies/T1590.003.md))
* [`Search Open Technical Databases` TTP](TTP/T1596_Search_Open_Technical_Databases/T1596.md)
* [`Search Open Technical Databases- CDNs` TTP](TTP/T1596_Search_Open_Technical_Databases/004_CDNs/T1596.004.md)


### Active
* ([`Active Scanning` TTP](TTP/T1595_Active_Scanning/T1595.md))
* ([`Active Scanning - Scanning IP Blocks` TTP](TTP/T1595_Active_Scanning/001_Scanning_IP_Blocks/T1595.001.md))
* ([`Active Scanning - Vulnerability Scanning` TTP](TTP/T1595_Active_Scanning/002_Vulnerability_Scanning/T1595.002.md))


## External Assets

1. Microsoft Authentication
	* Legacy Authentication
1. Web Assets
	* Default Creds
1. Network Assets
	* Firewalls

* Web
	* Google Dorks
* Cloud
	1. Identify existing Azure IP Ranges ([`Gather Victim Network Information - IP Addresses` TTP](TTP/T1590_Gather_Victim_Network_Information/005_IP_Addresses/T1590.005.md))
* Social Engineering
* Content
	* Google Dorks


### Data/DNS/SSL/IP

* Recon-ng -<br />[]](https://bitbucket.org/LaNMaSteR53/recon-ng)
	* A full featured Web Reconnissance Framework) - Lanmaster53
* OpenData -<br />[https://opendata.rapid7.com/](https://opendata.rapid7.com/)
	* Rapid7
	* Sonar Reverse DNS -<br />[https://opendata.rapid7.com/sonar.rdns_v2/](https://opendata.rapid7.com/sonar.rdns_v2/)
	* Sonar Forward DNS -<br />[https://opendata.rapid7.com/sonar.fdns_v2/](https://opendata.rapid7.com/sonar.fdns_v2/)
	* Sonar SSL data -<br />[https://opendata.rapid7.com/sonar.ssl/](https://opendata.rapid7.com/sonar.ssl/)
* Google Transparency Report -<br />[](https://transparencyreport.google.com/https/certificates?hl=en)
* Crunchbase -<br />[https://www.crunchbase.com/](https://www.crunchbase.com/)
* Comodo Certificate Transparency List -<br />[https://crt.sh/](https://crt.sh/)
* SSL Tools -<br />[http://ssltools.com/](http://ssltools.com/)
* ARIN WHOI -<br />[https://whois.arin.net/ui/](https://whois.arin.net/ui/)
* RIPE Database -<br />[https://apps.db.ripe.net/db-web-ui/#/query](https://apps.db.ripe.net/db-web-ui/#/query)
* BGP Toolkit -<br />[https://bgp.he.net/](https://bgp.he.net/)
* DNS Dumpster -<br />[https://dnsdumpster.com/](https://dnsdumpster.com/)
* Ultra Tools -<br />[https://www.ultratools.com/tools/dnsLookup](https://www.ultratools.com/tools/dnsLookup)

### Sub-Domain Discovery
* Amass -<br />[](https://github.com/OWASP/Amass)
	* caffix (Recommended in Bug Bounty Hunter Methodology V3 by Jason Haddix)
* Subfinder -<br />[](https://github.com/Ice3man543/subfinder)
	* Ice3man543 (Recommended in Bug Bounty Hunter Methodology V3 by Jason Haddix)
* Sublist3r -<br />[](https://github.com/aboul3la/Sublist3r)
	* Runs quickly but has low number of sources) - aboul3la
* Domain -<br />[(https://github.com/jhaddix/domain) (alt-dns & recon-ng automation script) - Jason Haddix

### Sub-Domain Takeover

* [Can I take over XYZ](https://github.com/EdOverflow/can-i-take-over-xyz) - Ed0verflow

### DNS Brute Force
* [Massdns](https://github.com/blechschmidt/massdns) - blechschmidt (Fastest)
  * [Run with all.txt](https://gist.github.com/jhaddix/86a06c5dc309d08580a018c66354a056) - Jason Haddix
* [Gobuster](https://github.com/OJ/gobuster) (Directory/file & DNS busting tool written in Go) - OJ
* [Fierce](http://tools.kali.org/information-gathering/fierce) (DNS brute forcer) - RSnake

### Port Scanners
 * [Nmap](https://nmap.org/download.html) - Nmap Project
 * [Nmap NSE Scripts](https://nmap.org/nsedoc/) - Nmap Project
 * [Masscan](https://github.com/robertdavidgraham/masscan) - Robert Graham
 
### VPN 
 * GitHub: VPN Hunter -<br />[https://github.com/vineetkrgupta/VpnHunter]](https://github.com/vineetkrgupta/VpnHunter)
 
### Email Discovery
 * Hunter.io -<br />[https://hunter.io/](https://hunter.io/)
 
### Data Leak Lookup
 * We Leak Info -<br />[https://search.weleakinfo.com/search](https://search.weleakinfo.com/search)