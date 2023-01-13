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
# PeopleSoft
### References
* []()

### Overview

### Attacks

* PeopleSoft SSO Token (`PSTOKEN`) Abuse
	* References
		* []()
	* Overview
		* PeopleSoft's deployment requires a node password be set
		* A hash of the node password may be obtained by any authenticated user through the 
		* A cracked node password can be used to impersonate any user in PeopleSoft
	* BurpSuite Extension: PeopleSoft Token Extractor
		* References
		* Overview
			* This extension help test PeopleSoft SSO tokens. The features are:
		    * Extracts and displays token information based on the decompressed data
			* Generates the Hashcat format - to perform brute-force/dictionary attacks in order to obtain the local node password
			* Generates a new PSTOKEN value that can be used in order to authenticate as another user (requires knowledge of the local node password)
		* Attack
			1. Authenticate as a valid user
			1. Retrieve the `PSTOKEN` token stored for the user
			1. Insert the token in the BurpSuite Extension (should be top left box).
			1. Copy the derived hash (should be bottom left box).
			1. Crack the hash.
			1. Insert the cracked password (should be the top-right box).
			1. Specify a username (should be the right-middle box).
			1. Copy the new token, insert it into your cookies, and refresh the webpage.
