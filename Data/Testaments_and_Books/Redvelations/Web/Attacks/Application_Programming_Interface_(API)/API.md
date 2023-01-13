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
# API
## References
* <details><summary>References (Click to expand)</summary><p>
	* OWASP: Top 10 API vulnerabilities -<br />[https://github.com/OWASP/API-Security/blob/master/2019/en/dist/owasp-api-security-top-10.pdf](https://github.com/OWASP/API-Security/blob/master/2019/en/dist/owasp-api-security-top-10.pdf)
	* [https://github.com/carlospolop/hacktricks/blob/master/pentesting/pentesting-web/web-api-pentesting.md](https://github.com/carlospolop/hacktricks/blob/master/pentesting/pentesting-web/web-api-pentesting.md)
	* Shieldfy GitHub: Web API Checklist -<br />[https://github.com/shieldfy/API-Security-Checklist](https://github.com/shieldfy/API-Security-Checklist)
	* A collection of useful resources for building RESTful HTTP+JSON APIs. -<br />[yosriady/api-development-tools](https://github.com/yosriady/api-development-tools)

## Overview

* Several TTPs occur naturally through the use of tools and attacks described in this guide, and sometimes multiple
	* [Steal Application Access Token](TTP/T1528_Steal_Application_Access_Token/T1528.md)
* <details><summary>Web Services (SOAP/XML) (Click to expand)</summary><p>
	* The documentation uses **WSDL** format and is usually saved in the `?wsdl` path like `https://api.example.com/api/?wsdl`
	* An example of this documentation can be found in [http://www.dneonline.com/calculator.asmx](http://www.dneonline.com/calculator.asmx) (WSDL document in [http://www.dneonline.com/calculator.asmx?wsdl](http://www.dneonline.com/calculator.asmx?wsdl)) and you can see an example request calling the `Add` method in [http://www.dneonline.com/calculator.asmx?op=Add](http://www.dneonline.com/calculator.asmx?op=Add)
	* For parsing these files and create example requests you and use the tool **SOAPUI** or the **WSDLer** Burp Suite Extension.
* <details><summary>REST APIs (JSON) (Click to expand)</summary><p>
	* The standard documentation is the WADL file.
		* Example
			* [https://www.w3.org/Submission/wadl/](https://www.w3.org/Submission/wadl/).
		* Dev-friendly API representation engines - Swagger (Demo Page)
			* [https://swagger.io/tools/swagger-ui/](https://swagger.io/tools/swagger-ui/)
	* For parsing these files and create example requests you an use the tool **Postman**
* [GraphQL Guide](Testaments_and_Books/Redvelations/Apps_and_Services/Web/Applications/graphql.md)

## Tools

* <details><summary>Tools (Click to expand)</summary><p>
	* Imperva's customizable API attack tool takes an API specification as an input, generates and runs attacks that are based on it as an output.
		* [https://github.com/imperva/automatic-api-attack-tool](https://github.com/imperva/automatic-api-attack-tool)
	* RESTler -<br />[https://github.com/microsoft/restler-fuzzer](https://github.com/microsoft/restler-fuzzer)
		* Stateful REST API fuzzing tool
		* Automatically tests cloud services through REST APIs
		* Identifies cloud security and reliability bugs
		* For a given cloud service with an OpenAPI/Swagger specification, RESTler analyzes its entire specification, and then generates and executes tests that exercise the service through its REST API.
	* api testing
		* [https://github.com/flipkart-incubator/Astra](https://github.com/flipkart-incubator/Astra)
	* Enumerate API Endpoints
		* [https://github.com/assetnote/kiterunner](https://github.com/assetnote/kiterunner)

## Process

* <details><summary>SOAP, XML (Click to expand)</summary><p>
	* XXE ([XXE Attack Guide](Testaments_and_Books/Redvelations/Apps_and_Services/Web/Attacks/XML_External_Entities_(XXE).md))
		* Uncommon, but check if user input `DTD Declarations` are allowed.
		* Try to insert payloads via `CDATA` tags, provided XML is still correct
* CORS ([Guide](Testaments_and_Books/Redvelations/Apps_and_Services/Web/Attacks/Cross-Origin_Resource_Sharing_(CORS)/00-0_Cross-Origin_Resource_Sharing_(CORS).md))
* Patterns
	* Search for API patterns inside the api and try to use it to discover more.
	* If you find  `_/api/albums/<album_id>/photos/<photo_id>_`, you could try also things like:  `_/api/posts/<post_id>/comment/_` (Note posts and comment positions)
	* Use some fuzzer to discover this new endpoints.
* Add parameters
	* Something like the following example might get you access to another user’s photo album:

			_/api/MyPictureList --> /api/MyPictureList?user_id=<other_user_id>_
* Replace parameters
	* You can try to **fuzz parameters** or **use** parameters **you have seen** in a different endpoints to try to access other information
	* For example, if you see something like: _/api/albums?**album\_id=\<album id>**_
	* You could **replace** the **`album_id`** parameter with something completely different and potentially get other data: _/api/albums?**account\_id=\<account id>**_
* Parameter pollution

		/api/account?id=<your account id> -->  /api/account?id=<your account id>&id=<admin's account id>
* Wildcard parameter
	* Try to use the following symbols as wildcards
	* `**\***`, `**%**`, `**\_**`, `**.**`
	* ` /api/users/\*`
	* `/api/users/%`
	* `/api/users/\_`
	* `/api/users/.`
* HTTP request method change
	* You can try to use the HTTP methods: **GET, POST, PUT, DELETE, PATCH, INVENTED** to try check if the web server gives you unexpected information with them.
* Request content-type
	* Try to play between the following content-types (bodifying acordinly the request body) to make the web server behave unexpectedly:
		* **x-www-form-urlencoded** --> user=test
		* **application/xml** -->  \<user>test\</user>
		* **application/json** -->  {"user": "test"}
		* Parameters types
			* JSON, unexpected data types

					{"username": "John"}
					{"username": true}
					{"username": null}
					{"username": 1}
					{"username": \[true]}
					{"username": \["John", true]}
					{"username": {"$neq": "lalala"}}
		* any other combination you may imagine
* If you can send **XML** data, check for **XXE injections**.
* If you send regular POST data, try to send arrays and dictionaries:
	* `username\[]=John`
	* `username\[$neq]=lalala`
* Play with routes

		/files/..%2f..%2f + victim ID + %2f + victim filename
* Check possible versions
	* Old versions may be still be in use and be more vulnerable than latest endpoints
		* `/api/v1/login`
		* `/api/v2/login`\
		*  `/api/CharityEventFeb2020/user/pp/<ID>`
		*  `/api/CharityEventFeb2021/user/pp/<ID>`
* API Endpoint Lists/Wordlists
	* [https://gist.github.com/yassineaboukir/8e12adefbd505ef704674ad6ad48743d](https://gist.github.com/yassineaboukir/8e12adefbd505ef704674ad6ad48743d)

#### Checklist

* Authentication
	* Don't use `Basic Auth`. Use standard authentication instead (e.g. [JWT](https://jwt.io/), [OAuth](https://oauth.net/)).
	* Don't reinvent the wheel in `Authentication`, `token generation`, `password storage`. Use the standards.
	* Use `Max Retry` and jail features in Login.
	* Use encryption on all sensitive data.
	* JWT (JSON Web Token)
		* Use a random complicated key (`JWT Secret`) to make brute forcing the token very hard.
		* Don't extract the algorithm from the header. Force the algorithm in the backend (`HS256` or `RS256`).
		* Make token expiration (`TTL`, `RTTL`) as short as possible.
		* Don't store sensitive data in the JWT payload, it can be decoded [easily](https://jwt.io/#debugger-io).
	* OAuth
		* Always validate `redirect_uri` server-side to allow only whitelisted URLs.
		* Always try to exchange for code and not tokens (don't allow `response_type=token`).
		* Use `state` parameter with a random hash to prevent CSRF on the OAuth authentication process.
		* Define the default scope, and validate scope parameters for each application.
* Access
	* Limit requests (Throttling) to avoid DDoS / brute-force attacks.
	* Use HTTPS on server side to avoid MITM (Man in the Middle Attack).
	* Use `HSTS` header with SSL to avoid SSL Strip attack.
	* For private APIs, only allow access from whitelisted IPs/hosts.
* Input
	* Use the proper HTTP method according to the operation: `GET (read)`, `POST (create)`, `PUT/PATCH (replace/update)`, and `DELETE (to delete a record)`, and respond with `405 Method Not Allowed` if the requested method isn't appropriate for the requested resource.
	* Validate `content-type` on request Accept header (Content Negotiation) to allow only your supported format (e.g. `application/xml`, `application/json`, etc.) and respond with `406 Not Acceptable` response if not matched.
	* Validate `content-type` of posted data as you accept (e.g. `application/x-www-form-urlencoded`, `multipart/form-data`, `application/json`, etc.).
	* Validate user input to avoid common vulnerabilities (e.g. `XSS`, `SQL-Injection`, `Remote Code Execution`, etc.).
	* Don't use any sensitive data (`credentials`, `Passwords`, `security tokens`, or `API keys`) in the URL, but use standard Authorization header.
	* Use an API Gateway service to enable caching, Rate Limit policies (e.g. `Quota`, `Spike Arrest`, or `Concurrent Rate Limit`) and deploy APIs resources dynamically.
* Processing
	* Check if all the endpoints are protected behind authentication to avoid broken authentication process.
	* User own resource ID should be avoided. Use `/me/orders` instead of `/user/654321/orders`.
	* Don't auto-increment IDs. Use `UUID` instead.
	* If you are parsing XML files, make sure entity parsing is not enabled to avoid `XXE` (XML external entity attack).
	* If you are parsing XML files, make sure entity expansion is not enabled to avoid `Billion Laughs/XML bomb` via exponential entity expansion attack.
	* Use a CDN for file uploads.
	* If you are dealing with huge amount of data, use Workers and Queues to process as much as possible in background and return response fast to avoid HTTP Blocking.
	* Do not forget to turn the DEBUG mode OFF.
* Output
	* Send `X-Content-Type-Options: nosniff` header.
	* Send `X-Frame-Options: deny` header.
	* Send `Content-Security-Policy: default-src 'none'` header.
	* Remove fingerprinting headers - `X-Powered-By`, `Server`, `X-AspNet-Version`, etc.
	* Force `content-type` for your response. If you return `application/json`, then your `content-type` response is `application/json`.
	* Don't return sensitive data like `credentials`, `Passwords`, or `security tokens`.
	* Return the proper status code according to the operation completed. (e.g. `200 OK`, `400 Bad Request`, `401 Unauthorized`, `405 Method Not Allowed`, etc.).
* CI & CD
	* Audit your design and implementation with unit/integration tests coverage.
	* Use a code review process and disregard self-approval.
	* Ensure that all components of your services are statically scanned by AV software before pushing to production, including vendor libraries and other dependencies.
	* Design a rollback solution for deployments.