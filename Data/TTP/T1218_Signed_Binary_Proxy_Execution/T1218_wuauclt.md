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
# wuauclt
### References
* LOLBAS Project: wuauclt.exe -<br />[https://lolbas-project.github.io/lolbas/Binaries/Wuauclt/](https://lolbas-project.github.io/lolbas/Binaries/Wuauclt/)

### Overview
* `wuauclt.exe` is a Microsoft signed binary that requires a DLL with specific exported functions, specifically: **DownloadManager** and **DataStore**.

### Process
* These can be created with SplinterNet during the payload generation, and used in the following context:

		wuauclt.exe /UpdateDeploymentProvider C:\users\user1\Desktop\localdll.dll /RunHandlerComServer
