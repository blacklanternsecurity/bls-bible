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

1. https://www.splunk.com/en_us/blog/security/hunting-your-dns-dragons.html
2. https://www.splunk.com/en_us/blog/security/hunting-with-splunk-the-basics.html
3. https://docs.splunk.com/Documentation/SCS/current/SearchReference/mvexpandcommandoverview#How_the_mvexpand_command_works


## [-] NOTES

- Increase in volume of requests by the client (indicating C&C or data movement)
- Change in the type of resource records we see (e.g., TXT records from hosts that don’t typically send them)
- Variance in the length of the request (indicating DGA or encoded/obfuscated data stream)
- Variability in the frequency of requests (Beaconing activity to C&C)
- Randomness in domain names (DGA)
- Substitution of domains to very slightly altered domains (typo-squatting)


## [-] USE CASE

__============ STEP 1 ============__

__PROBLEM STATEMENT__ - How do DNS queries change overtime for each src IP? Do you see spikes in traffic?

__APPROACH__ 

        tag=dns message_type="Query" 
        | timechart span=1h limit=10 usenull=f useother=f count AS Requests by src

__STEPS EXPLAINED__

1. Execute a search for DNS queries
2. timechart - look at 1 hour increments, limit=10 (give me the 10 highest scoring distinct values), usenull=f - do not create events that do not contains a split-by field(src), useother=f - DO NOT merge all the series that are excluded by the limit option into a single new series.
3. timechart - for every hour show the DNS queries that were executed by SRC. Only include the top 10 SRC IPs with the most queries.

__============ STEP 2 ============__

__PROBLEM STATEMENT__ - How do requests for specific record types change over time? Do you see changes in the mix/ratio of records requested?

__APPROACH__ 

        tag=dns message_type="QUERY"
        | timechart span=1h count BY record_type

__STEPS EXPLAINED__

1. Execute a search for DNS queries
2. timechart - look at 1 hour increments by record type.

__============ STEP 3 ============__

__PROBLEM STATEMENT__ - Examine the query length for each SRC IP.  Can you see attempts to exfiltrate data?

__APPROACH__ 

        tag=dns message_type="QUERY"
        | mvexpand query                         
        | eval queryLength=len(query)
        | stats count by queryLength, src
        | sort -queryLength, count
        | table src queryLength count → remeber that “count” is just another field at this point in the pipeline
        | head 1000

- (MVEXPAND) creates individual events, or rows, for each value in a multivalue field. “query” is the multi-valued field.
- (EVAL) creates a new field called querylength in each event
- (STATS) count by the src, querylength pair
- (SORT) sort first by querylength (descending) and then by count (ascending)
- (TABLE) create a table with these 3 fields
- (HEAD) show top 1000 results

__STEPS EXPLAINED__

1. Execute a search for DNS queries
2. mvexpand - create a new event for every query executed. If there are 2 values in the query{} field, creak them out as separate events
3. eval - for each event, calculate the length of the query, and add as a new field in the event
4. stats - look at the counts for the querylength-src pairs
5. sort - sort first by querylength (descending) and then by count (ascending)
6. table - create a table with these 3 fields
7. head - show top 1000 results

__============ STEP 4 ============__

__PROBLEM STATEMENT__ - Look for DNS beaconing

__APPROACH__ 

        tag=dns message_type="QUERY"
        | fields _time, query
        | streamstats current=f last(_time) as last_time by query
        | eval gap=last_time - _time
        | stats count avg(gap) AS AverageBeaconTime var(gap) AS VarianceBeaconTime BY query
        | eval AverageBeaconTime=round(AverageBeaconTime,3), VarianceBeaconTime=round(VarianceBeaconTime,3)
        | sort -count
        | where VarianceBeaconTime < 60 AND count > 2 AND AverageBeaconTime>1.000
        | table  query VarianceBeaconTime  count AverageBeaconTime

__STEPS EXPLAINED__

1. FIELDS - First select the _time and query fields for each event. Do not use any other data. Each event has only 2 fields going through this pipeline.
2. STREAMSTATS - As each event comes in, use streamstats to the capture the last time a DNS QUERY was made for that specific record. current=f ensures that the current event being considered is NOT used to set the last_time variable being created. For example, if we see a query for cnn.com, we go back and find the last time a query was made for cnn.com. Set that as last_time.
3. EVAL - For each event, use eval to calculate the gap in time between the current QUERY and the last time a QUERY was made for that record. Add “gap” as a field for each event that comes in. So after this step, the event wil now include _time, query, and gap. We started with 2 fields. Now we have 3.
4. STATS - For all the QUERIES made for a specific record up to and including the current time, count them up, calculate the average gap time and calculate the variance in gap time.
5. EVAL - Use eval to round off the average beacon time and the variance. AverageBeaconTime and VarianceBeaconTime are now added as fields to each processed event. Now we have 5 fields. This is what streamstats does. As you process more and more DNS query events the AverageBeaconTime and VarianceBeaconTime are updated based on the DNS QUERY. For true beaconing, we should see a high count AND a low variance
6. SORT - Sort the events in descending order according to the number of times a DNS query was made
7. WHERE - Only show events that satisfy specific requirements for AverageBeaconTime and VarianceBeaconTime 
8. TABLE - Show a table with entries as specified above. These are the FINAL results for each DNS QUERY MADE. Each DNS QUERY event was considered and is now reflected in the table results. It's almost like STREAMSTATS acts as a WHILE loop so long as DNS QUERY events continue to come in.


## [-] TAGS

#streamstats #eval #stats #sort #mvexpand #table #head #where #fields
