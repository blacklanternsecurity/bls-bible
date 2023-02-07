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
# Manual Enumeration
## References
* [PayloadsAllTheThings Directory Traversal](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Directory%20Traversal)

## Process
* Basic Information

		nc -v domain.com 80 # GET / HTTP/1.0
		openssl s_client -connect domain.com:443 # GET / HTTP/1.0
* Server Information
* <details><summary>Usernames ([Usernames Guide](Testaments_and_Books/Redvelations/Accounts/001_Usernames.md)) (Click to expand)</summary><p>
	* UserID rotation
	* Popular usernames
		* `Admin`
		* `administrator`
		* `testuser`
* <details><summary>Passwords and Credentials ([Passwords and Credentials Guide](Testaments_and_Books/Redvelations/Accounts/002_Passwords_and_Credentials.md)) (Click to expand)</summary><p>
	* SAML2Spray -<br />[https://github.com/LuemmelSec/SAML2Spray](https://github.com/LuemmelSec/SAML2Spray)
* Subdomains and Content ([TTP]())
* <details><summary>Image Information (Click to expand)</summary><p>
	1. wget

			wget <url>
		* Note that downloading images directly from a web page will apply the latest
	1. exiftool

			exiftool <file>
* External-focused enumeration
	* Tools
		* BBOT
* Internal-focused enumeration
	* Tools
		* gowitness
* Inpsect source of pages
	* Technology in Use
		* Content Management System
	* Comments
	* Paths


1. Perform Passive Checks
	* <details><summary>Identify areas where user input is accepted (Click to expand)</summary><p>
		* Forms
		* Logins
	* <details><summary>OSINT (Click to expand)</summary><p>
		* API Key Leaks -<br />[https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/API%20Key%20Leaks](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/API%20Key%20Leaks)
1. Begin performing light active enumeration and testing
	* <details><summary>Automatic/Scanning (Click to expand) ([`Active Scanning` TTP](TTP/T1595_Active_Scanning/T1595.md), [`Active Scanning - Vulnerability Scanning` TTP](TTP/T1595_Active_Scanning/002_Vulnerability_Scanning/T1595.002.md))</summary><p>
		* Load balancing ([TTP]())
		* Web services on other ports (e.g. 8080) ([TTP]())
	* <details><summary>Manual (Click to expand)</summary><p>
		* Directory Traversal ([TTP](TTP/T1083_File_and_Directory_Discovery/T1083.md))
