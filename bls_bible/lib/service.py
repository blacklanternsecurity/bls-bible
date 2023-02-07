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

import os
from bls_bible.lib.config.app_config import config_management
from bls_bible.lib.update import update, mitre_update, git_update
from bls_bible.lib.utils import utils
from bls_bible.lib.file_editing import file_editing
from bls_bible.lib.ui import ui
from bls_bible.lib.search import search, search_filter
from bls_bible.lib.verse_of_the_day import verse_of_the_day, update_verses
from bls_bible.lib.cli.api_handler import api_handler
from bls_bible.lib.threat_profiles import manage_profiles
from bls_bible.lib.threat_profiles import analyze_profiles
from bls_bible.lib.devtools import developer_tools
from bls_bible.lib import leaderboard


class BibleService:
    def __init__(self):
        # self.model = TacticsModel()
        self.config_management = config_management()
        # Data pulled from config
        self.token = self.config_management.config["token"]
        self.domain = self.config_management.config["domain"]
        self.repo = self.config_management.config["repo"]
        self.projectId = self.config_management.config["id"]
        self.branch = self.config_management.config["branch"]
        self.parent = self.config_management.config["parent"]
        self.source = self.config_management.config["source"]
        self.Assessalonians_Repo = self.config_management.config["Assessalonians_Repo"]
        self.bitwarden_server = self.config_management.config["bitwarden_server"]
        self.bls_bible_server = self.config_management.config["bls_bible_server"]
        self.localDeployment = self.config_management.load_app_config()[
            "localDeployment"
        ]
        self.localPath = os.path.abspath(os.path.join(os.getcwd())) + "/"
        # Data defined here
        self.redParent = "Data/Testaments_and_Books/Redvelations/"
        self.blueParent = "Data/Testaments_and_Books/Blue_Testament/"
        self.assessmentParent = "Data/Testaments_and_Books/Assessalonians/"
        self.purpleParent = "Data/Testaments_and_Books/Purplippians/"
        self.ttpParent = "Data/TTP/"
        self.apocryphaParent = "Data/Testaments_and_Books/Apocrypha/"
        self.source = "local"
        self.safePath = self.localPath + self.parent
        self.accordionKey = 0
        # Check if data files exist
        # create data files if not
        # config management
        # updates
        self.update = update(
            self.source,
            self.redParent,
            self.blueParent,
            self.purpleParent,
            self.apocryphaParent,
            self.assessmentParent,
            self.localPath,
            self.ttpParent,
            self.localDeployment,
            self.parent,
            self.safePath,
            self.projectId,
            self.branch,
            self.domain,
            self.token,
        )
        self.mitre_update = mitre_update(self.localPath)
        self.utils = utils(self.localPath)
        self.git_update = git_update(
            self.token,
            self.domain,
            self.repo,
            self.config_management.config["id"],
            self.branch,
            self.parent,
            self.localPath,
        )
        # UI
        self.ui = ui(self.localPath, self.parent, self.safePath)
        self.api_handler = api_handler(self.bls_bible_server)
        # Search
        self.search = search(self.source, self.localPath)
        self.search_filter = search_filter(self.localPath)
        self.manage_profiles = manage_profiles(self.localPath)
        self.analyze_profiles = analyze_profiles(
            localPath=self.localPath,
            localDeployment=self.localDeployment,
            safePath=self.safePath,
            parent=self.parent,
        )
        # File Editing
        self.file_editing = file_editing(
            self.localPath, self.localDeployment, self.parent, self.safePath
        )
        self.developer_tools = developer_tools(
            self.source,
            self.parent,
            self.localPath,
            self.safePath,
            self.localDeployment,
        )
        self.leaderboard = leaderboard.LeaderBoard(
            self.token, self.repo, self.branch, self.parent
        )

    # lib.cli.api_handler

    def threat_profile_list_api_handler(self):
        return self.api_handler.threat_profile_list_api_handler()

    def threat_profile_api_handler(self, id, method):
        return self.api_handler.threat_profile_api_handler(id, method)

    def ttp_list_api_handler(self):
        return self.api_handler.threat_profile_list_api_handler()

    def ttp_api_handler(self, id, method):
        return self.api_handler.threat_profile_api_handler(id, method)

    def proxy_list_api_handler(self):
        return self.api_handler.threat_profile_list_api_handler()

    def proxy_api_handler(self, id, method):
        return self.api_handler.threat_profile_api_handler(id, method)

    # lib.app_config
    ## class config_management
    def new_app_config(
        self,
        newToken,
        newDomain,
        newRepo,
        newId,
        newBranch,
        newParent,
        newSource,
        newLocalDeployment,
        newAssessalonians_Repo,
        bitwarden_server,
        bls_bible_server,
    ):
        return self.config_management.new_app_config(
            newToken,
            newDomain,
            newRepo,
            newId,
            newBranch,
            newParent,
            newSource,
            newLocalDeployment,
            newAssessalonians_Repo,
            bitwarden_server,
            bls_bible_server,
        )

    def update_app_config(self, key, value):
        return self.config_management.update_app_config(key, value)

    def list_configs(self):
        return self.config_management.list_configs()

    # def set_vars(self):
    # return self.config_management.set_vars()

    def reset_default_configs(self):
        return self.config_management.reset_default_configs()

    # lib.threat_profiles
    # class: manage_profiles

    def getGroups(self):
        return self.manage_profiles.getGroups()

    def getGroupForEdit(self, group_id):
        return self.manage_profiles.getGroupForEdit(group_id)

    def createGroup(self):
        return self.manage_profiles.createGroup()

    def deleteGroup(self, group_id):
        return self.manage_profiles.deleteGroup(group_id)

    def updateGroup(self, group_id, name, ttps):
        return self.manage_profiles.updateGroup(group_id, name, ttps)

    def getGroupsForAddProfile(self, path):
        return self.manage_profiles.getGroupsForAddProfile(path)

    def addTTPToProfile(self, filePath, profileId):
        return self.manage_profiles.addTTPToProfile(filePath, profileId)

    # lib.threat_profiles
    # class: analyze_profiles

    def get_matching_profiles(self, profile_ids):
        return self.analyze_profiles.get_matching_profiles(profile_ids)

    def export_to_navigator(self, profile_ids):
        return self.analyze_profiles.export_to_navigator(profile_ids)

    def open_profile_in_tabs(self, profile_ids):
        return self.analyze_profiles.open_profile_in_tabs(profile_ids)

    def export_profile_to_pdf(self, profile_ids):
        return self.analyze_profiles.export_profile_to_pdf(profile_ids)

    # lib.verse_of_the_day.py
    def verse_of_the_day(self):
        return verse_of_the_day(self.localPath)

    def update_verses(self):
        return update_verses(self.localPath)

    # lib.search.py
    ## class: search
    def search_advanced(self, regex, context):
        return self.search.search_advanced(regex, context)

    def search_local(
        self,
        term,
        osTags,
        onpremTags,
        cloudTags,
        applicationTags,
        specialTags,
        guideTtpTags,
        aptTags,
    ):
        return self.search.search_local(
            term,
            osTags,
            onpremTags,
            cloudTags,
            applicationTags,
            specialTags,
            guideTtpTags,
            aptTags,
        )

    # class: search_filter
    def filter_apts(self, apt):
        return self.search_filter.filter_apts(apt)

    # lib.ui.py
    def get_theme(self):
        return self.ui.get_theme()

    def change_theme(self, color):
        return self.ui.change_theme(color)

    def highlight_ttps(self, path):
        return self.ui.highlight_ttps(path)

    def endpoint_blocked(self):
        return self.ui.endpoint_blocked()

    def getTabContent(self, path):
        return self.ui.getTabContent(path)

    # lib.update.py
    ## class: update
    def update_json_file(self):
        return self.update.update_json_file()

    def get_reverse_references(self):
        return self.update.get_reverse_references()

    ## class: mitre_update
    def get_apts(self):
        return self.mitre_update.get_apts()

    def crawlGroups(self):
        return self.mitre_update.crawlGroups()

    def crawlJson(self, id):
        return self.mitre_update.crawlJson(id)

    def crawlJsonForDownload(self, id):
        return self.mitre_update.crawlJsonForDownload(id)

    def downloadMitreGroups(self):
        return self.mitre_update.downloadMitreGroups()

    def downloadLatestAttack(self):
        return self.mitre_update.downloadLatestAttack()

    ## class: git_update
    def git_repo_update(self):
        return self.git_update.git_repo_update()

    def git_submodule_pull(self):
        return self.git_update.git_submodule_pull()

    def git_assessalonians_pull(self):
        return self.git_update.git_assessalonians_pull(
            self.Assessalonians_Repo, self.assessmentParent
        )

    """
    ## class: autoupdate
    def schedule_update(self):
        return self.autoupdate.schedule_update()
    """

    # methods from lib.utils.py
    def get_content(self, path):
        return self.utils.get_content(
            path, self.safePath, self.localDeployment, self.parent
        )

    # methods from lib.leaderboard.py
    def getLeaderBoard(self):
        return self.leaderboard.getLeaderBoard()

    def getLeaderBoardUI(self, board):
        return self.leaderboard.getLeaderBoardUI(board)

    # methods from lib.file_editing.py
    def edit_file(self, path):
        return self.file_editing.edit_file(path)

    def save_file(self, path, content):
        return self.file_editing.save_file(path, content)

    # methods from lib.devtools.py
    def devTools(self):
        return self.developer_tools.devTools()

    def get_missing_techniques(self):
        return self.developer_tools.get_missing_techniques()

    def get_revoked_techniques(self):
        return self.developer_tools.get_revoked_techniques()

    def get_guides_not_referencing(self):
        return self.developer_tools.get_guides_not_referencing()

    def validate_folder_naming(self):
        return self.developer_tools.validate_folder_naming()

    def getBroken(self):
        return self.developer_tools.getBroken()

    def get_missing_guide_references(self):
        return self.developer_tools.get_missing_guide_references()

    # content generation
    def get_guides_referencing_technique(self, technique):
        return self.utils.get_guides_referencing_technique(technique)

    def parseJsonData(self, json, type):
        return self.ui.parseJsonData(json, type)

    def getAccordion(self, file, type):
        return self.ui.getAccordion(file, type)

    def getUrls(self, data, urls):
        return self.utils.getUrls(data, urls)

    def fileIndexer(self):
        return self.ui.fileIndexer()
