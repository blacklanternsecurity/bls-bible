<!--
 -------------------------------------------------------------------------------
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
 -------------------------------------------------------------------------------
-->

# Illicit Consent Grant

## Tags
<details><summary>Tags</summary><p>

`#@Azure #@AAD #@Token #@AccessToken #@RefreshToken #@Refresh #@Access #@Phishing #@Consent`

</details>

## Background

By default, any user can register an application in Azure AD. We can register an application (only for the target tenant) that needs high impact permissions with admin consent - like sending mail on a user's behalf, role management, etc. This will allow us to execute phishing attacks that would be very fruitful in case of success

## Set up a MSFT Tenant

- Go to `portal.azure.com`
- Login
- Click the hamburger
- Select `Azure Active Directory`
- select `Create A Tenant`
- Select the radio button for `Azure Active Directory` and hit Next
- Fill in organization name and initial domain name to match something you want to be phishing with and hit `Next`
- Review your inputs and hit `Create`
	+ You may have to prove you're not a cyborg
- Once creation is finished, the info dialog box will notify you in green and give you a link to manage your new tenant

## Register your evil application

- In the newly created tenant dashboard, navigate to `Azure Active Directory` from the hamburger menu
- Navigate over to `App Registrations`
- Navigate to `New Registration`
- On this page, fill out the following fields
	+ `Name` : Name of your application, this will be visible to the target user, so use something that fits your narrative, like `Resume Viewer`
- Select the radio button for
	+ `Accounts in any organizational directory (Any Azure AD directory - Multitenant)`
- Fill in an appropriate URL for the `Redirect URI`, here we want to use a system we control that can be reached publicly
	+ You may want to set up a VM in azure to accomplish this and will need one to run o365-stealer later on anyway
    + https://IP-OF-PUBLIC-SYSTEM/login/authorized
- Select `Register`
- Once the application is registered, navigate over to `Certificates & secrets` in the new application dashboard
- Create a new client secret ( `New client secret` button ), give it a useful sounding name ( `Secret` ), set expiration to what you think is reasonable ( `12 Months` ), click `Add`
- Copy the values `Value` and `Secret ID` somewhere safe
	+ Value: `<some-value>`
	+ Secret ID: `<some-id>`
- Navigate over to `API Permissions`
	+ `User.Read` is typically already populated, if not add it as well as `User.ReadBasic.All` by:
		* clicking on `Add a permission` 
		* Select `Microsoft Graph`
		* Select `Delegated Permissions`
		* Type in `User.ReadBasic.All`
		* Expand the `User` row and check the `User.ReadBasic.All` Permission
	+ Select `Add permissions`
	+ It should be noted that these two permissions should not require any sort of Admin approval on the target end, even if they have their tenant security policies in order
	+ If they do not have them in order, or if you are specifically targetting a known Admin account, you can ask for many more things such as:
		* `Mail.Read`
		* `Notes.Read.All`
		* `Mailboxsettings.ReadWrite`
		* `Files.ReadWrite.All`
		* `Mail.Send`
        * `Directory.AccessAsUser.All`

## O365-Stealer

### Set up a VM

- We're going to need a public facing system to catch stolen tokens and interact with the target
- Log in to `portal.azure.com` under your tenant
- Navigate over to `Virtual Machines` in the hamburger menu
- Create a new virtual machine
- Fill in the following
    + Subscription: `subscription`
    + Resource Group: Whatever is appropriate
    + Virtual Machine Name: Whatever is appropriate
    + Region: Try to match up with the HQ location of target organization
    + Availability Options: No infrastructure redundancy required
    + Image: Windows 10 Pro - Gen1
    + Azure Spot instance: unchecked
    + Size: Standard_B2s - 2 vcpus, 4 GiB memory
    + Username: `<username>`
    + Password: generate a secure password for this
    + Select Inbound Ports: HTTP (80), HTTPS (443), RDP (3389)
        * Restrict 3389 access to your IP
    + Confirm you have a license
- Proceed to the Disk settings
    + OS Disk Type: Standard SSD
    + Encryption Type: (Default) Encryption at-rest
    + Enable Ultra Disk compatibility: unchecked
- Proceed to `Review + create`
    + Make sure everything looks okeedokee and click on `Create`
- It will take some time to deploy, so just grab some coffee or a ham sammich

### Set up O365-Stealer

- In the azure portal, under the hamburger menu, go to `Virtual Machines`
- Select the one you just created
- Copy down the public IP address
    + At this point, you may want to go back to your evil application and edit the `Redirect URI`
- Connect into your VM using RDP (Remmina [linux] or RDP [windows] )
    + Will take some time on initial setup
- Open up a browser and navigate to `https://www.apachefriends.org/download.html` and download XAMPP for Windows, at time of writing the newest available version is 8.0.10
- Run the installer, you don't need FTP
- Once installed, open up `XAMPP` and start the `Apache` service
    + Allow windows firewall rules to be created for Apache service
- Download the o365-stealer repo to the system
- https://github.com/AlteredSecurity/365-Stealer
- Create `C:\xampp\htdocs\365-Stealer`
- Copy the contents of the repo archive there
- Install Python3 if you don't already have it
- Inside the `365-Stealer` directory run `pip install -r requirements.txt`
- On the XAMPP dashboard, next to Apache, click `Config` and select `php.ini`
- Search for `extension=sqlite3` and remove the `;` from the beginning to uncomment it out, save and close
- (Re)start the Apache server
- To avoid conflict between Apache and 365-stealer, change the httpd.conf and httpd-ssl.conf to listen on 8000 and 8443 respectively. Restart the Apache service to reflect changes
- Edit `C:/xampp/htdocs/yourvictims/index.php` to include the location of the database file that holds victim information `../database.db` , path of `../365-stealer.py` and the path to `python.exe`. Save and close
    + Note, if the path to `python.exe` contains spaces, the full quoted path will be needed
- Whitelisting is enabled by default to only allow localhost to access the stealer dashboard. You can add other IPs there
- Now, we need to set out client-id, client-secret and redirect-url, so navigate to `C:\xampp\htdocs\365-Stealer`
- Execute `python .\365-stealer.py --set-config`
- Supply the necessary data for the beforementioned variables, you can leave the rest blank
    + Client ID can be found by navigating to the evil app in our evil tenant and grabbing the application's `client-id`

### Execute

- With everything configured properly, it's time to run `365-stealer.py`
- Open up a powershell or cmd prompt and navigate to the `C:\xampp\htdocs\365-Stealer` directory
- Execute `python .\365-stealer.py --run-app`
- Copy down the phishing link supplied, and give it a test run
- You should be able to gather at least the users within a tenant, once they have clicked, signed in, and authorized on the authenticator, you will receive all the good infos and tokens
- Navigate over to `http://localhost:8000/365-Stealer/yourvictims/` to get your gold

