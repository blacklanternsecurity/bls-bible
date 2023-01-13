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
# Sysmon

#### References

* [https://docs.microsoft.com/en-us/sysinternals/downloads/sysmon](https://docs.microsoft.com/en-us/sysinternals/downloads/sysmon)
* [https://github.com/SwiftOnSecurity/sysmon-config](https://github.com/SwiftOnSecurity/sysmon-config)
* [https://github.com/olafhartong/sysmon-modular](https://github.com/olafhartong/sysmon-modular)
<br>

#### Tags

<br>

#### Overview

**Sysmon** (short for System Monitor) is a tool released by Microsoft as part of the Sysinternals Suite. This utility functions by installing a Windows service and device driver that monitors system level activity as specified in a user supplied configuration file. The activity that is monitored generates a log in a dedicated Windows Event Log channel, 

**NOTE: Sysmon is considered a SUPPLEMENTAL logging utility and should not be used as a replacement for standard Windows Event Log logging.** 

Sysmon currently has 27 event IDs that can be generated. 

Event ID | Name | Explanation
---- | ---- | ----
1 | Process Creation | Information on newly created processes. Includes full command line and hash of the associated file.
2 | File Creation Time Modification | File creation time is explicitly modified by a process. This is a common legitimate occurence and does not mean malicious activity.
3 | Network Connection | Information on TCP/UDP connections on the machine. Logs are linked to a particular process and include Src and Dest IP address and port numbers.
4 | Sysmon Service State Change | Reports actions impacting the Sysmon logging service.
5 | Process Terminated | Inofmration about process that are terminated.
6 | Driver Loaded | Information about drivers being loaded on the system.  
7 | Image Loaded | Information on modules loaded in a specific process. WILL GENERATE A LOT OF LOGS.
8 | Create Remote Thread | Log is generated when a process creates a thread in another process.  
9 | Raw Access Read | Log is generated when a process conducts reading operations using the `\\.\` denotation. 
10 | Process Access | Log is generated when a process opens another process.
11 | File Create | Log is generated when a file is created or overwritten.  
12 | Registry Event (Create/Delete) | Log is generated when a registry key and value are created or deleted. 
13 | Registry Event (Value Set) | Log is generated when a registry value is set. 
14 | Registry Event (Rename) | Log is generated when a registry key or value is renamed. 
15 | File Create Stream Hash | Log is generated when a named file stream is created. Useful for tracking alternate data streams. 
16 | Service Configuration Change | Monitors changes to the Sysmon configuration. 
17 | Pipe Event (Created) | Log is generated when a named pipe is created. 
18 | Pipe Event (Connected) | Log is generated when a named pipe connection is made between a client and a server. 
19 | WMI Event (Filter) | Log is generated when a WMI event filter is registered. 
20 | WMI Event (Consumer) | Log is generated when a WMI envent consumer is registered.
21 | WMI Event (Consumer to Filter) | Log is generated when a consumer binds to a filter.  
22 | DNS Event | Log is generated when a process attempts a DNS query (whether the result is a success or failure). 
23 | File Delete | Log is generated when a file is deleted. A copy of the deleted file is also archived in the Archive Directory of Sysmon (C:\Sysmon by default). 
24 | Clipboard Change | Log generated when the system clipboard content changes. 
25 | Process Tampering | Log generated when process hiding techniques are discovered.  
26 | File Delete Detected | Same as event ID 23, but a copy of the file is not collected and archived. 
255 | Error | Log generated if the Sysmon service experiences any sort of error.  
<br>



#### Guides

* <details><summary>Recommended Configuration Files (Click to expand)</summary><p>

   * **SwiftOnSecurity** - Solid baseline that is well notated and attempts to limit the noise of known legitimate activities. Performs a series of log exclusions to whitelist large amounts of default Windows entries.
   [https://github.com/SwiftOnSecurity/sysmon-config](https://github.com/SwiftOnSecurity/sysmon-config)
   * **Sysmon Modular** - Sysmon events include a MITRE ATT&CK specific tag. Includes a script that can be used to generate a configuration file in an easier manner. 
   [https://github.com/olafhartong/sysmon-modular](https://github.com/olafhartong/sysmon-modular)

* <details><summary>Installation (Click to expand)</summary><p>
    
    *Must be executed from an administrative command line.*
    *No reboot required.*

    `sysmon.exe -i --accepteula`

    No logs will be generated until a configuration file is provided to the service. 
    
    Validate the service was installed successfully.

    `sc query Sysmon` 

* <details><summary>Display Current Config (Click to expand)</summary><p>
    
    *Must be executed from an administrative command line.*
    *No reboot required.*

    `sysmon.exe -c`

    Note the schema version being used:

    `sysmon.exe -? config`
 

* <details><summary>Update/Install Config (Click to expand)</summary><p>
    
    *Must be executed from an administrative command line.*
    *No reboot required.*

    `sysmon.exe -c [Config_path_and_name]`
 

* <details><summary>Uninstall (Click to expand)</summary><p>
    
    *Must be executed from an administrative command line.*

    `sysmon.exe -u [Optional: force]`
<br>

#### Gotchas

Helpful troubleshooting commands:

`net stop sysmon`

`net stop sysmondrv`

`del c:\windows\sysmon.exe`

`del c:\windows\sysmondrv.sys`

`reg delete HKLM\SYSTEM\CurrentControlSet\Services\SysmonDrv /f`

`reg delete HKLM\SYSTEM\CurrentControlSet\Services\Sysmon /f`
<br>

#### Unexplored

* SysmonSearch - Tool from JPCERT to visualize Sysmon log data. [https://github.com/JPCERTCC/SysmonSearch](https://github.com/JPCERTCC/SysmonSearch)


