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

1. https://www.splunk.com/en_us/blog/security/i-need-to-do-some-hunting-stat.html
2. https://www.splunk.com/en_us/blog/security/hunting-with-splunk-the-basics.html


## [-] NOTES

1. Who are the top talkers by SRC/DST IP?
2. Who are the least talkers by  SRC/DST IP?
3. Who are the top talkers by bytes exchanged?
4. Who are the least talkers by bytes exchanged? (beacons)
5. Are there numerous internal hosts speaking with the same external IP?
6. Are there numerous internal hosts speaking with the same external IP and passing the SAME amount of data? 
7 Look at all bytes leaving a single internal IP . Then look at bytes leaving from the internal IP to each external IPs alongside the total bytes leaving from that internal IP.


## [-] USE CASES

__============ BYTES IN and OUT ============__

__PROBLEM STATEMENT__ - Analyze SRC-DST IP, group, and then look at stats for total bytes that come in and out per IP pair.

__APPROACH__

        sourcetype=fgt_traffic src=192.168.225.* NOT (dest=192.168.* OR dest=10.* OR dest=8.8.4.4 OR dest=8.8.8.8 OR dest=224.*)
        | stats sum(bytes_in) as total_bytes_in sum(bytes_out) as total_bytes_out by src dest
        | table src dest total_bytes_in total_bytes_out
        | sort – total_bytes_out

__STEPS EXPLAINED__ 

1. search - return events for for a specific /24 subnet and exclude specific IPs and IP ranges as the destination IP
2. stats - for each src, dest pair sum the total bytes IN and the total bytes OUT
3. table - show src, dst, total bytes in, and total bytes out
4. sort - sort by largets to smallest bytes out

__============ TOP EGRESS OUT ============__

__PROBLEM STATEMENT__ - Analyze internal hosts for data leaving the network. Sort by those pushing the greatest amount of data out.

__APPROACH__

        sourcetype=fgt_traffic src=192.168.225.* NOT (dest=192.168.* OR dest=10.* OR dest=8.8.4.4 OR dest=8.8.8.8 OR dest=224.*) bytes_out>0
        | eventstats sum(bytes_out) AS total_bytes_out by src
        | table src dest bytes_out total_bytes_out
        | sort src – bytes_out

__STEPS EXPLAINED__

1. search - return events for for a specific /24 subnet and exclude specific IPs and IP ranges as the destination IP
2. eventstats - for all events and for each src IP, sum the total bytes OUT
3. table - show src, dest, bytes out for event, and total bytes out for the SRC. 
4. sort - sort by src and then the largest to smallest bytes out

__============ MAJORITY EGRESS TO SINGLE SYSTEM ============__

__PROBLEM STATEMENT__ - Look for internal systems where > 60% of the data going out is to a single system

__APPROACH__

        sourcetype=fgt_traffic src=192.168.225.* NOT (dest=192.168.* OR dest=10.* OR dest=8.8.4.4 OR dest=8.8.8.8 OR dest=224.*)
        | eventstats sum(bytes_out) AS total_bytes_out by src
        | eval percent_bytes_out = bytes_out/total_bytes_out * 100
        | table src dest bytes_in bytes_out total_bytes_out percent_bytes_out
        | where percent_bytes_out > 60
        | sort - percent_bytes_out dest

__STEPS EXPLAINED__

1. search - return events for for a specific /24 subnet and exclude specific IPs and IP ranges as the destination IP
2. eventstats - Applies to search results. For events from search results, for each src IP, sum the total bytes OUT
3. eval - for each event in the search results, for each src, calcluate the percentage bytes out with repect to the total bytes out for that src. eval adds “percent_bytes_out” as a field to each event returned
4. table / where - show results for src IPs where > 60 percent of data is going to single system 

__============ BURSTY TRAFFIC ============__

__PROBLEM STATEMENT__ - Look at a single SRC IP. Look at bytes out and total bytes out as a function of time. You can see that the traffic is bursty.

__APPROACH__

        sourcetype=fgt_traffic src=192.168.225.* NOT (dest=192.168.* OR dest=10.* OR dest=8.8.4.4 OR dest=8.8.8.8 OR dest=224.*) bytes_out>0
        | sort date
        | streamstats sum(bytes_out) as total_bytes_out by src
        | table date bytes_out total_bytes_out

__STEPS EXPLAINED__

1. search - return events for for a specific /24 subnet and exclude specific IPs and IP ranges as the destination IP. Bytes must be > 0
2. sort - sort events by date
3. streamstats - as events come in sum the total bytes out by SRC
4. table - show results for bytes out and total_bytes_out 


## [-] TAGS

\#stats #eval #eventstats #streamstats #table #sort #where
