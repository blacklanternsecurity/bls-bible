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
# WiFi Pineapple
## Setup

1. Plug in WiFi pineapple nano into computer with included USB cable 
1. Wait a few seconds and an Ethernet device will show up
1. **[Optional]** You can rename to something easier to follow (e.g., **Pineapple**)
    1. Go to: `Control Panel\Network and Internet\Network Connections`
    1. Click on the corresponding Ethernet label (In this case Ethernet4) and change the name
1. Share your Internet Connection with the pineapple by using the **sharing** function in Windows.
    1. Right click on the network that has internet access and click Properties.
    1. Select the Sharing tab and check the box Allow other network users etc. 
    1. Select the Pineapple from the dropdown and click OK
1. After configuring, the connection sharing the **pineapple** ethernet should change (e.g., 192.168.137.1).
    1. You may need configure that manually.
1. Login to the pineapple
    1. go to http://172.16.42.1:1471
        * You may need to check ipconfig to see if this has been changed by windows
1. Download the latest firmware from WiFiPineapple.com [https://www.wifipineapple.com/downloads/nano/latest](https://www.wifipineapple.com/downloads/nano/latest)
1. Change the logon password.
1. Download and install modules.
    * **Troubleshooting:** Unable to connect to the Internet from the pineapple (on tethered windows 10)
        * Workaround
            1. `Networking`-> `Wifi Client Mode`
            1. Connect to your wifi access point.
1. Next download modules for the pineapple
Another method for updating the pineapple is to plug-in the extra wifi adapter into the pineapple.
1. Login to the pineapple at `172.16.42.1:1471`, or connect to its https://www.wifipineapple.com/downloads/nano/latest wifi that was previously configured
Go to Networking -> WiFi Client Mode  
Select Interface wlan2 (the second wifi you connected) then click Scan.
Connect to your local wifi network.


The pineapple will now be connected to the internet on the second wifi and can download updates and modules

## Configuring kismet for Wardriving with GPS

Insert an sd card into the pineapple and format it via the web based interface.

[[File:Kismet7.png|400px]]

ssh to the pineapple:

putty root@172.16.42.1

check to see that the sd card is recognized:
```bash
root@Pineapple:# fdisk -l
```
We'll download and install kismet to the sd card.

run the following commands:
```bash
root@Pineapple:/sd# opkg update
root@Pineapple:/sd# opkg list | grep kismet
root@Pineapple:/sd# opkg --dest sd install kismet-server
root@Pineapple:/sd# opkg --dest sd install kismet-client
```
(ignore errors when issuing the install commands)

Next install gpsd for the USB GPS device

The packages to be installed are:

* libgps_3.7-1_ar71xx.ipk
* libgpsd_3.7-1_ar71xx.ipk
* gpsd_3.7-1_ar71xx.ipk
* gpsd-clients_3.7-1_ar71xx.ipk


```bash
root@Pineapple:~# cd /sd
root@Pineapple:/sd# wget https://downloads.openwrt.org/attitude_adjustment/12.09/ar71xx/generic/packages/libgps_3.7-1_ar71xx.ipk
root@Pineapple:/sd# wget https://downloads.openwrt.org/attitude_adjustment/12.09/ar71xx/generic/packages/libgpsd_3.7-1_ar71xx.ipk
root@Pineapple:/sd# wget https://downloads.openwrt.org/attitude_adjustment/12.09/ar71xx/generic/packages/gpsd_3.7-1_ar71xx.ipk 
root@Pineapple:/sd# wget https://downloads.openwrt.org/attitude_adjustment/12.09/ar71xx/generic/packages/gpsd-clients_3.7-1_ar71xx.ipk
root@Pineapple:/sd# opkg --dest sd install libgps_3.7-1_ar71xx.ipk
root@Pineapple:/sd# opkg --dest sd install libgpsd_3.7-1_ar71xx.ipk
root@Pineapple:/sd# opkg --dest sd install gpsd_3.7-1_ar71xx.ipk 
root@Pineapple:/sd# opkg --dest sd install gpsd-clients_3.7-1_ar71xx.ipk
```

Clean up:
```bash
root@Pineapple:/sd# rm *.ipk
```

Insert the USB GPS and test to see if it's working:
```bash
root@Pineapple:/sd# gpsd -D 5 -N -n /dev/ttyUSB0
```

You can get the GPS version by telnetting:
```bash
root@Pineapple:~# telnet 127.0.0.1:2947
{"class":"VERSION","release":"3.7","rev":"3.7","proto_major":3,"proto_minor":7}
```
Download the MAC to Manufacturer file:
```bash
wget -O /sd/manuf http://anonsvn.wireshark.org/wireshark/trunk/manuf
ln -s /sd/manuf /etc/manuf
```

Edit `/etc/kismet/kismet.conf` and change (`vi /etc/kismet/kismet.conf`)

```bash
logprefix=/sd/.kismet
ncsource=wlan1
gps=true
ouifile=/etc/manuf
```

create `run_kismat.sh` to start everything as follows:

```bash
#!/bin/bash

echo "==> Setting wlan1 in monitor mode"
ifconfig wlan1 down
iwconfig wlan1 mode monitor
ifconfig wlan1 up

echo "==> Starting GPSD with /dev/ttyUSB0"
killall gpsd
gpsd -n /dev/ttyUSB0
sleep 3

echo "==> Starting Kismet server in background"
killall kismet_server
kismet_server -p /sd/.kismet -c wlan1 --daemonize
```

Make it executable:
```bash
chmod +x run_kismat.sh
```

### Wardrive

To do a wardrive ssh into the pineapple and run `./run_kismat.sh`

You can connect to the kismet_server to test by running:
```bash
kismet_client
```

To convert the generated file into a google earth kml file run the following on Kali.

1. Copy the `.netxml` file to kali from the `/sd/.kismet` folder on the pineapple (i.e. use WinSCP).
```bash
giskismet -x Kismet-20110221-08-56-26-1.netxml
giskismet -q "select * from wireless" -o giskismet_demo.kml
```