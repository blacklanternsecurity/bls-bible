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
# File Share Enumeration
## Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@enum #@enumerate #@enumeration #@smb #@file #@share #@fileshare

Tools

		#@impacket #@pcaptools #@pcap #@nmap #@zmap #@ldapsearch #@ldapsearch-ad #@rpcclient #@smbmap #@crackmapexec #@manspider #@adidnsdump #@dnsrecon #@enum4linux #@nopac

</p></details>

## Overview

 

## Enumeration
### From a Linux Machine
* Enumerate Open File Shares ([`Network Share Discovery` TTP](TTP/T1135_Network_Share_Discovery/T1135.md))
	* <details><summary>crackmapexec (Click to expand) </summary><p>

			crackmapexec smb -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD --shares $TARGET
	* <details><summary>smbmap  (Click to expand) -<br />[https://github.com/ShawnDEvans/smbmap](https://github.com/ShawnDEvans/smbmap)</summary><p>
		* Examples
			* Example 1: null session

					smbmap -H 10.10.10.10
			* Example 2: recursive listing

					smbmap -H 10.10.10.10 -R
			* Example 3: guest smb session

					smbmap -H 10.10.10.10 -u fakeuser
			* Example 4: 

					smbmap -H 10.10.10.10 -d "DOMAIN.LOCAL" -u "USERNAME" -p "Password123*"
	* <details><summary>impacket's smbclient.py  (Click to expand) </summary><p>
		* Examples
			* Example 1

					smbclient -I 10.10.10.100 -L ACTIVE -N -U ""
					        Sharename       Type      Comment
					        ---------       ----      -------
					        ADMIN$          Disk      Remote Admin
					        C$              Disk      Default share
					        IPC$            IPC       Remote IPC
					        NETLOGON        Disk      Logon server share
					        Replication     Disk      
					        SYSVOL          Disk      Logon server share
					        Users           Disk
			* Commands once interactive:
				* Select a Sharename

					use Sharename
				* Move inside a folder

						cd Folder
				* List files

						ls
	* <details><summary>samba smbclient (Click to expand)</summary><p>
		* Examples
			* Example 1

					smbclient -U username //10.0.0.1/SYSVOL
			* Example 2

					smbclient //10.0.0.1/Share

			* Commands once interactive: Download a folder recursively

					smb: \> mask ""
					smb: \> recurse ON
					smb: \> prompt OFF
					smb: \> lcd '/path/to/go/'
					smb: \> mget *
* Enumerate File Shares for credentials ([`Unsecured Credentials` TTP](TTP/T1552_Unsecured_Credentials/T1552.md), `Unsecured Credentials - Credentials In Files` TTP](TTP/T1552_Unsecured_Credentials/001_Credentials_In_Files/T1552.001.md), [`Automated Collection` TTP](TTP/T1119_Automated_Collection/T1119.md))
	* <details><summary>manspider (Click to expand) -<br />[https://github.com/blacklanternsecurity/MANSPIDER](https://github.com/blacklanternsecurity/MANSPIDER)</summary><p>
		* Examples
			* Example 1: Across a CIDR

					manspider 192.168.0.0/24 -f passw user admin account network login logon cred -d evilcorp -u bob -p Passw0rd
			* Example 2: Search for XSLX files with passwords

					manspider share.evilcorp.local -c password -e xlsx -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD
* Enumerate shares matching your credentials ([`Network Share Discovery` TTP](TTP/T1135_Network_Share_Discovery/T1135.md))
	* <details><summary>manspider (Click to expand) -<br />[https://github.com/blacklanternsecurity/MANSPIDER](https://github.com/blacklanternsecurity/MANSPIDER)</summary><p>
		* Examples
			* Example 1: Scan across a CIDR target using a password

				manspider $TARGET_CIDR -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD
	* SMBSR -<br />[https://github.com/oldboy21/SMBSR](https://github.com/oldboy21/SMBSR)
	* <details><summary>SMBMap (Click to expand)</summary><p>

			SMBMap
	* <details><summary>crackmapexec (Click to expand) ([crackmapexec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md))</summary><p>

			crackmapexec smb <CIDR> -u '<username>' -p '<password>' -d <domain> --shares
		* Example Output

				./CME smb 10.0.0.0/24 -u 'domain_user' -p 'P@ssw0rd' -d securelab.local --shares
				SMB	 	  10.0.0.10	    445	 DC02	 	 	  [*] Windows 10.0 Build 17763 x64 (name:DC02) (domain:securelab.local) (signing:True) (SMBv1:False)
				SMB	 	  10.0.0.2	 	 445	 CA	 	 	    [*] Windows 10.0 Build 17763 x64 (name:CA) (domain:securelab.local) (signing:False) (SMBv1:False)
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:securelab.local) (signing:True) (SMBv1:False)
				SMB	 	  10.0.0.10	    445	 DC02	 	 	  [+] securelab.local\domain_user:P@ssw0rd 
				SMB	 	  10.0.0.22	    445	 NONE	 	 	  [*]  (name:) (domain:securelab.local) (signing:False) (SMBv1:True)
				SMB	 	  10.0.0.2	 	 445	 CA	 	 	    [+] securelab.local\domain_user:P@ssw0rd 
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  [+] securelab.local\domain_user:P@ssw0rd 
				SMB	 	  10.0.0.10	    445	 DC02	 	 	  [+] Enumerated shares
				SMB	 	  10.0.0.10	    445	 DC02	 	 	  Share	 	    Permissions	  Remark
				SMB	 	  10.0.0.10	    445	 DC02	 	 	  -----	 	    -----------	  ------
				SMB	 	  10.0.0.10	    445	 DC02	 	 	  ADMIN$	 	 	 	 	 	   Remote Admin
				SMB	 	  10.0.0.10	    445	 DC02	 	 	  C$	 	 	 	 	 	 	   Default share
				SMB	 	  10.0.0.10	    445	 DC02	 	 	  IPC$	 	 	 READ	 	 	 Remote IPC
				SMB	 	  10.0.0.10	    445	 DC02	 	 	  NETLOGON	 	 READ	 	 	 Logon server share 
				SMB	 	  10.0.0.10	    445	 DC02	 	 	  SYSVOL	 	   READ	 	 	 Logon server share 
				SMB	 	  10.0.0.2	 	 445	 CA	 	 	    [+] Enumerated shares
				SMB	 	  10.0.0.2	 	 445	 CA	 	 	    Share	 	    Permissions	  Remark
				SMB	 	  10.0.0.2	 	 445	 CA	 	 	    -----	 	    -----------	  ------
				SMB	 	  10.0.0.2	 	 445	 CA	 	 	    ADMIN$	 	 	 	 	 	   Remote Admin
				SMB	 	  10.0.0.2	 	 445	 CA	 	 	    C$	 	 	 	 	 	 	   Default share
				SMB	 	  10.0.0.2	 	 445	 CA	 	 	    CertEnroll	   READ	 	 	 Active Directory Certificate Services share
				SMB	 	  10.0.0.2	 	 445	 CA	 	 	    IPC$	 	 	 READ	 	 	 Remote IPC
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  [+] Enumerated shares
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  Share	 	    Permissions	  Remark
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  -----	 	    -----------	  ------
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  ADMIN$	 	 	 	 	 	   Remote Admin
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  C$	 	 	 	 	 	 	   Default share
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  IPC$	 	 	 READ	 	 	 Remote IPC
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  NETLOGON	 	 READ	 	 	 Logon server share 
				SMB	 	  10.0.0.1	 	 445	 DC01	 	 	  SYSVOL	 	   READ	 	 	 Logon server share 
* Crawl Content on File Shares
	* <details><summary>crackmapexec (Click to expand) </summary><p>

			crackmapexec smb -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD --shares $TARGET
	* <details><summary>Manspider (Click to expand) </summary><p>

			manspider $SUBNET_CIDR -f passw user admin account network login logon cred -d $DOMAIN -u $USER -p $PASSWORD
* GPP Password Enumeration
	* <details><summary>crackmapexec (Click to expand) </summary><p>
		* Examples
			* Example 1: gpp_autologin module

					cme smb 10.10.10.10 -u Administrator -H 89[...]9d -M gpp_autologin
			* Example 2: gpp_password module 

					cme smb 10.10.10.10 -u Administrator -H 89[...]9d -M gpp_password
	* <details><summary>Get-GPPPassword.py (Click to expand) </summary><p>
		* Examples
			* Example 1: Null Session

					Get-GPPPassword.py -no-pass $DOMAIN_CONTROLLER
			* Example 2: Cleartext credentials

					Get-GPPPassword.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$DOMAIN_CONTROLLER
			* Example 3: Pass-the-hash

					Get-GPPPassword.py -hashes 'LMhash':'NThash' 'DOMAIN'/'USER':'PASSWORD'@$DOMAIN_CONTROLLER



### From a Windows Machine

* Find password in SYSVOL

		findstr /S /I cpassword \\<FQDN>\sysvol\<FQDN>\policies\*.xml