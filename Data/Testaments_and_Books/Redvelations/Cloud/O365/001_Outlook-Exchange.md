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
# Outlook
### Overview
([`Office - Outlook Forms` TTP](TTP/T1137_Office_Application_Startup/003_Outlook_Forms/T1137.003.md))
([`Office - Outlook Home Page` TTP](TTP/T1137_Office_Application_Startup/004_Outlook_Home_Page/T1137.004.md))
([`Office - Outlook Rules` TTP](TTP/T1137_Office_Application_Startup/005_Outlook_Rules/T1137.005.md))

### Enumeration
	* <details><summary>Test for legacy authentication (Click to expand)</summary><p>
		* [exchangelib script](Testaments_and_Books/Redvelations/Active_Directory/scripts/exchangelib.py)
		* <details><summary>Method 1: IMAP (Click to expand)</summary><p>
			* To test if IMAP authentication is allowed, a user can simply attempt to authenticate using the curl command line utility.

					curl -v "imaps://outlook.office365.com:993/INBOX" --user "username:password"
			* The URL and port may change depending on mail server. The previous example tests a normal Outlook email. If the credentials are sent correctly and IMAP authentication is allowed, then the user will receive an "Authentication Successful" message.
		* <details><summary>Method 2: POP (Click to expand)</summary><p>
			* To test if POP authentication is allowed, a user can utilize the previous command and just change the protocol from "IMAP" to "POP" as seen in the following command.

					curl -v "pop3s://outlook.office365.com:995/INBOX" --user "user:password"
				* Notice that although it is using the same mail server, the port needed to be changed to 995 for the POP protocol. If the credentials are sent correctly and POP authentication is allowed, then the user will receive an "+OK User successfully authenticated" message.
		* <details><summary>Method 3: SMTP (Click to expand)</summary><p>
			* To test if SMTP authentication is allowed, a user can utilize the previous command and just change the protocol from "POP" to "SMTP" as seen in the following command. Additionally the "--ssl" flag needs to be provided at the end if the server utilizes it (which most modern servers do).

					curl -v "smtp://outlook.office365.com:587/INBOX" --user "user:password" --ssl
			* try this one too

					curl -v "smtp://smtp.office365.com:587/INBOX" --user "user:password" --ssl
			* If the credentials are sent correctly and SMTP authentication is allowed, then the user will receive an "235 2.7.0 Authentication successful" message.
		* <details><summary>Method 4: Outdated Office Client (Click to expand)</summary><p>
			* This last method is fairly straight-forward and only requires the user to find an outdated Office Client such as 2010 or older. Once this has been done then the user can simply attempt to authenticate with valid Office365 credentials to test if this Legacy Authentication method is allowed.

					curl -v -H 'Content-Type: text/xml' https://outlook.office365.com/EWS/Exchange.asmx --user "BOB@EVILCORP.COM:Password123" --data-binary $'<?xml version=\'1.0\' encoding=\'utf-8\'?>\x0a<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:m=\"http://schemas.microsoft.com/exchange/services/2006/messages\" xmlns:t=\"http://schemas.microsoft.com/exchange/services/2006/types\"><s:Header><t:RequestServerVersion Version=\"Exchange2019\"/></s:Header><s:Body><m:ResolveNames ReturnFullContactData=\"false\"><m:UnresolvedEntry>BOB@EVILCORP.COM</m:UnresolvedEntry></m:ResolveNames></s:Body></s:Envelope>'