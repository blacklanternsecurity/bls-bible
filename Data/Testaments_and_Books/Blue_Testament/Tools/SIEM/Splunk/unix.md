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

1. https://docs.splunk.com/Documentation/Splunk/8.1.3/SearchReference/DateandTimeFunctions


## [-] NOTES

- TBD


## [-] USE CASES

__============ CRYPTOMINING ============__

__PROBLEM STATEMENT__ - How long was a browser engaged in crypto-mining activity?

        Date format in logs event → Mon Aug 20 14:05:20 2018

__APPROACH__ 

        index=botsv3 source=cisconvmflowdata dh=*coinhive*
        | eval epochtime_start=strptime(fst, "%a %B %d %H:%M:%S %Y")
        | eval epochtime_end=strptime(fet, "%a %B %d %H:%M:%S %Y")
        | eval duration=round(epochtime_end-epochtime_start)
        | table sa dh pn epochtime_end epochtime_start duration
        | stats sum(duration) as miningTime

__STEPS EXPLAINED__ 

1. Search ciso logs for all events that have a destination host including *coinhive*
2. eval - Convert fst to UNIX epochtime
3. eval - Convert fet to UNIX epochtime
4. eval - Calculate the duration of the connection for each event
5. table - Show data
6. stats - Sum each duration to get the total mining time


## [-] TAGS

\#strptime #eval #stats 
