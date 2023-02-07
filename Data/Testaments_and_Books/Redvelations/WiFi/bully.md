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
# Bully

#@WiFi

# bully
Tool for cracking old WPS 1.0 networks. These are newer than WEP, but not by much.

## Simple WPS brute-force attack

```bash
# put the interface in monitor mode
airmon-ng start wlan0
# start bully (channel is optional)
bully --channel 6 --bssid de:ad:ed:be:ee:ef wlan0mon
```