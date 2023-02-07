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
# app_ops.py

from bls_bible.lib.service import BibleService
from flask import request, send_file
import json
import os


class app_ops:
	def __init__(self, app):

		self.Bs = BibleService()
		self.app = app

	def app_ops_content(self):

		# update functions

		@self.app.route('/update')
		def update():
			return self.app.send_static_file('update.html')

		@self.app.route('/_update')
		def get_update():
			response = ''
			content = search = reverse = apts = attack = False
			if request.args.get('content') == "true":
				content = True
			if request.args.get('search') == "true":
				search = True
			if request.args.get('reverse') == "true":
				reverse = True
			if request.args.get('apts') == "true":
				apts = True
			if request.args.get('attack') == "true":
				attack = True

			if content:
				self.Bs.update_json_file()
			if search:
				self.Bs.fileIndexer()
			if reverse:
				self.Bs.get_reverse_references()

			if apts:
				try:
					self.Bs.downloadMitreGroups()
				except Exception:
					response += 'Issue downloading APTs from MITRE. Connection issue?'

			if attack:
				try:
					self.Bs.downloadLatestAttack()
				except Exception:
					response += 'Issue downloading latest MITRE ATT&CK dataset. Connection issue?'

			return response + "Sync Completed"

		# Retrieve MITRE ATT&CK Content: Groups
		@self.app.route('/downloadMitreGroups')
		def download_groups():
			return self.Bs.downloadMitreGroups()

		# Threat Profiles: Manage Profiles

		@self.app.route('/_get_groups')
		def get_groups():
			response = ''
			response = self.Bs.getGroups()
			return response

		@self.app.route('/_get_group_for_edit')
		def get_group_for_edit():
			response = ''
			id = request.args.get('id')
			response = self.Bs.getGroupForEdit(id)
			return response

		@self.app.route('/_create_group')
		def create_group():
			response = ''
			response = self.Bs.createGroup()
			return response

		@self.app.route('/_delete_group')
		def delete_group():
			response = ''
			id = request.args.get('id')
			response = self.Bs.deleteGroup(id)
			return response

		@self.app.route('/_update_group')
		def update_group():
			response = ''
			data = request.args.get('data')
			profile = json.loads(data)
			id = profile['id']
			name = profile['name']
			ttps = profile['ttps']
			response = self.Bs.updateGroup(id, name, ttps)
			return response

		@self.app.route('/_get_groups_for_add_profile')
		def get_groups_for_add_profile():
			response = ''
			data = json.loads(request.args.get('data'))
			path = data['path']
			response = self.Bs.getGroupsForAddProfile(path)
			return response

		@self.app.route('/_add_ttp_to_profile')
		def add_ttp_to_profile():
			response = ''
			data = json.loads(request.args.get('data'))
			filePath = data['filePath']
			profileId = data['profileId']
			response = self.Bs.addTTPToProfile(filePath, profileId)
			return response

		# Threat Profiles: Analyze Profiles

		@self.app.route('/_get_matching_profiles')
		def get_matching_profiles():
			data = json.loads(request.args.get('data'))
			profileIds = data['profiles']
			return self.Bs.get_matching_profiles(profileIds)

		@self.app.route('/_export_to_navigator')
		def export_to_navigator():
			data = json.loads(request.args.get('data'))
			profileIds = data['profiles']
			jsonData = json.dumps(self.Bs.export_to_navigator(profileIds))
			return jsonData

		@self.app.route('/_open_profile_in_tabs')
		def open_profile_in_tabs():
			data = json.loads(request.args.get('data'))
			profileIds = data['profiles']
			files = self.Bs.open_profile_in_tabs(profileIds)
			return files

		@self.app.route('/_export_profile_to_pdf')
		def export_profile_to_pdf():
			data = json.loads(request.args.get('data'))
			profileIds = data['profiles']
			doc = self.Bs.export_profile_to_pdf(profileIds)
			f = open(self.Bs.localPath + 'bls_bible/PDF_Export.pdf', 'wb+')
			f.write(doc)
			f.close()
			start_size = os.path.getsize(self.Bs.localPath + 'bls_bible/PDF_Export.pdf')
			while True:
				if start_size != os.path.getsize(self.Bs.localPath + 'bls_bible/PDF_Export.pdf'):
					start_size = os.path.getsize(self.Bs.localPath + 'bls_bible/PDF_Export.pdf')
				else:
					break
			return '/_pdf'

		@self.app.route('/_pdf')
		def download_pdf():
			index = os.stat(self.Bs.localPath + 'bls_bible/static/index.html')
			uid = index.st_uid
			gid = index.st_gid
			os.chown(self.Bs.localPath + 'bls_bible/PDF_Export.pdf', uid, gid)
			return send_file(self.Bs.localPath + 'bls_bible/PDF_Export.pdf', as_attachment=True)

		# Variable Groups: Variable Groups
		@self.app.route('/_get_variable_groups')
		def get_variable_groups():
			response = ''
			response = self.Bs.getVariableGroups()
			return response

		@self.app.route('/_create_variable_group')
		def create_variable_group():
			response = self.Bs.createVariableGroups()
			return response

		@self.app.route('/_create_new_variable_group')
		def create_new_variable_group():
			group_type = request.args.get('type')
			group_name = request.args.get('name')
			return self.Bs.createNewVariableGroup(group_type, group_name)

		@self.app.route('/_delete_variable_group')
		def delete_variable_group():
			response = ''
			id = request.args.get('id')
			response = self.Bs.deleteVariableGroup(id)
			return response

		@self.app.route('/_get_variable_group_for_edit')
		def get_variable_group_for_edit():
			response = ''
			id = request.args.get('id')
			group_type = request.args.get('type')
			response = self.Bs.getVariableGroupForEdit(id, group_type)
			return response

		@self.app.route('/_update_variable_group')
		def update_variable_group():
			response = ''
			data = request.args.get('data')
			group = json.loads(data)
			response = self.Bs.updateVariableGroup(group)
			return response

		@self.app.route('/_get_variable_groups_for_add_new_group')
		def get_variable_groups_for_add_new_group():
			response = ''
			data = json.loads(request.args.get('data'))
			path = data['path']
			response = self.Bs.getVariableGroupsForAddNewGroup(path)
			return response

		@self.app.route('/_add_variable_to_variable_group')
		def add_variable_to_variable_group():
			response = ''
			data = json.loads(request.args.get('data'))
			filePath = data['filePath']
			profileId = data['profileId']
			response = self.Bs.addVariableToVariableGroup(filePath, profileId)
			return response

		# Variable Groups: Analyze Variables

		@self.app.route('/_get_compromised')
		def get_compromised():
			data = json.loads(request.args.get('data'))
			profileIds = data['profiles']
			return self.Bs.getCompromised(profileIds)

		@self.app.route('/_summarize_domain_variables')
		def summarizeDomainVariables():
			data = json.loads(request.args.get('data'))
			profileIds = data['profiles']
			return self.Bs.summarize_domain_variables(profileIds)
