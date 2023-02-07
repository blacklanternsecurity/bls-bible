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

1. https://docs.splunk.com/Documentation/Splunk/8.1.2/SearchReference/Rex


## [-] NOTES

- This command is used to extract values from fields based on the regex that is submitted


## [-] USE CASES

__============ EXTRACT ADDRESSES FROM POST DATA ============__

__PROBLEM STATEMENT__ - Extract an address from POST data

      src_content: {"addressInformation":{"shipping_address":{"countryId":"US","regionId":"62","regionCode":"WA","region":"Washington","street":["1654 Virginia Ave"],"company":"","telephone":"206-548-9033","postcode":"98101",    "city":"Seattle","firstname":"Sanaa","lastname":"Arellano","save_in_address_book":1},"billing_address":{"countryId":"US","regionId":"62","regionCode":"WA","region":"Washington","street":["1654 Virginia Ave"],"company":"","telephone":"206-548-9033","postcode":"98101","city":"Seattle","firstname":"Sanaa","lastname":"Arellano","save_in_address_book":1,"saveInAddressBook":null},"shipping_method_code":"flatrate","shipping_carrier_code":"flatrate"}}

__APPROACH__ 

      * sourcetype=stream:http site=*froth* *address* *shipping* NOT uri="*\.js"
      | rex field=src_content "street\"\:\[\"(?<streetnumber>[0-9]{1,})(\s*)(?<streetname>[a-zA-Z]{1,})(\s*)(?<abbr>[a-zA-Z]{1,})"
      | where len(streetnumber) > 0
      | where len(streetname) > 0
      | where len(abbr) > 0
      | eval combined=streetnumber + " " + streetname + " " + abbr
      | table combined

__STEPS EXPLAINED__

1. Execute the high-level search to capture POST data that contains an address
2. rex - extract the address from the data using 3 separate capture groups
3. where - each where statement ensures that the capture groups are not NULL
4. eval - combine the address into a single string
5. table - display a table 

__============ BASE64 EXTRACTION ============__

__PROBLEM STATEMENT__  - Extract and decode base64 encoded powershell command

      C:\Windows\System32\WindowsPowershell\v1.0\powershell -noP -sta -w 1 -enc  WwBSAGUARgBdAC4AQQBTAHMARQBNAGIATABZAC4ARwBlAFQAVABZAHAAZQAoACcAUwB5AH

__APPROACH__ 

      . * host="wrk-klagerf" sourcetype="XmlWinEventLog:Microsoft-Windows-Sysmon/Operational" EventID=1 NOT cmdline=*splunk* ParentCommandLine=*powershell*
      | rex field=ParentCommandLine "(\s+)\-enc(\s+)(?<thing>[0-9a-zA-Z=]{1,})"
      | eval clength=len(thing)%4
      | table clength thing
      | base64 field="thing" action="decode"
      | eval thing = trim(replace(thing, "\\\\x00", ""))
      | stats values(thing)

__STEPS EXPLAINED__ 

1. Execute a basic search for process creation events with powershell in the ParentCommandLine
2. rex - extract the base64 encoded command
3. base64 - decoded the data that was extracted
4. eval - format the decoded data using “trim” and “replace”
5. stats - display unique values for the decoded data

__============ EXAMINE 3rd LEVEL DOMAIN LENGTH ============__ 

__PROBLEM STATEMENT__  - Find the average length of the distinct third-level subdomains in the queries

__APPROACH__  

      * source="lambda:DNS"
      | rex field=_raw "((\s+)|(([a-zA-Z0-9\-]{1,}\.)){1.})(?<urlyd>[a-zA-Z0-9\-]{1,})(\.brewertalk\.com)(\s+)"
      | where len(urlyd) > 1 → I dont agree with this change though
      | eval run=len(urlyd)
      | stats avg(run) as avg_run 
      | eval avg_run=round(avg_run,2)


__STEPS EXPLAINED__ 

1. Retrieve all DNS records
2. rex - extract 3rd level subdomains fromm each URL
3. where - selected out those 3rd level subdomains that have a length greater than 1
4. eval - calculate the length for each
5. stats - caluclate the average
6. eval - round the average to 2 decimal places 

__============ URLs and FILENAMES ============__ 

__PROBLEM STATEMENT__  - Find all URLs with an exact filename “iindex,jpeg”

__APPROACH__  

      * sourcetype=stream:http
      | rex field=uri_path "(?<file>i[a-zA-Z0-9]{5,5}\.[a-zA-Z]{4,4})"
      | where len(file) > 1
      | stats values(file)

__STEPS EXPLAINED__ 

1. Return every stream:http event
2. rex - extract all files that fit a very specific format from uri_path
3. where - select results where the length is > 1
4. stats - look at unique results


## [-] TAGS

\#rex #eval #where #base64 #stats #avg #len
