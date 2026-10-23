<!--
# -------------------------------------------------------------------------------
# MachineAccountQuota query from The Hacker Recipes. Author: Charlie Bromberg (@_nwodtuhs)
# License: GPL-3.0, https://github.com/The-Hacker-Recipes/The-Hacker-Recipes
# Not Black Lantern Security work; see THIRD_PARTY_NOTICES.md.
# -------------------------------------------------------------------------------
-->
import ldap3

target_dn = "DC=domain,DC=local" # change this
domain = "domain" # change this
username = "username" # change this
password = "password" # change this

user = "{}\\{}".format(domain, username)
server = ldap3.Server(domain)
connection = ldap3.Connection(server = server, user = user, password = password, authentication = ldap3.NTLM)
connection.bind()
connection.search(target_dn,"(objectClass=*)", attributes=['ms-DS-MachineAccountQuota'])
print(connection.entries[0])