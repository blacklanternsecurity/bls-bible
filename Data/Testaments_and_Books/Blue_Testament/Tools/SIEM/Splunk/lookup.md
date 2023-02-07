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

1. https://www.splunk.com/en_us/blog/security/lookup-before-you-go-go-hunting.html


## [-] NOTES

- TBD

## [-] USE CASES

__============ LOOK-UPS FOR MALICIOUS USER AGENT ============__

__PROBLEM STATEMENT__ - How can you simplify searches using lookups? This is going to be important when we have a list of IOCs we need to search on within a SPECIFIC FIELD in our data set. Find all events where the user_agent field matches the user agents identified for the Hafnium APT Group

__APPROACH__ 

        index=msexchange 
            [| inputlookup es-cve-2021-26855-user-agents.csv]
    
__STEPS EXPLAINED__ - Search behind the scenes this is actually transformed to:    

        index=msexchange 
            useragent="DuckDuckBot/1.0;+(+http://duckduckgo.com/duckduckbot.html)" OR useragent="..."
    
__============ LOOK-UPS FOR MALICIOUS WEB SHELL DESCRIPTION ============__

__PROBLEM STATEMENT__ - Return the description for a webshell within the hafnium_webshells lookup

__APPROACH__ 

        | makeresults
        | eval test_field="xx.aspx"
        | lookup hafnium_webshells filename AS test_field OUTPUT description    

__STEPS EXPLAINED__

1. 

## [-] TAGS

#makeresults #eval #lookup #inputlookup
