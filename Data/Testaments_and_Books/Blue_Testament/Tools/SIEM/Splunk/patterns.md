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

__============ LOGIN ACTIVITY ============__

__PROBLEM STATEMENT__


__APPROACH__ 

        index=botsv3 sourcetype=stream:http *login*
        | stats count by src uri_path
        | sort -count
        | stats list(uri_path) as URI, list(count) as count, sum(count) as Total by src

The stats command operates on the result set that comes before it and not the original search results

__STEPS EXPLAINED__ 

1. Search for any events in the http stream that have *login* anywhere in the event
2. stats - Count by src and uri_path pairs
3. stats - for each SRC IP (BY Clause), list the uri_paths that were hit list(uri_path), the number of times each was hit list(count), and the total number of hits for ALL uri_paths associated with that SRC IP


## [-] TAGS

\#stats #sort #list
