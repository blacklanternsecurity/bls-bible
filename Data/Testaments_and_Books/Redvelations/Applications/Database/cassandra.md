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
# 9042/9160 - Pentesting Cassandra

## Basic Information

Apache Cassandra is a highly scalable, high-performance distributed database designed to handle large amounts of data across many commodity servers, providing high availability with no single point of failure. It is a type of NoSQL database.\
In several cases you will find **cassandra accepting any credentials** (as there aren't any configured) and you will be able to enumerate the database.

**Default port:** 9042,9160

```
PORT     STATE SERVICE   REASON
9042/tcp open  cassandra-native Apache Cassandra 3.10 or later (native protocol versions 3/v3, 4/v4, 5/v5-beta)
9160/tcp open  cassandra syn-ack
```

## Enumeration

### Manual

```bash
pip install cqlsh
cqlsh <IP>
#Basic info enumeration
SELECT cluster_name, thrift_version, data_center, partitioner, native_protocol_version, rack, release_version from system.local;
#Keyspace enumeration
SELECT keyspace_name FROM system.schema_keyspaces;
desc <Keyspace_name>    #Decribe that DB
desc system_auth        #Describe the DB called system_auth
SELECT * from system_auth.roles;  #Retreive that info, can contain credential hashes
SELECT * from logdb.user_auth;    #Can contain credential hashes
SELECT * from logdb.user;
SELECT * from configuration."config";
```

### Automated

There aren't much options here and nmap doesn't obtain much info

```bash
nmap -sV --script cassandra-info -p <PORT> <IP>
```

### **Shodan**

`port:9160 Cluster`\
****`port:9042 "Invalid or unsupported protocol version"`
