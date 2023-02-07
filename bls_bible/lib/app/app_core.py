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
# app_core.py

from bls_bible.lib.service import BibleService
from flask import request
from flask import make_response


class app_core:
	def __init__(self, app):

		self.Bs = BibleService()
		self.app = app

	def app_core_content(self):
		@self.app.route('/_get_verse_of_the_day')
		def get_verse_of_the_day():
			return self.Bs.verse_of_the_day()

		# Content
		@self.app.route("/_get_tab_content")
		def get_tab_content():
			content = self.Bs.getTabContent(request.args.get('path'))
			return content

		@self.app.route('/_get_data_red')
		def get_data_red():
			redAccordion = self.Bs.getAccordion(self.Bs.localPath + "bls_bible/static/red.json", "Red")
			return redAccordion

		@self.app.route('/_get_data_blue')
		def get_data_blue():
			blueAccordion = self.Bs.getAccordion(self.Bs.localPath + "bls_bible/static/blue.json", "Blue")
			return blueAccordion

		@self.app.route('/_get_data_ttp')
		def get_data_ttp():
			ttpAccordion = self.Bs.getAccordion(self.Bs.localPath + "bls_bible/static/ttp.json", "Ttp")
			return ttpAccordion

		@self.app.route('/_get_data_purple')
		def get_data_purple():
			purpleAccordion = self.Bs.getAccordion(self.Bs.localPath + "bls_bible/static/purple.json", "Purple")
			return purpleAccordion

		@self.app.route('/_get_data_assessment')
		def get_data_assessment():
			assessmentAccordion = self.Bs.getAccordion(self.Bs.localPath + "bls_bible/static/assessment.json", "Assessment")
			return assessmentAccordion

		@self.app.route('/_get_data_apocrypha')
		def get_data_apocrypha():
			apocryphaAccordion = self.Bs.getAccordion(self.Bs.localPath + "bls_bible/static/apocrypha.json", "Apocrypha")
			return apocryphaAccordion

		@self.app.route('/_highlight_ttps')
		def highlight_ttps():
			result = self.Bs.highlight_ttps(request.args.get('path'))
			return result

		@self.app.route('/_highlight_guides')
		def highlight_guides():
			tech_path = request.args.get('path')
			techId = tech_path.split('/')[-1].replace('.md', '')
			data = self.Bs.get_guides_referencing_technique(techId)
			for guide in data['guides_referencing']:
				guide['guide_path'] = guide['guide_path'].replace(self.Bs.localPath + self.Bs.parent + 'Testaments_and_Books/', '')
			return data

		@self.app.route('/_get_content')
		def get_content():
			path = request.args.get('path', self.Bs.localPath + self.Bs.parent + "README.md", type=str)
			content = self.Bs.get_content(path)
			return content

		@self.app.route('/_get_content_remote')
		def get_content_remote():
			path = request.args.get('path', self.Bs.parent, type=str)
			name = request.args.get('name', "README.md", type=str)
			content = self.Bs.get_content_remote(path, name)
			return content

		@self.app.route('/_edit_file')
		def edit_file():
			path = request.args.get('path', self.Bs.parent, type=str)
			content = self.Bs.edit_file(path)
			response = make_response(content)
			response.mimetype = "text/plain"
			return response

		@self.app.route('/_save_file', methods=['POST'])
		def save_file():
			path = request.form['path']
			newContent = request.form['content']
			self.Bs.save_file(path, newContent)
			return ''

		@self.app.route('/_get_theme')
		def get_theme():
			theme = self.Bs.get_theme()
			return theme

		@self.app.route('/_change_theme')
		def change_theme():
			color = request.args.get('color')
			self.Bs.change_theme(color)
			return ''

		@self.app.route('/_get_apts')
		def get_apts():
			return self.Bs.get_apts()

		@self.app.route('/_filter_apts')
		def filter_apts():
			apt = request.args.get('apt')
			return str(self.Bs.filter_apts(apt))

		# search

		@self.app.route('/_search_local')
		def search():
			tag = request.args.get('tag', '', type=str)
			osTags = request.args.getlist('osTags[]')
			onpremTags = request.args.getlist('onpremTags[]')
			cloudTags = request.args.getlist('cloudTags[]')
			applicationTags = request.args.getlist('applicationTags[]')
			specialTags = request.args.getlist('specialTags[]')
			guideTtpTags = request.args.getlist('guideTtpTags[]')
			aptTags = request.args.getlist('aptTags[]')
			selectBox = self.Bs.search_local(tag, osTags, onpremTags, cloudTags, applicationTags, specialTags, guideTtpTags, aptTags)
			return selectBox

		@self.app.route('/_search_advanced')
		def search_advanced():
			regex = request.args.get('regex')
			context = int(request.args.get('context'))
			results = self.Bs.search_advanced(regex, context)
			return results


		# leaderboard

		@self.app.route("/leaderboard")
		def leaderboard():
			return self.app.send_static_file('leaderboard.html')

		@self.app.route('/_get_leaderboard_content')
		def get_leaderboard_content():
			content = ''
			try:
				board = self.Bs.getLeaderBoard()
			except Exception:
				content += '<span>Issue downloading leaderboard information from GitLab. ' \
						   'Are you sure your connection is okay?</span>'
				return content
			return self.Bs.getLeaderBoardUI(board)
