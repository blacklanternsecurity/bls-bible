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
# FFUF Usage
### References

### Overview

### Process
* Basic Usage

		ffuf -u http://foo.com/FUZZ -w ./wl.txt

#### Response filtering

			ffuf -u http://foo.com/FUZZ -w ./wl.txt -fc 301
		* -fX - filter out responses, where X is:
			* `c` - response code
			* `s` - size
			* `w` - words
			* `l` - lines
			* `r` - regex
			* `t` - time (requires special arguments, e.g. < or >)
		* `-mX` - match responses; same arguments as above
		* Both modes accept ranges, e.g. `-fs 120-160`
		* GET data
			
				ffuf -u http://foo.com/download.php?file=FUZZ' -w ./wl.txt
		* POST data

				ffuf -u http://foo.com/download.php -d 'file=FUZZ' -w ./wl.txt

#### Credential fuzzing

		ffuf -u http://foo.com/login.aspx -d '{"user": "admin", "password": "FUZZ"}' -w ./wl.txt

*  Password spraying

		ffuf -u http://foo.com/login.aspx -d '{"user": "FUZZ", "password": "Winter2021!"}' -w ./users.txt

#### Multiple wordlists

		ffuf -u http://foo.com/PAGE.aspx -d '{"user": "admin", "password": "PASS"}' -w ./wl.txt:PAGE -w ./wl2.txt:PASS

## VHost fuzzing
	1. Get response size for base domain:

			ffuf -u http://foo.com/index.html?FUZZ -w wl.txt
	2. Fuzz vhosts

			ffuf -u http://foo.com/index.html -H "Host: FUZZ.foo.com" -w ./wl.txt -fs $BASE_RESPONSE_SIZE

#### Extensions

		ffuf -u http://foo.com/FUZZ -e .html,.php,.txt -w wl.txt

#### Recursion

		ffuf -u http://foo.com/FUZZ -w ./wl.txt -recursion
* Recursion limit

		ffuf -u http://foo.com/FUZZ -w ./wl.txt -recursion -recursion-depth 2

#### Interactive
* Press enter during a scan for a menu that will let you pause, resume, filter, recurse, etc. without restarting