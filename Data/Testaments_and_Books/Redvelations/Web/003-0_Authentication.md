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
# Authentication
## Overview

Authentication is managed through various methods, including:

* Cookies
* Tokens
* Identifiers

Authentication must track the following pieces of information accurately to prevent abuse:

* Authentication - Who are you?
* Authorization - What are you allowed to do?
* Non-repudiation - Are you the only one who could have done X?

Example issues when these aspects are not employed:

* Not using encryption when they should have used signatures
	* Example
		* JWT design options
			* Only handle authentication (`(body is {"userid": "1"})`)
			* Handle both authentication and authorization `(body is {"userid": "1", "role": "admin"})`
		* Compare the status of the JWT responsibilities to how the application behaves
			* If the application restricts activities intended for adminsitrators, then it must be comparing your userid to a list of role assignments on the backend

## Enumeration
### Specific notes
* Flask
	* Many abuses for flask involve cracking/recovering the flask secret and forging auth tokens

### Process
* Check for hard-coded keys
	* Test if tokens are reusable across instances
		* Applies to many forms of authentication, including:
			* JWTs
			* Flask session cookies
			* Django session cookies
			* ASP.Net viewstates
		* Viewstate Comparison Process
			1. Identify two cases where the same app can be observed
				* Local Source Copy
				* Primary Instance
				* Secondary Instances
			1. Grab the viewstate from both instances' login page.
			1. Compare each viewstate
			1. Compare the signature. If the signatures are the same, there is potentially machine key re-use.
		* Capitalizing on identical viewstates
			* When the two compared apps are a local copy and the target online instance
				1. Load the local instance
				1. Copy your session id
				1. Pass the session id to the target online instance and confirm if authentication succeeds
		* Resolution
			* One option is to generate application secrets at runtime instead of defining a static secret
* Check for weak cryptography managing authentication
	* Example: Encrypted session token analysis
		1. Acquire 2 accounts identical in properties except for a single property such as the username length.
		1. Authenticate to the web application and note the issued session tokens.
		1. Compare the session tokens, and identify if the session tokens vary in length as a result of the difference in the single property (e.g., username length).
			* In the case of username length, if the length of the session tokens vary according to the username length, then you may be able to conclude that the username is included in the token rather than a numeric user ID.
			* In the case where repeated characters in a username (e.g., 50 As) leads to repeated characters in the session token, a weak cryptography is likely in effect. Cleartext information should never be able to influence the ciphertext
			* If the token the site issues you is a GUID instead of a JWT/b64/binary string, there's probably not much you can do
			* similarly, in the case of a JWT or Viewstate, you have (presumably) plaintext followed by a signature ("presumably" because viewstates can be encrypted)
			* The same applies for formsauth cookies, which are long (encrypted) hex strings
			* Similarly, in the case of a JWT or Viewstate, you have (presumably) plaintext followed by a signature
			* Verbose errors help a lot in these cases, where you can give it a token that may or may not be valid and it will tell you what's wrong

