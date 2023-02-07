<!--
# -------------------------------------------------------------------------------
# Copyright: (c) BLS OPS LLC.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------------
-->
#!/usr/bin/env/python

import string
from exchangelib import DELEGATE, Account, Credentials, Configuration

credentials = Credentials('bob@evilcorp.com', 'Azerty.1')
config = Configuration(service_endpoint='https://outlook.office365.com/EWS/Exchange.asmx', credentials=credentials)
account = Account(primary_smtp_address='bob@evilcorp.com', config=config, autodiscover=False, access_type=DELEGATE)

#for item in account.inbox.all().order_by('-datetime_received')[:1]:
#    print(item.subject, item.sender, item.datetime_received)
f = open("all_users.txt", "a")
for i in list(string.ascii_lowercase):
    for mailbox, contact in account.protocol.resolve_names([i], return_full_contact_data=True):
        f.write(mailbox.email_address + "\n")
f.close()