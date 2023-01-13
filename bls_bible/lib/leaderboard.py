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
# service.py

import gitlab


class LeaderBoard():
	def __init__(self, token, domain, repo, id, branch, parent):
		self.token = token
		self.domain = domain
		self.repo = repo
		self.projectId = id
		self.branch = branch
		self.parent = parent
		self.gl = gitlab.Gitlab(self.domain, private_token=self.token, ssl_verify=False)

	def getLeaderBoard(self):
		merges = self.gl.projects.get(self.projectId).mergerequests.list(all=True)
		board = {}
		for idx, merge in enumerate(merges):
			mr = merge.changes()
			author = mr["author"]["name"]
			if mr["changes_count"] == "1000+":
				changes = 1000
			elif mr["changes_count"] is None:
				continue
			else:
				changes = int(mr["changes_count"])
			if not author in board:
				board[author] = {"Files Changed": changes, "Merge Requests": 1}
			else:
				board[author]["Files Changed"] += changes
				board[author]["Merge Requests"] += 1
		return board

	def getLeaderBoardUI(self, board):
		content = '<thead>'
		content += '<tr>'
		content += '<th scope="col">Rank</th>'
		content += '<th scope="col">Name</th>'
		content += '<th class="sortable-leaderboard-column" scope="col" onclick="sortTable(1)">Merge Requests</th>'
		content += '<th class="sortable-leaderboard-column" scope="col" onclick="sortTable(2)">Files Changed</th>'
		content += '</tr>'
		content += '</thead>'
		content += '<tbody>'
		rank = ''
		for player in board:

			fcRank = board[player]["Files Changed"]
			fc = f"{fcRank:,}"
			mri = board[player]["Merge Requests"]
			mr = f"{mri:,}"

			if (fcRank >= 10000):
				rank = 'Seraphim'
			elif (fcRank >= 9000):
				rank = 'Cherubim'
			elif (fcRank >= 8000):
				rank = 'Throne'
			elif (fcRank >= 7000):
				rank = 'Dominion'
			elif (fcRank >= 6000):
				rank = 'Virtue'
			elif (fcRank >= 5000):
				rank = 'Power'
			elif (fcRank >= 4000):
				rank = 'Principality'
			elif (fcRank >= 3000):
				rank = 'Archangel'
			elif (fcRank >= 500):
				rank = 'Angel'
			elif (fcRank >= 100):
				rank = 'Half-Angel'
			elif (fcRank >= 15):
				rank = 'Practitioner'
			else:
				rank = 'Observer'

			content += '<tr>'
			content += '<th scope="row">' + rank + '</th>'
			content += '<td><b>' + player + '</b></td>'
			content += '<td>' + mr + '</td>'
			content += '<td>' + fc + '</td>'
			content += '</tr>'
		return content
