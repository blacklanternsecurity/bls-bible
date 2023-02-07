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

1. https://docs.splunk.com/Documentation/Splunk/8.1.2/Search/Findingandremovingoutliers


## [-] NOTES

- Find and analyze statistical outliers


## [-] USE CASES

__============ SQLI SLEEP() ============__

__PROBLEM STATEMENT__ - SQLI sometimes leverages the SLEEP() function to detect SQLi vulnerabilities. Can you identify events where the SLEEP() command was successful? In this case, can you look for response times for SLEEP() events/queries that are statistical outliers based on the overall stats for the server?

__APPROACH__ 

        index=viningsparks sourcetype=iis time_taken=\*
        | eventstats median(time_taken) as median p25(time_taken) as p25 p75(time_taken) as p75
        | eval iqr=(p75-p25)
        | eval upper_bound=(median+iqr\*20) 
        | eval is_outlier=if(time_taken > upper_bound, "outlier", "not_outlier")
        | eval is_sleep=if(_raw="*sleep*", "sleep", "not_sleep")
        | eval filter=is_sleep . "," . is_outlier
        | timechart span=5m count by filter

This is really clear cut, for example, we did  not observe a single event with a SLEEP() statement that could be considered an outlier. That is, nothing is charted for the “sleep, outlier” filter.

__STEPS EXPLAINED__

1. eventstats - calculates the median, the boundary for the first quartile, and the boundary for the third quartile
2. eval iqr - calculates the inter-quartile range (IQR)
3. eval_upper_bound - calculates the upperbound using the IQR and a sensitivity factor of 20
4. The next 2 eval statements set a value based on [1] whether or not the time_taken is outside the upper boundary and [2] whether or not a SLEEP() command was included in the raw event data
5. eval filter - Think of this as creating the buckest that are going to be used in the timechart
6. Once the chart is created, look at how many items appear for “sleep, outlier”, which indicates that the sleep command might have been successful.

__============ LOW/HIGH EVENT COUNTS ============__

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

\#eventstats #iqr #eval #if #timechart #web #tstats #join #where #rename
