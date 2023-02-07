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
# Automated OSINT Collection
* General enumeration
	* <details><summary>bbot -<br />[https://github.com/blacklanternsecurity/bbot](https://github.com/blacklanternsecurity/bbot)</summary><p>
		* <details><summary>Overview</summary><p>
			* Recommended for broad enumeration
			* Recommended use is to use all modules at the start, as BBOT runs recurscively and feeds its data collection back into collectors.
		* <details><summary>Usage Images and Gifs</summary><p>
			<img src="https://user-images.githubusercontent.com/20261699/182274919-d4f5aa69-993a-40aa-95d5-f5e69e96026c.gif" style="float": left; width="1200" />
		* <details><summary>Setup</summary><p>
			* bbot install. Recommended: pipx, as pipx creates a virtual environment distinct to bbot.

					pipx install bbot
			* Neo4j
				* Dockerized

						docker run -p 7687:7687 -p 7474:7474 --env NEO4J_AUTH=neo4j/bbotislife neo4j
			* Other required tools
				* By default, bbot will install 
		* Examples
			* Example 1: Quick start, use all safe modules

					bbot --targets
			* Example 2: Run a safe, passive scan

					bbot --targets
			* Example 3: Run bbot with "deadly" option (e.g., nuclei scans), but limit scan to only modules with specified flags

					bbot --allow-deadly -rf active,aggressive,brute-force,deadly,passive,portscan,report,safe,slow,subdomain-enum,web --targets 
			* Example 4: list modules

					bbot -l
			* Example 5: subdomain enumeration

					bbot --flags subdomain-enum --modules naabu httpx --targets evilcorp.com
			* Example 6: passive modules only

					bbot --flags passive --targets evilcorp.com
			* Example 7: Capture web screenshots with gowitness

					bbot -m naabu httpx gowitness --name my_scan --output-dir . -t evilcorp.com 1.2.3.4/28 4.3.2.1 targets.txt
			* Example 8: web spider (search for emails, etc.)

					bbot -m httpx -c web_spider_distance=2 web_spider_depth=2 -t www.evilcorp.com
	* <details><summary>spiderfoot</summary><p>
	* <details><summary>reconspider</summary><p>