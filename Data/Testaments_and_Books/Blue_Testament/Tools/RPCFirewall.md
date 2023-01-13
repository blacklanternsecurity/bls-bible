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
# RPC Firewall
### References
* Zero Network's GitHub: RPC Firewall -<br />[https://github.com/zeronetworks/rpcfirewall](https://github.com/zeronetworks/rpcfirewall)

### Commands
* Check Status

		RpcFwManager.exe /status
* Recommend use: Start with just `/start`. This command starts the RPC Firewall service (for 'fw' or no suffix), and creates the RPC Filters (for 'flt' or no suffix).

		RpcFwManager.exe /start
	* Once started, the RPC Firewall will persiste across reboots. RPC Filters are also persistent.
	* It is also possible to use the RPC Firewall ad-hoc, to protect specific processes. This will no start the RPC Firewall service, and will not persist reboots.
* Protect a single process by pid:

		RpcFwManager.exe /start pid <pid>
* Protect a single process by name:

		RpcFwManager.exe /start process <process name>
* Stop the protection, simply issue the '/stop' command with the appropriate suffix (it is not possible to stop protection for a specific process).

		RpcFwManager.exe /stop

### Rules
* Detection
	* Sigma Rules by Sigma HQ -<br />[https://github.com/SigmaHQ/sigma/tree/master/rules/application/rpc_firewall](https://github.com/SigmaHQ/sigma/tree/master/rules/application/rpc_firewall)
* Prevention
	* References
		* [https://github.com/zeronetworks/rpcfirewall/blob/master/Configuration_templates/RpcFw.conf.FirewallOnly](https://github.com/zeronetworks/rpcfirewall/blob/master/Configuration_templates/RpcFw.conf.FirewallOnly)
		* [https://github.com/zeronetworks/rpcfirewall/blob/master/Configuration_templates/RpcFw.conf.FiltersOnly](https://github.com/zeronetworks/rpcfirewall/blob/master/Configuration_templates/RpcFw.conf.FiltersOnly)
		* [https://github.com/zeronetworks/rpcfirewall/blob/master/Configuration_templates/RpcFw.conf.Both](https://github.com/zeronetworks/rpcfirewall/blob/master/Configuration_templates/RpcFw.conf.Both)
