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
# jok3r
### References
* [https://github.com/koutto/jok3r](https://github.com/koutto/jok3r)

### Guide
* Start existing container

        docker start -i jok3r-container
* Run in docker

        docker pull koutto/jok3r
        docker run -i -t --name jok3r-container-updated -w /root/jok3r -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --shm-size 2g --net=host koutto/jok3r

        root@jok3r-docker:~/jok3r# python3 jok3r.py db
        jok3rdb[default]> mission -a mayhem

        [+] Mission "mayhem" successfully added
        [*] Selected mission is now mayhem

        jok3rdb[mayhem]> quit
* Single target

        docker run -i -t --name jok3r-container-updated -w /root/jok3r -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --shm-size 2g --net=host koutto/jok3r

        root@jok3r-docker:~/jok3r# python3 jok3r.py attack -t https://www.evilcorp.com/ --add2db mayhem
    * Parameters and Flags
        * `--fast` - execute without user interaction
* Multiple targets

        docker start -i jok3r-container
        $ python3 jok3r.py db -m mayhem
        jok3rdb[default]> help

        Import
        ================================================================================
        file                Import a list of targets from a file
                            One target per line, with the following syntax:
                            - For any service: <IP/HOST>:<PORT>,<SERVICE>
                            - For HTTP service: <URL> (must begin with http(s)://)
        nmap                Import Nmap results (XML)

        jok3rdb[default]> nmap --no-http-recheck evilcorp_top1000.xml
        jok3rdb[default]> quit
* Search only for "easy wins" (critical vulns & easy to exploit) on all services registered in mission "mayhem":

        python3 jok3r.py attack -m mayhem --profile red-team --fast
* Run all security checks against all services in the given mission and store results in the database:

        python3 jok3r.py attack -m mayhem --fast