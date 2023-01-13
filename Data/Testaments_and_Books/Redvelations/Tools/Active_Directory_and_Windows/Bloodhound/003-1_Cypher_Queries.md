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
# Cypher Queries

## Querying With Cypher Query Language

* <details><summary>Querying with Cypher Query Language (Click to expand)</summary><p>
	* Notes
		* Bloodhound uses the Cypher Query Language in order to conduct queries within the Neo4j database. 
		* You can use these sample queries if you want to look for specific users, computers, etc. within the Bloodhound Database:
* <details><summary>Query A User Within Bloodhound (Click to expand)</summary><p>

		MATCH (n) WHERE n.name =~ "(?i).*USERNAME_HERE.*" RETURN n LIMIT 10
* <details><summary>References (Click to expand)</summary><p>
	* [cptjesus intro to cypher](https://blog.cptjesus.com/posts/introtocypher)
	* [Hausec](https://hausec.com/2019/09/09/bloodhound-cypher-cheatsheet/)
	* [cypheroth list of queries](https://github.com/seajaysec/cypheroth.git)


## Cypher Query Examples
* Cypher is the query syntax for Neo4J, similar to SQL
* <details><summary>Cypher Query Examples (Click to expand)</summary><p>
	1. Find All Users with an SPN/Find all Kerberoastable Users

			MATCH (n:User)WHERE n.hasspn=true RETURN n
	1. Find All Users with an SPN/Find all Kerberoastable Users with passwords last set > 5 years ago

			MATCH (u:User) WHERE u.hasspn=true AND u.pwdlastset < (datetime().epochseconds - (1825 * 86400)) AND NOT u.pwdlastset IN [-1.0, 0.0] RETURN u.name, u.pwdlastset order by u.pwdlastset
	1. Find SPNs with keywords (swap SQL with whatever)

			MATCH (u:User) WHERE ANY (x IN u.serviceprincipalnames WHERE toUpper(x) CONTAINS 'SQL') RETURN u
	1. Kerberoastable Users with a path to DA

			MATCH (u:User {hasspn:true}) MATCH (g:Group {name:'DOMAIN ADMINS@<domain>.<tld>'}) MATCH p = shortestPath( (u)-[*1..]->(g) ) RETURN p
	1. Find workstations a user can RDP into.

			Match p=(g:Group)-[:CanRDP]->(c:Computer) where g.name STARTS WITH 'DOMAIN USERS' AND NOT c.operatingsystem CONTAINS ‘Server’ return p
	1. Find servers a user can RDP into.

			Match p=(g:Group)-[:CanRDP]->(c:Computer) where g.name STARTS WITH 'DOMAIN USERS' AND c.operatingsystem CONTAINS 'Server' return p
	1. All active DA sessions

			MATCH (n:User)-[:MemberOf]->(g:Group {name:'DOMAIN ADMINS@<domain>.<tld>'}) MATCH p = (c:Computer)-[:HasSession]->(n) return p
	1. DA sessions not on a certain group (e.g. domain controllers)

			OPTIONAL MATCH (c:Computer)-[:MemberOf]->(t:Group) WHERE NOT t.name = 'DOMAIN CONTROLLERS@<domain>.<tld>' WITH c as NonDC MATCH p=(NonDC)-[:HasSession]->(n:User)-[:MemberOf]->(g:Group {name:”DOMAIN ADMINS@<domain>.<tld>”}) RETURN DISTINCT (n.name) as Username, COUNT(DISTINCT(NonDC)) as Connexions ORDER BY COUNT(DISTINCT(NonDC)) DESC
	1. Find all computers with Unconstrained Delegation

			MATCH (c:Computer {unconstraineddelegation:true}) return c
	1. Find unsupported OSs

			MATCH (H:Computer) WHERE H.operatingsystem =~ '(?i).(2000|2003|2008|xp|vista|7|me).' RETURN H
	1. Find computers recently logged into (convert today into Windows epoch)

			Match (n:Computer) WHERE n.lastlogon > 1536449424 RETURN n
	1. Find users that logged in within the last 90 days. Change 90 to whatever threshold you want. (GUI Compatible)

			MATCH (u:User) WHERE u.lastlogon < (datetime().epochseconds - (90 * 86400)) and NOT u.lastlogon IN [-1.0, 0.0] RETURN u
	1. Find users with passwords last set within the last 90 days. Change 90 to whatever threshold you want. (GUI Compatible)

			MATCH (u:User) WHERE u.pwdlastset < (datetime().epochseconds - (90 * 86400)) and NOT u.pwdlastset IN [-1.0, 0.0] RETURN u
	1. View all GPOs

			Match (n:GPO) return n
	1. View all GPOs that contain a keyword

			Match (n:GPO) WHERE n.name CONTAINS "SERVER" return n
	1. View all groups that contain the word ‘admin’

			Match (n:Group) WHERE n.name CONTAINS "ADMIN" return n
	1. Find user that doesn’t require kerberos pre-authentication (aka AS-REP Roasting)

			MATCH (u:User {dontreqpreauth: true}) RETURN u
	1. Find a group with keywords. E.g. SQL ADMINS or SQL 2017 ADMINS

			MATCH (g:Group) WHERE g.name =~ '(?i).SQL.ADMIN.*' RETURN g
	1. Show all high value target group

			MATCH p=(n:User)-[r:MemberOf*1..]->(m:Group {highvalue:true}) RETURN p
	1. Find All Users with an SPN/Find all Kerberoastable Users with passwords last set > 5 years ago (In Console)

			MATCH (u:User) WHERE n.hasspn=true AND WHERE u.pwdlastset < (datetime().epochseconds - (1825 * 86400)) and NOT u.pwdlastset IN [-1.0, 0.0] RETURN u.name, u.pwdlastset order by u.pwdlastset
	1. Kerberoastable Users with most privileges

			MATCH (u:User {hasspn:true}) OPTIONAL MATCH (u)-[:AdminTo]->(c1:Computer) OPTIONAL MATCH (u)-[:MemberOf*1..]->(:Group)-[:AdminTo]->(c2:Computer) WITH u,COLLECT(c1) + COLLECT(c2) AS tempVar UNWIND tempVar AS comps RETURN u.name,COUNT(DISTINCT(comps)) ORDER BY COUNT(DISTINCT(comps)) DESC
	1. Find users that logged in within the last 90 days. Change 90 to whatever threshold you want. (In Console)

			MATCH (u:User) WHERE u.lastlogon < (datetime().epochseconds - (90 * 86400)) and NOT u.lastlogon IN [-1.0, 0.0] RETURN u.name, u.lastlogon order by u.lastlogon
	1. Find users with passwords last set thin the last 90 days. Change 90 to whatever threshold you want. (In Console)

			MATCH (u:User) WHERE u.pwdlastset < (datetime().epochseconds - (90 * 86400)) and NOT u.pwdlastset IN [-1.0, 0.0] RETURN u.name, u.pwdlastset order by u.pwdlastset
	1. Find constrained delegation (In Console)

			MATCH (u:User)-[:AllowedToDelegate]->(c:Computer) RETURN u.name,COUNT(c) ORDER BY COUNT(c) DESC
	1. View OUs based on member count. (In Console)

			MATCH (o:OU)-[:Contains]->(c:Computer) RETURN o.name,o.guid,COUNT(c) ORDER BY COUNT(c) DESC
	1. Return each OU that has a Windows Server in it (In Console)

			MATCH (o:OU)-[:Contains]->(c:Computer) WHERE toUpper(o.name) STARTS WITH "WINDOWS SERVER" RETURN o.name,c.name,c.operatingsystem
	1. Find computers that allow unconstrained delegation that AREN’T domain controllers. (In Console)

			MATCH (c1:Computer)-[:MemberOf*1..]->(g:Group) WHERE g.objectsid ENDS WITH '-516' WITH COLLECT(c1.name) AS domainControllers MATCH (c2:Computer {unconstraineddelegation:true}) WHERE NOT c2.name IN domainControllers RETURN c2.name,c2.operatingsystem ORDER BY c2.name ASC
	1. Find the number of principals with control of a “high value” asset where the principal itself does not belong to a “high value” group

			MATCH (n {highvalue:true}) OPTIONAL MATCH (m1)-[{isacl:true}]->(n) WHERE NOT (m1)-[:MemberOf*1..]->(:Group {highvalue:true}) OPTIONAL MATCH (m2)-[:MemberOf*1..]->(:Group)-[{isacl:true}]->(n) WHERE NOT (m2)-[:MemberOf*1..]->(:Group {highvalue:true}) WITH n,COLLECT(m1) + COLLECT(m2) AS tempVar UNWIND tempVar AS controllers RETURN n.name,COUNT(DISTINCT(controllers)) ORDER BY COUNT(DISTINCT(controllers)) DESC
	1. Enumerate all properties (In Console)

			Match (n:Computer) return properties(n)
	1. Match users that are not AdminCount 1, have generic all, and no local admin

			MATCH (u:User)-[:GenericAll]->(c:Computer) WHERE  NOT u.admincount AND NOT (u)-[:AdminTo]->(c) RETURN u.name, c.name
	1. What permissions does Everyone/Authenticated users/Domain users/Domain computers have”

			MATCH p=(m:Group)- [r:AddMember|AdminTo|AllExtendedRights|AllowedToDelegate|CanRDP|Contains|ExecuteDCOM|ForceChangePassword|GenericAll|GenericWrite|GetChanges|GetChangesAll|HasSession|Owns|ReadLAPSPassword|SQLAdmin|TrustedBy|WriteDACL|WriteOwner|AddAllowedToAct|AllowedToAct]->(t) WHERE m.objectsid ENDS WITH '-513' OR m.objectsid ENDS WITH '-515' OR m.objectsid ENDS WITH 'S-1-5-11' OR m.objectsid ENDS WITH 'S-1-1-0' RETURN m.name,TYPE(r),t.name,t.enabled
	1. Find computers with descriptions and display them (along with the description, sometimes admins save sensitive data on domain objects descriptions like passwords):

			MATCH (c:Computer) WHERE c.description IS NOT NULL RETURN c.name,c.description
	1. Return the name of every computer in the database where at least one SPN for the computer contains the string “MSSQL”:

			MATCH (c:Computer) WHERE ANY (x IN c.serviceprincipalnames WHERE toUpper(x) CONTAINS 'MSSQL') RETURN c.name,c.serviceprincipalnames ORDER BY c.name ASC
	1. Find any computer that is NOT a domain controller and it is trusted to perform unconstrained delegation:

			MATCH (c1:Computer)-[:MemberOf*1..]->(g:Group) WHERE g.objectsid ENDS WITH '-516' WITH COLLECT(c1.name) AS domainControllers MATCH (c2:Computer {unconstraineddelegation:true}) WHERE NOT c2.name IN domainControllers RETURN c2.name,c2.operatingsystem ORDER BY c2.name ASC
	1. Or alternatively, show machines that allow unconstrained delegation and that aren’t DCs:

			MATCH (c:Computer)-[:MemberOf]->(g1:Group {name:'DOMAIN CONTROLLERS@DOMAIN.GR'}) WITH collect(distinct c) as DC MATCH (c1:Computer) WHERE NOT c1 in DC WITH DISTINCT(c1) AS NonDC MATCH (NonDC {unconstraineddelegation:true}) RETURN DISTINCT(NonDC.name) ORDER BY NonDC.name
	1. Find every computer account that has local admin rights on other computers. Return in descending order of the number of computers the computer account has local admin rights to:

			MATCH (c1:Computer) OPTIONAL MATCH (c1)-[:AdminTo]->(c2:Computer) OPTIONAL MATCH (c1)-[:MemberOf*1..]->(:Group)-[:AdminTo]->(c3:Computer) WITH COLLECT(c2) + COLLECT(c3) AS tempVar,c1 UNWIND tempVar AS computers RETURN c1.name AS COMPUTER,COUNT(DISTINCT(computers)) AS ADMIN_TO_COMPUTERS ORDER BY COUNT(DISTINCT(computers)) DESC
	1. Alternatively, find every computer that has local admin rights on other computers and display these computers:

			MATCH (c1:Computer) OPTIONAL MATCH (c1)-[:AdminTo]->(c2:Computer) OPTIONAL MATCH (c1)-[:MemberOf*1..]->(:Group)-[:AdminTo]->(c3:Computer) WITH COLLECT(c2) + COLLECT(c3) AS tempVar,c1 UNWIND tempVar AS computers RETURN c1.name AS COMPUTER,COLLECT(DISTINCT(computers.name)) AS ADMIN_TO_COMPUTERS ORDER BY c1.name
	1. Get the names of the computers without admins, sorted by alphabetic order:

			MATCH (n)-[r:AdminTo]->(c:Computer) WITH COLLECT(c.name) as compsWithAdmins MATCH (c2:Computer) WHERE NOT c2.name in compsWithAdmins RETURN c2.name ORDER BY c2.name ASC
	1. Show computers (excluding Domain Controllers) where Domain Admins are logged in:

			MATCH (n:User)-[:MemberOf*1..]->(g:Group {name:'DOMAIN ADMINS@DOMAIN.GR'}) WITH n as privusers 
	1. Find the percentage of computers with path to Domain Admins:

			MATCH (totalComputers:Computer {domain:'DOMAIN.GR'}) MATCH p=shortestPath((ComputersWithPath:Computer {domain:'DOMAIN.GR'})-[r*1..]->(g:Group {name:'DOMAIN ADMINS@DOMAIN.GR'})) WITH COUNT(DISTINCT(totalComputers)) as totalComputers, COUNT(DISTINCT(ComputersWithPath)) as ComputersWithPath RETURN 100.0 * ComputersWithPath / totalComputers AS percentComputersToDA
	1. Find on each computer who can RDP (searching only enabled users):

			MATCH (c:Computer) OPTIONAL MATCH (u:User)-[:CanRDP]->(c) WHERE u.enabled=true OPTIONAL MATCH (u1:User)-[:MemberOf*1..]->(:Group)-[:CanRDP]->(c) where u1.enabled=true WITH COLLECT(u) + COLLECT(u1) as tempVar,c UNWIND tempVar as users RETURN c.name AS COMPUTER,COLLECT(DISTINCT(users.name)) as USERS ORDER BY USERS desc
	1. Find on each computer the number of users with admin rights (local admins) and display the users with admin rights:

			MATCH (c:Computer) OPTIONAL MATCH (u1:User)-[:AdminTo]->(c) OPTIONAL MATCH (u2:User)-[:MemberOf*1..]->(:Group)-[:AdminTo]->(c) WITH COLLECT(u1) + COLLECT(u2) AS TempVar,c UNWIND TempVar AS Admins RETURN c.name AS COMPUTER, COUNT(DISTINCT(Admins)) AS ADMIN_COUNT,COLLECT(DISTINCT(Admins.name)) AS USERS ORDER BY ADMIN_COUNT DESC
	1. Account Operators: Active Directory group with default privileged rights on domain users and groups, plus the ability to logon to Domain Controllers

			MATCH (u:User)-[r1:MemberOf*1..]->(g1:Group {name:'ACCOUNT OPERATORS@DOMAIN.GR'}) RETURN u.name
	1. Server Operators: Members in the Server Operators group can administer domain servers. Memebers of the Server Operators group can sign in to a server interactively, create and delete network shared resources, start and stop services, back up and restore files, format the hard disk drive of the computer, and shut down the computer.

			MATCH (u:User)-[r1:MemberOf*1..]->(g1:Group {name:'SERVER OPERATORS@DOMAIN.GR'}) RETURN u.name
	1. Backup Operators: Local or Active Directory group. AD group members can backup or restore Active Directory and have logon rights to Domain Controllers (default).

			MATCH (u:User)-[r1:MemberOf*1..]->(g1:Group {name:'BACKUP OPERATORS@DOMAIN.GR'}) RETURN u.name
	1. Allowed RODC Password Replication Group: Active Directory group where members can have their domain password cached on a RODC after successfully authenticating (includes user and computer accounts).

			MATCH (u:User)-[r1:MemberOf*1..]->(g1:Group {name:'ALLOWED RODC PASSWORD REPLICATION GROUP@DOMAIN.GR'}) RETURN u.name
	1. CERTIFICATE SERVICE DCOM ACCESS: Members of this group are allowed to connect to certification authorities in the enterprise.

			MATCH (u:User)-[r1:MemberOf*1..]->(g1:Group {name:'CERTIFICATE SERVICE DCOM ACCESS@DOMAIN.GR'}) RETURN u.name
	1. Cert Publishers: Members of the Cert Publishers group are authorized to publish certificates for User objects in Active Directory.

			MATCH (u:User)-[r1:MemberOf*1..]->(g1:Group {name:'CERT PUBLISHERS@DOMAIN.GR'}) RETURN u.name
	1. Distributed COM Users: Members of the Distributed COM Users group are allowed to launch, activate, and use Distributed COM objects on the computer.

			MATCH (u:User)-[r1:MemberOf*1..]->(g1:Group {name:'DISTRIBUTED COM USERS@DOMAIN.GR'}) RETURN u.name
	1. DnsAdmins: Local or Active Directory group. Members of this group have admin rights to AD DNS and can run code via DLL on a Domain Controller operating as a DNS server.

			MATCH (u:User)-[r1:MemberOf*1..]->(g1:Group {name:'DNSADMINS@DOMAIN.GR'}) RETURN u.name
	1. Event Log Readers: Members of this group can read event logs from local computers. 

			MATCH (u:User)-[r1:MemberOf*1..]->(g1:Group {name:'EVENT LOG READERS@DOMAIN.GR'}) RETURN u.name
	1. GROUP POLICY CREATOR OWNERS@DOMAIN.GR: Active Directory group with the ability to create Group Policies in the domain. This group is authorized to create, edit, or delete Group Policy Objects in the domain. By default, the only member of the group is Administrator.

			MATCH (u:User)-[r1:MemberOf*1..]->(g1:Group {name:'GROUP POLICY CREATOR OWNERS@DOMAIN.GR'}) RETURN u.name
	1. Hyper-V Administrators: Members of the Hyper-V Administrators group have complete and unrestricted access to all the features in Hyper-V.

			MATCH (u:User)-[r1:MemberOf*1..]->(g1:Group {name:'HYPER-V ADMINISTRATORS@DOMAIN.GR'}) RETURN u.name
	1. Pre–Windows 2000 Compatible Access: Members of the Pre–Windows 2000 Compatible Access group have Read access for all users and groups in the domain. This group is provided for backward compatibility for computers running Windows NT 4.0 and earlier. 

			MATCH (u:User)-[r1:MemberOf*1..]->(g1:Group {name:'PRE-WINDOWS 2000 COMPATIBLE ACCESS@DOMAIN.GR'}) RETURN u.name
	1. Print Operators: Members of this group can manage, create, share, and delete printers that are connected to domain controllers in the domain. They can also manage Active Directory printer objects in the domain. Members of this group can locally sign in to and shut down domain controllers in the domain. This group has no default members. Because members of this group can load and unload device drivers on all domain controllers in the domain, add users with caution.

			MATCH (u:User)-[r1:MemberOf*1..]->(g1:Group {name:'PRINT OPERATORS@DOMAIN.GR'}) RETURN u.name
	1. Remote Desktop Users: The Remote Desktop Users group on an RD Session Host server is used to grant users and groups permissions to remotely connect to an RD Session Host server. 

			MATCH (u:User)-[r1:MemberOf*1..]->(g1:Group {name:'REMOTE DESKTOP USERS@DOMAIN.GR'}) RETURN u.name
	1. Schema Admins: Members of the Schema Admins group can modify the Active Directory schema. This group exists only in the root domain of an Active Directory forest of domains. The group is authorized to make schema changes in Active Directory. By default, the only member of the group is the Administrator account for the forest root domain. This group has full administrative access to the schema.

			MATCH (u:User)-[r1:MemberOf*1..]->(g1:Group {name:'SCHEMA ADMINS@DOMAIN.GR'}) RETURN u.name
	1. Find groups that contain both users and computers:

			MATCH (c:Computer)-[r:MemberOf*1..]->(groupsWithComps:Group) WITH groupsWithComps MATCH (u:User)-[r:MemberOf*1..]->(groupsWithComps) RETURN DISTINCT(groupsWithComps) as groupsWithCompsAndUsers
	1. Find which domain Groups are Admins to what computers:

			MATCH (g:Group) OPTIONAL MATCH (g)-[:AdminTo]->(c1:Computer) OPTIONAL MATCH (g)-[:MemberOf*1..]->(:Group)-[:AdminTo]->(c2:Computer) WITH g, COLLECT(c1) + COLLECT(c2) AS tempVar UNWIND tempVar AS computers RETURN g.name AS GROUP, COLLECT(computers.name) AS AdminRights
	1. Find which domain Groups (excluding the Domain Admins and Enterprise Admins) are Admins to what computers:

			MATCH (g:Group) WHERE NOT (g.name =~ '(?i)domain admins@.*' OR g.name =~ "(?i)enterprise admins@.*") OPTIONAL MATCH (g)-[:AdminTo]->(c1:Computer) OPTIONAL MATCH (g)-[:MemberOf*1..]->(:Group)-[:AdminTo]->(c2:Computer) WITH g, COLLECT(c1) + COLLECT(c2) AS tempVar UNWIND tempVar AS computers RETURN g.name AS GROUP, COLLECT(computers.name) AS AdminRights
	1. Find which domain Groups (excluding the high privileged groups marked with AdminCount=true) are Admins to what computers:

			MATCH (g:Group) WHERE g.admincount=false OPTIONAL MATCH (g)-[:AdminTo]->(c1:Computer) OPTIONAL MATCH (g)-[:MemberOf*1..]->(:Group)-[:AdminTo]->(c2:Computer) WITH g, COLLECT(c1) + COLLECT(c2) AS tempVar UNWIND tempVar AS computers RETURN g.name AS GROUP, COLLECT(computers.name) AS AdminRights
	1. Find the most privileged groups on the domain (groups that are Admins to Computers. Nested groups will be calculated):

			MATCH (g:Group) OPTIONAL MATCH (g)-[:AdminTo]->(c1:Computer) OPTIONAL MATCH (g)-[:MemberOf*1..]->(:Group)-[:AdminTo]->(c2:Computer) WITH g, COLLECT(c1) + COLLECT(c2) AS tempVar UNWIND tempVar AS computers RETURN g.name AS GroupName,COUNT(DISTINCT(computers)) AS AdminRightCount ORDER BY AdminRightCount DESC
	1. Find the number of computers that do not have local Admins:

			MATCH (n)-[r:AdminTo]->(c:Computer) WITH COLLECT(c.name) as compsWithAdmins MATCH (c2:Computer) WHERE NOT c2.name in compsWithAdmins RETURN COUNT(c2)
	1. Find groups with most local admins (either explicit admins or derivative/unrolled):

			MATCH (g:Group) WITH g OPTIONAL MATCH (g)-[r:AdminTo]->(c1:Computer) WITH g,COUNT(c1) as explicitAdmins OPTIONAL MATCH (g)-[r:MemberOf*1..]->(a:Group)-[r2:AdminTo]->(c2:Computer) WITH g,explicitAdmins,COUNT(DISTINCT(c2)) as unrolledAdmins RETURN g.name,explicitAdmins,unrolledAdmins, explicitAdmins + unrolledAdmins as totalAdmins ORDER BY totalAdmins DESC
	1. Find percentage of non-privileged groups (based on admincount:false) to Domain Admins group:

			MATCH (totalGroups:Group {admincount:false}) MATCH p=shortestPath((GroupsWithPath:Group {admincount:false})-[r*1..]->(g:Group {name:'DOMAIN ADMINS@DOMAIN.GR'})) WITH COUNT(DISTINCT(totalGroups)) as totalGroups, COUNT(DISTINCT(GroupsWithPath)) as GroupsWithPath RETURN 100.0 * GroupsWithPath / totalGroups AS percentGroupsToDA
	1. Find every user object where the “userpassword” attribute is populated (wald0):

			MATCH (u:User) WHERE NOT u.userpassword IS null RETURN u.name,u.userpassword
	1. Find every user that doesn’t require kerberos pre-authentication (wald0):

			MATCH (u:User {dontreqpreauth: true}) RETURN u.name
	1. Find all users trusted to perform constrained delegation. The result is ordered by the amount of computers:

			MATCH (u:User)-[:AllowedToDelegate]->(c:Computer) RETURN u.name,COUNT(c) ORDER BY COUNT(c) DESC
	1. Find the active sessions that a specific domain user has on all domain computers:

			MATCH p1=shortestPath(((u1:User {name:'USER@DOMAIN.GR'})-[r1:MemberOf*1..]->(g1:Group))) MATCH (c:Computer)-[r:HasSession*1..]->(u1) RETURN DISTINCT(u1.name) as users, c.name as computers ORDER BY computers
	1. Count the number of the computers where each domain user has direct Admin privileges to:

			MATCH (u:User)-[:AdminTo]->(c:Computer) RETURN count(DISTINCT(c.name)) AS COMPUTER, u.name AS USER ORDER BY count(DISTINCT(c.name)) DESC
	1. Count the number of the computers where each domain user has derivative Admin privileges to:

			MATCH (u:User)-[:MemberOf*1..]->(:Group)-[:AdminTo]->(c:Computer) RETURN count(DISTINCT(c.name)) AS COMPUTER, u.name AS USER ORDER BY u.name
	1. Display the computer names where each domain user has derivative Admin privileges to:

			MATCH (u:User)-[:MemberOf*1..]->(:Group)-[:AdminTo]->(c:Computer) RETURN DISTINCT(c.name) AS COMPUTER, u.name AS USER ORDER BY u.name
	1. Find Kerberoastable users who are members of high value groups:

			MATCH (u:User)-[r:MemberOf*1..]->(g:Group) WHERE g.highvalue=true AND u.hasspn=true RETURN u.name AS USER
	1. Find Kerberoastable users and where they are AdminTo:

			OPTIONAL MATCH (u1:User) WHERE u1.hasspn=true OPTIONAL MATCH (u1)-[r:AdminTo]->(c:Computer) RETURN u1.name AS user_with_spn,c.name AS local_admin_to
	1. Find the percentage of users with a path to Domain Admins:

			MATCH (totalUsers:User {domain:'DOMAIN.GR'}) MATCH p=shortestPath((UsersWithPath:User {domain:'DOMAIN.GR'})-[r*1..]->(g:Group {name:'DOMAIN ADMINS@DOMAIN.GR'})) WITH COUNT(DISTINCT(totalUsers)) as totalUsers, COUNT(DISTINCT(UsersWithPath)) as UsersWithPath RETURN 100.0 * UsersWithPath / totalUsers AS percentUsersToDA
	1. Find the percentage of enabled users that have a path to high value groups:

			MATCH (u:User {domain:'DOMAIN.GR',enabled:True}) MATCH (g:Group {domain:'DOMAIN.GR'}) WHERE g.highvalue = True WITH g, COUNT(u) as userCount MATCH p = shortestPath((u:User {domain:'DOMAIN.GR',enabled:True})-[*1..]->(g)) RETURN 100.0 * COUNT(distinct u) / userCount
	1. List of unique users with a path to a Group tagged as “highvalue”:

			MATCH (u:User) MATCH (g:Group {highvalue:true}) MATCH p = shortestPath((u:User)-[r:AddMember|AdminTo|AllExtendedRights|AllowedToDelegate|CanRDP|Contains|ExecuteDCOM|ForceChangePassword|GenericAll|GenericWrite|GpLink|HasSession|MemberOf|Owns|ReadLAPSPassword|TrustedBy|WriteDacl|WriteOwner|GetChanges|GetChangesAll*1..]->(g)) RETURN DISTINCT(u.name) AS USER, u.enabled as ENABLED,count(p) as PATHS order by u.name
	1. Find users who are NOT marked as “Sensitive and Cannot Be Delegated” and have Administrative access to a computer, and where those users have sessions on servers with Unconstrained Delegation enabled (by NotMedic):

			MATCH (u:User {sensitive:false})-[:MemberOf*1..]->(:Group)-[:AdminTo]->(c1:Computer) WITH u,c1 MATCH (c2:Computer {unconstraineddelegation:true})-[:HasSession]->(u) RETURN u.name AS user,COLLECT(DISTINCT(c1.name)) AS AdminTo,COLLECT(DISTINCT(c2.name)) AS TicketLocation ORDER BY user ASC
	1. Find users with constrained delegation permissions and the corresponding targets where they allowed to delegate:

			MATCH (u:User) WHERE u.allowedtodelegate IS NOT NULL RETURN u.name,u.allowedtodelegate
	1. Alternatively, search for users with constrained delegation permissions,the corresponding targets where they are allowed to delegate, the privileged users that can be impersonated (based on sensitive:false and admincount:true) and find where these users (with constrained deleg privs) have active sessions (user hunting) as well as count the shortest paths to them:

			OPTIONAL MATCH (u:User {sensitive:false, admincount:true}) WITH u.name AS POSSIBLE_TARGETS OPTIONAL MATCH (n:User) WHERE n.allowedtodelegate IS NOT NULL WITH n AS USER_WITH_DELEG, n.allowedtodelegate as DELEGATE_TO, POSSIBLE_TARGETS OPTIONAL MATCH (c:Computer)-[:HasSession]->(USER_WITH_DELEG) WITH USER_WITH_DELEG,DELEGATE_TO,POSSIBLE_TARGETS,c.name AS USER_WITH_DELEG_HAS_SESSION_TO OPTIONAL MATCH p=shortestPath((o)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct*1..]->(USER_WITH_DELEG)) WHERE NOT o=USER_WITH_DELEG WITH USER_WITH_DELEG,DELEGATE_TO,POSSIBLE_TARGETS,USER_WITH_DELEG_HAS_SESSION_TO,p RETURN USER_WITH_DELEG.name AS USER_WITH_DELEG, DELEGATE_TO, COLLECT(DISTINCT(USER_WITH_DELEG_HAS_SESSION_TO)) AS USER_WITH_DELEG_HAS_SESSION_TO, COLLECT(DISTINCT(POSSIBLE_TARGETS)) AS PRIVILEGED_USERS_TO_IMPERSONATE, COUNT(DISTINCT(p)) AS PATHS_TO_USER_WITH_DELEG
	1. Find computers with constrained delegation permissions and the corresponding targets where they allowed to delegate:

			MATCH (c:Computer) WHERE c.allowedtodelegate IS NOT NULL RETURN c.name,c.allowedtodelegate
	1. Alternatively, search for computers with constrained delegation permissions, the corresponding targets where they are allowed to delegate, the privileged users that can be impersonated (based on sensitive:false and admincount:true) and find who is LocalAdmin on these computers as well as count the shortest paths to them:

			OPTIONAL MATCH (u:User {sensitive:false, admincount:true}) WITH u.name AS POSSIBLE_TARGETS OPTIONAL MATCH (n:Computer) WHERE n.allowedtodelegate IS NOT NULL WITH n AS COMPUTERS_WITH_DELEG, n.allowedtodelegate as DELEGATE_TO, POSSIBLE_TARGETS OPTIONAL MATCH (u1:User)-[:AdminTo]->(COMPUTERS_WITH_DELEG) WITH u1 AS DIRECT_ADMINS,POSSIBLE_TARGETS,COMPUTERS_WITH_DELEG,DELEGATE_TO OPTIONAL MATCH (u2:User)-[:MemberOf*1..]->(:Group)-[:AdminTo]->(COMPUTERS_WITH_DELEG) WITH COLLECT(DIRECT_ADMINS) + COLLECT(u2) AS TempVar,COMPUTERS_WITH_DELEG,DELEGATE_TO,POSSIBLE_TARGETS UNWIND TempVar AS LOCAL_ADMINS OPTIONAL MATCH p=shortestPath((o)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct*1..]->(COMPUTERS_WITH_DELEG)) WHERE NOT o=COMPUTERS_WITH_DELEG WITH COMPUTERS_WITH_DELEG,DELEGATE_TO,POSSIBLE_TARGETS,p,LOCAL_ADMINS RETURN COMPUTERS_WITH_DELEG.name AS COMPUTERS_WITH_DELG, LOCAL_ADMINS.name AS LOCAL_ADMINS_TO_COMPUTERS_WITH_DELG, DELEGATE_TO, COLLECT(DISTINCT(POSSIBLE_TARGETS)) AS PRIVILEGED_USERS_TO_IMPERSONATE, COUNT(DISTINCT(p)) AS PATHS_TO_USER_WITH_DELEG
	1. Find if any domain user has interesting permissions against a GPO:

			MATCH p=(u:User)-[r:AllExtendedRights|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|GpLink*1..]->(g:GPO) RETURN p LIMIT 25
	1. Shortest paths to Domain Admins group from computers:

			MATCH (n:Computer),(m:Group {name:'DOMAIN ADMINS@DOMAIN.GR'}),p=shortestPath((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct*1..]->(m)) RETURN p
	1. Shortest paths to Domain Admins group from computers excluding potential DCs (based on ldap/ and GC/ spns):

			WITH '(?i)ldap/.*' as regex_one WITH '(?i)gc/.*' as regex_two MATCH (n:Computer) WHERE NOT ANY(item IN n.serviceprincipalnames WHERE item =~ regex_two OR item =~ regex_two ) MATCH(m:Group {name:"DOMAIN ADMINS@DOMAIN.GR"}),p=shortestPath((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct*1..]->(m)) RETURN p
	1. Shortest paths to Domain Admins group from all domain groups (fix-it):

			MATCH (n:Group),(m:Group {name:'DOMAIN ADMINS@DOMAIN.GR'}),p=shortestPath((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct*1..]->(m)) RETURN p
	1. Shortest paths to Domain Admins group from non-privileged groups (AdminCount=false)

			MATCH (n:Group {admincount:false}),(m:Group {name:'DOMAIN ADMINS@DOMAIN.GR'}),p=shortestPath((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct*1..]->(m)) RETURN p
	1. Shortest paths to Domain Admins group from the Domain Users group:

			MATCH (g:Group) WHERE g.name =~ 'DOMAIN USERS@.*' MATCH (g1:Group) WHERE g1.name =~ 'DOMAIN ADMINS@.*' OPTIONAL MATCH p=shortestPath((g)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct|SQLAdmin*1..]->(g1)) RETURN p
	1. Find interesting privileges/ACEs that have been configured to DOMAIN USERS group:

			MATCH (m:Group) WHERE m.name =~ 'DOMAIN USERS@.*' MATCH p=(m)-[r:Owns|:WriteDacl|:GenericAll|:WriteOwner|:ExecuteDCOM|:GenericWrite|:AllowedToDelegate|:ForceChangePassword]->(n:Computer) RETURN p
	1. Shortest paths to Domain Admins group from non privileged users (AdminCount=false):

			MATCH (n:User {admincount:false}),(m:Group {name:'DOMAIN ADMINS@DOMAIN.GR'}),p=shortestPath((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct*1..]->(m)) RETURN p
	1. Find all Edges that a specific user has against all the nodes (HasSession is not calculated, as it is an edge that comes from computer to user, not from user to computer):

			MATCH (n:User) WHERE n.name =~ 'HELPDESK@DOMAIN.GR'MATCH (m) WHERE NOT m.name = n.name MATCH p=allShortestPaths((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct|SQLAdmin*1..]->(m)) RETURN p
	1. Find all the Edges that any UNPRIVILEGED user (based on the admincount:False) has against all the nodes:

			MATCH (n:User {admincount:False}) MATCH (m) WHERE NOT m.name = n.name MATCH p=allShortestPaths((n)-[r:MemberOf|HasSession|AdminTo|AllExtendedRights|AddMember|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|CanRDP|ExecuteDCOM|AllowedToDelegate|ReadLAPSPassword|Contains|GpLink|AddAllowedToAct|AllowedToAct|SQLAdmin*1..]->(m)) RETURN p
	1. Find interesting edges related to “ACL Abuse” that uprivileged users have against other users:

			MATCH (n:User {admincount:False}) MATCH (m:User) WHERE NOT m.name = n.name MATCH p=allShortestPaths((n)-[r:AllExtendedRights|ForceChangePassword|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner*1..]->(m)) RETURN p
	1. Find interesting edges related to “ACL Abuse” that unprivileged users have against computers:

			MATCH (n:User {admincount:False}) MATCH p=allShortestPaths((n)-[r:AllExtendedRights|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|AdminTo|CanRDP|ExecuteDCOM|ForceChangePassword*1..]->(m:Computer)) RETURN p
	1. Find if unprivileged users have rights to add members into groups:

			MATCH (n:User {admincount:False}) MATCH p=allShortestPaths((n)-[r:AddMember*1..]->(m:Group)) RETURN p
	1. Find the active user sessions on all domain computers:

			MATCH p1=shortestPath(((u1:User)-[r1:MemberOf*1..]->(g1:Group))) MATCH p2=(c:Computer)-[*1]->(u1) RETURN p2
	1. Find all the privileges (edges) of the domain users against the domain computers (e.g. CanRDP, AdminTo etc. HasSession edge is not included):

			MATCH p1=shortestPath(((u1:User)-[r1:MemberOf*1..]->(g1:Group))) MATCH p2=(u1)-[*1]->(c:Computer) RETURN p2
	1. Find only the AdminTo privileges (edges) of the domain users against the domain computers:

			MATCH p1=shortestPath(((u1:User)-[r1:MemberOf*1..]->(g1:Group))) MATCH p2=(u1)-[:AdminTo*1..]->(c:Computer) RETURN p2
	1. Find only the CanRDP privileges (edges) of the domain users against the domain computers:

			MATCH p1=shortestPath(((u1:User)-[r1:MemberOf*1..]->(g1:Group))) MATCH p2=(u1)-[:CanRDP*1..]->(c:Computer) RETURN p2
	1. Display in BH a specific user with constrained deleg and his targets where he allowed to delegate:

			MATCH (u:User {name:'USER@DOMAIN.GR'}),(c:Computer),p=((u)-[r:AllowedToDelegate]->(c)) RETURN p
	1. Show me all the sessions from the users in the OU with the following GUID

			MATCH p=(o:OU {guid:'045939B4-3FA8-4735-YU15-7D61CFOU6500'})-[r:Contains*1..]->(u:User) MATCH (c:Computer)-[rel:HasSession]->(u) return u.name,c.name
	1. Creating a property on the users that have an actual path to anything high_value(heavy query. takes hours on a large dataset)

			MATCH (u:User) MATCH (g:Group {highvalue: true}) MATCH p = shortestPath((u:User)-[r:AddMember|AdminTo|AllExtendedRights|AllowedToDelegate|CanRDP|Contains|ExecuteDCOM|ForceChangePassword|GenericAll|GenericWrite|GetChangesAll|GpLink|HasSession|MemberOf|Owns|ReadLAPSPassword|SQLAdmin|TrustedBy|WriteDacl|WriteOwner|AddAllowedToAct|AllowedToAct*1..]->(g)) SET u.has_path_to_da =true
	1. What “user with a path to any high_value group” has most sessions?

			MATCH (c:Computer)-[rel:HasSession]->(u:User {has_path_to_da: true}) WITH COLLECT(c) as tempVar,u UNWIND tempVar as sessions WITH u,COUNT(DISTINCT(sessions)) as sessionCount RETURN u.name,u.displayname,sessionCount ORDER BY sessionCount desc
	1. Creating a property for Tier 1 Users with regex:

			MATCH (u:User) WHERE u.name =~ 'internal_naming_convention[0-9]{2,5}@EXAMPLE.LOCAL' SET u.tier_1_user = true
	1. Creating a property for Tier 1 Computers via group-membership:

			MATCH (c:Computer)-[r:MemberOf*1..]-(g:Group {name:'ALL_SERVERS@EXAMPLE.LOCAL'}) SET c.tier_1_computer = true
	1. Creating a property for Tier 2 Users via group name and an exclusion:

			MATCH (u:User)-[r:MemberOf*1..]-(g:Group)WHERE g.name CONTAINS  'ALL EMPLOYEES' AND NOT u.name contains 'TEST' SET u.tier_2_user = true
	1. Creating a property for Tier 2 Computers via nested groups name:

			MATCH (c:Computer)-[r:MemberOf*1..]-(g:Group) WHERE g.name STARTS WITH 'CLIENT_' SET c.tier_2_computer = true
	1. List Tier 2 access to Tier 1 Computers

			MATCH (u)-[rel:AddMember|AdminTo|AllowedToDelegate|CanRDP|ExecuteDCOM|ForceChangePassword|GenericAll|GenericWrite|GetChangesAll|HasSession|Owns|ReadLAPSPassword|SQLAdmin|TrustedBy|WriteDACL|WriteOwner|AddAllowedToAct|AllowedToAct|MemberOf|AllExtendedRights]->(c:Computer) WHERE u.tier_2_user = true AND c.tier_1_computer = true RETURN u.name,TYPE(rel),c.name,labels(c)
	1. List Tier 1 Sessions on Tier 2 Computers

			MATCH (c:Computer)-[rel:HasSession]->(u:User) WHERE u.tier_1_user = true AND c.tier_2_computer = true RETURN u.name,u.displayname,TYPE(rel),c.name,labels(c),c.enabled
	1. List all users with local admin and count how many instances (variation of Waldo’s computer query) 

			OPTIONAL MATCH (c1)-[:AdminTo]->(c2:Computer) OPTIONAL MATCH (c1)-[:MemberOf*1..]->(:Group)-[:AdminTo]->(c3:Computer) WITH COLLECT(c2) + COLLECT(c3) AS tempVar,c1 UNWIND tempVar AS computers RETURN c1.name,COUNT(DISTINCT(computers)) ORDER BY COUNT(DISTINCT(computers)) DESC
	1. Find all users within a VPN group

			Match (u:User)-[:MemberOf]->(g:Group) WHERE g.name CONTAINS "VPN" return u.name,g.name
