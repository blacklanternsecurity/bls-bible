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
# app_dev.py

from bls_bible.lib.service import BibleService
from flask import Flask, request

class app_dev:
	def __init__(self, app):

		self.Bs = BibleService()
		self.app = app

	def app_dev_content(self):
		# Developer Endpoints
		@self.app.route('/devTools')
		def dev_tools():
			page = self.Bs.devTools()
			return page

		@self.app.route('/getBroken')
		def get_broken():
			page = self.Bs.getBroken()
			return page

		@self.app.route('/getMissing')
		def get_missing():
			page = self.Bs.get_missing_techniques()
			return page

		@self.app.route('/getRevoked')
		def get_revoked():
			page = self.Bs.get_revoked_techniques()
			return page

		@self.app.route('/getGuidesNotReferencing')
		def get_guides_not_referencing():
			page = self.Bs.get_guides_not_referencing()
			return page

		@self.app.route('/_get_guides_referencing_technique')
		def get_guides_referencing_technique():
			technique = request.args.get('technique')
			data = self.Bs.get_guides_referencing_technique(technique)
			return data

		@self.app.route('/validateFolderNaming')
		def validate_folder_naming():
			data = self.Bs.validate_folder_naming()
			return data

		@self.app.route('/getMissingGuideReferences')
		def get_missing_guide_references():
			page = self.Bs.get_missing_guide_references()
			return page