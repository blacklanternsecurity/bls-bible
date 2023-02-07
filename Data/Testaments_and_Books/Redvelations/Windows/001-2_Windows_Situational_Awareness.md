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
# Windows Situational Awareness

## Overview


## Process
1. Enumerate the Environment
	1. Identify System Information (Hostname, Logged on users, OS Version, Virtual Environment, Patch Level) ([TTP](TTP/T1082_System_Information_Discovery/T1082.md))
	1. Examine Mapped and Local Drives ([TTP](TTP/T1135_Network_Share_Discovery/T1135.md))
	1. Examine the Network
		1. Dump arp cache ([TTP](TTP/T1049_System_Network_Connections_Discovery/T1049.md))
		1. List network connections ([TTP](TTP/T1049_System_Network_Connections_Discovery/T1049.md))
		1. Dump networking config ([TTP](TTP/T1049_System_Network_Connections_Discovery/T1049.md))
		1. Dump the DNS cache ([TTP](TTP/T1049_System_Network_Connections_Discovery/T1049.md))
		1. Name Servers ([TTP](TTP/T1049_System_Network_Connections_Discovery/T1049.md))
	1. System uptime ([TTP](TTP/T1082_System_Information_Discovery/T1082.md))
	1. Enumerate Domain Information
		1. Domain Name ([TTP](TTP/T1069_Permission_Groups_Discovery/002_Domain_Groups/T1069.002.md))
		1. Domain Controllers ([TTP](TTP/T1087_Account_Discovery/002_Domain_Account/T1087.002.md))
		1. Password Policy / Lockout ([TTP](TTP/T1201_Password_Policy_Discovery/T1201.md))
	1. Create a recursive directory listing file ([TTP](TTP/T1083_File_and_Directory_Discovery/T1083.md))
1. Check Defenses
	1. Running AV/EDR Processes ([TTP](TTP/T1518_Software_Discovery/001_Security_Software_Discovery/T1518.001.md))
	1. Credential Guard ([TTP](TTP/T1518_Software_Discovery/001_Security_Software_Discovery/T1518.001.md))
	1. Application Whitelisting enabled
1. Permissions
	1. List running tasks and check integrity levels ([TTP](TTP/T1057_Process_Discovery/T1057.md))
	1. Local and Domain Permissions
		1. Domain Admins ([TTP](TTP/T1087_Account_Discovery/002_Domain_Account/T1087.002.md))
		1. Group Policy Information ([TTP](TTP/T1069_Permission_Groups_Discovery/002_Domain_Groups/T1069.002.md))
		1. Current user ([TTP](TTP/T1033_System_Owner-User_Discovery/T1033.md))
1. Software:
	1. Check installed software
		1. Overall ([TTP](TTP/T1518_Software_Discovery/T1518.md))
		1. Installed browsers ([TTP](TTP/T1518_Software_Discovery/T1518.md))
		1. Password management Utilities ([TTP](TTP/T1518_Software_Discovery/T1518.md))
1. Persist
	1. Create a scheduled task ([TTP](TTP/T1053_Scheduled_Task-Job/T1053.md))
	1. If the account is an administrator, add a backdoor user ([TTP](TTP/T1136_Create_Account/001_Local_Account/T1136.001.md))