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
# SAML

- https://epi052.gitlab.io/notes-to-self/blog/2019-03-07-how-to-test-saml-a-methodology/
- https://epi052.gitlab.io/notes-to-self/blog/2019-03-13-how-to-test-saml-a-methodology-part-two/
- https://epi052.gitlab.io/notes-to-self/blog/2019-03-16-how-to-test-saml-a-methodology-part-three/

## SAML Raider Burp Extension Tutorial

1. Install the `SAML Raider` Burp extension

    - Side tangent: generate and clone a sample cert:
        - Generate an X.509 certificate
        ~~~
        $ openssl req -x509 -newkey rsa:4096 -keyout /tmp/cert.key -out /tmp/cert.pem -days 365 -nodes
        ~~~
        - Go to the `SAML Raider Certificates` tab in Burp and click `Import`
            - Import the cert we just put in `/tmp/cert.pem`
        - You can clone the cert in SAML raider, export, and diff it like this:
            ~~~
            $ diff <(openssl x509 -in /tmp/cloned-cert.pem -text -noout) <(openssl x509 -in /tmp/cert.pem -text -noout)
            ~~~
2. Turn on intercept (for response too) and start the auth process
3. Intercept the SAML certificate with Burp and import it into SAML Raider
    - You may need to base64-decode the cert
4. Intercept the SAML request and try modifying pieces of it in the SAML Raider tab
    - Try changing the parameters and re-signing the message


Note: The XSW (XML Signature Wraping) attacks in SAML Raider try to exploit vulnerabilities in the XML parser.  Essentially, because the part of the code that *validates* the XML and the part of the code that *uses* the XML are different, you can sometimes move the signed part of the tree off into its own little area where it passes verification isn't actually used.

## XXE 
- don't forget to try this

## XLST
- don't forget to try this
~~~
<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
  ...
  <ds:Transforms>
    <ds:Transform>
      >>> XSLT payload goes here <<<
    </ds:Transform>
  </ds:Transforms>
</ds:Signature>
~~~