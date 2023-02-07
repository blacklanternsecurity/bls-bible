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
3. https://docs.splunk.com/Documentation/SplunkCloud/8.1.2101/SearchReference/Metadata


## [-] NOTES


## [-] USE CASES

__============ AVAILABLE INDICES ============__

__PROBLEM STATEMENT__ - View Available Indices

__APPROACH__ 

        | eventcount summarize=false index=* index=_* | dedup index | fields index

__STEPS EXPLAINED__ 

1. eventcount summarize=false - provides an event count for each index. each index is listed under column=index
2. index=* _index=* - search for all index values in the results
3. dedup - remove deuplicate values for indices
4. fields - only use the index field for the results displayed

__============ SOURCES ============__

__PROBLEM STATEMENT__ - View SOURCES for all indices

__APPROACH__ 

        | tstats count WHERE index=* OR index=_* by index source
        | sort - count

__STEPS EXPLAINED__ 

1. tstats - performs quey against indexed data
2. where - return stats for ALL possible indices
3. by - show the event count for each source within a given index

__============ SOURCES for SPECIFIC INDEX ============__

__PROBLEM STATEMENT__ - View SOURCES for specified index

__APPROACH__ 

        | tstats count WHERE index=boop by index source

        OR

        > | metadata type=sources index=botsv2

__STEPS EXPLAINED__

1. tstats - performs query against indexed data for index=VALUE
2. where - return stats for index=VALUE
3. by - show the event count for each source within the specified index

__============ FIELDS for SOURCES for SPECIFIC INDEX ============__

__PROBLEM STATEMENT__ - Show fields for every SOURCE within specified INDEX

__APPROACH__ 

The "head command operates on the first record returned.

        index=main source=* 
        | head 1 
        | fieldsummary
        |  table field

__STEPS EXPLAINED__

1. Search - Return all events fo all sources for the Benevis index
2. Head - display a single event
3. fieldsummary - show summary statistics for each field
4. table - show all fields

__============ SEARCH FIELD NAMES in ALL INDICES ============__

__PROBLEM STATEMENT__ - Search for fieldnames with a specific string (eg. “src”)

__APPROACH__ 

        index=* | fieldsummary “src”

__STEPS EXPLAINED__

1. search - all events for all indices
2. fieldsummary - for all fields that include “src”

__============ AVAILABLE SOURCETYPES for SPECIFIC INDEX ============__

__PROBLEM STATEMENT__ - View Available SOURCETYPES for an INDEX

__APPROACH__ 

        > | metadata type=sourcetypes index=botsv2

__STEPS EXPLAINED__

1. The first, last, and recent times will tell you when that specific source type interacted with the indexer.
2. Pay attention to what data is available for the timeframe you are interesated in

__============ HOST OUTLIERS ============__

__PROBLEM STATEMENT__ - For any INDEX, look for outliers that may be logging an unusually large number of events based on median(average values)

__APPROACH__ 

        | tstats count WHERE index=os earliest=-7d by host, _time span=3h
        | stats median(count) AS median BY host
        | join host [| tstats count WHERE index=os earliest=-3h by host]
        | eval percentage_diff=((count/median)*100)-100
        | where percentage_diff<-5 OR percentage_diff>5
        | sort percentage_diff
        | rename AS “Median Event Count Past Week”, count AS “Event Count of Events Past 3 Hours”, percentage_diff as “Percentage Difference”

__STEPS EXPLAINED__

1. For each host, for the last seven days, count events in the OS index for each 3 hour increment. In other words, for the os index how many events am I seeing for each host every 3 hours?
2. Calculate the median event count per host. Take an average for each “3 hour” event measurment
3. Now,  take the median event counts by host and JOIN it to a subsearch for events in the os index by host for the last 3 hours. JOIN on “host”.
4. So now, for each host we have a median 3 hour event counts for the last 7 days AND the event count for the last 3 hours
5. For each host, calculate the percent difference between events over the last 3 hours and the median from the last 7 days
6. Now show results where there has been a DROP or INCREASE of more than 5%
7. Sort on percentage_diff
8. Plot


## [-] TAGS

#dedup #eventcount #fields #tstats #sort #where #head #fieldsummary #eval #join #stats #rename

