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
# Clickjacking

## Key Takeaway

>>>
Be on the lookout for missing x-frame-options / CSP headers. If there are also buttons in protected areas that perform sensitive actions, you may have an exploitable clickjacking vulnerability. 
>>>

## Summary

Clickjacking, (also known as UI redressing) is an attack that involves overlaying an invisible (target) page over top of a decoy page. The end goal is similar to cross-site request forgery (coercing a victim into performing an action on a site they are logged into) with a very different delivery mechanism. The UI trickery is typically performed via loading the target page into an invisible iframe and carefully manipulating CSS. Although someone limited by the fact that it can only induce clicks, in the right situation it can be a devastating attack. 

In practice, clickjacking is becoming uncommon as modern browsers have provided many ways for developers to defend against it. By setting X-Frame-Options headers, or through the use of content security policy 
(frame-ancestors directive) headers it is possible to prevent a given web page from being loaded into another page as an iframe. Using the sameSite cookie attribute also prevents access to post-authentication content if the page is loaded into a frame. Finally, there are a variety of "frame-buster" Javascript-based protection mechanisms. 


## Resources

* PortSwigger - ClickJacking [https://portswigger.net/web-security/clickjacking](https://portswigger.net/web-security/clickjacking)
* OWASP - Clickjacking [https://owasp.org/www-community/attacks/Clickjacking](https://owasp.org/www-community/attacks/Clickjacking)
* Using Click Bandit [https://portswigger.net/support/using-burp-to-find-clickjacking-vulnerabilities](https://portswigger.net/support/using-burp-to-find-clickjacking-vulnerabilities)

## Tools

By far the most mature and effective tool is Burpsuite's built in "click bandit" tool.

## Payloads

A simple PoC payload that can be used to verify the target is vulnerable (but will never actually trick anyone) is below:

```
<!DOCTYPE html>
<html>
<head>
<title>Clickjacking PoC</title>
</head>
<body>
<input type=button value="Click here to Win Prize" style="z-index:-1;left:1200px;position:relative;top:800px;"/>
<iframe src="http://esmuat/" width=100% height=100% style=”opacity: 0.5;”></iframe>
</body>
</html>
```

If you need to construct a usable payload, the best option is to use click bandit - a tool built into burpsuite. Burpsuite will provide some Javascript to paste into the console of the vulnerable page that provides an interactive interface for making an exploit page. Then, host the exploit on a public facing web server and phish or otherwise coerce them into visiting the exploit page. 
