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
# Active Directory Hardening
### Important Checks

* Harden GPOs ([Active Directory GPOs Guide](Testaments_and_Books/Blue_Testament/Active_Directory/004-0_Active_Directory_GPOs.md))
* Dangerous Account Setting Flags
	* Password not required for authentication (`PASSWD_NOTREQD`)
	* Password never expires (`.`)
* SPNs (Kerberoasting) ([Kerberoasting TTP](TTP/T1558_Steal_or_Forge_Kerberos_Tickets/003_Kerberoasting/T1558.003.md))
	* Reasons to target service accounts
		* Service Accounts are attractive targets for an attacker for multiple reasons including:
		* They are typically over privileged and provide access to High-value objects in the domain;
		* Passwords tend to be weak and easily guessed or cracked'
		* Passwords are not rotated as frequently as regular user accounts.
	* Recommendations
		* All service accounts should have STRONG randomly generated passwords of 28 characters or more; no dictionary words and a mixture of alphanumerics, upper case, lower case, and symbols.
		* Service account passwords should be periodically rotated (e.g. once every 12 months).
		* Service account passwords should be periodically audited for strength. Can Kerberoastable account password hashes be cracked in less than 72 hours on a reasonably resourced password cracking rig?
		* Unless it is absolutely required, service accounts should not be Domain Administrators or members of other High-Value Groups.
		* Minimize Local Administrator access for Kerberoastable accounts. Unless Local Administrator access is required for day-to-day operators, it should be removed. An attacker who is able to Kerberoast, crack, and compromise a Service Account immediately gains local administrative access to the Systems under the account. As a Local Administrator an attacker may escalate to SYSTEM-level privileges and gather credentials from running processes in memory. These credentials can then be leverage to move laterally to additional systems, escalate privileges, and/or access sensitive data.
* Special Accounts
	* Managed Service Accounts (MSA)
	* Group Managed Service Accounts (gMSA)
* <details><summary>Dangerous Group Membership (Click to expand)</summary><p>
	* Forest Root
		* ENTERPRISE ADMINS
			* Has full AD rights to every domain in the AD forest. It is granted this right through membership in the Administrators group in every domain in the forest.
		* SCHEMA ADMINISTRATORS
			* Has the ability to modify the Active Directory forest schema.
	* AD Group
		* ACCOUNT OPERATORS
			* Has the rights to modify accounts and groups in the domain. Also has the ability to log on to Domain Controllers by default (assigned via the Default Domain Controllers Policy GPO). This group cannot directly modify AD admin groups, though associated privileges provides a path for escalation to AD admin.
		* ADMINISTRATORS
			* The group that has default admin rights to Active Directory and Domain Controllers and provides these rights to Domain Admins and Enterprise Admins, as well as any other members.
		* BACKUP OPERATORS
			* Is granted the ability to logon to, shut down, and perform backup/restore operations on Domain Controllers (assigned via the Default Domain Controllers Policy GPO). This group cannot directly modify AD admin groups, though associated privileges provides a path for escalation to AD admin. Backup Operators have the ability to schedule tasks which may provide an escalation path. They also are able to clear the event logs on Domain Controllers.
		* CERTIFICATE PUBLISHERS
			* 
		* DNS ADMINS
			* has administrative access to Microsoft Active Directory DNS and is often granted the ability to logon to Domain Controllers.
			* By default, members of the DNSAdmins group are able to run a DLL on a Domain Controller which could provide privilege escalation to Domain Admin rights: https://medium.com/@esnesenon/feature-not-bug-dnsadmin-to-dc-compromise-in-one-line-a0f779b8dc83
		* DOMAIN ADMINS
			* The AD group that most people think of when discussing Active Directory administration. This group has full admin rights by default on all domain-joined servers and workstations, Domain Controllers, and Active Directory. It gains admin rights on domain-joined computers since when these systems are joined to AD, the Domain Admins group is added to the computer’s Administrators group.
		* DOMAIN CONTROLLERS
			* 
		* ENTERPRISE KEY ADMINISTRATORS
			* 
		* GROUP POLICY CREATOR OWNERS
			* 
		* KEY ADMINISTRATORS
			* 
		* PRINT OPERATORS
			* Is granted the ability to manage printers and load/unload device drivers on Domain Controllers as well as manage printer objects in Active Directory. By default, this group can logon to Domain Controllers and shut them down. This group cannot directly modify AD admin groups.
		* Remote Desktop Users
			* Is a domain group designed to easily provide remote access to systems. In many AD domains, this group is added to the “Allow log on through Terminal Services” right in the Default Domain Controllers Policy GPO providing potential remote logon capability to DCs.
		* SERVER OPERATORS
			* Is granted the ability to logon to, shut down, and perform backup/restore operations on Domain Controllers (assigned via the Default Domain Controllers Policy GPO). This group cannot directly modify AD admin groups, though associated privileges provides a path for escalation to AD admin.
* <details><summary>Unusual PrimaryGroup IDs (Click to expand)</summary><p>
	* The "primarygroupid" parameter for AD objects contains the RID (last digits of an SID, which is a unique identifier for an AD object) of the group targeted. This setting can be used by attackers to store hidden membership as this attribute is not often analyzed or reviewed. Unless there is a strong business-based justification, it is recommended to change the primary group id back to their default settings. 