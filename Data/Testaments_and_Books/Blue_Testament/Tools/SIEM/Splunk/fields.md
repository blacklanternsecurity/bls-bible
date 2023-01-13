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

1. https://www.splunk.com/en_us/blog/tips-and-tricks/metadata-metalore.html
2. https://www.splunk.com/en_us/blog/security/i-need-to-do-some-hunting-stat.html


## [-] NOTES

- TBD


## [-] USE CASES

__============ FIND SOURCETYPES THAT CONTAIN FIELDS w/ GIVEN STRING ============__

__PROBLEM STATEMENT__ - What sourcetypes have fields that might include the MAC address?

__APPROACH__ 

        index=* 
        | stats dc(*) as * by sourcetype
        | transpose header_field=sourcetype
        | search column="*mac*"
        | transpose header_field=column

__STEPS EXPLAINED__ 

1. stats - provide a distinct count OF every field by sourcetype. For each event that contains the field it will increment the count under that sourcetype.
2. transpose - fields (columns) transposed to rows AND sourcetype (rows) transposed to columns
3. search - look for rows (fields) that contain the string “src”.
4. tranpose - For the search results returned, execute transpose again.  fields (rows) transposed back to columns AND sourcetype (columns) transposed back to rows


## [-] TAGS

\#stats #transpose 
