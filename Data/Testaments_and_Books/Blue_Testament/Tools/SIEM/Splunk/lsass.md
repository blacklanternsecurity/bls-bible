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


## [-] NOTES


## [-] USE CASES

__============ DUMPING HASHES ============__

__PROBLEM STATEMENT__  - Detect Sharpdump of LSASS (Event ID 1 - Process Create)

__APPROACH__ 

        index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1 host=windows1
        | fields ProcessGUID Message ParentImage Image ParentCommandLine
        | rename ProcessGUID as ParentProcessGUID
        | rex field=Message "Company: (?<Company>.+)"
        | join ParentProcessGUID [search index=main source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=10 | fields ParentProcessGUID TargetImage GrantedAccess]
        | search TargetImage="C:\\Windows\\System32\\lsass.exe" NOT Company="Microsoft Corporation"
        | table ParentImage Image TargetImage GrantedAccess ParentCommandLine

__STEPS EXPLAINED__ 

1. Look for process creation events on a specific hosts
2. Bring forward select fields from the initial search
3. Rename the ProcessGUID
4. Set up to extract the company name
5. Join on the ParentProcessGUID. This is the ProcessGUID for ANY EventCode 1. Now search for EventCode 10 and return 3 other fields.
6. Now you can see the Parent Process GUID resposnible for EventCode 10
7. Search for lsass.exe as the target
8. Remove MSFT as company
9. Show results  


## [-] TAGS

\#lsass #sharphound #fields #rename #rex #join #search #table
