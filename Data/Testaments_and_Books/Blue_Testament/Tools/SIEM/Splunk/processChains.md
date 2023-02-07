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
## [-] REFERENCES

1. https://nasbench.medium.com/demystifying-the-svchost-exe-process-and-its-command-line-options-508e9114e747


## [-] NOTES


## [-] USE CASES

__============ MALICIOUS PROCESS CHAINS ============__

__PROBLEM STATEMENT__  - Analyze first degree process chaining (Event ID 1 - Process Create)

__APPROACH__ 

        index=main sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1
        | regex ParentCommandLine!="(\s\-k\s|CollectGuestLogs|winlogon)"
        | dedup CommandLine
        | stats values(CommandLine) as ExecutingCmd list(ParentCommandLine) as OriginatingCmd by _time, host

__STEPS EXPLAINED__ 

1. Execute a search for process creatiopn events
2. regex - filter the search results and remove ParentCommandLine results we are not interested in. It eliminates svchost.exe -k  calls which calls registry values for Service Host Groups. It also  filters winlogon and a log gathering executable run by Azure.
3. dedup - remove duplicate events with identical entries for CommandLine
4. stats - for unique values of CommandLine list the associated ParentCommandLine by _time and host

__============ WMIEXE ============__

__PROBLEM STATEMENT__  - wmiexe shell pivot (Event ID 1 - Process Create):

__APPROACH__ 

        index=main sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1
        | regex ParentCommandLine!="(\s\-k\s|CollectGuestLogs|winlogon)"
        | dedup CommandLine
        | search *wmi*
        | stats values(CommandLine) by _time, host, ParentCommandLine

__STEPS EXPLAINED__ 

1. Execute a search for process creatiopn events
2. regex - filter the search results and remove ParentCommandLine results we are not interested in. It eliminates svchost.exe -k  calls which calls registry values for Service Host Groups. It also  filters winlogon and a log gathering executable run by Azure.
3. dedup - remove duplicate events with identical entries for CommandLine
4. search - Look for instances that include *wmi* specifically
5. stats - for unique values of CommandLine list the associated ParentCommandLine by _time and host


## [-] TAGS

\#regex #dedup #stats


