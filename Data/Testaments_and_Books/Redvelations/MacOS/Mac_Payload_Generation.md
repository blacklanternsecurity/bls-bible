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
# Mac Payload Generation
### References

* null-byte blog: Create Backdoor on OSX -<br />[https://null-byte.wonderhowto.com/how-to/create-backdoor-osx-0162551/](https://null-byte.wonderhowto.com/how-to/create-backdoor-osx-0162551/)
* Justin Bui, slyd0g Twitter profile -<br />[https://twitter.com/slyd0g](https://twitter.com/slyd0g)
* Objective-See: The Mac Malware of 2021  -<br />[https://objective-see.com/blog/blog_0x6B.html](https://objective-see.com/blog/blog_0x6B.html)

### Overview, Notes
* Use Mythic C2 to accomplish

* `apfell` agent cannot connect to a self-signed certificate because the apfell agent is unable to override Apple's ATS (Application Transport Security)
	* Workarounds
		* Valid Cert
		* Standard HTTP Traffic
	* Limitation in Apple's language to override that. So, Apfell throws an error and doesn't let you connect
* There was a change in Apfell in Monterey (the latest Apple version) and Big Sir.
	* One of our payload attempts (or the self-signed cert?) had worked with Big Sir but not Monterey.

* [https://twitter.com/slyd0g/status/1461449115074580480](https://twitter.com/slyd0g/status/1461449115074580480)
* Shellcon talk
	* [https://twitter.com/slyd0g/status/1446307477524414465](https://twitter.com/slyd0g/status/1446307477524414465)



https://twitter.com/slyd0g/status/1445521535066775554
In-memory Swift Mach-o execution and captured output with the Poseidon agent from the Mythic framework. Two things to note:
- Swift mangles the function names so you can use the `nm` binary to find your mangled function name
- Function must return char * to capture output
	More Apple info on swift mangling: https://github.com/apple/swift/blob/main/docs/ABI/Mangling.rst

https://github.com/D00MFist/Mystikal
https://twitter.com/runasand/status/1443928693902958593
"I looked at an old CIA implant for OS X called Green Lambert."

https://twitter.com/objective_see/status/1444057508218245121
"In "The Wild World of macOS Installers" Tony Lambert (@ForensicITGuy) of @redcanary discusses macOS installation methods (ab)used by APTs & adware PackageAlien monster + shows the malware execution using data from EDRs to provide ideas for effective analytics! Shield #OBTS"


* Justin Bui: "Where in the World is Carmen Sandiego: Abusing Location Services on macOS" -<br />[https://medium.com/@slyd0g/where-in-the-world-is-carmen-sandiego-abusing-location-services-on-macos-10e9f4eefb71](https://medium.com/@slyd0g/where-in-the-world-is-carmen-sandiego-abusing-location-services-on-macos-10e9f4eefb71)
	* [https://github.com/slyd0g/SwiftLiverpool](https://github.com/slyd0g/SwiftLiverpool)