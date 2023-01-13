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
# ldapsearch-ad.py
### Installation
* GitHub -<br />[https://github.com/yaap7/ldapsearch-ad](https://github.com/yaap7/ldapsearch-ad)
* Ubuntu

		apt install ldap-utils

### Attacks

* <details><summary>No Creds (Click to expand)</summary><p>

		ldapsearch-ad.py -l <dc_ip> -t info
	* Domain functional level
	* Naming Contexts
	* <details><summary>Example Output (Click to expand)</summary><p>

			(ldapsearch-ad-cWbJ38xp) root@ubuntu:/# python ldapsearch-ad.py -l 10.0.0.1 -t info                                                                                           
			### Server infos ###
			[+] Forest functionality level = Windows 2016
			[+] Domain functionality level = Windows 2016
			[+] Domain controller functionality level = Windows 2016
			[+] rootDomainNamingContext = DC=securelab,DC=local
			[+] defaultNamingContext = DC=securelab,DC=local
			[+] ldapServiceName = securelab.local:dc01$@SECURELAB.LOCAL
			[+] naming_contexts = ['DC=securelab,DC=local', 'CN=Configuration,DC=securelab,DC=local', 'CN=Schema,CN=Configuration,DC=securelab,DC=local', 'DC=DomainDnsZones,DC=securelab,DC=local', 'DC=ForestDnsZones,DC=securelab,DC=local']
* <details><summary>Domain User Creds (Click to expand)</summary><p>

		ldapsearch-ad.py -l 192.168.56.20 -d evilcorp -u jjohnny -p 'P@$$word' -t all
	* <details><summary>Example Output (Click to expand)</summary><p>

			(ldapsearch-ad-cWbJ38xp) root@ubuntu:/# python ldapsearch-ad.py -l 10.0.0.1 -d securelab -u domain_user -p 'P@ssword' -t all
			### Server infos ###
			[+] Forest functionality level = Windows 2016
			[+] Domain functionality level = Windows 2016
			[+] Domain controller functionality level = Windows 2016
			[+] rootDomainNamingContext = DC=securelab,DC=local
			[+] defaultNamingContext = DC=securelab,DC=local
			[+] ldapServiceName = securelab.local:dc01$@SECURELAB.LOCAL
			[+] naming_contexts = ['DC=securelab,DC=local', 'CN=Configuration,DC=securelab,DC=local', 'CN=Schema,CN=Configuration,DC=securelab,DC=local', 'DC=DomainDnsZones,DC=securelab,DC=local', 'DC=ForestDnsZones,DC=securelab,DC=local']
			### Result of "admins" command ###
			All members of group "Domain Admins":
			[*]     Administrator (DONT_EXPIRE_PASSWORD)
			[*]     domain_admin (DONT_EXPIRE_PASSWORD)
			All members of group "Administrators":
			[*]     Administrator (DONT_EXPIRE_PASSWORD)
			[*]     domain_admin (DONT_EXPIRE_PASSWORD)
			All members of group "Enterprise Admins":
			[*]     Administrator (DONT_EXPIRE_PASSWORD)
			### Result of "pass-pols" command ###
			Default password policy:
			[+] |___Minimum password length = 7
			[+] |___Password complexity = Enabled
			[*] |___Lockout threshold = Disabled
			[+] No fine grained password policy found (high privileges are required).
			### Result of "trusts" command ###
			### Result of "kerberoast" command ###
			### Result of "asreqroast" command ###
			### Result of "goldenticket" command ###
			[+] [DN: CN=krbtgt,CN=Users,DC=securelab,DC=local - STATUS: Read - READ TIME: 2021-11-06T22:27:14.041025
			    whenChanged: 2021-11-01 23:18:25+00:00
			]
			### Result of "search-delegation" command ###
			[*] DN: CN=DC01,OU=Domain Controllers,DC=securelab,DC=local - STATUS: Read - READ TIME: 2021-11-06T22:27:14.048034
			    cn: DC01
			    sAMAccountName: DC01$

			[*] DN: CN=DC02,OU=Domain Controllers,DC=securelab,DC=local - STATUS: Read - READ TIME: 2021-11-06T22:27:14.048091
			    cn: DC02
			    sAMAccountName: DC02$


* <details><summary>List all domain users (Click to expand)</summary><p>

		ldapsearch -LLL -x -H ldap://pwnylabdc01.pwny.lab -D "jar-jar.binks@pwny.lab" -w Welcome2015 -b dc=pwny,dc=lab "(objectClass=user)" sAMAccountName userPrincipalName memberOf
* <details><summary>Enumerate Password Policy (Click to expand)</summary><p>
		
		ldapsearch-ad.py -l $LDAP_SERVER -d $DOMAIN -u $USER -p $PASSWORD -t pass-pol
* <details><summary>List all domain groups (Click to expand)</summary><p>

		ldapsearch -LLL -x -H ldap://pwnylabdc01.pwny.lab -D "jar-jar.binks@pwny.lab" -w Welcome2015 -b dc=pwny,dc=lab "(objectClass=group)" sAMAccountName member memberOf
* <details><summary>List all domain joined systems (Click to expand)</summary><p>

		ldapsearch -LLL -x -H ldap://pwnylabdc01.pwny.lab -D "jar-jar.binks@pwny.lab" -w Welcome2015 -b dc=pwny,dc=lab "(objectClass=computer)" name dNSHostname operatingSystem operatingSystemVersion lastLogonTimestamp servicePrincipalName
* <details><summary>Enumerate all members of a group (Click to expand)</summary><p>

		ldapsearch -LLL -x -H ldap://pwnylabdc01.pwny.lab -D "jar-jar.binks@pwny.lab" -w Welcome2015 -b dc=pwny,dc=lab "(&(objectClass=user)(memberof:1.2.840.113556.1.4.1941:=CN=Domän-Admins,CN=Users,DC=PWNY,DC=LAB))" | grep sAMAccountName | cut -d" " -f2
* <details><summary>Enumerate all groups a user is member of (Click to expand)</summary><p>

		ldapsearch -LLL -x -H ldap://pwnylabdc01.pwny.lab -D "jar-jar.binks@pwny.lab" -w Welcome2015 -b dc=pwny,dc=lab "(sAMAccountName=darth.vader)" sAMAccountName userPrincipalName memberOf | grep memberOf | cut -d "=" -f2 | cut -d"," -f1

