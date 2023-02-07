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
# AD CVE Enumeration
## Tags
<details><summary>Tags (Click to expand)</summary><p>

Environment

		#@active #@directory #@activedirectory #@microsoft

Context

		#@enum #@enumerate #@enumeration #@dns #@dhcp #@ldap #@smb #@cve #@exploit #@vuln #@vulnerability #@vulnerabilities #@vulns #@nopac #@no #@pac #@drop #@the #@mic #@zero #@logon #@zerologon

Tools

		#@impacket #@pachine #@crackmapexec

</p></details>

## Enumeration
### From a Linux Machine
#### No Domain Credentials Required (Usually)
* Zerologon
	* <details><summary>crackmapexec (Click to expand)</summary><p>
		* Example

				cme smb -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -M zerologon $DOMAIN_CONTROLLER
			* Example Output

					root@jack-Virtual-Machine:~# cme smb -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -M zerologon $DOMAIN_CONTROLLER
					SMB         dc01.microsoftdelivery.com 445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
					SMB         dc01.microsoftdelivery.com 445    DC01             [+] microsoftdelivery.com\domain_user:P@ssw0rd 
					ZEROLOGO... dc01.microsoftdelivery.com 445    DC01             VULNERABLE
					ZEROLOGO... dc01.microsoftdelivery.com 445    DC01             Next step: https://github.com/dirkjanm/CVE-2020-1472
	* <details><summary>SecuraBV's GitHub: CVE-2020-1472 -<br />[https://github.com/SecuraBV/CVE-2020-1472](https://github.com/SecuraBV/CVE-2020-1472) (Click to expand)</summary><p>
		* References
			* [https://twitter.com/YaronZi/status/1237005749273927681](https://twitter.com/YaronZi/status/1237005749273927681)
		* Example

				python zerologon_tester.py $DOMAIN_CONTROLLER_NO_DOMAIN $DC_IP
			* Example Output

					(CVE-2020-1472) root@jack-Virtual-Machine:~/CVE-2020-1472# python zerologon_tester.py dc01 10.0.0.1                                                                            
					Performing authentication attempts...                                                                                                                                          
					===============================================================================================================================================================================
					=========================================================================                                                                                                      
					Success! DC can be fully compromised by a Zerologon attack.


#### Domain Credentials Required (Usually)
* noPac
	* <details><summary>Ly4k's Github: Pachine (Click to expand) -<br />[https://github.com/ly4k/Pachine](https://github.com/ly4k/Pachine)</summary><p>
		* Examples

				python pachine.py -scan $DOMAIN/$DOMAIN_USER:$PASSWORD -dc-host $DOMAIN_CONTROLLER
			* Example Output

					python pachine.py -scan $DOMAIN/$DOMAIN_USER:$PASSWORD -dc-host $DOMAIN_CONTROLLER

					(Pachine) root@jack-Virtual-Machine:~/Pachine# python pachine.py -scan $DOMAIN/$DOMAIN_USER:$PASSWORD -dc-host $DOMAIN_CONTROLLER
					Impacket v0.10.0 - Copyright 2022 SecureAuth Corporation

					[*] Domain controller dc01.microsoftdelivery.com is most likely vulnerable
	* <details><summary>crackmapexec</summary><p>
		* Example
			* Example 1: Using Password

					cme smb -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -M nopac $DOMAIN_CONTROLLER
				* Example Output

						root@jack-Virtual-Machine:~# cme smb -d $DOMAIN -u $DOMAIN_USER -p $PASSWORD -M nopac $DOMAIN_CONTROLLER
						SMB         dc01.microsoftdelivery.com 445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:microsoftdelivery.com) (signing:True) (SMBv1:False)
						SMB         dc01.microsoftdelivery.com 445    DC01             [+] microsoftdelivery.com\domain_user:P@ssw0rd 
						NOPAC       dc01.microsoftdelivery.com 445    DC01             TGT with PAC size 1596
						NOPAC       dc01.microsoftdelivery.com 445    DC01             TGT without PAC size 783
						NOPAC       dc01.microsoftdelivery.com 445    DC01             
						NOPAC       dc01.microsoftdelivery.com 445    DC01             VULNEABLE
						NOPAC       dc01.microsoftdelivery.com 445    DC01             Next step: https://github.com/Ridter/noPac
* Drop The Mic
	* <details><summary>CVE 2019-1040 Scanner (Fox-It) (Click to expand) -<br />[https://github.com/fox-it/cve-2019-1040-scanner](https://github.com/fox-it/cve-2019-1040-scanner)</summary><p>
		* Example

				python ./scan.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$DOMAIN_CONTROLLER
			* Example Output (Not Vulnerable)

					python ./scan.py $DOMAIN/$DOMAIN_USER:$PASSWORD@$DOMAIN_CONTROLLER
					[*] CVE-2019-1040 scanner by @_dirkjan / Fox-IT - Based on impacket by SecureAuth
					[*] Target dc01.microsoftdelivery.com is not vulnerable to CVE-2019-1040 (authentication was rejected)
* Broad Enumeration of non-AD Vulnerabilities is maintained in the [Network Enumeration Guide](Testaments_and_Books/Redvelations/Network/001-0_Network_Enumeration.md)

### From a Windows Machine
* noPac
	* cube0x0's GitHub: noPac -<br />[https://github.com/cube0x0/noPac](https://github.com/cube0x0/noPac)