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
# VNC (Port 5900^)

* VNC Enumeration
    * Scans
        * 5900^ for direct access.5800 for HTTP access.
* VNC Brute Force
    * Password Attacks
        * Remote
            * Password Guess
                * vncrack
            * Password Crack
                * vncrack
                * Packet Capture
                    * Phoss -<br />[http://www.phenoelit.de/phoss](http://www.phenoelit.de/phoss)
        * Local
            * Registry Locations

                    \HKEY_CURRENT_USER\Software\ORL\WinVNC3
                    \HKEY_USERS\.DEFAULT\Software\ORL\WinVNC3
            * Decryption Key

                    0x238210763578887
* Examine Configuration Files

        .vnc
        /etc/vnc/config
        $HOME/.vnc/config
        /etc/sysconfig/vncservers
        /etc/vnc.conf
