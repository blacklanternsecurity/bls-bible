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
# Active Directory GPOs
### References
* [https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/user-rights-assignment](https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/user-rights-assignment)

### GPO Guide
* <details><summary>Overview (Click to expand)</summary><p>
	* User Configuration: Holds settings applied to users (at sign-in and during periodic background refresh)
	* Computer Configuration: Holds settings applied to computers (at startup and during periodic background refresh)
* Computer Configuration
	* <details><summary>Windows Settings (Click to expand)</summary><p>
		* <details><summary>Security Settings (Click to expand)</summary><p>
			* <details><summary>Account Policies (Click to expand)</summary><p>
				* <details><summary>Password Policy (Click to expand) ([`Brute Force` TTP](TTP/T1110_Brute_Force/T1110.md), [`Brute Force - Password Cracking` TTP](TTP/T1110_Brute_Force/002_Password_Cracking/T1110.002.md), [`Brute Force - Password Spraying` TTP](TTP/T1110_Brute_Force/003_Password_Spraying/T1110.003.md))</summary><p>
					* Enforce Password History: 24 or more passwords
					* Maximum Password Age: 60 or fewer days, but not 0
					* Minimum Password Age: 1 or more day(s)
					* Minimum Password Length: 14 or more characters
					* Password must meet complexity requirements: Enabled
					* Store passwords using reversible encryption: Disabled
				* <details><summary>Kerberos Policy (Click to expand)</summary><p>
					* Enforce user logon restrictions
						* Enabled (default)
					* Maximum lifetime for service ticket
						* 600 minutes (default)
					* Maximum lifetime for user ticket
						* 10 hours (default)
					* Maximum lifetime for user ticket renewal
						* 7 days (default)
					* Maximum tolerance for computer clock synchronization
						* 5 minutes (default)
			* <details><summary>Advanced Audit Policy Configuration (Click to expand)</summary><p>
				* <details><summary>Audit Policies (Click to expand)</summary><p>
					* <details><summary>Account Logon (Click to expand)</summary><p>
						* Reports each instance of a security principal (for example, user, computer, or service account) that is logging on to or logging off from one computer in which another computer is used to validate the account, this includes authentication events performed by a Domain Controller (DC). Local logons are tracked under a different category. This category can generate a lot of noise, but as highlighted in the following comments, these logs can be essential for investigating a security incident.
						* Credential Validation
							* BLSOPS: Success/Failure
							* Microsoft Best Practices: Success (Default)
							* Malware Archaeology: Success/Failure
							* CIS: Success/Failure
						* Kerberos Authentication Service
							* BLSOPS: Success/Failure
							* Microsoft Best Practices: Success/Failure (Adv)
							* Malware Archaeology: Success/Failure (Adv)
							* CIS: Success/Failure
						* Kerberos Service Ticket Operations
							* BLSOPS: Success/Failure
							* Microsoft Best Practices: Microsoft Best Practices: Success/Failure (Adv)
							* Malware Archaeology: Success/Failure (Adv)
							* CIS: Success/Failure
						* Other Account Logon Events
							* BLSOPS: Success/Failure
							* Microsoft Best Practices: Success/Failure (Adv)
							* Malware Archaeology: Success/Failure
							* CIS: N/A
					* <details><summary>Account Management (Click to expand)</summary><p>
						* Determines whether to track management of users and groups (creation, modifications, and deletion events). These events are extremely important for incident response and post-mortem security investigations.
						* Application Group Management
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing (Default)
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: Success/Failure
						* Computer Account Management
							* BLSOPS: Success
							* Microsoft Best Practices: Success (Default)
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: Success
						* Distribution Group Management
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing (Default)
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: Success
						* Other Acct Management Events
							* BLSOPS: Success
							* Microsoft Best Practices: Success
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: Success
						* Security Group Management
							* BLSOPS: Success
							* Microsoft Best Practices: Success (Default)
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: Success
						* User Account Management
							* BLSOPS: Success/Failure
							* Microsoft Best Practices: Success (Default)
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: Success/Failure
					* <details><summary>Detailed Tracking (Click to expand)</summary><p>
						* Determines whether to audit detailed process tracking information for events such as program activation, process exit, handle duplication, and indirect object access. This category is useful for tracking malicious users and the programs that they use. Enabling Audit Process Tracking generates a large number of events, so typically it is set to No Auditing by most organizations. However, this setting can provide a great benefit during an incident response from the detailed log of the processes started and the time they were launched. For domain controllers and other single-role infrastructure servers, this category can be safely turned on all the time. Single role servers do not generate much process tracking traffic during the normal course of their duties. As such, they can be enabled to capture unauthorized events if they occur.
						* DPAPI Activity
							* BLSOPS: No Auditing
							* Microsoft Best Practices: Success\Failure (Adv)
							* Malware Archaeology: No Auditing
							* CIS Benchmarks: N/A
						* Plug and Play
							* BLSOPS: Success
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: Success
							* CIS Benchmarks: N/A
						* Process Creation
							* BLSOPS: Success
							* Microsoft Best Practices: Success
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: Success
						* Process Termination
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: Success (Adv)
							* CIS Benchmarks: N/A
						* RPC Events
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: N/A
						* Token Right Adjusted Events
							* BLSOPS: Success
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: Success
							* CIS Benchmarks: N/A
					* <details><summary>DS Access (Click to expand)</summary><p>
						* Microsoft does not provide much guidance on these settings in their best practices guidelines. This setting's category determines whether to audit security principal access to an Active Directory object that has its own specified system access control list (SACL). In general, this category of policies should only be enabled on domain controllers.
						* Detailed Directory Service Replication
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: No Auditing
							* CIS Benchmarks: N/A
						* Directory Service Access
							* BLSOPS: Success
							* Microsoft Best Practices: No Auditing
							* Success/Failure (Adv)
							* CIS Benchmarks: Failure
						* Directory Service Changes
							* BLSOPS: Success
							* Microsoft Best Practices: No Auditing (Default)
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: Success
						* Directory Service Replication
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing
							* Success/Failure (Adv)
							* CIS Benchmarks: N/A
					* <details><summary>Logon/Logoff (Click to expand)</summary><p>
						* Logon/Logoff events are generated when a local security principal is authenticated on a local computer.
						* Account Lockout ([`Brute Force` TTP](TTP/T1110_Brute_Force/T1110.md), [`Brute Force - Password Spraying` TTP](TTP/T1110_Brute_Force/003_Password_Spraying/T1110.003.md), [`Brute Force - Credential Stuffing` TTP](TTP/T1110_Brute_Force/004_Credential_Stuffing/T1110.004.md))
							* BLSOPS: Success
							* Microsoft Best Practices: Success (Default)
							* Malware Archaeology: Success
							* CIS Benchmarks: Failure
						* Group Membership
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: Success
							* CIS Benchmarks: N/A
						* IPsec Extended Mode
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: No Auditing
							* CIS Benchmarks: N/A
						* IPsec Main Mode
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: No Auditing
							* CIS Benchmarks: N/A
						* IPsec Quick Mode
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: No Auditing
							* CIS Benchmarks: N/A
						* Logoff
							* BLSOPS: Success
							* Microsoft Best Practices: Success (Default)
							* Malware Archaeology: Success
							* CIS Benchmarks: Success
						* Logon
							* BLSOPS: Success/Failure
							* Microsoft Best Practices: Success/Failure (Default)
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: Success/Failure
						* Network Policy Server
							* BLSOPS: Success/Failure
							* Microsoft Best Practices: Success/Failure (Default)
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: N/A
						* Other Logon/Logoff Events
							* BLSOPS: Success
							* Microsoft Best Practices: No Auditing (Default)
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: Success/Failure
						* Special Logon
							* BLSOPS: Success
							* Microsoft Best Practices: Success (Default)
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: Success
						* User / Device Claims
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: No Auditing
							* CIS Benchmarks: N/A
					* <details><summary>Object Access (Click to expand)</summary><p>
						* No Microsoft recommendations are provided for this settings category. Object Access can generate events when subsequently defined objects with auditing enabled are accessed (for example, Opened, Read, Renamed, Deleted, or Closed). After the main auditing category is enabled, the administrator must individually define which objects will have auditing enabled. Many Windows system objects come with auditing enabled, so enabling this category will usually begin to generate events before the administrator has defined any.
						* Application Generated
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: N/A
						* Certification Services
							* BLSOPS: Success/Failure
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: N/A
						* Central Policy Staging
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: No Auditing
							* CIS Benchmarks: N/A
						* Detailed File Share
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing (Default)
							* Malware Archaeology: Success
							* CIS Benchmarks: Failure
						* File Share
							* BLSOPS: Success/Failure (As needed)
							* Microsoft Best Practices: No Auditing (Default)
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: Success/Failure
						* File System
							* BLSOPS: Success (As needed)
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: Success
							* CIS Benchmarks: N/A
						* Filtering Platform Connection
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: Success (Adv)
							* CIS Benchmarks: N/A
						* Filtering Platform Packet Drop
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: Success (Adv)
							* CIS Benchmarks: N/A
						* Handle Manipulation
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: Success (Adv)
							* CIS Benchmarks: N/A
						* Kernel Object
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: No Auditing
							* CIS Benchmarks: N/A
						* Other Object Access Events
							* BLSOPS: Success (As needed)
							* Microsoft Best Practices: No Auditing (Default)
							* Success/Failure (Adv)
							* CIS Benchmarks: Success/Failure
						* Removable Storage
							* BLSOPS: Success/Failure
							* Microsoft Best Practices: No Auditing (Default)
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: Success/Failure
						* Registry
							* BLSOPS: Success (As needed)
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: Success
							* CIS Benchmarks: N/A
						* SAM
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: Success
							* CIS Benchmarks: N/A
					* <details><summary>Policy Change (Click to expand)</summary><p>
						* This policy setting determines whether to audit every incidence of a change to user rights assignment policies, Windows Firewall policies, Trust policies, or changes to the audit policy. This category should be enabled on all computers. It generates very little noise.
						* Audit Policy Change
							* BLSOPS: Success/Failure
							* Microsoft Best Practices: Success/Failure
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: Success
						* Authentication Policy Change
							* BLSOPS: Success/Failure
							* Microsoft Best Practices: Success (Default)
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: Success
						* Authorization Policy Change
							* BLSOPS: Success/Failure
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: Success
						* Filtering Platform Policy Change
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: Success
							* CIS Benchmarks: N/A
						* MPSSVC Rule-Level Policy Change
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing (Default)
							* Malware Archaeology: No Auditing
							* CIS Benchmarks: Success/Failure
						* Other Policy Change Events
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing (Default)
							* Malware Archaeology: No Auditing
							* CIS Benchmarks: Failure
					* <details><summary>Privilege Use (Click to expand)</summary><p>
						* There are dozens of user rights and permissions in Windows (for example, Logon as a Batch Job and Act as Part of the Operating System). This policy setting determines whether to audit each instance of a security principal exercising a user right or privilege. Enabling this category results in a lot of "noise," but it can be helpful in tracking security principal accounts using elevated privileges when properly tuned.
						* Non Sensitive Privilege Use
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: No Auditing
							* CIS Benchmarks: N/A
						* Other Privilege Use Events
							* BLSOPS: No Auditing
							* Microsoft Best Practices: No Auditing
							* Malware Archaeology: No Auditing
							* CIS Benchmarks: N/A
						* Sensitive Privilege Use
							* BLSOPS: Success/Failure
							* Microsoft Best Practices: No Auditing (Default)
							* Malware Archaeology: Success/Failure
						* CIS Benchmarks: Success/Failure
					* <details><summary>System (Click to expand)</summary><p>
						* This subcategory is almost a generic catch-all category, registering various events that impact the computer, its system security, or the security log. It includes events for computer shutdowns and restarts, power failures, system time changes, authentication package initializations, audit log clearings, impersonation issues, and a host of other general events. In general, enabling this audit category generates a lot of "noise," but it generates enough very useful events that it is difficult to ever recommend not enabling it.
						* IPsec Driver
							* BLSOPS: Success
							* Microsoft Best Practices: Success/Failure
							* Malware Archaeology: Success (Adv)
							* CIS Benchmarks: Success/Failure
						* Other System Events
							* BLSOPS: Failure
							* Microsoft Best Practices: Success/Failure (Default)
							* Malware Archaeology: Failure (Adv)
							* CIS Benchmarks: Success/Failure
						* Security State Change
							* BLSOPS: Success/Failure
							* Microsoft Best Practices: Success/Failure
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: Success
						* Security System Extension
							* BLSOPS: Success/Failure
							* Microsoft Best Practices: Success/Failure
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: Success
						* System Integrity
							* BLSOPS: Success/Failure
							* Microsoft Best Practices: Success/Failure (Default)
							* Malware Archaeology: Success/Failure
							* CIS Benchmarks: Success/Failure
			* <details><summary>Local Policies (Click to expand)</summary><p>
				* <details><summary>Security Options (Click to expand)</summary><p>
					* <details><summary>Accounts (Click to expand)</summary><p>
					 	* Administrator account status ([`Valid Accounts - Default Accounts` TTP](TTP/T1078_Valid_Accounts/001_Default_Accounts/T1078.001.md))
							* Recommended Setting: N/A
							* Disabling the administrator account can become a maintenance issue under certain circumstances. For example, in a domain environment, if the secure channel that constitutes your connection fails for any reason, and there is no other local administrator account, you must restart the computer in safe mode to fix the problem that broke your connection status.
						* Block Microsoft accounts
							* Recommended Setting: Users can't add or log on with Microsoft accounts
							* Organizations that want to effectively implement identity management policies and maintain firm control of what accounts are used to log onto their computers will probably want to block Microsoft accounts. Organizations may also need to block Microsoft accounts in order to meet the requirements of compliance standards that apply to their information systems.
						* Guest account status ([`Valid Accounts - Default Accounts` TTP](TTP/T1078_Valid_Accounts/001_Default_Accounts/T1078.001.md))
							* Recommended Setting: Disabled
							* Set Guest account status to Disabled so that the built-in Guest account is no longer usable. All network users will have to authenticate before they can access shared resources on the system.
						* Limit local account use of blank passwords to console logon only ([`Valid Accounts - Local Accounts` TTP](TTP/T1078_Valid_Accounts/003_Local_Accounts/T1078.003.md))
							* Recommended Setting: Enabled
						* Rename administrator account ([`Valid Accounts - Default Accounts` TTP](TTP/T1078_Valid_Accounts/001_Default_Accounts/T1078.001.md))
							* Recommended Setting: Changed from default
						* Rename guest account ([`Valid Accounts - Default Accounts` TTP](TTP/T1078_Valid_Accounts/001_Default_Accounts/T1078.001.md))
							* Recommended Setting: Changed from default
							* N/A
					* <details><summary>Devices (Click to expand)</summary><p>
						* Allow undock without having to log on
							* Recommended Setting: N/A
						* Allowed to format and eject removable media
							* Recommended Setting: Administrators
						* Prevent users from installing printer drivers
							* Recommended Setting: Enabled
						* Restrict CD-ROM access to locally logged-on user only
							* Recommended Setting: N/A
						* Restrict floppy access to locally logged-on user only
							* Recommended Setting: N/A
							* N/A
					* <details><summary>Domain Controller (Click to expand)</summary><p>
						* Allow server operators to schedule tasks ([`Scheduled Task/Job` TTP](TTP/T1053_Scheduled_Task-Job/T1053.md), [`Scheduled Task/Job - At Windows` TTP](TTP/T1053_Scheduled_Task-Job/002_At_Windows/T1053.002.md), [`Scheduled Task/Job - Scheduled Task` TTP](TTP/T1053_Scheduled_Task-Job/005_Scheduled_Task/T1053.005.md))
							* Recommended Setting: Disabled
							* Best practices for this policy are dependent on your security and operational requirements for task scheduling. The impact should be small for most organizations. Users (including those in the Server Operators group) can still create jobs by means of the Task Scheduler snap-in. However, those jobs run in the context of the account that the user authenticates with when setting up the job.
						* LDAP server signing requirements ([`Adversary-in-the-Middle` TTP](TTP/T1557_Adversary-in-the-Middle/T1557.md), ([`Adversary-in-the-Middle` TTP](TTP/T1557_Adversary-in-the-Middle/001_LLMNR-NBT-NS_Poisoning_and_SMB_Relay_By_responding_to_LLMNR-NBT-NS_network_traffic/T1557.001.md)))
							* Recommended Setting: Require Signing
							* Unsigned network traffic is susceptible to adversary-in-the-middle attacks. In such attacks, an intruder captures packets between the server and the client, modifies them, and then forwards them to the client. Where LDAP servers are concerned, an attacker could cause a client to make decisions that are based on false records from the LDAP directory. Some non-Microsoft operating systems do not support LDAP signing. If you enable this policy setting, client computers that use those operating systems may be unable to access domain resources.
						* Refuse machine account password changes
							* Recommended Setting: Disabled
					* <details><summary>Domain Member (Click to expand)</summary><p>
						* Digitally encrypt or sign secure channel data (always) ([`Adversary-in-the-Middle` TTP](TTP/T1557_Adversary-in-the-Middle/T1557.md))
							* Recommended Setting: Enabled
						* Digitally encrypt secure channel data (when possible) ([`Adversary-in-the-Middle` TTP](TTP/T1557_Adversary-in-the-Middle/T1557.md))
							* Recommended Setting: Enabled
						* Digitally sign secure channel data (when possible) ([`Adversary-in-the-Middle` TTP](TTP/T1557_Adversary-in-the-Middle/T1557.md))
							* Recommended Setting: Enabled
						* Disable machine account password changes
							* Recommended Setting: Disabled
						* Maximum machine account password age
							* Recommended Setting: 30 or fewer days, but not 0
						* Require strong (Windows 2000 or later) session key
							* Enabled
					* <details><summary>Interactive Logon (Click to expand)</summary><p>
						* Display user information when the session is locked
							* Recommended Setting: N/A
							* This policy depends on the organization's security requirements for displayed logon information.
						* Don't display last signed-in ([`Brute Force` TTP](TTP/T1110_Brute_Force/T1110.md), [`Brute Force - Password Guessing` TTP](TTP/T1110_Brute_Force/001_Password_Guessing/T1110.001.md), [`Brute Force - Credential Stuffing` TTP](TTP/T1110_Brute_Force/004_Credential_Stuffing/T1110.004.md))
							* Enabled
							* An attacker with access to the console (for example, someone with physical access or someone who is able to connect to the server through Remote Desktop Services) could view the name of the last user who logged on to the server. The attacker could then try to guess the password, use a dictionary, or use a brute-force attack to try and log on.
						* Don't display username at sign-in
							* Recommended Setting: N/A
							* This policy depends on the organization's security requirements for displayed logon information.
						* Do not require CTRL+ALT+DEL
							* Recommended Setting: Disabled
						* Machine account lockout threshold ([`Brute Force` TTP](TTP/T1110_Brute_Force/T1110.md), [`Brute Force - Password Cracking` TTP](TTP/T1110_Brute_Force/002_Password_Cracking/T1110.002.md))
							* Recommended Setting: N/A
							* If not set, the device could be compromised by an attacker using brute-force password cracking software. If set too low, productivity might be hindered because users who become locked out will be unable to access the device without providing the 48-digit BitLocker recovery password.
						* Machine inactivity limit
							* Recommended Setting: 900 or fewer second(s), but not 0
							* This security policy setting can limit unauthorized access to unsecured computers; however, that requirement must be balanced with the productivity requirements of the intended user.
						* Message text for users attempting to log on
							* Recommended Setting: Configured
						* Message title for users attempting to log on
							* Configured
						* Number of previous logons to cache (in case domain controller is not available)
							* Recommended Setting: 4 or fewer logon(s)
							* Microsoft recommendations do not suggest modifying this setting.
						* Prompt user to change password before expiration
							* Recommended Setting: between 5 and 14 days
						* Require Domain Controller authentication to unlock workstation
							* Recommended Setting: Enabled
							* By default, the computer caches in memory the credentials of any users who are  authenticated locally. The computer uses these cached credentials to authenticate anyone who attempts to unlock the console. When cached credentials are used, any changes that have recently been made to the account — such as user rights assignments, account lockout, or the account being disabled — are not considered or applied after the account is authenticated. User privileges are not updated, and (more importantly) disabled accounts are still able to unlock the console of the computer.
						* Require smart card
							* Recommended Setting: N/A
						* Smart card removal behavior
							* Recommended Setting: Lock Workstation
					* <details><summary>Microsoft Network Client (Click to expand)</summary><p>
						* Digitally sign communications (always) ([`Adversary-in-the-Middle` TTP](TTP/T1557_Adversary-in-the-Middle/T1557.md))
							* Recommended Setting: Enabled
						* Digitally sign communications (if server agrees) ([`Adversary-in-the-Middle` TTP](TTP/T1557_Adversary-in-the-Middle/T1557.md))
							* Recommended Setting: Enabled
							* This is configured by default to be disabled. In highly secure environments it is recommended that you configure this setting to Enabled. However, that configuration may cause slower performance on client devices and prevent communications with earlier SMB applications and operating systems.
						* Send unencrypted password to third-party SMB servers ([`Adversary-in-the-Middle` TTP](TTP/T1557_Adversary-in-the-Middle/T1557.md))
							* Recommended Setting: Disabled
					* <details><summary>Microsoft Network Server (Click to expand)</summary><p>
						* Amount of idle time required before suspending session
							* Recommended Setting: 15 or fewer minute(s)
						* Attempt S4U2Self to obtain claim information
							* Recommended Setting: Default Settings
						* Digitally sign communications (always) ([`Adversary-in-the-Middle` TTP](TTP/T1557_Adversary-in-the-Middle/T1557.md))
							* Recommended Setting: Enabled
						* Digitally sign communications (if client agrees) ([`Adversary-in-the-Middle` TTP](TTP/T1557_Adversary-in-the-Middle/T1557.md))
							* Recommended Setting: Enabled
						* Disconnect clients when logon hours expire
							* Recommended Setting: Enabled
						* Server SPN target name validation level
							* Recommended Setting: N/A
					* <details><summary>Network Access (Click to expand)</summary><p>
						* Allow anonymous SID/Name translation
							* Recommended Setting: Disabled
							* Default configuration
						* Do not allow anonymous enumeration of SAM accounts
							* Recommended Setting: N/A
						* Do not allow anonymous enumeration of SAM accounts and shares
							* Recommended Setting: N/A
						* Do not allow storage of passwords and credentials for network authentication
							* Recommended Setting: Enabled
							* Passwords that are cached can be accessed by the user when logged on to the computer.
						* Let Everyone permissions apply to anonymous users
							* Recommended Setting: Disabled
						* Named Pipes that can be accessed anonymously
							* Recommended Setting: Configured
							* Limiting named pipes that can be accessed anonymously will reduce the attack surface of the system.
						* Remotely accessible registry paths
							* Recommended Setting: Configured
							* An attacker could use this information to facilitate unauthorized activities. To reduce the risk of such an attack, suitable ACLs are assigned throughout the registry to help protect it from access by unauthorized users.
						* Remotely accessible registry paths and subpaths
							* Recommended Setting: Configured
						* Restrict anonymous access to Named Pipes and Shares
							* Recommended Setting: Enabled
						* Restrict clients allowed to make remote calls to SAM
							* Recommended Setting: N/A
						* Shares that can be accessed anonymously
							* None
							* Default configuration
						* Sharing and security model for local accounts
							* Classic - local users authenticate as themselves
					* <details><summary>Network Security (Click to expand)</summary><p>
						* Allow Local System to use computer identity for NTLM 
							* Enabled
							* This policy setting determines whether Local System services that use Negotiate when reverting to NTLM authentication can use the computer identity. Services running as Local System that use Negotiate when reverting to NTLM authentication will use the computer identity. This might cause some authentication requests between Windows operating systems to fail and log an error.
						* Allow LocalSystem NULL session fallback
							* Disabled
							* Default configuration
						* Allow PKU2U authentication requests to this computer to use online identities
							* Disabled
							* Default configuration
						* Configure encryption types allowed for Kerberos
							* AES128_HMAC_SHA1, AES256_HMAC_SHA1, Future Encryption types
						* Do not store LAN Manager hash value on next password change ([`OS Credential Dumping` TTP](TTP/T1003_OS_Credential_Dumping/T1003.md))
							* Enabled
						* Force logoff when logon hours expire
							* Enabled
						* LAN Manager authentication level ([`Adversary-in-the-Middle` TTP](TTP/T1557_Adversary-in-the-Middle/T1557.md), ([`Adversary-in-the-Middle` TTP](TTP/T1557_Adversary-in-the-Middle/001_LLMNR-NBT-NS_Poisoning_and_SMB_Relay_By_responding_to_LLMNR-NBT-NS_network_traffic/T1557.001.md)))
							* Send NTLMv2 response only. Refuse LM & NTLM
							* Allowing NTLMv1 is a significant vulnerability in modern Windows environments.
						* LDAP client signing requirements  ([`Adversary-in-the-Middle` TTP](TTP/T1557_Adversary-in-the-Middle/T1557.md), ([`Adversary-in-the-Middle` TTP](TTP/T1557_Adversary-in-the-Middle/001_LLMNR-NBT-NS_Poisoning_and_SMB_Relay_By_responding_to_LLMNR-NBT-NS_network_traffic/T1557.001.md)))
							* Negotiate signing or higher
						* Minimum session security for NTLM SSP based (including secure RPC) clients [`Adversary-in-the-Middle` TTP](TTP/T1557_Adversary-in-the-Middle/001_LLMNR-NBT-NS_Poisoning_and_SMB_Relay_By_responding_to_LLMNR-NBT-NS_network_traffic/T1557.001.md)))
							* 'Require NTLMv2 session security, Require 128-bit encryption
						* Minimum session security for NTLM SSP based (including secure RPC) servers [`Adversary-in-the-Middle` TTP](TTP/T1557_Adversary-in-the-Middle/001_LLMNR-NBT-NS_Poisoning_and_SMB_Relay_By_responding_to_LLMNR-NBT-NS_network_traffic/T1557.001.md)))
							* 'Require NTLMv2 session security, Require 128-bit encryption
							* Default configuration
					* <details><summary>Shutdown (Click to expand) ([`System Shutdown/Reboot` TTP](TTP/T1529_System_Shutdown-Reboot/T1529.md))</summary><p>
						* Allow system to be shut down without having to log on
							* Disabled
						* Clear virtual memory pagefile
							* N/A
					* <details><summary>System Objects (Click to expand)</summary><p>
						* Require case insensitivity for non-Windows subsystems
							* Enabled
							* Default configuration
						* Strengthen default permissions of internal system objects (e.g. Symbolic Links) ([`Boot or Logon Autostart Execution - Shortcut Modification` TTP](TTP/T1547_Boot_or_Logon_Autostart_Execution/009_Shortcut_Modification/T1547.009.md))
							* Enabled
					* <details><summary>User Account Control (Click to expand)</summary><p>
						* Admin Approval Mode for the Built-in Administrator account ([`Valid Accounts - Default Accounts` TTP](TTP/T1078_Valid_Accounts/001_Default_Accounts/T1078.001.md))
							* Enabled
							* If enabled, the built-in Administrator account uses Admin Approval Mode. Users that log on using the local Administrator account will be prompted for consent whenever a program requests an elevation in privilege, just like any other user would.
						* Allow UIAccess applications to prompt for elevation without using the secure desktop
							* N/A
						* Behavior of the elevation prompt for administrators in Admin Approval Mode ([`Valid Accounts - Default Accounts` TTP](TTP/T1078_Valid_Accounts/001_Default_Accounts/T1078.001.md))
							* Prompt for consent on the secure desktop
						* Behavior of the elevation prompt for standard users
							* Automatically deny elevation requests
						* Detect application installations and prompt for elevation
							* Enabled
							* Some malicious software will attempt to install itself after being given permission to run. When an application installation package is detected that requires elevation of privilege, the user is prompted to enter an administrative user name and password. If the user enters valid credentials, the operation continues with the applicable privilege.
						* Only elevate executables that are signed and validated
							* N/A
						* Only elevate UIAccess applications that are installed in secure locations
							* Enabled
							* Default configuration
						* Switch to the secure desktop when prompting for elevation
							* Enabled
							* Default configuration
						* Virtualize file and registry write failures to per-user locations
							* Enabled
							* Default configuration
						* Run all administrators in Admin Approval Mode ([`Valid Accounts - Default Accounts` TTP](TTP/T1078_Valid_Accounts/001_Default_Accounts/T1078.001.md))
							* Enabled
							* Default configuration
				* <details><summary>User Rights Assignment (Click to expand)</summary><p>
					* Access Credential Manager as a trusted caller
						* No one
					* Access this computer from the network
						* Administrators, Authenticated Users, ENTERPRISE DOMAIN CONTROLLERS
					* Act as part of the operating system
						* No one
					* Add workstations to domain ([`Create Account - Domain Account` TTP](TTP/T1136_Create_Account/002_Domain_Account/T1136.002.md))
						* Administrators
							* It is recommended to restrict this ability to administrators ONLY
							* `SeMachineAccountPrivilege`
					* Adjust memory quotas for a process
						* Administrators, LOCAL SERVICE, NETWORK SERVICE
					* Allow log on locally
						* Administrators
					* Allow log on through Remote Desktop Services ([`Remote Services- Remote Desktop Services` TTP](TTP/T1021_Remote_Services/001_Remote_Desktop_Protocol/T1021.001.md))
						* Administrators
							* This setting allows defined users to access the logon screen through RDP. It is possible to establish a remote connection but not be able to logon. This setting offers a layer of protection by designating certain users that are allowed to even attempt logon.
					* Back up files and directories
						* Administrators
					* Bypass traverse checking
						* Use Default
					* Change the system time
						* Administrators, LOCAL SERVICE
							* This should be review and limited if not necessary.
					* Change the time zone
						* Administrators, LOCAL SERVICE
							* This setting is not currently configured. It can be used to limit this privilege to a certain designated group or user. This should be evaluated to enforce least privilege.
					* Create a pagefile
						* Administrators
					* Create a token object ([`Access Token Manipulation` TTP](TTP/T1134_Access_Token_Manipulation/T1134.md), [`Access Token Manipulation - Token Impersonation/Theft` TTP](TTP/T1134_Access_Token_Manipulation/001_Token_Impersonation-Theft/T1134.001.md), [`Access Token Manipulation - Create Process with Token` TTP](TTP/T1134_Access_Token_Manipulation/002_Create_Process_with_Token/T1134.002.md), [`Access Token Manipulation - Make and Impersonate Token` TTP](TTP/T1134_Access_Token_Manipulation/003_Make_and_Impersonate_Token/T1134.003.md))
						* No one
					* Create global objects
						* Administrators, LOCAL SERVICE, NETWORK SERVICE, SERVICE
					* Create permanent shared objects
						* No one
					* Create symbolic links
						* Administrators
					* Debug programs
						* Administrators
							* This setting should be reviewed and limited to the Administrators group if this capability is no longer necessary for the exchange devices.
					* Deny access to this computer from the network
						* Guests
							* The guest account should be included in this list.
					* Deny log on as a batch job
						* Guests
							* The guest account should be included in this list.
					* Deny log on as a service
						* Guests
							* The guest account should be included in this list.
					* Deny log on locally
						* Guests
							* The guest account should be included in this list.
					* Deny log on through Remote Desktop Services ([`Remote Services- Remote Desktop Services` TTP](TTP/T1021_Remote_Services/001_Remote_Desktop_Protocol/T1021.001.md))
						* Guests
					* Enable computer and user accounts to be trusted for delegation
						* Administrators
					* Force shutdown from a remote system ([`System Shutdown/Reboot` TTP](TTP/T1529_System_Shutdown-Reboot/T1529.md))
						* Administrators
					* Generate security audits
						* LOCAL SERVICE, NETWORK SERVICE
					* Impersonate a client after authentication
						* Administrators, LOCAL SERVICE, NETWORK SERVICE, SERVICE
					* Increase a process working set
						* Default settings
					* Increase scheduling priority
						* Administrators
					* Load and unload device drivers ([`Boot or Logon Autostart Execution` TTP](TTP/T1547_Boot_or_Logon_Autostart_Execution/T1547.md), [`Boot or Logon Autostart Execution - LSASS Driver` TTP](TTP/T1547_Boot_or_Logon_Autostart_Execution/008_LSASS_Driver/T1547.008.md), [`Boot or Logon Autostart Execution - Print Processors` TTP](TTP/T1547_Boot_or_Logon_Autostart_Execution/012_Print_Processors/T1547.012.md), [`Disk Wipe` TTP](TTP/T1561_Disk_Wipe/T1561.md), [`Disk Wipe - Disk Content Wipe` TTP](TTP/T1561_Disk_Wipe/001_Disk_Content_Wipe/T1561.001.md), [`Disk Wipe - Disk Structure Wipe` TTP](TTP/T1561_Disk_Wipe/002_Disk_Structure_Wipe/T1561.002.md), [`Exploitation for Privilege Escalation` TTP](TTP/T1068_Exploitation_for_Privilege_Escalation/T1068.md), [`Input Capture` TTP](TTP/T1056_Input_Capture/T1056.md), [`Input Capture - Keylogging` TTP](TTP/T1056_Input_Capture/001_Keylogging/T1056.001.md), [`Two-Factor Authentication Interception` TTP](TTP/T1111_Two-Factor_Authentication_Interception/T1111.md))
						* Administrators
						* `SeLoadDriverPrivilege`
						* Can be used to take control of the system by loading a specifically designed driver3. This procedure can be performed by low privileged users as the driver can be defined in HKCU. Unless there is a business requirement for this setting, it is recommended to limit this activity to administrators only.
					* Lock pages in memory
						* No one
					* Log on as a batch job
						* Administrators
							* The recommendation is for this setting to have only the Administrators group listed. There are many x-accounts listed in the current setting. This should be reviewed and limited to only the accounts necessary.
					* Log on as a service
						* Minimize to only necessary accounts
							* This should be reviewed and limited if not required.
					* Manage auditing and security log
						* Administrators
							* Any users with this permission can set SACL for objects in the domain. These users can also view and clear the security log. This should be limited to Administrators ONLY.
					* Modify an object label
						* No one
					* Modify firmware environment values ([`Pre-OS Boot - System Firmware` TTP](TTP/T1542_Pre-OS_Boot/001_System_Firmware/T1542.001.md)
						* Administrators
					* Perform volume maintenance tasks
						* Administrators
					* Profile single process
						* Administrators
					* Profile system performance
						* Administrators, NT SERVICE\WdiServiceHost
					* Remove computer from docking station
						* Default Settings
					* Replace a process level token ([`Access Token Manipulation` TTP](TTP/T1134_Access_Token_Manipulation/T1134.md), [`Access Token Manipulation - Token Impersonation/Theft` TTP](TTP/T1134_Access_Token_Manipulation/001_Token_Impersonation-Theft/T1134.001.md), [`Access Token Manipulation - Create Process with Token` TTP](TTP/T1134_Access_Token_Manipulation/002_Create_Process_with_Token/T1134.002.md), [`Access Token Manipulation - Make and Impersonate Token` TTP](TTP/T1134_Access_Token_Manipulation/003_Make_and_Impersonate_Token/T1134.003.md))
						* LOCAL SERVICE, NETWORK SERVICE
					* Restore files and directories
						* Administrators
					* Shut down the system ([`System Shutdown/Reboot` TTP](TTP/T1529_System_Shutdown-Reboot/T1529.md))
						* Administrators
							* This should be reviewed and limited to only those necessary.
					* Synchronize directory service data
						* No one
					* Take ownership of files or other objects
						* Administrators
				* <details><summary>Audit Policies (Click to expand)</summary><p>
					* Legacy Audit Policy
						* With the added flexibility of the modern logging configuration capabilities included in the Advanced Audit Policy settings, there is no real value in using legacy audit settings in a modern Windows environment.
	* <details><summary>Policies (Click to expand)</summary><p>
		* <details><summary>Windows Settings (Click to expand)</summary><p>
			* <details><summary>Security Settings (Click to expand)</summary><p>
				* <details><summary>Account Policies (Click to expand)</summary><p>
					* <details><summary>Account Lockout Policy (Click to expand) ([`Brute Force` TTP](TTP/T1110_Brute_Force/T1110.md), [`Brute Force - Password Spraying` TTP](TTP/T1110_Brute_Force/003_Password_Spraying/T1110.003.md), [`Brute Force - Credential Stuffing` TTP](TTP/T1110_Brute_Force/004_Credential_Stuffing/T1110.004.md))</summary><p>
						* Account lockout duration
							* 15 or more minute(s)
						* Account lockout threshold
							* 10 or fewer invalid logon attempt(s)
						* Reset account lockout counter after
							* 15 or more minute(s)
	* <details><summary>Administrative Templates (Click to expand)</summary><p>
		* Network
			* DNS Client
				* Turn off multicast name resolution ([`Adversary-in-the-Middle` TTP](TTP/T1557_Adversary-in-the-Middle/001_LLMNR-NBT-NS_Poisoning_and_SMB_Relay_By_responding_to_LLMNR-NBT-NS_network_traffic/T1557.001.md)))
					* Set to Enabled to prevent LLMNR poisoning attacks
		* Windows Components
			* Windows PowerShell ([`Command and Scripting Interpreter - PowerShell` TTP](TTP/T1059_Command_and_Scripting_Interpreter/001_PowerShell/T1059.001.md))
				* Turn on PowerShell Script Block Logging
					* Enabled (at the very least for DCs)
					* It is not practical to disable PowerShell in a corporate network entirely
			* Credential User Interface
				* Enumerate administrator accounts on elevation ([`Account Discovery` TTP](TTP/T1087_Account_Discovery/T1087.md), [`Account Discovery - Local Account` TTP](TTP/T1087_Account_Discovery/001_Local_Account/T1087.001.md), [`Account Discovery - Domain Account` TTP](TTP/T1087_Account_Discovery/002_Domain_Account/T1087.002.md))
					* Disable
		* <details><summary>System (Click to expand)</summary><p>
			* Audit Process Creation
				* Detailed Tracking/Process Creation
					* Include command line in process creation events
						* Enabled
						* Event ID 4688
						* Generally considered an advanced logging configuration not typically seen in most organizations due to the shear volume of logs created. However, this single log, if properly configured, can provide the most value of any native logging component in Windows.

### Microsoft Administrative Templates (Non-Default Installs)
* <details><summary>Overview (Click to expand)</summary><p>
	* Administrative Templates are template files used by Group Policy to describe where registry-based policy settings are stored in the registry. Microsoft Windows Server 2003 and newer systems include several predefined security templates an administrator can apply to increase the level of security on their network. Several of these templates provide significantly added security customization. The CIS Benchmarks recommend a group of these security templates to be configured and deployed. Some of the most important ones are highlighted in the following section.
* <details><summary>Configure SMB v1 client driver (Click to expand)</summary><p>
	* Enabled: Disable driver
	* Since September 2016, Microsoft has strongly encouraged that SMBv1 be disabled and no longer used on modern networks, as it is a 30 year old design that is much more vulnerable to attacks then much newer designs such as SMBv2 and SMBv3.
* <details><summary>Configure SMB v1 server (Click to expand)</summary><p>
	* Disabled
	* Since September 2016, Microsoft has strongly encouraged that SMBv1 be disabled and no longer used on modern networks, as it is a 30 year old design that is much more vulnerable to attacks then much newer designs such as SMBv2 and SMBv3.
* <details><summary>Enable Structured Exception Handling Overwrite Protection (SEHOP) (Click to expand)</summary><p>
	* Enabled
	* This feature is designed to block exploits that use the Structured Exception Handler (SEH) overwrite technique. This protection mechanism is provided at run-time. Therefore, it helps protect applications regardless of whether they have been compiled with the latest improvements, such as the `/SAFESEH` option.
* <details><summary>Extended Protection for LDAP Authentication (Domain Controllers only) (Click to expand)</summary><p>
	* Enabled: Enabled, always
	* Configuring the `LdapEnforceChannelBinding` registry value can help to increase protection against "adversary-in-the-middle" attacks.
* <details><summary>NetBT NodeType configuration (Click to expand)</summary><p>
	* Enabled: P-node
	* In order to help mitigate the risk of NetBIOS Name Service (NBT-NS) poisoning attacks, setting the node type to P-node (point-to-point) will prevent the system from sending out NetBIOS broadcasts.
* <details><summary>WDigest Authentication (Click to expand)</summary><p>
	* Disabled
	* Preventing the plaintext storage of credentials in memory may reduce opportunity for credential theft.
* <details><summary>Encryption Oracle Remediation (Click to expand)</summary><p>
	* Enabled
	* This setting is important to mitigate the CredSSP encryption oracle vulnerability, for which information was published by Microsoft on 03/13/2018 (CVE-2018-0886). All versions of Windows Server from Server 2008 (non-R2) onwards are affected by this vulnerability, and will be compatible with this recommendation provided that they have been patched up through May 2018 (or later).
* <details><summary>Remote host allows delegation of non-exportable credentials (Click to expand)</summary><p>
	* Enabled
	* Restricted Admin Mode was designed to help protect administrator accounts by ensuring that reusable credentials are not stored in memory on remote devices that could potentially be compromised. Windows Defender Remote Credential Guard helps you protect your credentials over a Remote Desktop connection by redirecting Kerberos requests back to the device that is requesting the connection. Both features should be enabled and supported, as they reduce the chance of credential theft.