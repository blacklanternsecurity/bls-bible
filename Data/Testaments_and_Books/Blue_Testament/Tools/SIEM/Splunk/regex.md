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

1. https://docs.splunk.com/Documentation/Splunk/8.1.2/SearchReference/Regex


## [-] NOTES

- This is a SEARCH command and will filter searh results based on the content of the REGEX command


## [-] USE CASES

__============ PROCESS CHAINING ============__

__PROBLEM STATEMENT__ - Analyze the process/cmdline chains for SYSMON process creation events. Find malicious processes

__APPROACH__ 

        index=main sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1
        | regex ParentCommandLine!="(\s\-k\s|CollectGuestLogs|winlogon)"
        | dedup CommandLine
        | stats values(CommandLine) as ExecutingCmd list(ParentCommandLine) as OriginatingCmd by _time, host

__STEPS EXPLAINED__ 

1. Search process creation events in SYSMON
2. regex - filter down search results based on regex for the ParentCommandLine
3. dedup - deduplicate events that have the same content in the CommandLine
4. stats - find unique command line values. List associated ParentCommandLine. All according to _time and host.


## [-] TAGS

#dedup #regex #stats #sysmon

