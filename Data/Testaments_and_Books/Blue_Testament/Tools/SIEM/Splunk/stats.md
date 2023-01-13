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

1. https://www.splunk.com/en_us/blog/tips-and-tricks/search-command-stats-eventstats-and-streamstats-2.html
2. https://docs.splunk.com/Documentation/Splunk/8.1.2/Search/Aboutsearchlanguagesyntax
3. https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/CommonStatsFunctions


## [-] NOTES

- Calculate aggregate statistics over the dataset, similar to SQL aggregation. 
- If called without a by clause, one row is produced, which represents the aggregation over the entire incoming result set. 
- If called with a by-clause, one row is produced for each distinct value of the by-clause. 
- With each Splunk command or term, an intermediate table is produced without the user having to issue any command to allocate the tables.
- Notice that the bytes column is empty above, because once the table is created by the stats command, Splunk now knows nothing about the original bytes field earlier in the pipeline.
- The "Anatomy" of a search is super helpful. Also, finally realized that stats is BLIND to the original search. It only knows about the output that is RIGHT BEFORE the stats command is called. Finally see why eventstats and stats are very different.
- It is also odd to see that once "count" shows up as a column in a table it can be manipulated just like any other column. It loses its special functions status if you want 


## [-] USE CASES

__============ LOGINS from DIFFERENT IPs and USER AGENTS ============__

__PROBLEM STATEMENT__ - Which user ID experienced the most logins to their account from different IP address and user agent combinations? Answer guidance: The user ID is an email address

__APPROACH__

        * sourcetype=stream:http site=*froth* uri=*login* form_data=*
        | rex field=form_data "password\]=(?<pass>.*)&"
        | rex field=form_data "username\]=(?<user>.*?)&"
        | stats dc(src_ip) by user
        | sort - dc(src_ip)

__STEPS EXPLAINED__

1. Execute search for login activity
2. rex - extract username and password
3. stats - do a distinct count of src IP by user
4. sort - sort by largest to smallest count

__PROBLEM STATEMENT__ - Do a distinct count on http_user_agent by user

__APPROACH__ 

        * sourcetype=stream:http site=*froth* uri=*login* form_data=*
        | rex field=form_data "password\]=(?<pass>.*)&"
        | rex field=form_data "username\]=(?<user>.*?)&"
        | stats dc(http_user_agent) by user
        | sort - dc(http_user_agent)

__STEPS EXPLAINED__ 

1. Execute search for login activity
2. rex - extract username and password
3. stats - do a distinct count of user agent by user
4. sort - sort by largest to smallest count

__============ SHARED PASSWORDS ============__

__PROBLEM STATEMENT__ - Several user accounts sharing a common password is usually a precursor to undesirable scenario orchestrated by a fraudster. Which password is being seen most often across users logging into http://store.froth.ly.

__APPROACH__

        * sourcetype=stream:http site=*froth* uri=*login* form_data=*
        | rex field=form_data "password\]=(?<pass>.*)&"
        | rex field=form_data "username\]=(?<user>.*?)&"
        | stats dc(user) by pass
        | sort - dc(user)

__STEPS EXPLAINED__

1. Execute search for login activity
2. rex - extract username and password
3. stats - do a distinct count of users by password
4. sort - sort by largest to smallest count


## [-] TAGS

\#rex #stats #sort 
