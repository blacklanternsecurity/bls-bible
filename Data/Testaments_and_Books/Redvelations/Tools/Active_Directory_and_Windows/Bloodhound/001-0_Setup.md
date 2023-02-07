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
# Setup
## Installation
* <details><summary>Bloodhound Installation (Click to expand)</summary><p>
	* [GitHub Repo](https://github.com/adaptivethreat/BloodHound)
	* [GitHub](https://github.com/fox-it/bloodhound.py)
	* [Binary](https://github.com/BloodHoundAD/BloodHound/releases)
	* <details><summary>Additional Requirements (Click to expand)</summary><p>
		* [Neo4j](https://neo4j.com/download/community-edition/)
* <details><summary>Neo4j Setup and Install (Click to expand)</summary><p>
	1. Download the community version
	1. Modify the configuration file to use the bloodhound database
	1. Copy the `BloodHoundExampleDB.graphdb` directory under the Bloodhound repo (`$root/Bloodhound/BloodHoundExampleDB.graphdb`) to the Neo4j Database Directory (`$root/neo4j/data/databases/`).
	1. Modify the configuration file under `$root/neo4j/conf/neo4j.conf`, modify the line `dbms.active_datbase` to:

		dbms.active_database=BloodHoundExampleDB.graphdb
	1. Start the Neo4j service by executing:

		root/neo4j/bin/neo4j start
	1. Browse to the webserver listing on port `7474`, and log into Neo4j
		* username: `neo4j`
		* password: `neo4j`
	1. Change the password to something secure.
		* If you forget the neo4j password, you can reset the neo4j password by deleting `/var/lib/neo4j/data/dbms/auth`
	1. Launch bloodhound. This can be done through the command line, simply typing "bloodhound."
	1. Authenticate using the username `neo4j` and the password you just set.
	1. Import Bloodhound Data (see following steps).

## Troubleshooting
* <details><summary>Troubleshooting (Click to expand)</summary><p>
	* White screen issue
		* `CTRL+R` - reload the GUI
	* Nothing happens 

			./bloodhound --no-sandbox