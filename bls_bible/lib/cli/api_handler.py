# -------------------------------------------------------------------------------
# Copyright:   (c) BLS OPS LLC.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------------
# api_handler.py

import os
import requests
import json
import datetime
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class api_handler:
	def __init__(self, bls_bible_server):

		self.bls_bible_server = bls_bible_server
		self.headers = None #'bls-bible-api-key'

	def api_handler_wrapper(self, endpoint, method, data, list=None):

		#print(self.bls_bible_server + endpoint)
		#print(self.headers)
		#print(data)

		if method == 'get':

			if list == 'list':

				response = requests.get(self.bls_bible_server + endpoint, verify=False, headers=self.headers)

			else:

				response = requests.get(self.bls_bible_server + endpoint, verify=False, headers=self.headers, json=data)

		elif method == 'put':

			response = requests.put(self.bls_bible_server + endpoint, verify=False, headers=self.headers, json=data)

		elif method == 'post':

			response = requests.post(self.bls_bible_server + endpoint, verify=False, headers=self.headers, json=data)

		elif method == 'delete':

			response = requests.delete(self.bls_bible_server + endpoint, verify=False, headers=self.headers, json=data)

		try:

			response_json = json.loads(response.text)
			return response_json

		except Exception as e:

			return e

	def threat_profile_list_api_handler(self):

		endpoint = '/threat_profile'
		method = 'get'
		data = None

		return self.api_handler_wrapper(endpoint, method, data, 'list')

	def threat_profile_api_handler(self, id, method='get'):

		endpoint = '/threat_profile/' + id
		method_options = ['get','put','post','delete']

		if method not in method_options:

			print("Invalid method. Exiting.")
			exit()

		data = None

		return self.api_handler_wrapper(endpoint, method, data)

	def ttp_list_api_handler(self):

		endpoint = '/threat_profile'
		method = 'get'
		data = None

		return self.api_handler_wrapper(endpoint, method, data)

	def ttp_api_handler(self, id, method='get'):

		endpoint = '/threat_profile/' + id
		method_options = ['get','put','post','delete']

		if method not in method_options:

			print("Invalid method. Exiting.")
			exit()

		data = None

		return self.api_handler_wrapper(endpoint, method, data)

	def proxy_list_api_handler(self):

		endpoint = '/threat_profile'
		method = 'get'
		data = None

		return self.api_handler_wrapper(endpoint, method, data)

	def proxy_api_handler(self, id, method='get'):

		endpoint = '/threat_profile/' + id
		method_options = ['get','put','post','delete']

		if method not in method_options:

			print("Invalid method. Exiting.")
			exit()

		data = None

		return self.api_handler_wrapper(endpoint, method, data)
