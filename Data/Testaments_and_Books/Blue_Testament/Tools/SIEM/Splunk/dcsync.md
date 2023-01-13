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

1. https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4662
2. https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/1522b774-6464-41a3-87a5-1e5633c3fbbb
3. https://www.blacklanternsecurity.com/2020-12-04-DCSync/#SIEM


## [-] NOTES

- TBD


## [-] USE CASES

__============ DCSYNC ============__

__PROBLEM STATEMENT__  - DCSync (Event ID 4662 - Object Acces)

__APPROACH__ 

        index=main EventCode=4662 Access_Mask=0x100
        | regex Account_Name!="\w+\$$"
        | rex field=Message "\s(?<prop_id>\{​​​​​​​​​[^\}​​​​​​​​​]+\}​​​​​​​​​)"
        | dedup prop_id
        | eval dc_sync=case(prop_id=="{​​​​​​​​​1131f6ad-9c07-11d1-f79f-00c04fc2dcd2}​​​​​​​​​", "DCSYNC - Replication Get Changes All", prop_id=="{​​​​​​​​​1131f6aa-9c07-11d1-f79f-00c04fc2dcd2}​​​​​​​​​", "DCSYNC - Replication Get Changes", prop_id=="{​​​​​​​​​9923a32a-3607-11d2-b9be-0000f87a36b2}​​​​​​​​​", "DCSYNC - Install Replica")
        | table Account_Name prop_id host dc_sync

__STEPS EXPLAINED__ 

1. Search on EventCode 4662 (An operation was performed on an object). Access_Mask=0x100 → This is the type of access used for the operation.  The right to perform an operation controlled by an extended access right.
2. regex - remove 4662 events associated with a computer account for the DC. These are legitimate replication activities.
3. rex - extract the properties GUID . We are looking for registered GUIDs that represent each of the RPC functions associated with the replication attempt.
4. dedup - remove duplicate events for the same prop_id
5. eval - assign a string value to dc_sync based on the RPC call that is made and the value of prop_id.  
6. table - display and analyze results


## [-] TAGS

#dcsync #dedup #regex #rex #eval
