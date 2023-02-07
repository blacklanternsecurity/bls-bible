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
# App-Specific Scans
## Overview

## Tools
### General

	#@TODO - check out below tools
1. Acunetix
2. Grendelscan
3. NStealth
4. Obiwan III
5. w3af

* SSRFmap -<br />([https://github.com/swisskyrepo/SSRFmap](https://github.com/swisskyrepo/SSRFmap))
* damnwebscanner https://github.com/swisskyrepo/DamnWebScanner

### Wordpress
#### wpscan
* [GitHub](https://github.com/wpscanteam/wpscan) https://wpscan.com/wordpress-security-scanner

#### wordpresscan

https://github.com/swisskyrepo/Wordpresscan


### Domino

* dominoaudit

		dominoaudit.pl [options] -h <IP>


### Joomla

cms_few
```
./cms.py <site-name>
```
joomsq
```
./joomsq.py <IP>
```

joomlascan
```
./joomlascan.py <site> <options>  [options i.e. -p/-proxy <host:port> : Add proxy support -404 : Don't show 404 responses]
```

joomscan
```
./joomscan.py -u "www.site.com/joomladir/" -o site.txt -p 127.0.0.1:80
```

jscan
```jscan.pl -f hostname```
    (shell.txt required)

aspaudit.pl
```asp-audit.pl http://target/app/filename.aspx (options i.e. -bf)```

## Vbulletin
```
vbscan.py
vbscan.py <host> <port> -v
vbscan.py -update
```

## ZyXel
```zyxel-bf.sh```
