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
# Cracking
## References

* Hashcat Automation Tool -<br />[https://github.com/sp00ks-git/hat](https://github.com/sp00ks-git/hat)

## Overview

* TTPs used through the tools:
	* [`Brute Force - Password Cracking` TTP](TTP/T1110_Brute_Force/002_Password_Cracking/T1110.002.md)

## Cracking Options

* <details><summary>Public Cracking (or rainbow tables) Sites (Click to expand)</summary><p>
	* crack.sh
	* Hashes.org
	* Hashkiller.io
	* Google the hash
	* Rainbow Tables websites
* DCSync
	* <details><summary>Format (Click to expand)</summary><p>

			username : unique_identifier : LMhash : NThash
			testuser:29418:aad3b435b51404eeaad3b435b51404ee:58a478135a93ac3bf058a5ea0e8fdb71
		* Tip
			* Use the following command to quickly format your DCSync file to hashcat-compatible format

					cut -d\\ -f2 dcsync.ntds | cut -d: -f1,2,3,4
	* <details><summary>Hashcat (Click to expand)</summary><p>

			hashcat -m 1000 -w 4 -O -a 0 -o pathtopotfile pathtohashes pathtodict -r ./rules/best64.rule --opencl-device-types 1,2
* Kerberos
	* Kerberoast
		* <details><summary>Hashcat (Click to expand)</summary><p>
			* $krb5tgs$23= etype 23

					Mode 	Description
					13100 	Kerberos 5 TGS-REP etype 23 (RC4)
					19600 	Kerberos 5 TGS-REP etype 17 (AES128-CTS-HMAC-SHA1-96)
					19700 	Kerberos 5 TGS-REP etype 18 (AES256-CTS-HMAC-SHA1-96)
			* Example

					./hashcat -m 13100 -a 0 kerberos_hashes.txt crackstation.txt
		* <details><summary>JohnTheRipper (Click to expand)</summary><p>
			* Example

					./john --wordlist=/opt/wordlists/rockyou.txt --fork=4 --format=krb5tgs ~/kerberos_hashes.txt
	* ASRepRoast
		* <details><summary>Hashcat (Click to expand)</summary><p>

				hashcat -m 18200 -a 0 ASREProastables.txt $wordlist
* Active Directory Relay Hashes
	* <details><summary>Captured Auth (Click to expand)</summary><p>
		* Note: Cracking NetNTLMv2 Response for *machine* accounts is virtually impossible.
		* NetNTLMv1
			* Recommended: Supply to crack.sh in the format: `NTHASH:1C1F1122CBC14FB2B0A054BC9B2BB0868EDE87CCC0D2117B`. Requires that challenge was set to `1122334455667788`.
			* Alternative: `ntlmv1-multi` by evilmog
				* Execute the below and perform the commands follow the guidance of the output.

						python3 ntlmv1.py --ntlmv1 hashcat::DUSTIN-5AA37877:76365E2D142B5612980C67D057EB9EFEEE5EF6EB6FF6E04D:727B4E35F947129EA52B9CDEDAE86934BB23EF89F50FC595:1122334455667788
		* NetNTLMv2
			* Recommended: Hashcat ([TTP](TTP/T1110_Brute_Force/002_Password_Cracking/T1110.002.md))
				
					hashcat -m 5600 <hashfile.txt> -o <outfile.txt> <wordlist.txt>
* LM Hashes
	* <details><summary>hashcat (Click to expand)</summary><p>

			hashcat -m 3000 lm-hash.txt -a3
* <details><summary>AEM (Click to expand)</summary><p>
	1. Convert the AEM hashes to a John-compatible format
		* [https://fossies.org/linux/privat/john-1.9.0-jumbo-1.tar.xz/john-1.9.0-jumbo-1/run/aem2john.py?m=t](https://fossies.org/linux/privat/john-1.9.0-jumbo-1.tar.xz/john-1.9.0-jumbo-1/run/aem2john.py?m=t)
		* -<br />[https://github.com/openwall/john/pull/3240](https://github.com/openwall/john/pull/3240)

				python3 aem2john.py <hashes.txt>
	1. Run John
		* John Rules Guide-<br />[https://charlesreid1.com/wiki/John_the_Ripper/Rules](https://charlesreid1.com/wiki/John_the_Ripper/Rules)

				python3 aem2john.py <hashes.txt>