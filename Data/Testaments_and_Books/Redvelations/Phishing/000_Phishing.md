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
# Phishing ([`Phishing` TTP](TTP/T1566_Phishing/T1566.md))
## Tags

<details><summary>Tags</summary><p>

		#@PHISHING

</p></details>

## References

* <details><summary>References (Click to expand)</summary><p>
	*  enigma0x3: Phishing for Credentials: If you want it, just ask! -<br />[https://enigma0x3.net/2015/01/21/phishing-for-credentials-if-you-want-it-just-ask/](https://enigma0x3.net/2015/01/21/phishing-for-credentials-if-you-want-it-just-ask/)
	* StackOverflow: Encode / Decode .EXE into Base64 -<br />[https://stackoverflow.com/questions/42592518/encode-decode-exe-into-base64/42592976](https://stackoverflow.com/questions/42592518/encode-decode-exe-into-base64/42592976)
	* Mike F Robins Blog: Simple Obfuscation with PowerShell using Base64 Encoding -<br />[https://mikefrobbins.com/2017/06/15/simple-obfuscation-with-powershell-using-base64-encoding/](https://mikefrobbins.com/2017/06/15/simple-obfuscation-with-powershell-using-base64-encoding/)
	* FortyNorthSecurity Github: Offensive Maldocs Presentation -<br />[https://github.com/FortyNorthSecurity/Presentations/blob/master/Offensive%20Maldocs%20in%202020.pdf](https://github.com/FortyNorthSecurity/Presentations/blob/master/Offensive%20Maldocs%20in%202020.pdf)
	*  -<br />[https://www.youtube.com/watch?v=RW5U9yxilf4](https://www.youtube.com/watch?v=RW5U9yxilf4)

## Guide 

1. <details><summary>Collect initial information on target (Click to expand) ([OSINT and Prep Guide](Testaments_and_Books/Redvelations/OSINT_and_Prep/000_OSINT_and_Prep.md))</summary><p>
	* Industry
	* Relationships
		* Customer types
		* Vendor types
	* Active Times
		* Check for holidays
	* Employee Names ([`Gather Victim Identity Information - Employee Names` TTP](TTP/T1589_Gather_Victim_Identity_Information/003_Employee_Names/))
		* LinkedIn
			* [https://github.com/joeyism/linkedin_scraper](https://github.com/joeyism/linkedin_scraper)
		* hunter.io
		* **credshed**
	* Email Addresses ([`Gather Victim Identity Information - Email Addresses` TTP](TTP/T1589_Gather_Victim_Identity_Information/002_Email_Addresses/))
1. <details><summary>Define social engineering premise (Click to expand)</summary><p>
	* Popular
		* Pursue details in Contact Us page as a potential B2B customer
		* Student pursuing internship with the target
1. <details><summary>Setup infrastructure (Click to expand)</summary><p>
	* Domain ([Domains Guide](Testaments_and_Books/Redvelations/OSINT_and_Prep/001-1_Phishing_Domains.md))
		* Domain Registrar
			* GoDaddy -<br />[https://www.godaddy.com/](https://www.godaddy.com/)
		* Reputation checking
			* brightcloud
	* Email ([Email Infrastructure Guide](Testaments_and_Books/Redvelations/OSINT_and_Prep/001-2_Phishing_Email_Infrastructure.md))
		* Tools
			* Mailinabox
	* Credential Capture ([Credential Infrastructure Guide](Testaments_and_Books/Redvelations/OSINT_and_Prep/001-3_Phishing_Credential_Infrastructure.md))
1. <details><summary>Gather additional information through social engineering (calls, emails) Send socially engineered emails to targets ([TTP](TTP/T1566_Phishing)) (Click to expand)</summary><p>
	* Information Gathering
1. <details><summary>Develop Payloads (Click to expand)</summary><p>
	* Payload Phishing
		* Develop malicious files ([TTP](TTP/T1566_Phishing/001_Spearphishing_Attachment/T1566.001.md)), ([`User Execution - Malicious File` TTP](TTP/T1204_User_Execution/002_Malicious_File/T1204.002.md))
			1. Develop Reverse Shell Payload
				* Windows
					* [Windows Reverse Shell Guide](Testaments_and_Books/Redvelations/Windows/004-1_Windows_Reverse_Shells.md)
						* See **Example Reverse Shells:** Phishing
					* [Windows Malware Guide](Testaments_and_Books/Redvelations/Windows/005-0_Malware.md)
						* Focus on the VBA Execution/Obfuscation
							* [VBA/VBS Execution Guide](Testaments_and_Books/Redvelations/Windows/002-3_VBA-VBS_Execution.md)
							* [VBA/VBS Obfuscation Guide](Testaments_and_Books/Redvelations/Windows/003-1_VBA-VBS_Obfuscation.md)
						* Consider persistence options
							* [Windows Persistence Guide](Testaments_and_Books/Redvelations/Windows/004-0_Windows_Persistence.md)
							* Outlook Rules ([TTP](TTP/T1137_Office_Application_Startup/005_Outlook_Rules/T1137.005.md))
				* Mac
				* Linux
			1. Obfuscate the files ([`Obfuscated Files or Information` TTP](TTP/T1027_Obfuscated_Files_or_Information/T1027.md))
				* Template Injection ([`Template Injection` TTP](TTP/T1221_Template_Injection/T1221.md))
				* Exploit the system to bypass security features ([`Exploitation for Defense Evasion` TTP](TTP/T1211_Exploitation_for_Defense_Evasion/T1211.md))
				* Process Injection ([`Process Injection` TTP](TTP/T1055_Process_Injection/T1055.md)) (and sub TTPs)
				* Trusted Developer Tools, MSBuild ([TTP](TTP/T1127_Trusted_Developer_Utilities_Proxy_Execution/001_MSBuild/T1127.001.md))
				* Execute through signed binaries (LOLBINs) ([`Signed Binary Proxy Execution` TTP](TTP/T1218_Signed_Binary_Proxy_Execution/T1218.md))
				* Install Root Certificate ([`Subvert Trust Controls - Install Root Certificate` TTP](TTP/T1553_Subvert_Trust_Controls/004_Install_Root_Certificate/T1553.004.md))
	* Credential Phishing
		* Develop phishing link ([TTP](TTP/T1566_Phishing/002_Spearphishing_Link/T1566.002.md)), ([`User Execution - Malicious Link` TTP](TTP/T1204_User_Execution/001_Malicious_Link/T1204.001.md))
			* Capture credentials through proxy (MitM Attack) ([TTP](TTP/T1557_Adversary-in-the-Middle/T1557.md))
			* Capture cookie through proxy (Steal Web Session Cookie) ([TTP](TTP/T1539_Steal_Web_Session_Cookie/T1539.md))
			* Capture user input ([TTP](TTP/T1056_Input_Capture/T1056.md))
1. <details><summary>Launch campaigns (Click to expand)</summary><p>
	* Phish for further information as campaigns develop ([`Phishing for Information` TTP](TTP/T1598_Phishing_for_Information/T1598.md))
		* Targeted Spearphishing
			* Attachment-based ([`Phishing for Information - Spearphishing Attachment` TTP](TTP/T1598_Phishing_for_Information/002_Spearphishing_Attachment/T1598.002.md))
			* Link-based ([`Phishing for Information - Spearphishing Link` TTP](TTP/T1598_Phishing_for_Information/003_Spearphishing_Link/T1598.003.md))
			* Service-based ([`Phishing for Information - Spearphishing Service` TTP](TTP/T1598_Phishing_for_Information/001_Spearphishing_Service/T1598.001.md))
	* Targeted campaigns with spearphishing
		* Attachment-based ([`Phishing - Spearphishing Attachment` TTP](TTP/T1566_Phishing/001_Spearphishing_Attachment/T1566.001.md))002_Spearphishing_Attachment/T1598.002.md))
		* Link-based ([`Phishing - Spearphishing Link` TTP](TTP/T1566_Phishing/002_Spearphishing_Link/T1566.002.md))
		* Using a service ([`Phishing for Information - Spearphishing Service` TTP](TTP/T1598_Phishing_for_Information/001_Spearphishing_Service/T1598.001.md))
		* Via a service ([`Phishing - Spearphishing via Service` TTP](TTP/T1566_Phishing/003_Spearphishing_via_Service/T1566.003.md))
	* Campaign Tracking
		* king phisher (Needs Research) -<br />[https://github.com/rsmusllp/king-phisher](https://github.com/rsmusllp/king-phisher)
		Define campaigns
		* Send malicious files to common group emails
			* Sometimes auto-uploads to ticket systems
			* Examples
				* `allcompany@domain.com`
					* Default O365 email address
					* Sends to all users in company if enabled
				* `ap@domain.com`
				* `accounts_payable@domain.com`
				* `helpdesk@domain.com`
				* `support@domain.com`
				* `help@domain.com`
1. <details><summary>Coerce User Interaction (Click to expand) ([`User Execution` TTP](TTP/T1204_User_Execution/T1204.md))</summary><p>
	* Active
		* Social Engineering
			* Phone Calls
			* Emails
	* Passive
		* Let existing premise unfold.
1. Monitor C2
1. <details><summary>Upon shell: Engage persistence (Click to expand)</summary><p>
	* [Windows Persistence Guide](Testaments_and_Books/Redvelations/Windows/004-0_Windows_Persistence.md)
		* schtasks
	* Outlook Rules ([TTP](TTP/T1137_Office_Application_Startup/005_Outlook_Rules/T1137.005.md))