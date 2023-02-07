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
# Sliver
## References
	* [https://sliver.sh/sliver/2021/07/07/getting-started.html](https://sliver.sh/sliver/2021/07/07/getting-started.html)

## Setup
* Installation
	* Linux
		1. Download mingw

				apt install mingw-w64
		1. Install nightly metasploit (source: https://docs.metasploit.com/docs/using-metasploit/getting-started/nightly-installers.html)

				curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && \
				  chmod 755 msfinstall && \
				  ./msfinstall
		1. Install sliver

				curl https://sliver.sh/install|sudo bash
		1. Confirm sliver is running properly

				sliver
* Setup sliver once installed
	1. Confirm no initial errors

			help
	1. Install the armory

			armory
	1. 

## General Help Output
```
Commands:
=========
  clear       clear the screen
  exit        exit the shell
  help        use 'help [command]' for command help
  monitor     Monitor threat intel platforms for Sliver implants         
  wg-config   Generate a new WireGuard client config
  wg-portfwd  List ports forwarded by the WireGuard tun interface        
  wg-socks    List socks servers listening on the WireGuard tun interface
         
         
Generic: 
======== 
  aliases           List current aliases       
  armory            Automatically download and install extensions/aliases
  background        Background an active session
  beacons           Manage beacons             
  canaries          List previously generated canaries
  dns               Start a DNS listener       
  env               List environment variables 
  generate          Generate an implant binary 
  hosts             Manage the database of hosts
  http              Start an HTTP listener     
  https             Start an HTTPS listener    
  implants          List implant builds        
  jobs              Job control                
  licenses          Open source licenses       
  loot              Manage the server's loot store
  mtls              Start an mTLS listener     
  prelude-operator  Manage connection to Prelude's Operator              
  profiles          List existing profiles     
  reaction          Manage automatic reactions to events
  regenerate        Regenerate an implant      
  sessions          Session management         
  settings          Manage client settings     
  stage-listener    Start a stager listener    
  tasks             Beacon task management     
  update            Check for updates          
  use               Switch the active session or beacon
  version           Display version information
  websites          Host static content (used with HTTP C2)
  wg                Start a WireGuard listener
```


## Establish Connection
### Overview

* The first payload generation requires internet connectivity so the server can retrieve necessary **go** code.
* You'll need to select either beacon- or session-based connectivity.
    * Beacon
        * Asynchronous communication
            * Periodic checks by the implant to retrieve tasks, execute, and returns results
    * Session
        * Interactive real time session connection between the implant and the server using either 1) a persistent connection or 2) long polling depending on the underlying C2 protocol

## Examples

* Establish a reverse shell connection on a Windows Host
    1. Generate an implant binary

        generate
    1. 
    1. Deliver the binary to the Windows target.
    1. Execute the binary on the Windows target.