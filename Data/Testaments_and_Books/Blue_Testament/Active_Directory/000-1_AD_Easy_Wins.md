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
# Active Directory Easy Wins
### References

* <details><summary>References (Click to expand)</summary><p>
	* Reference 1 -<br />[HTTP](HTTP)
	* Reference 2 -<br />[HTTP](HTTP)
	* Note to Brian: References placed here are for total hardening guides that cover all areas. My current strategy is to include, if necessary, links in the same format in above bullet point within the specific sections. So, links to blogs/tools that deserve credit for the ideas, etc.
</p></details>

### Easy Wins

1. <details><summary>GPO Hardening (Click to expand)</summary><p>
	1. <details><summary>View Effective GPOs (Click to expand)</summary><p>
		1. <details><summary>Optional: Export GPO HTML (Click to expand)</summary><p>
			1. On the DC, open "GPO Manager"
			1. Navigate to the enforced domain policies
			1. Right-click export
	1. <details><summary>Analyze GPOs for missing  for gaps between recommended and existing (Click to expand)</summary><p>
		* <details><summary>Recommended GPOs (Click to expand)</summary><p>
			* <details><summary>Logging (Click to expand)</summary><p>
			* <details><summary>Authentication (or, maybe, "Network"?) (Click to expand)</summary><p>
				* <details><summary>Enable SMB Signing (Click to expand)</summary><p>
					* `GPO/Located/Here/EndWithGPOName`
				* <details><summary>Enable LDAP Signing (Click to expand)</summary><p>
					* <details><summary>Client (Click to expand)</summary><p>
						* `GPO/Located/Here/EndWithGPOName`
					* <details><summary>Server (Click to expand)</summary><p>
						* `GPO/Located/Here/EndWithGPOName`
		* <details><summary>Default Insecure Configurations (Click to expand)</summary><p>
1. <details><summary>Log Enabling (Click to expand)</summary><p>
	1. <details><summary>Retrieve Asset Inventory (Click to expand)</summary><p>
		* Domain Controllers
		* Workstations
		* Servers
		* Note Firewall-separated VLANS
	1. <details><summary>Analyze Discrepancies in devices connected to central SIEM (Click to expand)</summary><p>
		* <details><summary>FortiSIEM (Click to expand)</summary><p>

				SCRIPT TO DEPLOY. In GUI, renders as click-to-copy line.
			* Flag Information
				* Required
					* `-A`
				* Optional
					* `-F`
1. <details><summary>Establish a Baseline (Click to expand)</summary><p>
	1. Record logs over the course of a month
	1. Record network traffic over a month
1. <details><summary>Implement Firewall Rules (Click to expand)</summary><p>
	1. <details><summary>Recommended for most situations (Click to expand)</summary><p>
		* Block outgoing SMB
	1. Use baseline to restrict
	1. Block traffic between VLANs
	1. Block most traffic to critical app servers
1. <details><summary>Threat Hunting (Click to expand)</summary><p>
	1. <details><summary>Enable/Collect Logs (Click to expand)</summary><p>
		1. <details><summary>GPO (Click to expand)</summary><p>
			* See GPO Hardening above
		1. <details><summary>SIEM (Click to expand)</summary><p>
			* Splunk
				* Enable by
			* FortiSIEM
				* Enable by
		1. <details><summary>Other (Click to expand)</summary><p>
			* Info
	1. <details><summary>Search for common threat vectors (Click to expand)</summary><p>
		* <details><summary>Specific Exploitation (Click to expand)</summary><p>
			* <details><summary>Kerberoasting (Click to expand)</summary><p>
				* <details><summary>Overview (Click to expand)</summary><p>
					* `Event ID 1234`
					* Expect logs of rapid SPN 
				* <details><summary>Splunk (Click to expand)</summary><p>

						SCRIPT TO DEPLOY. In GUI, renders as click-to-copy line.
					* Flag Information
						* Required
							* `-A`
						* Optional
							* `-F`
				* <details><summary>FortiSIEM (Click to expand)</summary><p>

						SCRIPT TO DEPLOY. In GUI, renders as click-to-copy line.
			* <details><summary>ZeroLogon (Click to expand)</summary><p>
				* <details><summary>Overview (Click to expand)</summary><p>
					* `Event ID 1234`
				* <details><summary>Splunk (Click to expand)</summary><p>

						SCRIPT TO DEPLOY. In GUI, renders as click-to-copy line.
					* Flag Information
						* Required
							* `-A`
						* Optional
							* `-F`
				* <details><summary>FortiSIEM (Click to expand)</summary><p>

						SCRIPT TO DEPLOY. In GUI, renders as click-to-copy line.
					* Flag Information
						* Required
							* `-A`
						* Optional
							* `-F`
		* <details><summary>Enumeration (Click to expand)</summary><p>
			* <details><summary>Logged On or Session Data Collection (Click to expand)</summary><p>
				* <details><summary>Overview (Click to expand)</summary><p>
					* Example red team tools are Bloodhound/Sharphound
					* `Event ID 1234`
				* <details><summary>Splunk (Click to expand)</summary><p>

						SCRIPT TO DEPLOY. In GUI, renders as click-to-copy line.
					* Flag Information
						* Required
							* `-A`
						* Optional
							* `-F`
				* FortiSIEM

						SCRIPT TO DEPLOY. In GUI, renders as click-to-copy line.
					* Flag Information
						* Required
							* `-A`
						* Optional
							* `-F`
			* <details><summary>Password Spraying (Click to expand)</summary><p>
			* <details><summary>Username Enumeration (Click to expand)</summary><p>
				* <details><summary>Other (Click to expand)</summary><p>Overview
					* May take the form of RID bruteforce 

		* <details><summary>Lateral Movement (Click to expand)</summary><p>
			* <details><summary>Workstation-to-Workstation Movement (Click to expand)</summary><p>
				* `Event ID 1234`
			* <details><summary>Abnormal DC Sessions (Click to expand)</summary><p>
			* <details><summary>Other (Click to expand)</summary><p>FortiSIEM

					SCRIPT TO DEPLOY. In GUI, renders as click-to-copy line.
				* Flag Information
					* Required
						* `-A`
					* Optional
						* `-F`
		* <details><summary>Exfiltraton (Click to expand)</summary><p>
			* `Event ID 1234`
			* <details><summary>Other (Click to expand)</summary><p>Splunk

					SCRIPT TO DEPLOY. In GUI, renders as click-to-copy line.
				* Flag Information
					* Required
						* `-A`
					* Optional
						* `-F`
			* <details><summary>Other (Click to expand)</summary><p>FortiSIEM

					SCRIPT TO DEPLOY. In GUI, renders as click-to-copy line.
				* Flag Information
					* Required
						* `-A`
					* Optional
						* `-F`

</p></details>