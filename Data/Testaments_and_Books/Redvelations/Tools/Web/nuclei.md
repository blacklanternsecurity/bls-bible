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
# Nuclei
### References

### Installation
1. Download The Latest Release
	* Linux amd64 zip [https://github.com/projectdiscovery/nuclei/releases/](https://github.com/projectdiscovery/nuclei/releases/)
1. Unzip The Downloaded Zip File 

		unzip nuclei_VERSION_linux_amd64.zip
	* Replace `VERSION` placeholder with the version number of nuclei downloaded
1. Download The Latest BLS Vetted Templates For Nuclei
1. Unzip The Downloaded BLS Vetted Templates For Nuclei In The Same Folder As The Nuclei Binary

		unzip nuclei-templates-bls-master.zip

### Usage

1. Compile A List Of URLs To Be Targeted Into A Text File Delineated By New Lines.
	* Preferred Formats
		* `https://example.com/`
		* `http://example.com:8080`
		* `http://example.com`
	* Additional Formats
		* https://example.com/Default.aspx
		* https://example.com/ApplicationFolder/
1. Launch the nuclei scan ([`Active Scanning - Vulnerability Scanning` TTP](TTP/T1595_Active_Scanning/002_Vulnerability_Scanning/T1595.002.md))

	 	./nuclei -stats -no-color -c 5 -rl 300 -t nuclei-templates/  -l LIST_OF_URLS  -tags security-survey -interactsh-server 'https://interactsh-server.com' -interactsh-token "INTERACTSH_TOKEN" | tee scan_results.txt
	* Flags
		* Replace `BLS_INTERACTSH_TOKEN` placeholder with the authentication token for BLS's interactsh server.
		* Replace `LIST_OF_URLS` placeholder with the file name of the file containing the list of URLs to target during the scan.
		* `-stats` - Display results as they come in
		* `tee` - Sends the results to a text file called `scan_results.txt`
