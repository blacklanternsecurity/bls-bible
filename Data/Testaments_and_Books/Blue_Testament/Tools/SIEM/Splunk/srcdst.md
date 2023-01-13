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

__============ SRC-DST Count ============__

__PROBLEM STATEMENT__ - Analyze SRC-DST IP, group, and then look at stats for SRC and DST IPs that communicate most often. 

__APPROACH__ 

        sourcetype=fgt_traffic src=192.168.225.* NOT (dest=192.168.* OR dest=10.* OR dest=8.8.4.4 OR dest=8.8.8.8 OR dest=224.*)
        | stats count by src dest
        | where count > 1
        | sort – count

__STEPS EXPLAINED__ 

1. search - filter on events from specific src. Remove private IP space
2. stats - count events for specific src dest pairs
3. where - look for pairs where the count is > 1
4. sort - sort by descending count

__============ TOP TALKERS by SRC ============__

__PROBLEM STATEMENT__ - Show top talkers by src IP

__APPROACH__ 

        index="benevis" sourcetype= pan:traffic | stats count by src_ip | sort -count

__STEPS EXPLAINED__ 

1. search - events from PAN traffic
2. stats - count events by SRC IP
3. sort - show me the top talkers

__============ TOP TALKERS by DST ============__

__PROBLEM STATEMENT__ - Show top talkers by dest IP

__APPROACH__ 

        index="benevis" sourcetype= pan:traffic | stats count by dst_ip | sort -count

__STEPS EXPLAINED__ 

1. search - events from PAN traffic
2. stats - count events by DST IP
3. sort - show me the top talkers

__============ TOP TALKERS by Specified SRC ============__

__PROBLEM STATEMENT__ - Show top talkers for compromised Nertscaler ADC. The ADC has 3 IPs.

__APPROACH__ 

        sourcetype=pan:traffic src_ip=10.100.99.41 OR src_ip=10.100.99.43 OR src_ip=10.100.253.60
        | fields src_ip, dest_ip
        | Table src_ip dest_ip
        |  stats count by src_ip dest_ip
        |  sort -count

__STEPS EXPLAINED__ 

1. search - events from PAN traffic. Filter on 3 specific SRC IPs
2. fields - from this search bring forward the src and dst IP fields
3. table - show src and dst IP fields
4. stats - count events for specific src dest pairs
5. sort - sort by descending count

__============ SRC IPS to SAME DST ============__

__PROBLEM STATEMENT__ - SRC IPs that talked to the same host

__APPROACH__ 

        index=botsv2 sourcetype=stream:ftp src_ip=10.0.2.109
        | rename src_ip AS src_ip_1
        | join dest_ip max=0 [search index=botsv2 sourcetype=stream:ftp src_ip=10.0.2.107
            | rename src_ip AS src_ip_2]
        | eval combined=src_ip_1 + " " + src_ip_2 + " " + dest_ip
        | stats values(combined) 

__STEPS EXPLAINED__ 

1. search - events from the FTP stream for the FIRST specific src_ip
2. rename - rename the first host as src_ip_1
3. join - join on the dest_ip. max=0 ensures that all rows will be returned and not just the first result
4. search - this sub search executes a search for events from the FTP stream for a SECOND specific src_ip
5. rename - rename the second host as src_ip_2
6. eval - combine src1, src2, and the dst IP as a string
7. stats values() - find all unique values for that string

__============ IMAGEs and NETWORK CONNECTIONS ============__

__PROBLEM STATEMENT__ - Look at the Images responsible for the connections

__APPROACH__ 

        index=main sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=3
        | stats values(DestinationIp) list(SourceIp) list(DestinationPort) list(_time) by Image
        | sort by _time

__STEPS EXPLAINED__ 

1. search - network connection events in the sysmon logs
2. stats values() - show unique values for the destination IP
3. list - for each Image and for unique destination IPs associated with that image, list the source IP, destination port, and _time 


## [-] TAGS

\#list #stats #search #rename #join #eval #stats #table #fields
