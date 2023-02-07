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

1. https://docs.splunk.com/Documentation/Splunk/8.1.2/SearchReference/DateandTimeFunctions


## [-] NOTES

- Dealing with dates. EpochTime is easier to subtract and manipulate.
- Concatenating strings


## [-] USE CASES

__============ CONVERT TO UNIX TIME ============__

__PROBLEM STATEMENT__ - Convert dates to UNX timestamps

__APPROACH__

        eval epochDate=strptime(date, "%a %b %d %Y %H:%M:%S PDT%z (%Z)")

__STEPS EXPLAINED__

1. Convert the current sate to the UNIX time format and assign it to the variable epochDate

__============ UNIQUE NAMES FOR BIG SPENDERS ============__

__PROBLEM STATEMENT__ - Find unique values for customer names

__APPROACH__ 

        * sourcetype=stream:http site=*froth* *address* *shipping* NOT uri="*\.js"
        | spath input=src_content 
        | rename "addressInformation.shipping_address.firstname" AS first
        | rename "addressInformation.shipping_address.lastname" AS last
        | spath input=dest_content 
        | rename "totals.grand_total" AS total
        | WHERE total > 999
        | eval fullname=first + " " + last
        | stats values(fullname)
        | stats dc(fullname)

__STEPS EXPLAINED__

1. Retrieve events with home and billing shipping addresses for all froth.ly websites
2. spath - assign the src_content to input. This allows us to leverage and search XML much more easily
3. rename - rename 2 fields from the source content data and based on the SPATH schema
4. spath - assign the dst_content to input. This allows us to leverage and search XML much more easily
5. rename - rename 1 field from the destination content data and based on the SPATH schema
6. where - filter the events down to those where more than $999 was spent
7. eval - concatenate first and last names into a single variable named “fullname”
8. stats - get unique values and a distinct count for fullname across the events returned

__============ SQLI SLEEP() STATEMENTS ============__

__PROBLEM STATEMENT__ - Determine whether or not the SLEEP statements submitted as part of a SQLi attack were successful

__APPROACH__ 

        index="viningsparks" sourcetype=iis "sleep"
        | rex field=_raw "sleep.(?<sleep_s>[^)]+)"
        | eval time_s=time_taken/1000
        | search sleep_s=*
        | eval delta=time_s-sleep_s
        | timechart span=1m max(delta)

__STEPS EXPLAINED__ 

1. Capture the actual sleep time. Remember that [^)] means match any character that is not in the set
2. Convert the time_taken from the event from milliseconds to seconds
3. Now find events that have a “SLEEP” statement
4. Subtract sleep_s from time_s
5. If the sleep statement did not work, then the value for “delta” should always be negative
6. For each minute plot the maximum value of delta
7. Where is delta positively valued? Did the sleep statement work?                 


## [-] TAGS

\#spath #rename #where #eval #stats #dc #values
