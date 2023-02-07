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

1. https://docs.splunk.com/Documentation/Splunk/8.1.2/SearchReference/ConditionalFunctions#if.28X.2CY.2CZ.29


## [-] NOTES

- If the condition X evaluates to TRUE, returns Y, otherwise returns Z.


## [-] USE CASES

__============ FIELDS TARGETED FOR SQLi ============__

__PROBLEM STATEMENT__ - A web application is being scanned by an attacker looking for vulnerabilities. Which fields were targeted? Were they all targeted equally?

__APPROACH__ 

        index=viningsparks sourcetype=iis 
        | fields _raw
        | rex field=_raw "^(\S+\s+){4}((?<sqli_uri>\S*'\S+)|\S+)\s+((?<sqli_query>\S*'\S+)|\S+)\s+(\S+\s+){3}((?<sqli_ua>\S*'\S+)|\S+)\s+((?<sqli_ref>\S*'\S+)|\S+)\s+.*$"
        | search sqli_uri=* OR sqli_query=* OR sqli_ua=* OR sqli_ref=*
        | eval is_sqli_uri=if(isnull(sqli_uri), "", "uri"), is_sqli_query=if(isnull(sqli_query), "", "query"), is_sqli_ua=if(isnull(sqli_ua), "", "user_agent"), is_sqli_ref=if(isnull(sqli_ref), "", "referer")
        | eval sqli_type=mvappend(is_sqli_uri, is_sqli_query, is_sqli_ua, is_sqli_ref)
        | timechart span=5m count by sqli_type
        | rename VALUE as not_sqli

__STEPS EXPLAINED__ 

1. First extract 4 values based on regex and raw event (rex)
2. Now return events where at least one of these capture groups IS NOT null  (search)
3. For each event, if the value of the capture group is NULL return an empty string, otherwise return a string. So for each event you now have 4 new fields. Some will have a string value and others might be null (eval)
4. Create an array for all values of s_sqli_uri, is_sqli_query, is_sqli_ua, is_sqli_ref from each array (mvappend)
5. When sqli_type is a single value, timechart loks at every 5 minute chunk and buckets the contents of sqli_type to get the bar chart. 
6. Rename “VALUE” so you can see which requests are not SQLi
7. The less the variation in color as you read across the bar graph, the less specific parameters were targetd. The stripes should be consistent in width.

__============ WEB APP TIMEOUTS and ERRORS ============__

__PROBLEM STATEMENT__ - Lets say you have an event with multiple fields. What if you wanted to execute a calculation based one one or more fields and then track how that value changes over time. For example, timeouts and errors for web application requests.

__APPROACH__ 

        index=viningsparks sourcetype=iis 
        | eval is_long=if(time_taken>5000, "timeout", "no_timeout"), is_error=if(sc_status=500, "error", "no_error"), filter=is_long . "," . is_error
        | timechart count by filter

__STEPS EXPLAINED__ 

1. FOR EVERY EVENT - Identify timeouts based on an if/then for the time_taken field. Identify errors based on if/then for the sc_status field. These are both Boolean conditions. A yes or no.
2. Create a filter based on those if/then statements. The filter pairs the variables is_long and is_error. The Period(.) is used for concatenation with eval.
3. Timechart now buckets all the filters values for each event into a bar chart.
4. Are timeout, error events evenly distributed?
5. Are no_timeout, error events evenly distrubuted?
6. Are timeout, no_error events evenly distributed?


## [-] TAGS

#fields #rex #search #eval #timechart #rename
