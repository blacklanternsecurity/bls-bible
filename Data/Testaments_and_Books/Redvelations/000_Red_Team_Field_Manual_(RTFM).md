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
# Red Team Field Manual (RTFM)
## Preparation
### Linux

<details><summary>Linux Preparation</summary><p>

* Install go-lang manually
	1. Retrieve golang (set for v1.19, although if there's a way to target "latest," please let me know)-<br />[https://go.dev/doc/install](https://go.dev/doc/install)

			wget https://go.dev/dl/go1.19.linux-amd64.tar.gz
	1. Remove any existing golang and extract the downloaded files

			rm -rf /usr/local/go && tar -C /usr/local -xzf go1.19.linux-amd64.tar.gz
	1. Set your path variable so that the installed go binary and retrieved tools can easily be referenced. The format of the two commands are designed to support an installation of go tools as the root user.
		* user installation

				echo 'export PATH=$PATH:/usr/local/go/bin' >> /etc/profile
		* root installation

				echo 'export PATH=$PATH:/root/go/bin/' >> /etc/profile
		* Other options
			* You can also try updating your path through your shell's config
				* zsh

						echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.zshrc
* Install latest python manually
	1. apt package installation (Ubuntu-/Debian-based)

			sudo apt install python3 python3-venv python3-pip python3.9 python3.9-venv -y
* Install pipx manually
	1. Install pre-requisites. **python3.9** is included, as some tools rely on python newer than the current debian distributions produce.
		1. pipx installation

				sudo python3.9 -m pip install --user pipx
				python3.9 -m pipx ensurepath
	1. Close the terminal and open a new one so that the path variables are updated



</p></details>

## Initial Access

Some cases of initial access fall outside the means of a traditional pentest but are worth describing.

* Vendors and Third Parties( [`Trusted Relationship` ](TTP/T1199_Trusted_Relationship/T1199.md))
	* Vendors and third parties can be granted sensitive access. Attackers can abuse this trust to gain an initial foothold.
	* Software and dependencies can create a trust relationship where the company trusts the software to be secure, and an attacker exploits the relationship in a supply chain attack.
* Applications, Web
	* Threat actor may abuse client applications to gain access to the internal servers. ([`Exploitation for Client Execution` TTP](TTP/T1203_Exploitation_for_Client_Execution/T1203.md))
	* Different from the "Exploit Public Facing Application" TTP, adversaries may abuse client endpoints as the client visits the site. The adversary may already control the website that the victim is visiting as the abuse occurs. ([`Drive-by Compromise` TTP](TTP/T1189_Drive-by_Compromise/T1189.md))
* [`Supply Chain Compromise` TTP](TTP/T1195_Supply_Chain_Compromise/T1195.md)
	* Software compromise, including when an attacker replaces the purchase of a legitimate software with the attacker's own malicious software.
* [`Hardware Additions` TTP](TTP/T1200_Hardware_Additions/T1200.md)
	* A threat actor may introduce hardware such as a "HID" into the network to perform additional computational abilities (including keyboard/mouse capability) beyond just the addition of a malicious USB device.


## Collection

* Email Collection ([`Email Collection` TTP](TTP/T1114_Email_Collection/T1114.md))
	* Threat actors may collect emails available as a result of Business Email Compromise as a way to understand the business or potentially compromise sensitive information.
* [`Email Collection - Remote Email Collection` TTP](TTP/T1114_Email_Collection/002_Remote_Email_Collection/T1114.002.md)
* [`Data from Local System` TTP](TTP/T1005_Data_from_Local_System/T1005.md)
	* Threat actors may collect data from compromised systems


## Impact

Some cases of initial access fall outside the means of a traditional pentest but are worth describing.

* Malicious data encryption ([`Data Encrypted for Impact` TTP](TTP/T1486_Data_Encrypted_for_Impact/T1486.md))
	* Ransomware may lead to encrypted data essential for the business and cause an impact.
* Malicious altering of records ([`Data Manipulation - Stored Data Manipulation` TTP](TTP/T1565_Data_Manipulation/001_Stored_Data_Manipulation/T1565.001.md))
	* Threat actors may identify that sensitive business details are relied upon for their accuracy. Consequently, to impact the business negatively, or even for personal gain, the threat actor may change the records.
* Data Destruction ([`Data Destruction` TTP](TTP/T1485_Data_Destruction/T1485.md))
	* Threat actors may destroy data important to the business or otherwise benefitting the threat actor.
* Resource Hijacking ([`Resource Hijacking` TTP](TTP/T1496_Resource_Hijacking/T1496.md))
	* Threat actors may use compromised systems to provide the threat actors with additional resources, such as CPU and RAM. Example advantages would be in the case of using compromised systems for cryptocurrency mining.
* [`Transmitted Data Manipulation` TTP](TTP/T1565_Data_Manipulation/002_Transmitted_Data_Manipulation/T1565.002.md)
	* Data manipulated in transit by a threat actor
* [`Defacement - External Defacement` TTP](TTP/T1491_Defacement/002_External_Defacement/T1491.002.md)
	* A threat actor may manipulate external facing applications to cause business impact
* [`Inhibit System Recovery` TTP](TTP/T1490_Inhibit_System_Recovery/T1490.md)
	* A threat actor may destroy critical system components that inhibit any ability for the systems to be recovered after an attack
* [`System Shutdown/Reboot` TTP](TTP/T1529_System_Shutdown-Reboot/T1529.md)
	* A threat actor may attempt to disrupt network availability by turning systems off
* [`Endpoint Denial of Service` TTP](TTP/T1499_Endpoint_Denial_of_Service/T1499.md)
	* A theat actor may focus on a specific endpoint instead of the network and disrupt the endpoint's service
* [`Network Denial of Service` TTP](TTP/T1498_Network_Denial_of_Service/T1498.md)
	* A theat actor may focus on disrupting the entire network to impact the business


## Process

1. Perform Reconnaissance and OSINT Gathering ([Guide](Testaments_and_Books/Redvelations/OSINT_and_Prep/000_OSINT_and_Prep.md))
	* Map Attack Surface
		* Public IP Block
		* External Websites
		* Company Employees
1. Perform OSINT and Prepare ([OSINT and Preparation Guide](Testaments_and_Books/Redvelations/OSINT_and_Prep/000_OSINT_and_Prep.md))
	* Infrastructure ([Infrastructure Guide](Testaments_and_Books/Redvelations/OSINT_and_Prep/001-0_Infrastructure.md))
		* Phishing
			* [Domain Setup Guide](Testaments_and_Books/Redvelations/OSINT_and_Prep/001-1_Phishing_Domains.md)
			* [Email Infrastructure Guide](Testaments_and_Books/Redvelations/OSINT_and_Prep/001-2_Phishing_Email_Infrastructure.md)
			* [Credential Infrastructure Guide](Testaments_and_Books/Redvelations/OSINT_and_Prep/001-3_Phishing_Credential_Infrastructure.md)
1. Establish Initial Access
	* Web Exploitation ([Guide](Testaments_and_Books/Redvelations/Web/000_Web_App_Attack_Guide.md))
	* Phishing ([Guide](Testaments_and_Books/Redvelations/Phishing/000_Phishing.md))
	* Cloud
		* Azure ([Guide](Testaments_and_Books/Redvelations/Cloud/Azure/002-0_Azure_Initial_Access.md))
		* AWS ([Guide](Testaments_and_Books/Redvelations/Cloud/AWS/000_AWS.md))
		* Oracle ([Guide](Testaments_and_Books/Redvelations/Cloud/Oracle/Oracle_Cloud_Privesc.md))
	* WiFi ([Guide](Testaments_and_Books/Redvelations/WiFi/000_WiFi.md))
	* Authentication Bypasses
1. Establish command execution and reverse shells
	* OS
		* Windows Reverse Shells ([Guide](Testaments_and_Books/Redvelations/Windows/004-1_Windows_Reverse_Shells.md))
1. Perform Host-level Situational Awareness (SA)
	* OS
		* [Windows SA Guide](Testaments_and_Books/Redvelations/Windows/001-2_Windows_Situational_Awareness.md))
1. Prepare TTPs in response to SA
1. Establish persistence in the environment
	* OS
		* ([Windows Persistence Guide](Testaments_and_Books/Redvelations/Windows/004-0_Windows_Persistence.md))
		* ([Linux Persistence Guide](Testaments_and_Books/Redvelations/Linux/004_Linux_Persistence.md))
	* On-Prem
		* Active directory
	* Cloud
		* Azure ([Guide](Testaments_and_Books/Redvelations/Cloud/Azure/000-0_Azure_Overview.md))
		* AWS ([Guide](Testaments_and_Books/Redvelations/Cloud/AWS/000_AWS.md))
		* Oracle ([Guide](Testaments_and_Books/Redvelations/Cloud/Oracle/Oracle_Cloud_Privesc.md))
	* Applications
		* Web ([Guide](Testaments_and_Books/Redvelations/Web/000_Web_App_Attack_Guide.md))
1. Perform Environment-Level Situational Awareness
1. Examine and explore the environment
	* Discovery and Enumeration
		* OS
			* Windows ([Guide](Testaments_and_Books/Redvelations/Windows/001-0_Windows_Enumeration.md))
			* Linux ([Guide](Testaments_and_Books/Redvelations/Linux/005_Linux_PrivEsc.md))
		* On-Prem
			* Active Directory
		* Cloud
			* Azure ([Guide](Testaments_and_Books/Redvelations/Cloud/Azure/000-0_Azure_Overview.md))
			* AWS ([Guide](Testaments_and_Books/Redvelations/Cloud/AWS/000_AWS.md))
			* Oracle ([Guide](Testaments_and_Books/Redvelations/Cloud/Oracle/Oracle_Cloud_Privesc.md))
		* Applications
			* Web ([Guide](Testaments_and_Books/Redvelations/Web/000_Web_App_Attack_Guide.md))
	* Privilege Escalation, Lateral Movement
		* OS
			* Windows ([Guide](Testaments_and_Books/Redvelations/Windows/006-0_Windows_Privilege_Escalation.md))
			* Linux ([Guide](Testaments_and_Books/Redvelations/Linux/005_Linux_PrivEsc.md))
		* On-Prem
			* Active Directory
		* Cloud
			* Azure ([Guide](Testaments_and_Books/Redvelations/Cloud/Azure/004-0_Azure_Lateral_Movement.md))
			* AWS ([Guide](Testaments_and_Books/Redvelations/Cloud/AWS/000_AWS.md))
			* Oracle ([Guide](Testaments_and_Books/Redvelations/Cloud/Oracle/Oracle_Cloud_Privesc.md))
		* Applications
			* Web ([Guide](Testaments_and_Books/Redvelations/Web/000_Web_App_Attack_Guide.md))
	* Defense Evasion
		* OS
			* Windows ([Guide](Testaments_and_Books/Redvelations/Windows/003-0_Windows_Defense_Evasion.md))
			* Linux ([Guide](Testaments_and_Books/Redvelations/Linux/003_Linux_Defense_Evasion.md))
		* On-Prem
			* Active Directory
		* Cloud
			* Azure ([Guide](Testaments_and_Books/Redvelations/Cloud/Azure/000-0_Azure_Overview.md))
			* AWS ([Guide](Testaments_and_Books/Redvelations/Cloud/AWS/000_AWS.md))
			* Oracle ([Guide](Testaments_and_Books/Redvelations/Cloud/Oracle/Oracle_Cloud_Privesc.md))
		* Applications
			* Web ([Guide](Testaments_and_Books/Redvelations/Web/000_Web_App_Attack_Guide.md))
1. Identify high value content. Collect and retrieve data from the systems and environment. ([TTP](TTP/T1083_File_and_Directory_Discovery/T1083.md))
1. Identify Impacts: IT and Business ([Guide](Testaments_and_Books/Purplippians/Impact/Impact.md))
1. Review results
	1. Revisit attack paths to identify, "Greatest potential impact for the least amount of effort"