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

1. https://docs.splunk.com/Documentation/Splunk/6.5.1/Knowledge/Usedefaultfields#punct


## [-] NOTES

- PUNCT appears to pattern out the entire raw event.
- This is an incredibly powerful shortcut to having to develop complicated REGEX


## [-] USE CASES

__============ SUCCESSFUL SQLi ============__

__PROBLEM STATEMENT__ - A web application is being scanned by an attacker looking for vulnerabilities. There is a spike in the number of PHP errors. Do the error logs tell you anything about whether or no the attacks were successful?

__APPROACH__ - For the current data set there are 12 distinct PUNCT values. A single PUNCT value captures 98.949% of the requesrs. 

1. Visualize PUNCT

        index=viningsparks sourcetype=php_error
        | timechart count by punct

2. Remove dominant PUNCT value. Look at other values.

        index=viningsparks sourcetype=php_error NOT punct="[--_::_]__:__\"\"______\"\".______\"_\"?__:\\\\\\\\-\\\\\\.___"
        | timechart count by punct

- Are there odd errors that appear ONLY on the days when the attack occurs?
- Does the error profile change radically during the attack or does it just increas in proportion to the intensity of the scans?
- What can these odd errros tell you about the success/failure of the attack?


## [-] TAGS

\#timechart #punct
