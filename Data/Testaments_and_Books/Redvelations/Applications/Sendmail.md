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
# Sendmail (Port 25)

1. Fingerprint Server ([Technique](TTP/T1592_Gather_Victim_Host_Information/T1592.md))
	* Banner grab

			telnet ip_address 25
1. Connect to the system ([TTP](TTP/T1569_System_Services/T1569.md))

## Mail Server Testing
* Enumerate users

		VRFY username (verifies if username exists - enumeration of accounts)
		EXPN username (verifies if username is valid - enumeration of accounts)
* Mail Spoof Test

		HELO anything MAIL FROM: spoofed_address RCPT TO:valid_mail_account DATA . QUIT
* Mail Relay Test

		HELO <anything>
	* Identical to/from - mail from: `<nobody@domain>` rcpt to: `<nobody@domain>`
	* Unknown domain - mail from: `<user@unknown_domain>`
	* Domain not present - mail from: `<user@localhost>`
	* Domain not supplied - mail from: `<user>`
	* Source address omission - mail from: `<>` rcpt to: `<nobody@recipient_domain>`
	* Use IP address of target server - mail from: `<user@IP_Address>` rcpt to: `<nobody@recipient_domain>`
	* Use double quotes - mail from: `<user@domain>` rcpt to: `<"user@recipent-domain">`
	* User IP address of the target server - mail from: `<user@domain>` rcpt to: `<nobody@recipient_domain@[IP Address]>`
	* Disparate formatting - mail from: `<user@[IP Address]>` rcpt to: `<@domain:nobody@recipient-domain>`
	* Disparate formatting2 - mail from: `<user@[IP Address]>` rcpt to: `<recipient_domain!nobody@[IP Address]>`