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
# Phishing Email Infrastructure
### References
* Selecting appropriate regions - Microsoft Azure https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/overview

### Overview

Testing email security with phishing requires infrastructure to direct the emails, payloads, and malicious links. Email providers such as Google's Gmail offer preset infrastructure. However, because of certain issues in using third party mail servers, BLS uses its own mail server on cloud infrastructure. The deployed VM must be supported by the chosen Mail Server, and the networking rules in the cloud settings must allow access to appropriate ports in the Mail Server. In this case, BLS deploys a MailInTheBox server on an Ubuntu OS in Azure. Some required ports for management include web ports, as well as ports for additional resources like SendGrid. SendGrid is a resource used to improve the trustworthiness of the mail server on the internet, improving the likelihood that sent emails is ultimately received.

### Requirements
* **Secure a clean domain name**
	* Utilize the Domain Bag tool to find an appropriate domain for phishing. A good rule is to only use domains with a BrightCloud score of 90 or greater. Also, keep in mind that it may take up to two weeks to gain ownership of a domain discovered through Domain Bag.
	* The pre-requisite to infrastructure is "**Step 0: Secure a clean domain name.**" This is required before setting up infrastructure and can take as long as 2 weeks to complete. Try to complete this before the engagement, and recognize that there is a lot of flexibility in choosing a domain name. Whenever you have a name that works for the engagement and can help a convincing premise, the infrastructure can be setup.
* **Other**
	* Complete a successful login with GoDaddy near the setup of infrastructure. Phil must send the MFA code to you for each login. However, the site remembers your login for some period of time (1-2 weeks?)

### Process
1. Deploy a VM in the Cloud (Azure)
	* Overview
		* The first step of infrastructure setup is to deploy a VM in the cloud. The Mail Server in this setup depends on a Linux OS for setup, so we use the latest Ubuntu LTS OS. The cloud infrastructure allows us constant uptime, provides a static IP address associated with a trusted provided, and integrates with other products supporting infrastructure. In this case, we use Azure, which has support for using SendGrid to setup email security features enabled in later step.
	* Process
		1. Create a New Resource group.
			1. Navigate to Azure dashboard ([https://portal.azure.com/#home](https://portal.azure.com/#home))
			1. Select **Resource Groups**, select **Add**
			1. Options:
				1. Subscription: **BLS Engagements**
				1. Region: **(US) East US** (or reliable region local to us)
				1. Resource Group: `Engagements-<client>`
			1. Select **Review + Create**, then **Create**
		1. Create a new VM resource in the Resource Group
			1. Navigate to the **Resource Groups** list, click into **Engagements-<client>**
			1. Click **Add** (top-left)
			1. Select the **Ubuntu 18.04 LTS OS**
				* Options:
					1. Region: **Region Near Client** (avoiding geoblocking later).
						* Example: 'Australia East' may be suitable for Australian client
					1. VM Size: **Standard_B1s** (or cheapest VM with at least 1 GB of RAM)
					1. Username (for SSH):`bls` (recommended)
						* **Note:** Write down the username for later
					1. SSH public key source: **Use existing public key**
					1. SSH Public Key: **Paste** in your SSH public key

						```bash
						cat ~/.ssh/id_rsa.pub
						```

			1. Select **Review + create**
		1. Modify IP Settings: Firewall Rules, Static IP for ReverseDNS ("rdns")
			1. Navigate to the **Engagements-<client>** Resource Group
			1. Click into **VM-Name**
			1. Click **Networking**
			1. Modify existing SSH rule, whitelist BLS IP
				* You can identify this by a Google search for "what is my IP" while connected to the BLS network.
				* **Note:** SSH to this later will require VPN or direct BLSHQ connection
			1. Create **New Inbound Rule** rule. Options:
				* **Destination Port Range:**
					* `443, 53, 25, 80, 587`
			1. **Accept**
			1. Navigate back to the Resource Group
			1. Click **VM-Name-ip**
			1. Within the **-ip** resource, click **Configuration**
			1. Click **Assignment**
			1. Select **Static** (not Dynamic)
			1. **Save!**
		1. **Configure Reverse DNS**
			* **Troubleshooting:**
				* [https://support.hostway.com/hc/en-us/articles/360001063664-How-to-set-up-reverse-DNS-on-Azure-Virtual-Machine](https://support.hostway.com/hc/en-us/articles/360001063664-How-to-set-up-reverse-DNS-on-Azure-Virtual-Machine)
			1. Place **the below code block** in a local text editor:

				```pwsh
				$pip = Get-AzureRmPublicIpAddress -Name "instancename-ip" -ResourceGroupName "Engagements"
				$pip.DnsSettings = New-Object -TypeName "Microsoft.Azure.Commands.Network.Models.PSPublicIpAddressDnsSettings"
				$pip.DnsSettings.DomainNameLabel = "rdnsrecord"
				$pip.DnsSettings.ReverseFqdn = "your.rdnsrecord.com"
				Set-AzureRmPublicIpAddress -PublicIpAddress $pip
				```

			1. Edit the following fields; retain quotes
				1. instancename-ip: VMName-ip (keep the "-ip" at the end)
				1. -ResourceGroupName: Engagements-<client>
				1. rdnsrecord: DNS Name used in engagement (Example.com --> Example)
				1. your.rdnsrecord.com: `Example.eastus.cloudapp.azure.com` - Replace "Example" with your domain name (region names can be found at https://azuretracks.com/2021/04/current-azure-region-names-reference/).
			1. **Copy** the modified code
			1. Click the **PowerShell Terminal icon** (top-right, looks like `>_`)
				* If prompted, create new Azure Storage. Select proper resource group and name it.
			1. Right-click the **interactive PowerShell CLI window**, click **paste**. Send commands.
1. Configure DNS Registrar (GoDaddy)
	* Overview
		* The DNS registrar should hold the domain acquired in step 0. The DNS registrar can be used to manage DNS records, name servers, and host names associated with the reserved domain. BLS uses GoDaddy for this purpose. In this step, we configure the domain name to direct the domain name lookups to our own nameserver, which is managed by us in the later-built MailInABox server. The nameserver configured in the DNS registrar has to use the IP of the cloud VM to work.
	* Process
		1. Log into GoDaddy ```https://www.godaddy.com/```
		1. Hold cursor over the accountholder name at the top right; click **My Products**
		1. Find the domain name on this page that will be used.
		1. Search for the domain selected in Step 0. Follow the link to its DNS management page.
		1. Click **Manage DNS** at bottom-right
		1. Click **Domains**
		1. Select the domain for the engagement
		1. Click **Host Names** at the bottom of the DNS Management page
		1. Add these host names; assign the cloud VM IP address:
			* `ns1`
			* `ns2`
		1. Return to DNS Management page (hyperlink available at top)
		1. In the **Nameservers** section, click **change.**
		1. Select **I'll use my own** and add two new custom nameservers (using the recently made hostnames):

				ns1.<yourdomainhere>.com
				ns2.<yourdomainhere>.com
			* **Note:** Changes will take time (10-30 mins) to update in background, but you can proceed.
1. Deploy the Mail Server (MailInABox)
	* Overview
		* The mail server for this setup uses MailInABox. This method allows BLS to complete email security tests without using other companies' mail servers.
	* Process
		1. SSH into the cloud VM
			* **Troubleshooting:** Default username (if you didn't modify): `azureuser`
		1. Update the system```sudo apt update; sudo apt upgrade -y```
		1. Initiate the **MailInABox Bash Setup Script**``` curl -s https://mailinabox.email/setup.sh | sudo bash```
			* **Note:** This will take time. Read ahead while monitoring the terminal.
		1. Install prompt answers:
			1. Contact email: `support@<yourdomainhere.com>` (**Delete Pre-filled data**; this is a new account)
			1 Hostname of the server: `<yourdomainhere.com>` (Your domain name; replace default output)
			1. Password: Secure password for the new **contact email** user
			* Note: Do not use subdomains at this point. If you wish to do so, you may make changes later.
		1. When setup concludes, confirm the account created in setup is able to log in using the below link. The link will be relevant in step 5.```http://yourdomainname.com/admin```
			* **Troubleshooting:** If there are issues after setup, a complete restart with a new VM is highly recommended rather than running the suggested command:

				```bash
				sudo mailinabox
				```
1. Setup and Configure Additional Mail Server Resources (SendGrid)
	* Overview
		* The MailInABox server establishes most of what we need as an email provider. However, the additional email resources like SendGrid add security features to the email service. As an example, we will setup DMARC in step 5, which verifies the sender's authenticity to other servers.
	* Troubleshooting
		* Create a Sendgrid account and obtain the API key: https://docs.microsoft.com/en-us/azure/sendgrid-dotnet-how-to-send-email.
	* Process
		1. Login/Create an account on SendGrid ([https://app.sendgrid.com](https://app.sendgrid.com))
			* **Note:** For registering, you can fill in fake information, but they check for a recognized email domain.
			* **Note:** Personal info will be requested; you can give fake information and avoid entering a phone number.
		1. Close out of your SendGrid tabs.
		1. Return to Azure. Navigate to the **Engagements** Resource Group.
		1. Click the **Sendgrid** resource link
		1. Click **Manage** (redirects to Sendgrid)
			* **Troubleshooting:** Authentication issues may occur. Recommendations:
				1. Log out and back in with Azure
				1. Log out and in with any Sendgrid account you've created
				1. Continuously click **Manage** until successful login
		1. Navigate to **Settings** (in the left pane)
		1. Generate an API key with full access. Save the API Key for the step where we modify server configurations.
		1. Keep SendGrid open for Steps 5 and 6.
1. Enable DMARC (Sendgrid)
	* References
		* [https://sendgrid.com/blog/what-is-dmarc/](https://sendgrid.com/blog/what-is-dmarc/)
	* Overview
		* Email security includes verifying that an email's sender is indeed the source the sender claims to be. The common method for this is DMARC (Domain-based Message Authentication, Reporting & Conformance).
		* We can demonstrate to recipients that we have ownership over the domain we are sending emails through resources such as SendGrid. SendGrid confirms ownership of the domain by confirming that we have the ability to set CNAME records for the domain that point to SendGrid-owned resources. When this is completed and DMARC is published, the domain reputation can increase with email providers and enable email tracking features. With success, the mail server should successfully authenticate and pass DMARC when messages are sent.
	* Process
		1. Navigate to the Sendgrid application through the steps previously mentioned in Step 4. Sengrid Accounts > Click on account > Manage should get you to the Dashboard page of Sendgrid.
		1. Click **Settings** tab, then **Sender Authentication** option
		1. Select **Authenticate Your Domain** section
		1. Options:
			* DNS host: **GoDaddy**
			* Rebrand Links: **No**
			* Then, enter your domain in the format "<yourdomainhere.com>"
		1. Click **next.**
		1. Confirm the DNS Records for Sendgrid
			* Notes
				* Sendgrid will ask you to navigate to GoDaddy, but IGNORE THAT. Follow the below steps instead!
			* Process
				1. Navigate to MailInABox server at `http://yourdomainname.com/admin`
				1. Login with the user created in setup
				1. Click **System**, then **Custom DNS**
				1. Insert the three CNAME records according to SendGrid requirements
				1. Click **Verify' in SendGrid
1. Modify Mail Server Configurations in VM
	1. Configure Sendgrid on Server
		* References
			* SendGrid Postfix-specific instructions: https://sendgrid.com/docs/for-developers/sending-email/postfix/
		* Process
			1. SSH to the server.
			1. Modify this text, insert your SendGrid API Key after "apikey:" (no spaces; **DO NOT DELETE TEXT "APIKEY:"**).
				* `sudo echo '[smtp.sendgrid.net]:587 apikey:' > /etc/postfix/sasl_passwd`
					* **Troubleshooting:** You may need to try `sudo su`
					* Example Key: SG.asdfJvNWSR6cRE3k-gsTBg.7Nkaai53zRm9brNWp7xxSjKW5f1aaS5xVaxhWxA1rrk
			1. chmod `600` the file
			
				```bash
				sudo chmod 600 /etc/postfix/sasl_passwd
				```
	1. Update the Postfix config file
		1. SSH into the VM.
		1. Edit these two lines in the `main.cf` file of postfix.
			* `sudo vim /etc/postfix/main.cf`

				```bash
				smtp_tls_security_level = encrypt
				relayhost = [smtp.sendgrid.net]:587
				```

		1. Append these lines to the file:

			```bash
			smtp_sasl_auth_enable = yes
			smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
			smtp_sasl_security_options = noanonymous
			smtp_sasl_tls_security_options = noanonymous
			header_size_limit = 4096000
			```

	1. Update the authentication data for Postfix
		1. Submit the below comands to restart Postfix

			```bash
			sudo postmap /etc/postfix/sasl_passwd
			sudo systemctl restart postfix
			```

1. Configure the Mail Server via Web
	1. Setup SSL certificates
		1. Navigate to the Admin Panel <yourdomainhere.com>/admin. 
		1. Click the **System** tab at the top, then **TLS (SSL) Certificates**
		1. Click **Provision** to generate SSL certs
		1. After the certificate is generated successfully, reboot the server
	1. Create Accounts for Premise
		1. Navigate to the web interface
		1. Select the **Mail & Users** tab, then select **Users**
		1. Add accounts for mail according to phishing premise
			* **Note:** Use the full email address with the FQDN (fully qualified domain name) when adding the user.
1. Confirm Server is Working
	* Process
		1. Navigate to the below URL and login with mail user credentials ```<yourdomainhere.com>/mail```
		1. Compose and send an email and send to your BLS email account
			* **Troubleshooting email to BLS account:**
				* Known, common factors of email failure include:
					* A step above was left incomplete
					* A keyword was detected associated with malicious emails. You may use very few words altogether to improve chances
					* An attachment was identified as malicious
					* The SendGrid IP was blocked
			* **Troubleshooting email during engagements:**
				* Clients may use software that prevents email delivery or reverse shells. Information is recorded in the Email Security Capability research in GitLab.
