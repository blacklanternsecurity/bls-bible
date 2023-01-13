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

1. https://www.splunk.com/en_us/blog/security/finding-islands-in-the-stream-of-data.html
2. https://www.splunk.com/en_us/blog/security/ut-parsing-domains-like-house-slytherin.html
3. https://docs.splunk.com/Documentation/SCS/current/SearchReference/lookupcommandoverview#How_the_lookup_command_works
4. https://www.splunk.com/en_us/blog/security/ut-parsing-domains-like-house-slytherin.html


## [-] NOTES

- What is the "URL Toolbox App?
- This is a Splunk Security App.
- To view the Apps that are installed on your Splunk instance, click the dropdown at the topleft > “Manage Apps”


## [-] USE CASES

__============ DNS DATA EXFILTRATION ============__

__PROBLEM STATEMENT__ - Examine DNS queries. Identify possible instances of data exfiltration 

__APPROACH__ 

        * sourcetype="stream:dns" record_type=A
        | table query{}
        | lookup ut_parse_extended_lookup url AS query{}
        | search ut_domain!=None NOT (ut_domain without_tld=microsoft OR ut_domain without_tld=msn OR ut_domain without_tld=akamaiedge OR ut_domain without_tld=akadns OR ut_domain without_tld=nsatc.net OR ut_domain without_tld=qwest.net OR ut_domain without_tld=windows.com OR ut_domain without_tld=arin.net)
        | `ut_shannon(ut_subdomain)`
        | stats count by query{} ut_subdomain ut_domain ut_domain_without_tld ut_tld ut_shannon
        | sort - ut_shannon

__STEPS EXPLAINED__ 

1. Search - For all indexes, search the DNS stream for events with record_type=A
2. table - Output a table with the query{} for each event. These are the FQDNs that users were attempting to resolve
3. lookup - Execute a lookup against the ut_parse_extended_lookup dataset. I'm not sure how or when it creates this dataset. This search takes the values in “query{}”, maps it to the url field in the dataset, and returns the results
4. search - This search makes sure that the “ut_domain” field is valued and removes domains that we are not interested in
5. \`ut_shannon(ut_subdomain)\` - This is a “macro” from the “URL Toolbox” App that calculates Shannon entropy
6. stats - Counts and displays results
7. sort - Sorts according to decreasing Shannon entropy


## [-] TAGS

\#lookup #table #url #toolbox #ut_shannon #stats #sort
