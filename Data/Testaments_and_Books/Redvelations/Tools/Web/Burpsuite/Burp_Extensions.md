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
# Recommended Burp Extensions
## References
* [https://giters.com/ximiluliyi/awesome-burp-extensions](https://giters.com/ximiluliyi/awesome-burp-extensions)

## Overview
* The following list represents a small sample of available Burp extensions which are particularly useful. It is by no means an exhaustive list. All of the featured extensions are available in the BApp store within Burpsuite's **Extender** tab.
* Some extensions require Jython. You will need to download the [Standalone Jython jar file](https://repo1.maven.org/maven2/org/python/jython-standalone/2.7.2/jython-standalone-2.7.2.jar) and configure Burp to point to it in the Extender tab options to use these extensions.

## Recommendations/Requirements

* jython - required for python-based extensions
    * Manual Download -<br />[https://www.jython.org/download.html](https://www.jython.org/download.html)
    * Standalone version (latest as of this writing) -<Br />[https://repo1.maven.org/maven2/org/python/jython-standalone/2.7.2/jython-standalone-2.7.2.jar](https://repo1.maven.org/maven2/org/python/jython-standalone/2.7.2/jython-standalone-2.7.2.jar)
    * Additional standalone copies to check for the next latest

## Extensions
* Logging
  * **Flow** -<br />[https://github.com/PortSwigger/flow](https://github.com/PortSwigger/flow)
      * Arguably the best logging extension. Similar to Logger++. One very important difference: It will display requests that do not have responses, which can be important when trying to exploit Http Request Smuggling. 
      * Having a logging extension which will allow you to view past repeater requests is critically important as it pertains to documenting your testing activities. 
  * **Logger++** -<br />[https://github.com/PortSwigger/logger-plus-plus](https://github.com/PortSwigger/logger-plus-plus)
      * My go-to for visually logging requests in burp. Color code your request status codes and responses and stuff
* WAF
    * **Bypass WAF** -<br />[https://github.com/PortSwigger/bypass-waf](https://github.com/PortSwigger/bypass-waf)
        * Adds some additional WAF bypass techniques to an active scan
* **Upload Scanner** -<br />[https://github.com/PortSwigger/upload-scanner](https://github.com/PortSwigger/upload-scanner)
    * Bit noisy, but will run through lots of checks on file upload forms
* **Backslash Powered Scanner** -[https://github.com/PortSwigger/backslash-powered-scanner](https://github.com/PortSwigger/backslash-powered-scanner)
     * Awesome for figuring out how parameters are handled by the application. Launch on requests with lots of juicy looking GET parameters
* **Notes** -[https://github.com/PortSwigger/Notes](https://github.com/PortSwigger/Notes)
    * Its nifty because all your web hacking notes can be directly in a burp tab and then exported later
* **JS Link Finder** -[https://github.com/PortSwigger/js-link-finder](https://github.com/PortSwigger/js-link-finder)
    * Just like the python based cli tool, except its all in burp
* Scan Enhancing
	* **Error Message Checks** -<br />[https://github.com/PortSwigger/error-message-checks](https://github.com/PortSwigger/error-message-checks)
		* Adds checks to passive scanning
        * Adds additional support for identifying verbose error messages in output. Prone to some false positives.
* Site Mapping
    * **Attack Surface Detector** -<br />[https://github.com/PortSwigger/attack-surface-detector](https://github.com/PortSwigger/attack-surface-detector)
	    * Finds shit out of the burp sitemap
* **Content Type Converter** -<br />[https://github.com/PortSwigger/content-type-converter](https://github.com/PortSwigger/content-type-converter)
	* Surprisingly useful conversion utility for converting between JSON and XML. JSON endpoints that also accept XML are great places to find hidden XXE vulnerabilities.
* **403 Bypasser** -<br />[https://github.com/PortSwigger/403-bypasser](https://github.com/PortSwigger/403-bypasser)
	* Scans for common ways to potentially bypass 403's such as when there is a reverse proxy and it handles URL input weird
* **Active Scan ++** -<br />[https://github.com/PortSwigger/active-scan-plus-plus](https://github.com/PortSwigger/active-scan-plus-plus)
	* Adds a variety of advanced attacks to the standard set deployed on any Burp scanner run. Written by James Kettle, lead security researcher at port swigger. Highly recommended any time you are using Burp scanning features.
* **Retire.js** -<br />[https://github.com/PortSwigger/retire-js](https://github.com/PortSwigger/retire-js)
	* Will detect old vulnerable versions of various Javascript libraries based on known-signatures
* **Http Request Smuggler** -<br />[https://github.com/PortSwigger/http-request-smuggler](https://github.com/PortSwigger/http-request-smuggler)
	* This is simply the best tool available to detect modern request smuggling. Written by James Kettle, who discovered the techniques used to discover and exploit them. This will not only handle the detection of request smuggling but will build starter PoC exploits which can be used to validate the vulnerability or as the basis of developing further exploits.
* **Param Miner** -<br />[https://github.com/PortSwigger/param-miner](https://github.com/PortSwigger/param-miner)
	* Another James Kettle extension. This one will brute force headers, cookies, and parameters and watch for differences in the response. This can be amazingly useful in detecting very subtle bugs and is basically required if you wish to find exploitable cache poisoning.
    * Originally used to help find cache poisoning and request smuggling, but its really good for finding unlinked params, hidden inputs and headers, etc.
* **Reflected Parameters** -<br />[https://github.com/PortSwigger/reflected-parameters](https://github.com/PortSwigger/reflected-parameters)
	* This extension passively monitors requests to look for instances where your input is reflected. Can be very useful for identifying a wide range of bugs, including XSS, and SSTI.
* **Collaborator Everywhere** -<br />[https://github.com/PortSwigger/collaborator-everywhere](https://github.com/PortSwigger/collaborator-everywhere)
	* This extension adds a variety of headers to **EVERY** request, trying to tease intermediate systems into hitting your collaborator server. This can be a tip off to very interesting vulnerabilities driven by malicious headers. As this automatically modifies every request, it should not be left on all the time and should be used with caution.
* **Hunt Scanner**
	* This is a very interesting extension that operates on the theory that statistically speaking certain parameter names are more vulnerable to specific types of attacks. The extension will watch traffic and let you know when it sees a parameter name that is historically associated with an attack type.
* **J2EEScan** -<br />[https://github.com/PortSwigger/j2ee-scan](https://github.com/PortSwigger/j2ee-scan)
	* This extension adds many N-day detections to burp scanner. This is highly recommended for any application based on a Java framework, as it coves many important known-vulnerabilities that should always be checked for.
* **Software Vulnerability Scanner** -<br />[https://github.com/PortSwigger/software-vulnerability-scanner](https://github.com/PortSwigger/software-vulnerability-scanner)
	* Another N-day extension checker, based on Vulners.com API. Not something to turn on all the time, but when scanning non-custom software, it may be able to identify known vulnerabilities. 
* **WSDLer** -<br />[https://github.com/PortSwigger/wsdler](https://github.com/PortSwigger/wsdler)
	* Extremely helpful when testing APIs that have a WSDL available. Will parse the WSDL and automatically generate sample requests which can be loaded into repeater.
* CMS
    * **CMS Scanner** -[https://github.com/PortSwigger/cms-scan](https://github.com/PortSwigger/cms-scan)
	    * Additional coverage for several popular CMS's. Drupal, Joomla, and WordPress.
    * **aem hacker** -<br />[https://github.com/0ang3el/aem-hacker](https://github.com/0ang3el/aem-hacker)
        * Can find privileged CMS users
* **Freddy, Deserialization Bug Finder** -<br />[https://github.com/PortSwigger/freddy-deserialization-bug-finder](https://github.com/PortSwigger/freddy-deserialization-bug-finder)
	* Will scan for a large range of known deserialization vulnerabilities with Java and .Net
* **GadgetProbe** -<br />[https://github.com/PortSwigger/gadgetprobe](https://github.com/PortSwigger/gadgetprobe)
	* An amazing tool for potentially identifying non-known Java deserialization bugs. Will take a wordlist of classes and automatically build test payloads with them in an attempt to identify classes and libraries which are available on the remote Java classpath.
* **SAML Raider** -<br />[https://github.com/PortSwigger/saml-raider](https://github.com/PortSwigger/saml-raider)
	* The standard tool for testing a variety of common issues with SAML infrastructures.
* **Paramalyzer** -<br />[https://github.com/PortSwigger/paramalyzer](https://github.com/PortSwigger/paramalyzer)
	* Will analyze the contents of data found in various parameters and try to identify them. Might be able to spot something like a hash that you might overlook as random data. 
* AutoRepeater -[https://github.com/PortSwigger/auto-repeater](https://github.com/PortSwigger/auto-repeater)
    * If you need to test for access control bugs. This is my favorite thing to use.
* JWT
    * **JSON Web Tokens** -<br />[https://github.com/PortSwigger/json-web-tokens](https://github.com/PortSwigger/json-web-tokens)
        * Will analyze JWT's, and allow you to edit them and test for some known JWT vulnerabilities. Decidedly not as good as [jwt_tool](https://github.com/ticarpi/jwt_tool), but convenient as its available within Burp.
* **Java Deserialization Scanner** -<br />[https://github.com/PortSwigger/java-deserialization-scanner](https://github.com/PortSwigger/java-deserialization-scanner)
	* Adds additionally Java deserialization discovery and exploitation capability.
* **GraphQL Raider** -<br />[https://github.com/PortSwigger/graphql-raider](https://github.com/PortSwigger/graphql-raider)
	* If you ever encounter GraphQL, this is a must have.
* **ViewState Editor**-<br />[https://github.com/PortSwigger/viewstate-editor](https://github.com/PortSwigger/viewstate-editor)
	* Attempts to decode a ViewState. Useful for looking for potentially vulnerable ASP applications.
	* Amazing for .NET apps. Check if the ViewState is encrypted or not, if not, easily read and play with the ViewState
* **Turbo Intruder**
	* References
		* [https://portswigger.net/bappstore/9abaa233088242e8be252cd4ff534988](https://portswigger.net/bappstore/9abaa233088242e8be252cd4ff534988)
	* Timing-based/Time-based attacks
* Log4shell
    * Log4Shell Everywhere -<br />[https://github.com/PortSwigger/log4shell-everywhere](https://github.com/PortSwigger/log4shell-everywhere)
        * Just like collaborator everywhere except its log4j. Probably dont have this enabled all the time...
* Spring4Shell Scanners
    * S4S-Scanner Burp Extension -<br />[https://github.com/onurgule/S4S-Scanner](https://github.com/onurgule/S4S-Scanner)
    * Spring4Shell -<br />[https://github.com/Loneyers/Spring4Shell](https://github.com/Loneyers/Spring4Shell)
* Extensions not included in BApp Store (Download separately and import into burp)
	* Interactsh Collaborator
		* [https://github.com/wdahlenburg/interactsh-collaborator/releases](https://github.com/wdahlenburg/interactsh-collaborator/releases)
		* Download the latest `jar` file from the [releases](https://github.com/wdahlenburg/interactsh-collaborator/releases) page
				* [collaborate-1.0.1.jar](https://github.com/wdahlenburg/interactsh-collaborator/releases/download/v1.0.1/collaborator-1.0.1.jar)
				* In Burp Suite, go to the `Extensions` tab
					* Click `Add` under `Burp Extensions`
					* Under `Extension Details` click `Select file ...`
					* Choose the downloaded `collaborator-1.0.1.jar` file
					* Close the newly opened window
				* You will now have a new tab titled `Interactsh`
					* Click the `Configuration` tab
					* Enter in your interact.sh server IP/URL as the server
					* Enter `443` as the Port
					* Enter the authorization key as Authorization
					* Check TLS
					* Click `Update Settings`
				* Now, when you click `Generate Interactsh url` under the `Logs` tab, you will be able to test it works by pasting the generated url in a browser
* "Copy As" - Transfer requests to external tools
    * Copy As FFUF -<br />[https://github.com/d3k4z/burp-copy-as-ffuf](https://github.com/d3k4z/burp-copy-as-ffuf)
    * Copy As Python-Requests -<br />[https://github.com/PortSwigger/copy-as-python-requests](https://github.com/PortSwigger/copy-as-python-requests)
* PHP Object Injection Check -[https://github.com/PortSwigger/php-object-injection-check](https://github.com/PortSwigger/php-object-injection-check)
    * Adds to active scans. Don't want to miss out on PHP object injections even though they dont really happen on too many apps right now

