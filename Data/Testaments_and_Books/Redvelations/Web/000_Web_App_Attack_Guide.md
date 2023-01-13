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
# Web App Attack Guide ([`Exploit Public Facing Application` TTP](TTP/T1190_Exploit_Public-Facing_Application/T1190.md))
## Tags
* <details><summary>Tags (Click to expand)</summary><p>

## References

<details><summary>References (Click to expand)</summary><p>

* Request Smuggling
* James Kettle - Whitepapers

* [https://github.com/swisskyrepo/PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
* [https://github.com/danielmiessler/SecLists/tree/master/Discovery/Web-Content](https://github.com/danielmiessler/SecLists/tree/master/Discovery/Web-Content)

</p></details>

### Overview

* Ports: 80, 443, 8080, more

Several TTPs are present, sometimes simultaneously, for tools mentioned through the web attacks

* [`Input Capture - Web Portal Capture` TTP](TTP/T1056_Input_Capture/003_Web_Portal_Capture/T1056.003.md)
    * Capturing user input in web applications for the future benefit of the attacker.
* [`User Alternate Authentication Material - Application Access Token` TTP](/TTP/T1550_Use_Alternate_Authentication_Material/001_Application_Access_Token/T1550.001.md)
* [`Command and Scripting Interpreter - Javascript` TTP](TTP/T1059_Command_and_Scripting_Interpreter/007_JavaScript-JScript/T1059.007.md)

## Tools

<details><summary>Tools (Click to expand)</summary><p>

* Project Discovery Suite
    * vulnerability scanning and testing
        * nuclei -<br />[https://github.com/projectdiscovery/nuclei](https://github.com/projectdiscovery/nuclei)
            * nuclei templates -<br />[https://github.com/projectdiscovery/nuclei-templates](https://github.com/projectdiscovery/nuclei-templates)
    * Collaborative DNS Response server
        * interactsh -<br />[https://github.com/projectdiscovery/interactsh](https://github.com/projectdiscovery/interactsh)
    * DNS Reconnaissance
        * dnsx -<br />[https://github.com/projectdiscovery/dnsx](https://github.com/projectdiscovery/dnsx)
    * subdomain enumeration
        * subfinder -<br />[https://github.com/projectdiscovery/subfinder](https://github.com/projectdiscovery/subfinder)
* Broad Web Testing
    * Proxy-based
        * Burp Suite ([Burp Suite Tool Guide](Testaments_and_Books/Redvelations/Tools/Web/Burpsuite/burpsuite.md))
            * Burp Suite Extensions ([Burp Suite Tool Guide - Extensions](Testaments_and_Books/Redvelations/Tools/Web/Burpsuite/Burp_Extensions.md))
    * Reconnaissance (OSINT) and Web Testing
        * bbot -<br />[https://github.com/blacklanternsecurity/bbot](https://github.com/blacklanternsecurity/bbot)
        * spiderfoot -<br />[https://github.com/smicallef/spiderfoot](https://github.com/smicallef/spiderfoot)

</p></details>

## Example Attacks

* <details><summary>Quick nuclei usage with the project discovery suite (Click to expand)</summary><p>

		echo evilcorp.com | subfinder -silent  | sudo nabuu -retries 1 -c 256 -top-ports 1000 -silent | httpx -t 256 -silent | nuclei -rl 500 -t <local_templates_directory> -tags <tags_for_nuclei> -interactsh-server <interactshserver> -itoken <token> -stats


## Enumeration

Enumeration is highly recommended for situational awareness before performing attacks: [Web Application Enumeration Guide](Testaments_and_Books/Redvelations/Web/001-0_Enumeration.md)

## Checklist

* Authentication
	* [ ] - Attack, forge, or alter session information
		* [JWT Attack Guide](Testaments_and_Books/Redvelations/Web/Attacks/JSON_Web_Tokens/000-0_JWT.md)
* Attack Accounts
	* [ ] - Generate Usernames ([Usernames Guide](Testaments_and_Books/Redvelations/Accounts/001_Usernames.md))
	* [ ] - Test for Default Credential Usage ([Passwords and Credentials Guide](Testaments_and_Books/Redvelations/Accounts/002_Passwords_and_Credentials.md))
	* [ ] - Bruteforce login information
* Establish a reverse shell

## CLICK-TO-COPY CHECKLIST

```
* Authentication
	* [ ] - Attack, forge, or alter session information
* Attack Accounts
	* [ ] - Generate Usernames
	* [ ] - Test for Default Credential Usage
	* [ ] - Bruteforce login information
* Establish a reverse shell
```