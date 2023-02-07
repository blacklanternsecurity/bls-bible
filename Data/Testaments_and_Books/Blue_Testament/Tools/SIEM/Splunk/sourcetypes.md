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

- tstats ONLY looks at indexed metadata
- tstats can only operate on metadata fields (_time, host, source, sourcetype etc.)
- The seearch below looks at dns events and breask out data according to host in 12 hour intervals


## [-] USE CASES

__============ FIELDS for SOURCETYPE ============__

__PROBLEM STATEMENT__ - View available FIELDS for specific SOURCETYPE

__APPROACH__ 

        index="benevis" sourcetype= pan:traffic
        | head 1
        | fieldsummary
        | table field

__STEPS EXPLAINED__ 

1. Search - Return all events for the benevis index and the pan:traffic sourcetype
2. Head - display a single event
3. fieldsummary - show summary statistics for each field in that single event
4. table - show fields

__============ EVENT TIMELINE FOR SOURCETYPE ============__

__PROBLEM STATEMENT__ - Graph Events for a specific SOURCETYPE. At what rate might they be coming in?

__APPROACH__ 

        | tstats count where index=botsv2 sourcetype=stream:dns by _time, host span=12h
        | xyseries _time, host, count

__STEPS EXPLAINED__ 

1. tstats - return statistics for indexed events. Only look at the botsv2 index and the stream:dns sourcetype. Bucket events by _time and host for each 12h block of time. 
2. xyseries - plot the data. _time is the x field. host is the y name field. count is the y data field


## [-] TAGS

\#xyseries #tstats #fieldsummary #table
