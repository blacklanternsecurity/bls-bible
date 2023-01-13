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
## chcp.com
### References
* #@TODO

### Overview
chcp.com is a Microsoft signed binary that requires a DLL with specific exported functions: `NlsDllCodePageTranslation`

1. Use administrative privileges to make the Registry edit on the HKLM:
	`HKLM\SYSTEM\ControlSet001\Control\NIs\CodePage`
2. Modify a `REG_SZ` entry, for example `55001`.
3. Set the `Data` to a path to a DLL, where the local path will reference:
	`C:\Windows\system32\spool\drivers\color\pay.dll`
	* The data should be only a partial path (e.g. `spool\drivers\color\pay.dll`)

These can be created with SplinterNet during the payload generation, and used in the following context from a cmd.exe prompt:

```
chcp <number picked above, e.g. 55001>
```