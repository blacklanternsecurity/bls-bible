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

__============ KNOWN COMPROMISED HOSTs to MALICIOUS IPs ============__

__PROBLEM STATEMENT__ - Shows that ALL COUTBOUND traffic was BLOCKED from the compromised ADC to BOTH malicious IPs

__APPROACH__ 

        sourcetype=pan:traffic (src_ip=10.100.99.41 OR src_ip=10.100.99.43 OR src_ip=10.100.253.60) AND (dest_ip=62.113.112.33 OR dest_ip=185.178.45.221)
        | fields src_ip, dest_ip, rule, action
        | Table src_ip dest_ip rule action
        | stats count by src_ip dest_ip rule action
        | sort - count

__STEPS EXPLAINED__ 

1. Search firewall traffic for traffic going from 3 compromised IPs to 2 malicious DST IPs
2. fields - extract specific fields from search results
3. table - display results in a table
4. stats - generate count according to src_ip - dest_ip - rule - action
5. sort - display by descending count

__============ SEARCH FOR COMPROMISED HOSTS  ============__

__PROBLEM STATEMENT__ - Shows that no other IPs were communicating OUTBOUND with the malicious IPs

__APPROACH__ 

        sourcetype=pan:traffic (dest_ip=62.113.112.33 OR dest_ip=185.178.45.221) AND NOT (src_ip=10.100.99.41 OR src_ip=10.100.99.43 OR src_ip=10.100.253.60)

__STEPS EXPLAINED__ 

1. Exclude SRC IPs for hosts that are KNOWN to be compromised. Look for any other hosts communicating with Malicious IPs

__============ INBOUND TRAFFIC FROM MALICIOUS IPs to COMPROMISED HOSTS ============__

__PROBLEM STATEMENT__ - Shows that there was NO INBOUND traffic from BOTH malicious IPs to the compromised ADC

__APPROACH__ 

        sourcetype=pan:traffic (dest_ip=10.100.99.41 OR dest_ip=10.100.99.43 OR dest_ip=10.100.253.60) AND (src_ip=62.113.112.33 OR src_ip=185.178.45.221)
        | fields src_ip, dest_ip, rule, action
        | Table src_ip dest_ip rule action
        | stats count by src_ip dest_ip rule action
        | sort -count

__STEPS EXPLAINED__ 

1. Search firewall traffic for traffic ingressing from malicious IPs to compromised hosts on the internal network
2. fields - extract specific fields from search results
3. table - display results in a table
4. stats - generate count according to src_ip - dest_ip - rule - action
5. sort - display by descending count

__============ INBOUND TRAFFIC FROM MALICIOUS IPs to ANY ============__

__PROBLEM STATEMENT__ - Shows that there was NO INBOUND traffic from BOTH malicious IPs to ANY Benevis IPs

__APPROACH__ 

        sourcetype=pan:traffic src_ip=62.113.112.33 OR src_ip=185.178.45.221
        | fields src_ip, dest_ip, rule, action
        | Table src_ip dest_ip rule action
        | stats count by src_ip dest_ip rule action
        | sort -count

__STEPS EXPLAINED__ 

1. Search firewall traffic for traffic ingressing from malicious IPs to ANY host on the internal network
2. fields - extract specific fields from search results
3. table - display results in a table
4. stats - generate count according to src_ip - dest_ip - rule - action
5. sort - display by descending count


## [-] TAGS

\#fields #stat #sort #table

