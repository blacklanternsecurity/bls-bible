# Cisco
## Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@app #@apps #@application #@applications

Context

		#@cisco

Tools

		#@SeeYouCMThief #@See #@You #@CM #@Thief

</p></details>

## Attacks
* <details><summary>SeeYouCM-Thief (Click to expand) -<br />[https://github.com/trustedsec/SeeYouCM-Thief](https://github.com/trustedsec/SeeYouCM-Thief)</summary><p>
	* References
		* [https://www.trustedsec.com/blog/seeyoucm-thief-exploiting-common-misconfigurations-in-cisco-phone-systems/](https://www.trustedsec.com/blog/seeyoucm-thief-exploiting-common-misconfigurations-in-cisco-phone-systems/)
	* Examples
		* Example 1: User Enumeration

				./thief.py -H <CUCM server> --userenum
		* Example 2: Standard use

				./thief.py -H <Cisco CUCM Server>
			* "Sometimes the CUCM server supplies a list of hostnames. Without specifying a phone IP address the script will attempt to download every config in the listing."
		* Example 3: 

				./thief.py --phone <Cisco IP Phoner> [--verbose]
			* "if that doesnt work try using the --phone setting which will parse the web interface for the CUCM address and will do a reverse lookup for other phones in the same subnet."
		* Example 4: 

				./thief.py --subnet <subnet to scan> [--verbose]
			* if that doesnt work you can specify a subnet to scan with reverse lookups using
