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
# Installing Oracle JRE in Kali
- OpenJDK is fairly unstable and often does not work for software such as JD-GUI or Cobalt Strike
- Oracle's closed-source version is usually preferable.

## Step 1: Download Tarball

- Download the Linux x64 tarball from https://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html

## Step 2: Convert to .deb Package
- NOTE: Creating a temporary non-root user is necessary because "make-jpkg" refuses to run as root.
~~~
$ apt install java-package
# add temporary user
$ useradd tempuser0
# become temporary user
$ su tempuser0
# change to a directory where you have write access
$ cd /tmp
# this will create a .deb file in the current directory
$ make-jpkg /root/Downloads/jre-8u191-linux-x64.tar.gz
$ exit
# remove temporary user
$ userdel tempuser0
~~~


## Step 3: Install
~~~
$ dpkg -i /tmp/oracle-java8-jre_8u191_amd64.deb
# set default Java version
$ update-java-alternatives -s oracle-java8-jre-amd64
~~~

- Verify default Java version.  Output should look like:
~~~
$ java -version
java version "1.8.0_191"
Java(TM) SE Runtime Environment (build 1.8.0_191-b12)
Java HotSpot(TM) 64-Bit Server VM (build 25.191-b12, mixed mode)
~~~