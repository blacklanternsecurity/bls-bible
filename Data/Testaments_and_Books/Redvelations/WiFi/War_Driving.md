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
# War Driving
## References
#@TODO

## Setup

* This will walk you through getting a war drive setup going with GPS and WiFi coordination for use with Google Earth on Kali.

### Gear Needed

* Alfa AWUS036NHA [https://www.amazon.co.uk/Network-AWUS036NHA-Adapter-150-Mbps-802-11b/dp/B004Y6MIXS/ref=sr_1_3?ie=UTF8&qid=1551723601&sr=8-3&keywords=alfa+awus036nh%EF%BB%BF](https://www.amazon.co.uk/Network-AWUS036NHA-Adapter-150-Mbps-802-11b/dp/B004Y6MIXS/ref=sr_1_3?ie=UTF8&qid=1551723601&sr=8-3&keywords=alfa+awus036nh%EF%BB%BF)
* GlobalSat BU-353-S4 receiver [https://www.amazon.co.uk/GlobalSat-BU-353-S4-Receiver-SiRF-Black/dp/B008200LHW/ref=sr_1_1?ie=UTF8&qid=1551724582&sr=8-1&keywords=globalsat+bu-353-s4+usb+gps+receiver%EF%BB%BF](https://www.amazon.co.uk/GlobalSat-BU-353-S4-Receiver-SiRF-Black/dp/B008200LHW/ref=sr_1_1?ie=UTF8&qid=1551724582&sr=8-1&keywords=globalsat+bu-353-s4+usb+gps+receiver%EF%BB%BF)

### GPS Setup

1. Install GPSD:
```bash
apt install gpsd gpsd-clients
```
1. Run GPSD (way 1): (make sure your GPS device is ttyUSB0)
```bash
gpsd -n -N -D 2 /dev/ttyUSB0
```
1. Run GPSD (way 2): (should keep GPSD running in the background, check netstat to verify running on localhost:2947)
```bash
gpsd -n -N -D 2 -F /var/run/gpsd.sock /dev/ttyUSB0
```
1. Verify GPSD is working correctly
```bash
cgps -s
```

You can close **CGPS** if everything looks good. It may take a minute to start seeing data.

### 802.11 Setup

1. Run the following as root.
```bash
airmon-ng
```
1. Look for the interface that corresponds to rtl8187, that is the ALFA card.
1. Run: (replace wlan0 with the correct interface)
 airmon-ng start wlan0

Run airmon-ng again to verify rtl8187 is now in monitor mode

### Kismet Setup

1. First, we need to completely uninstall kismet because it is garbage. We need to replace it with older kismet garbage:
```bash
 sudo apt remove kismet
```
1. Make sure you have all these bits:
```bash
sudo apt install build-essential git libmicrohttpd-dev pkg-config zlib1g-dev libnl-3-dev libnl-genl-3-dev libcap-dev libpcap-dev libnm-dev libdw-dev libsqlite3-dev libprotobuf-dev libprotobuf-c-dev protobuf-compiler protobuf-c-compiler libsensors4-dev libusb-1.0.0-dev python3 python3-setuptools python3-protobuf python3-requests python3-numpy python3-serial python3-usb python3-dev librtlsdr0 libubertooth-dev libbtbb-dev
```

Then do these bits here:

```bash
 apt update
 apt upgrade
 wget https://www.kismetwireless.net/code/kismet-2016-07-R1.tar.xz
 tar -xvf kismet-2016-07-R1.tar.xz
 cd kismet-2016-07-R1
 ./configure
```

(check output for unmet dependencies)

```bash
make
sudo make suidinstall
sudo usermod -aG kismet $USER
```

Check that you are in the kismet group, if not, re-log and check again

 groups

You should be good to go now with Kismet.

### GISKismet Setup


```bash
git clone https://github.com/xtr4nge/giskismet.git
cd giskismet
sudo apt install libxml-libxml-perl libdbi-perl libdbd-sqlite3-perl
perl Makefile.PL
make
sudo make install
```

### Google Earth Setup

Grab the 64 bit `.deb` package from [https://www.google.com/earth/versions/#download-pro]

Then run:
 sudo dpkg -i google-earth-pro-stable_current_amd64.deb

Should install just fine.

## Execution: War Driving

To use all of this, first make sure GPSD is running by checking:

```bash
sudo netstat -antp
```

Make sure you see it running on port 2947.

Start up kismet as root:
```bash
sudo kismet
```

1. Select **Yes** to automatically start the Kismet server.
1. Default Options.
1. It will eventually ask you for a packet source to be defined.
1. Intf: wlan0mon
1. Name: whatever
1. Leave **Opts** blank

Once you hit **Add** you should start capturing traffic. To stop the process and exit gracefully, first go to the **Kismet** menu, select **Disconnect**. Then go back to the **Kismet** menu and select **Quit**. Check the current directory for your log outputs.

With the Kismet-...-.netxml document, load it into GISKismet:

```bash
giskismet -x Kismet-...-.netxml
```

This load the data into the sqlite3 database. Query the database to get a Google Earth compatible file:

```bash
giskismet -q "SELECT * FROM wireless" -o kismet-google-earth.kml
```

Open up Google Earth:
```bash
google-earth-pro
```
And open your `.kml` file to view your war driving results.