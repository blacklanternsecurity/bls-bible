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
# Windows Audit Policy

#### References

* [https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/audit-policy-recommendations](https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/audit-policy-recommendations)
* [https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/monitoring-active-directory-for-signs-of-compromise](https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/monitoring-active-directory-for-signs-of-compromise)
* [https://www.malwarearchaeology.com/cheat-sheets](https://www.malwarearchaeology.com/cheat-sheets)
* [https://www.cisecurity.org/cis-benchmarks/](https://www.cisecurity.org/cis-benchmarks/)

#### Tags

#### Overview

The Windows operating system, if properly configured, has the ability to provide a robust and granular logging capability. Out of the box, the default logging configuration is minimal. Windows event logs are an essential component for maintaining visibility of user and application activity within a Windows environment. These event logs can assist with and support efforts ranging from system administration and troubleshooting to incident response activities in the event of an identified security incident.  

Combining years of security investigation and incident response experience, BLSOPS Analysts have generated a core list of valuable logs that have played a pivotal role in responding to security incidents. This "wish list" of logging is our organization's recommendation as a **bare minimum** for the organization Audit Policy. The provided summary of logging configuration has also been compared to both the Microsoft Best Practices documentation, the CIS Microsoft Windows Server 2016 Benchmark v1.2.0, and the Malware Archaeology *Windows Logging Cheat Sheet* , which has become the security community's defacto reference for maximizing logging utility and efficiency. These additional comparisons should offer varying perspectives of the highlighted log priorities.

On systems prior to Windows Vista, a limited auditing configuration was available to either enable or disable logging for each of the nine primary categories delineated by Microsoft. This method of logging was limited to an "all or nothing" result. The legacy audit settings can be configured using Windows group policy settings. The settings can be found in the node path shown below.

```Computer Configuration\Windows Settings\Security Settings\Local Policies\Audit Policy\```

With the added flexibility of the modern logging configuration capabilities included in the Advanced Audit Policy settings, there is no real value in using legacy audit settings in a modern Windows environment. The preferred, granular Windows Audit Policy settings are located within the Advanced Audit Policy Configuration GPO:

```Computer Configuration > Policies > Windows Settings > Security Settings > Advanced Audit Policy Configuration > Audit Policies```

These settings, organized by subcategory, were introduced in Windows 7 and provide much more control of the logging capability than the original, high-level audit policy controls. The subcategory organization allows for limiting logging to only **what is of most use** to reduce log processing and storage requirements. The 9 primary categories have been broken down into their finely tunable subcategories.  

**Summary of the Primary Categories:**

* <details><summary>Account Logon (Click to expand)</summary><p>
    Reports each instance of a security principal (e.g., user, computer, or service account) that is logging on to or logging off from one computer in which another computer is used to validate the account, this includes authentication events performed by a Domain Controller (DC). The most important note about this category is that the relevant log is recorded on the system that performs the authentication of the principal. This means that if a local account is logged into and the local system performs the authentication activity, the associated log will be generated and stored on that local system, not the domain controller.

    Secondary Subcategory | BLSOPS | Microsoft Best Practices | Malware Archaeology | CIS Benchmarks
    -------- | -------- | -------- | -------- | -------- 
    Credential Validation     | Success/Failure     | Success (Default)     | Success/Failure     | Success/Failure
    Kerberos Authentication Service     | Success/Failure    | Success/Failure (Adv)     | Success/Failure (Adv)    | Success/Failure
    Kerberos Service Ticket Operations     | Success/Failure     | Success/Failure (Adv)     | Success/Failure (Adv)    | Success/Failure
    Other Account Logon Events     | Success/Failure     | Success/Failure (Adv)     | Success/Failure     | N/A

* <details><summary>Account Management (Click to expand)</summary><p>
    Determines whether to track management of users and groups (e.g., creation, modifications, and deletion events). These events are extremely important for incident response and post-mortem security investigations.

    | Secondary Subcategory   | BLSOPS    | Microsoft Best Practices    | Malware Archaeology    | CIS Benchmarks |
    | -------- |  -------- | -------- | -------- | -------- |
    | Application Group Management     | No Auditing     | No Auditing (Default)     | Success/Failure     | Success/Failure    |
    | Computer Account Management    | Success     | Success (Default)    | Success/Failure     | Success    |
    | Distribution Group Management     | No Auditing     | No Auditing (Default)    | Success/Failure     | Success    |
    | Other Acct Management Events     | Success    | Success     | Success/Failure     | Success    |
    | Security Group Management     | Success     | Success (Default)    | Success/Failure     | Success    |
    | User Account Management     | Success/Failure     | Success (Default)    | Success/Failure     | Success/Failure    |

* <details><summary>Detailed Tracking (Click to expand)</summary><p>
    Determines whether to audit detailed process tracking information for events such as program activation, process exit, handle duplication, and indirect object access. This category is useful for tracking malicious users and the programs that they use. Enabling Audit Process Tracking generates a large number of events, so typically it is set to **No Auditing** by most organizations. However, this setting can provide a great benefit during an incident response from the detailed log of the processes started and the time they were launched. For domain controllers and other single-role infrastructure servers, this category can be safely turned on all the time. Single role servers do not generate much process tracking traffic during the normal course of their duties. As such, they can be enabled to capture unauthorized events if they occur.

    | Secondary Subcategory    | BLSOPS    | Microsoft Best Practices    | Malware Archaeology    | CIS Benchmarks |
    | -------- | -------- | -------- | -------- | -------- |
    | DPAPI Activity     | No Auditing     | Success\Failure (Adv)     | No Auditing     | N/A    |
    | Plug and Play     | Success     | No Auditing     | Success     | N/A    |
    | Process Creation     | Success     | Success     | Success/Failure     | Success    |
    | Process Termination     | No Auditing     | No Auditing     | Success (Adv)     | N/A    |
    | RPC Events     | No Auditing     | No Auditing     | Success/Failure     | N/A    |
    | Token Right Adjusted Events     | Success     | No Auditing     | Success     | N/A    |

* <details><summary>DS Access (Click to expand)</summary><p>
    Microsoft does not provide much guidance on these settings in their best practices guidelines, but BLSOPS and the security community have found them to provide very valuable information when performing incident investigations. This settings category determines whether to audit security principal access to an Active Directory object that has its own specified system access control list (SACL). In general, this category of policies should only be enabled on domain controllers. There are special use cases that this can be beneficial on all assets in the organization, though.

    | Secondary Subcategory    | BLSOPS    | Microsoft Best Practices    | Malware Archaeology    | CIS Benchmarks |
    | -------- | -------- | -------- | -------- | -------- |
    | Detailed Directory Service Replication     | No Auditing     | No Auditing     | No Auditing     | N/A    |
    | Directory Service Access     | Success     | No Auditing     | Success/Failure (Adv)    | Failure    |
    | Directory Service Changes     | Success     | No Auditing (Default)     | Success/Failure     | Success    |
    | Directory Service Replication     | No Auditing     | No Auditing     | Success/Failure (Adv)    | N/A    |

* <details><summary>Logon/Logoff (Click to expand)</summary><p>
    Logon/Logoff events are generated when a local security principal is authenticated on a local computer. This event category is different from the Account Logon/Logoff events in that it records the actual action of access and not the authentication component. In an Active Directory supported environment, like { customer.shortname }, the authentication action is generally performed by the domain controller. The actual log generated from the logon action is created on the local system, though. This is another example why it is critical to centralize workstation logs in addition to the domain controller logs. 

    | Secondary Subcategory    | BLSOPS    | Microsoft Best Practices    | Malware Archaeology    | CIS Benchmarks |
    | -------- | -------- | -------- | -------- | -------- |
    | Account Lockout      | Success     | Success (Default)     | Success     | Failure    |
    | Group Membership      | No Auditing     | No Auditing     | Success     | N/A    |
    | IPsec Extended Mode      | No Auditing     | No Auditing     | No Auditing     | N/A    |
    | IPsec Main Mode      | No Auditing     | No Auditing     | No Auditing     | N/A    |
    | IPsec Quick Mode      | No Auditing     | No Auditing     | No Auditing     | N/A    |
    | Logoff      | Success     | Success (Default)     | Success     | Success    |
    | Logon      | Success/Failure     | Success/Failure (Default)    | Success/Failure     | Succ/Fail    |
    | Network Policy Server      | Success/Failure     | Success/Failure (Default)    | Success/Failure     | N/A    |
    | Other Logon/Logoff Events      | Success     | No Auditing (Default)    | Success/Failure     | Succ/Fail    |
    | Special Logon      | Success     | Success (Default)    | Success/Failure     | Success    |
    | User / Device Claims      | No Auditing     | No Auditing     | No Auditing     | N/A    |

* <details><summary>Object Access (Click to expand)</summary><p>
    No Microsoft recommendations are provided for this settings category. Object Access can generate events when subsequently defined objects with auditing enabled are accessed (e.g., Opened, Read, Renamed, Deleted, or Closed). After the main auditing category is enabled, the administrator must individually define which objects will have auditing enabled. Many Windows system objects come with auditing enabled, so enabling this category will usually begin to generate events before the administrator has defined any. This category of logging has proved helpful for tracking specific access actions in investigations performed by BLSOPS analysts in the past.

    | Secondary Subcategory    | BLSOPS    | Microsoft Best Practices    | Malware Archaeology    | CIS Benchmarks |
    | -------- | -------- | -------- | -------- | -------- |
    | Application Generated     | No Auditing     | No Auditing     | Success/Failure     | N/A    |
    | Certification Services     | Success/Failure     | No Auditing     | Success/Failure     | N/A    |
    | Central Policy Staging     | No Auditing     | No Auditing     | No Auditing     | N/A    |
    | Detailed File Share     | No Auditing     | No Auditing (Default)     | Success     | Failure    |
    | File Share     | Success/Failure (As needed)     | No Auditing (Default)    | Success/Failure     | Success/Failure    |
    | File System     | Success (As needed)     | No Auditing     | Success     | N/A    |
    | Filtering Platform Connection     | No Auditing     | No Auditing     | Success (Adv)     | N/A    |
    | Filtering Platform Packet Drop     | No Auditing     | No Auditing     | Success (Adv)     | N/A    |
    | Handle Manipulation     | No Auditing     | No Auditing     | Success (Adv)     | N/A    |
    | Kernel Object     | No Auditing     | No Auditing     | No Auditing     | N/A    |
    | Other Object Access Events     | Success (As needed)    | No Auditing (Default)     | Success/Failure (Adv)   | Success/Failure    |
    | Removable Storage     | Success/Failure     | No Auditing (Default)    | Success/Failure     | Success/Failure    |
    | Registry     | Success (As needed)     | No Auditing     | Success     | N/A    |
    | SAM     | No Auditing     | No Auditing     | Success     | N/A    |

* <details><summary>Policy Change (Click to expand)</summary><p>
    This policy setting determines whether to audit every incidence of a change to user rights assignment policies, Windows Firewall policies, Trust policies, or changes to the audit policy. This category should be enabled on all computers. It generates very little noise.

    | Secondary Subcategory    | BLSOPS    | Microsoft Best Practices    | Malware Archaeology    | CIS Benchmarks |
    | -------- | -------- | -------- | -------- | -------- |
    | Audit Policy Change     | Success/Failure     | Success/Failure     | Success/Failure     | Success    |
    | Authentication Policy Change     | Success/Failure     | Success (Default)     | Success/Failure     | Success     |
    | Authorization Policy Change     | Success/Failure     | No Auditing     | Success/Failure     | Success    |
    | Filtering Platform Policy Change     | No Auditing     | No Auditing     | Success     | N/A    |
    | MPSSVC Rule-Level Policy Change     | No Auditing     | No Auditing (Default)    | No Auditing     | Success/Failure    |
    | Other Policy Change Events     | No Auditing    | No Auditing (Default)    | No Auditing     | Failure    |

* <details><summary>Privilege Use (Click to expand)</summary><p>
    There are dozens of user rights and permissions in Windows (for example, Logon as a Batch Job and Act as Part of the Operating System). This policy setting determines whether to audit each instance of a security principal exercising a user right or privilege. Enabling this category results in a lot of "noise," but it can be helpful in tracking security principal accounts using elevated privileges when properly tuned.

    | Secondary Subcategory    | BLSOPS    | Microsoft Best Practices    | Malware Archaeology    | CIS Benchmarks |
    | -------- | -------- | -------- | -------- | -------- |
    | Non Sensitive Privilege Use     | No Auditing     | No Auditing     | No Auditing     | N/A    |
    | Other Privilege Use Events     | No Auditing     | No Auditing     | No Auditing     | N/A    |
    | Sensitive Privilege Use     | Success/Failure     | No Auditing (Default)    | Success/Failure     | Success/Failure    |

* <details><summary>System (Click to expand)</summary><p>
    This subcategory is almost a generic catch-all category, registering various events that impact the computer, its system security, or the security log. It includes events for computer shutdowns and restarts, power failures, system time changes, authentication package initializations, audit log clearings, impersonation issues, and a host of other general events. In general, enabling this audit category generates a lot of "noise," but it generates enough very useful events that it is difficult to ever recommend not enabling it.

    | Secondary Subcategory    | BLSOPS    | Microsoft Best Practices    | Malware Archaeology    | CIS Benchmarks |
    | -------- | -------- | -------- | -------- | -------- |
    | IPsec Driver     | Success     | Success/Failure     | Success (Adv)     | Success/Failure    |
    | Other System Events     | Failure     | Success/Failure (Default)     | Failure (Adv)     | Success/Failure    |
    | Security State Change     | Success/Failure     | Success/Failure     | Success/Failure     | Success    |
    | Security System Extension     | Success/Failure     | Success/Failure     | Success/Failure     | Success    |
    | System Integrity     | Success/Failure     | Success/Failure (Default)     | Success/Failure     | Success/Failure    |

#### Gotchas

* The policy configuration, **Detailed Tracking/Process Creation**, includes the ability of logging process creation events, **Event ID 4688**. This particular log is generally considered an advanced logging configuration not typically seen in most organizations due to the shear volume of logs created. However, this single log, if properly configured, can provide the most value of any native logging component in Windows. 

    There is an additional setting required to add command line logging to the 4688 events logs that should be separately configured in the GPO setup. In order to enable the command line logging component, the "**Include command line in process creation events**" setting should be enabled. This setting can be found in the node path shown below.

    ```Computer Configuration\Administrative Templates\System\Audit Process Creation\```

    It is important to note the recommended configuration does not generate any *additional* logs, but rather enriches the existing process creation logs with the context of the commands being executed. The added value of command line auditing cannot be overstated for such a simple modification to an existing configuration.


#### Guides

**Live Investigation:**

1. Using command line, list the current Audit policy:
    <br>*Must be run as administrator*

    ```AuditPol /get /category:*``` 

2. Verify the log size for the Security log:
    <br>*Must be run as administrator*

    ```WevtUtil gl Security```

3. Search for strings in particular logs
    <br>*Must be run as administrator*

    ```WevtUtil qe Security /q:"*[System[(EventID=4663)]]" /c:50 /rd:true /f:text | find /i "string"```


#### Unexplored

* Event Tracing for Windows (ETW)


