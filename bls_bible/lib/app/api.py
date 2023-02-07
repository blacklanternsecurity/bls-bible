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
# app.py

from flask_restful import reqparse, Api, Resource

from bls_bible.lib.service import BibleService


Bs = BibleService()

parser = reqparse.RequestParser()
parser.add_argument('proxy_id')
parser.add_argument('name')
parser.add_argument('ttp')
parser.add_argument('threat_profile_id')
parser.add_argument('threat_profile_name')
parser.add_argument('step_name')
parser.add_argument('finding')
parser.add_argument('threat_source')
parser.add_argument('ETM_Step_id')


class ThreatProfileList_API(Resource):

	def get(self):

		return Bs.get_threat_profiles()

class ThreatProfile_API(Resource):

	def post(self, name, ttp):

		return Bs.createProfile_ETM(name, ttp), 201

	def get(self, threat_profile_id):

		return Bs.get_specific_threat_profile(threat_profile_id)

	def delete(self, threat_profile_id):

		return Bs.deleteProfile_ETM(threat_profile_id), 204

	def put(self, threat_profile_id, threat_profile_name, ETM_Scenario_id, ttps):

		return Bs.updateProfile_ETM(threat_profile_id, threat_profile_name, ETM_Scenario_id, ttps), 201

class ProxyList_API(Resource):

	def get(self):

		return True

	def post(self):

		return True, 201

class Proxy_API(Resource):

	def get(self, proxy_id):
		return True # TODO
		# return TODOS[proxy_id]

	def delete(self, proxy_id):

		return '', 204

	def put(self, proxy_id):

		return True # TODO

class TTPList_API(Resource):

	def get(self):

		return Bs.get_threat_profiles()


class TTP_API(Resource):

	def post(self, mitreId, profileId, threat_source, step_name, finding, ETM_Step_id):

		return Bs.addTTPToProfile_ETM(mitreId, profileId, threat_source, step_name, finding, ETM_Step_id), 201

	def get(self, ttp_id):

		return Bs.get_specific_ttp(ttp_id)

	def delete(self, ttp_id):

		Bs.deleteProfile_ETM(ttp_id)

		return '', 204

	def put(self, ttp_id, step_name, ttp, finding, threat_source, ETM_Step_id):

		return Bs.updateTTPs_ETM(ttp_id, step_name, ttp, finding, threat_source, ETM_Step_id), 201

class api_service(Resource):

	def __init__(self, app):

		self.app = app
		self.api = Api(self.app)
		self.api.add_resource(api_service)

	def api_routing(self):

		self.api.add_resource(ThreatProfileList_API, '/threat_profile')
		self.api.add_resource(ThreatProfile_API, '/threat_profile/<threat_profile_id>')
		self.api.add_resource(ProxyList_API, '/Proxy')
		self.api.add_resource(Proxy_API, '/Proxy/<proxy_id>')
		self.api.add_resource(TTPList_API, '/ttp')
		self.api.add_resource(TTP_API, '/ttp/<ttp_id>')
