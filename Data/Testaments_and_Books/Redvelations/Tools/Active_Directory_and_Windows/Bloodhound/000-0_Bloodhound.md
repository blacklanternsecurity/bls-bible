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
# Bloodhound
## References

* <details><summary>References (Click to expand)</summary><p>
	* MITRE ATT&CK: Account Discovery: Local Account -<br />[https://attack.mitre.org/techniques/T1087/001](https://attack.mitre.org/techniques/T1087/001) BloodHound can identify users with local administrator rights.
	* MITRE ATT&CK: Account Discovery: Domain Account -<br />[https://attack.mitre.org/techniques/T1087/002](https://attack.mitre.org/techniques/T1087/002) BloodHound can collect information about domain users, including identification of domain admin accounts.
	* MITRE ATT&CK: Archive Collected Data -<br />[https://attack.mitre.org/techniques/T1560](https://attack.mitre.org/techniques/T1560) BloodHound can compress data collected by its SharpHound ingestor into a ZIP file to be written to disk.
	* MITRE ATT&CK: Command and Scripting Interpreter: PowerShell -<br />[https://attack.mitre.org/techniques/T1059](https://attack.mitre.org/techniques/T1059) BloodHound can use PowerShell to pull Active Directory information from the target environment.
	* MITRE ATT&CK: Domain Trust Discovery -<br />[https://attack.mitre.org/techniques/T1482](https://attack.mitre.org/techniques/T1482) BloodHound has the ability to map domain trusts and identify misconfigurations for potential abuse.
	* MITRE ATT&CK: Native API -<br />[https://attack.mitre.org/techniques/T1560](https://attack.mitre.org/techniques/T1106) BloodHound can use .NET API calls in the SharpHound ingestor component to pull Active Directory data.
	* MITRE ATT&CK: Password Policy Discovery -<br />[https://attack.mitre.org/techniques/T1560](https://attack.mitre.org/techniques/T1201) BloodHound can collect password policy information on the target environment.
	* MITRE ATT&CK: Permission Groups Discovery: Local Groups -<br />[https://attack.mitre.org/techniques/T1560](https://attack.mitre.org/techniques/T1069/001) BloodHound can collect information about local groups and members.
	* MITRE ATT&CK: Permission Groups Discovery: Domain Groups -<br />[https://attack.mitre.org/techniques/T1560](https://attack.mitre.org/techniques/T1069/002) BloodHound can collect information about domain groups and members.
	* MITRE ATT&CK: Remote System Discovery -<br />[https://attack.mitre.org/techniques/T1560](https://attack.mitre.org/techniques/T1018) BloodHound can enumerate and collect the properties of domain computers, including domain controllers.
	* MITRE ATT&CK: System Owner/User Discovery -<br />[https://attack.mitre.org/techniques/T1560](https://attack.mitre.org/techniques/T1033) BloodHound can collect information on user sessions.
	* MITRE ATT&CK: Account Discovery: Local Account -<br />[https://attack.mitre.org/techniques/T1087/001](https://attack.mitre.org/techniques/T1087/001)
	* MITRE ATT&CK: Account Discovery: Domain Account -<br />[https://attack.mitre.org/techniques/T1087/002](https://attack.mitre.org/techniques/T1087/002)
	* MITRE ATT&CK: Archive Collected Data -<br />[https://attack.mitre.org/techniques/T1560](https://attack.mitre.org/techniques/T1560)
	* MITRE ATT&CK: Command and Scripting Interpreter: PowerShell -<br />[https://attack.mitre.org/techniques/T1059](https://attack.mitre.org/techniques/T1059)
	* MITRE ATT&CK: Domain Trust Discovery -<br />[https://attack.mitre.org/techniques/T1482](https://attack.mitre.org/techniques/T1482)
	* MITRE ATT&CK: Native API -<br />[https://attack.mitre.org/techniques/T1560](https://attack.mitre.org/techniques/T1106)
	* MITRE ATT&CK: Password Policy Discovery -<br />[https://attack.mitre.org/techniques/T1560](https://attack.mitre.org/techniques/T1201)
	* MITRE ATT&CK: Permission Groups Discovery: Local Groups -<br />[https://attack.mitre.org/techniques/T1560](https://attack.mitre.org/techniques/T1069/001)
	* MITRE ATT&CK: Permission Groups Discovery: Domain Groups -<br />[https://attack.mitre.org/techniques/T1560](https://attack.mitre.org/techniques/T1069/002)
	* MITRE ATT&CK: Remote System Discovery -<br />[https://attack.mitre.org/techniques/T1560](https://attack.mitre.org/techniques/T1018)
	* MITRE ATT&CK: System Owner/User Discovery -<br />[https://attack.mitre.org/techniques/T1560](https://attack.mitre.org/techniques/T1033)

## Overview

* <details><summary>Overview (Click to expand)</summary><p>
	* Bloodhound is a tool that can extract information about a Windows Domain.
	* From regular user context, a user can extract current sessions and other information regarding the Domain to identify the fastest way to achieve Domain Admin.
	* It identifies Domain Trusts, current sessions, which user has domain on a machine, and other useful information to better plan an attack against a Domain.
	* This tool is popular for collecting data 
	* This technique is **optional-recommended** for the Discovery phase. This comes after access to the network is already established, and some form of initial access has been achieved with a Domain User Account.
	* Information from this technique can be used to improve the password spraying ([TTP](TTP/T1110_Brute_Force/003_Password_Spraying/T1110.003.md))

## Extracting Bloodhound Data

* Ingestor information is currently kept primarily in the [Active Directory LDAP Enumeration Guide](Testaments_and_Books/Redvelations/Active_Directory/001-2_LDAP_Enumeration.md)
* Other information will be stored in the [BloodHound Ingestors Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/002-0_Ingestors.md)

## Importing / Viewing Bloodhound Data

* <details><summary>Process (Click to expand)</summary><p>
	1. On your linux machine with Neo4j Installed and Bloodhound, copy over the CSV files.
		* You can run Bloodhound by going to the Bloodhound git repo and running the Bloodhound-x64 bin file. You can manually compile, but with the latest release of Bloodhound, they have precompiled bin's for linux.
	
				BloodHound/Bloodhound-linux-x64/Bloodhound
	1. This will launch a GUI, which you will enter the database URL as: bolt://localhost:7687
		* User: `neo4j`
		* password:`<password>`
	1. Once Bloodhound has logged into the server, if there is test data in the database, you can clear it with the button on the left. After it's cleared, import the CSV files (Button on the right), and you will import the typical 3 CSV files.
	1. After they have imported, you can then run queries for finding the fastest way to Admin, current sessions open, etc. These queries can be found on the top left menu context.

## Extract users with jq

* <details><summary>Examples (Click to expand)</summary><p>
	1. All users

			jq .users[].Properties.name users.json | tr -d '"' | tr '[:upper:]' '[:lower:]' | sort -u
	1. Enabled only

			jq '.users[].Properties | select(.enabled == true) | .name' users.json | tr -d '"' | tr '[:upper:]' '[:lower:]' | sort -u
	1. Extract servers

			jq '.computers[].Properties | select(.distinguishedname | contains("Server")) | .name' computers.json | tr -d '"' | tr '[:upper:]' '[:lower:]' | sort -u

## Bloodhound Tips and Tricks

* Mark as owned programmatically
	* Cypher Query

			LOAD CSV FROM "file:///cracked-users.csv" AS line MERGE (u:User {name: toUpper(line[0])}) ON MATCH SET u.owned = 1
	    * Note: 'name' is case sensitive
	    * `cracked-users.csv` came from `hashcat --show | awk -F: '{print $1}`
	* Tool
		* Bloodhound-Owned -<br />[https://github.com/porterhau5/BloodHound-Owned](https://github.com/porterhau5/BloodHound-Owned)
			* Command

					ruby bh-owned.rb -u neo4j -p bloodhoundpassword -a <user_file>