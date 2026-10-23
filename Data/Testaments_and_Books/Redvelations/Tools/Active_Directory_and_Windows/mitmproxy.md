<!---------------------------------------------------------------------------------
Copyright: (c) BLS OPS LLC.
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
--------------------------------------------------------------------------------->
# mitmproxy

* Installation

		python3 -m pip install mitmproxy
* Trust mitmproxy certificate
	1. initialize mitmproxy cert

			mitmproxy --help
	1. trust certificate

		cp ~/.mitmproxy/mitmproxy-ca-cert.cer /usr/local/share/ca-certificates/mitmproxy-ca-cert.crt
		update-ca-certificates
* Ignore domain (e.g. for windows update, which uses cert-pinning)

		mitmproxy --ignore-hosts '.*\.microsoft\.com' --ignore-hosts '.*\.live\.com' --ignore-hosts '.*\.windowsupdate\.com'
* Upstream proxy

		mitmproxy --mode upstream:localhost:8080
* Write to file

		mitmproxy -w mitmdump0
* Display event log

		console.view.eventlog