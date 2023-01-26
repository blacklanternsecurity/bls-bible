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

from github import Github
import logging


class LeaderBoard:
    def __init__(self, token, repo, branch, parent):
        self.token = token
        self.repo = repo
        self.branch = branch
        self.parent = parent
        self.g = Github(login_or_token=self.token)
        try:
            self.repo = self.g.get_repo(self.repo)
        except Exception as e:
            pass

    def getLeaderBoard(self):
        try:
            pulls = self.repo.get_pulls(state="all", base="stable")
        except Exception as e:
            logging.error(str(e))
            pulls = []
        board = {}
        for idx, pull in enumerate(pulls):
            author = pull.user.login
            changes = pull.changed_files
            if author not in board:
                board[author] = {"Files Changed": changes, "Pull Requests": 1}
            else:
                board[author]["Files Changed"] += changes
                board[author]["Pull Requests"] += 1
        return board

    def getLeaderBoardUI(self, board):
        content = "<thead>"
        content += "<tr>"
        content += '<th scope="col">Rank</th>'
        content += '<th scope="col">Name</th>'
        content += '<th class="sortable-leaderboard-column" scope="col" onclick="sortTable(1)">Pull Requests</th>'
        content += '<th class="sortable-leaderboard-column" scope="col" onclick="sortTable(2)">Files Changed</th>'
        content += "</tr>"
        content += "</thead>"
        content += "<tbody>"
        rank = ""
        if len(board) > 0:
            for player in board:

                fcRank = board[player]["Files Changed"]
                fc = f"{fcRank:,}"
                mri = board[player]["Pull Requests"]
                mr = f"{mri:,}"

                if fcRank >= 10000:
                    rank = "Seraphim"
                elif fcRank >= 9000:
                    rank = "Cherubim"
                elif fcRank >= 8000:
                    rank = "Throne"
                elif fcRank >= 7000:
                    rank = "Dominion"
                elif fcRank >= 6000:
                    rank = "Virtue"
                elif fcRank >= 5000:
                    rank = "Power"
                elif fcRank >= 4000:
                    rank = "Principality"
                elif fcRank >= 3000:
                    rank = "Archangel"
                elif fcRank >= 500:
                    rank = "Angel"
                elif fcRank >= 100:
                    rank = "Half-Angel"
                elif fcRank >= 15:
                    rank = "Practitioner"
                else:
                    rank = "Observer"

                content += "<tr>"
                content += '<th scope="row">' + rank + "</th>"
                content += "<td><b>" + player + "</b></td>"
                content += "<td>" + mr + "</td>"
                content += "<td>" + fc + "</td>"
                content += "</tr>"
        return content
