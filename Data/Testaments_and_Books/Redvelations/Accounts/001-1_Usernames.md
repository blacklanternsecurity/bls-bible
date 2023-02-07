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
# Usernames
### References

### Overview

### Reconnaissance

* [`Gather Victim Identity Information - Credentials` TTP](TTP/T1589_Gather_Victim_Identity_Information/001_Credentials/T1589.001.md)


### Usernames

* <details><summary>Generate Potential Usernames (Click to expand)</summary><p>
	* Collect Employee names and transform into usernames
    	* Employee Names ([TTP](TTP/T1589_Gather_Victim_Identity_Information/003_Employee_Names/T1589.003.md))
			* Shown on websites
				* Contact Us
				* Team
				* `info@company.com`
					* Great for phishing
			* OSINT
				* LinkedIn
	* Known Email Addresses ([TTP](TTP/T1589_Gather_Victim_Identity_Information/002_Email_Addresses/T1589.002.md))
	* Employee ID Number
		* Example: `123456`
	* Formats
		* `firstinitiallastname`
		* `lastnamefirstinitial`
		* `firstnamelastname`
		* `firstname.lastname`
		* `firstinitial.lastname`
		* `Employee ID`
	* Existing Username Lists
		* 
	* Default computer accounts
		* Administrator
		* Guests
* <details><summary>Web (Click to expand)</summary><p>
	* Password reset option
	* New account Creation
* <details><summary>Email (Click to expand)</summary><p>
	* Enumerate Password Policy
	* Accounts
		* <details><summary>Username (Click to expand)</summary><p>
			* Recommended: Trevorspray -<br />[https://github.com/blacklanternsecurity/TREVORspray](https://github.com/blacklanternsecurity/TREVORspray)
				1. Collect domain public endpoint information

						trevorspray.py --recon <public_domain_name.tld>
				1. Spray against discovered 

						trevorspray.py -e emails.txt -p <Fall2021!> --url <https://login.windows.net/b439d764-cafe-babe-ac05-2e37deadbeef/oauth2/token>
					* Options
						* `--delay <minutes>`
		