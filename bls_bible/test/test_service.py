import pytest
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
from bls_bible.lib.service import BibleService


class TestService:
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


@pytest.fixture
def bs_self():
    return TestService()


"""
def test_threat_profile_list_api_handler(bs_self):
	assert BibleService.threat_profile_api_handler() is not None


def test_threat_profile_api_handler(bs_self):
	assert BibleService.threat_profile_api_handler(bs_self) is not None


def test_ttp_list_api_handler(bs_self):
	assert BibleService.ttp_list_api_handler(bs_self) is not None


def test_ttp_api_handler(bs_self):
	assert BibleService.ttp_api_handler(bs_self, id , method)


def test_proxy_list_api_handler(bs_self):
	assert False


def test_proxy_api_handler(bs_self):
	assert False
"""


def test_new_app_config(bs_self):
    assert (
        BibleService.new_app_config(
            bs_self,
            bs_self.token,
            bs_self.domain,
            bs_self.repo,
            bs_self.projectId,
            bs_self.branch,
            bs_self.parent,
            bs_self.source,
            bs_self.localDeployment,
            bs_self.Assessalonians_Repo,
            bs_self.bitwarden_server,
            bs_self.bls_bible_server,
        )
        is not None
    )


def test_update_app_config(bs_self):
    result = BibleService.update_app_config(bs_self, "bls_bible_server", "")
    assert "localDeployment" in result


def test_list_configs(bs_self):
    result = BibleService.list_configs(bs_self)
    assert result


def test_reset_default_configs(bs_self):
    result = BibleService.reset_default_configs(bs_self)
    assert result


def test_get_groups(bs_self):
    with open("./bls_bible/test/test_profiles.json") as f:
        test_data = f.read()
    with open("./bls_bible/static/profiles.json", "w+") as f:
        original = f.read()
        f.write(test_data)
    result = BibleService.getGroups(bs_self)
    with open("./bls_bible/static/profiles.json", "w+") as f:
        f.write(original)
    assert len(result) > 0


def test_get_group_for_edit(bs_self):
    with open("./bls_bible/test/test_profiles.json") as f:
        test_data = f.read()
    with open("./bls_bible/static/profiles.json", "w+") as f:
        original = f.read()
        f.write(test_data)
    result = BibleService.getGroupForEdit(bs_self, "8c921b02990f9d76ca4b7212e68e48d6")
    with open("./bls_bible/static/profiles.json", "w+") as f:
        f.write(original)
    assert "Test Profile 2" in result


def test_create_group(bs_self):
    with open("./bls_bible/test/test_profiles.json") as f:
        test_data = f.read()
    with open("./bls_bible/static/profiles.json", "w+") as f:
        original = f.read()
        f.write(test_data)
    result = BibleService.createGroup(bs_self)
    with open("./bls_bible/static/profiles.json", "w+") as f:
        f.write(original)
    assert "New Threat Profile" in result


def test_delete_group(bs_self):
    with open("./bls_bible/test/test_profiles.json") as f:
        test_data = f.read()
    with open("./bls_bible/static/profiles.json", "w+") as f:
        original = f.read()
        f.write(test_data)
    result = BibleService.deleteGroup(bs_self, "8c921b02990f9d76ca4b7212e68e48d6")
    with open("./bls_bible/static/profiles.json", "w+") as f:
        f.write(original)
    assert "Test Profile 2" not in result


def test_update_group(bs_self):
    with open("./bls_bible/test/test_profiles.json") as f:
        test_data = f.read()
    with open("./bls_bible/static/profiles.json", "w+") as f:
        original = f.read()
        f.write(test_data)
    result = BibleService.updateGroup(
        bs_self, "8c921b02990f9d76ca4b7212e68e48d6", "Test Profile 3", {}
    )
    with open("./bls_bible/static/profiles.json", "w+") as f:
        f.write(original)
    assert "Test Profile 3" in result


def test_get_groups_for_add_profile(bs_self):
    with open("./bls_bible/test/test_profiles.json") as f:
        test_data = f.read()
    with open("./bls_bible/static/profiles.json", "w+") as f:
        original = f.read()
        f.write(test_data)
    result = BibleService.getGroupsForAddProfile(
        bs_self, "./Data/TTP/T1001_Data_Obfuscation/T1001.md"
    )
    with open("./bls_bible/static/profiles.json", "w+") as f:
        f.write(original)
    assert "T1001.md" in result


def test_add_ttpto_profile(bs_self):
    with open("./bls_bible/test/test_profiles.json") as f:
        test_data = f.read()
    with open("./bls_bible/static/profiles.json", "w+") as f:
        original = f.read()
        f.write(test_data)
    result = BibleService.addTTPToProfile(
        bs_self,
        "./Data/TTP/T1001_Data_Obfuscation/T1001.md",
        "8c921b02990f9d76ca4b7212e68e48d6",
    )
    with open("./bls_bible/static/profiles.json", "w+") as f:
        f.write(original)
    assert "T1001.md" in result


def test_get_matching_profiles(bs_self):
    with open("./bls_bible/test/test_profiles.json") as f:
        test_data = f.read()
    with open("./bls_bible/static/profiles.json", "w+") as f:
        original = f.read()
        f.write(test_data)
    result = BibleService.get_matching_profiles(
        bs_self, ["8c921b02990f9d76ca4b7212e68e48d6"]
    )
    with open("./bls_bible/static/profiles.json", "w+") as f:
        f.write(original)
    assert result is not None


def test_export_to_navigator(bs_self):
    with open("./bls_bible/test/test_profiles.json") as f:
        test_data = f.read()
    with open("./bls_bible/static/profiles.json", "w+") as f:
        original = f.read()
        f.write(test_data)
    result = BibleService.export_to_navigator(
        bs_self, ["8c921b02990f9d76ca4b7212e68e48d6"]
    )
    with open("./bls_bible/static/profiles.json", "w+") as f:
        f.write(original)
    assert result is not None


def test_open_profile_in_tabs(bs_self):
    with open("./bls_bible/test/test_profiles.json") as f:
        test_data = f.read()
    with open("./bls_bible/static/profiles.json", "w+") as f:
        original = f.read()
        f.write(test_data)
    result = BibleService.open_profile_in_tabs(
        bs_self, ["8c921b02990f9d76ca4b7212e68e48d6"]
    )
    with open("./bls_bible/static/profiles.json", "w+") as f:
        f.write(original)
    assert len(result) > 0


def test_export_profile_to_pdf(bs_self):
    with open("./bls_bible/test/test_profiles.json") as f:
        test_data = f.read()
    with open("./bls_bible/static/profiles.json", "w+") as f:
        original = f.read()
        f.write(test_data)
    result = BibleService.export_profile_to_pdf(
        bs_self, ["8c921b02990f9d76ca4b7212e68e48d6"]
    )
    with open("./bls_bible/static/profiles.json", "w+") as f:
        f.write(original)
    assert len(result) > 0


def test_verse_of_the_day(bs_self):
    result = BibleService.verse_of_the_day(bs_self)
    assert result is not None


def test_update_verses(bs_self):
    result = BibleService.update_verses(bs_self)
    assert result


def test_search_advanced(bs_self):
    result = BibleService.search_advanced(bs_self, "Active Directory", 1)
    assert result is not None


def test_search_local(bs_self):
    result = BibleService.search_local(
        bs_self, "AD", None, None, None, None, None, None, None
    )
    assert result is not None


def test_filter_apts(bs_self):
    result = BibleService.filter_apts(bs_self, "G0018")
    assert result is not None


def test_get_theme(bs_self):
    result = BibleService.get_theme(bs_self)
    assert result is not None


def test_change_theme(bs_self):
    result = BibleService.change_theme(bs_self, "cyan")
    assert result is not None


"""
def test_highlight_ttps(bs_self):
	assert False


def test_endpoint_blocked(bs_self):
	assert False


def test_get_tab_content(bs_self):
	assert False


def test_update_json_file(bs_self):
	assert False


def test_get_reverse_references(bs_self):
	assert False


def test_get_apts(bs_self):
	assert False


def test_crawl_groups(bs_self):
	assert False


def test_crawl_json(bs_self):
	assert False


def test_crawl_json_for_download(bs_self):
	assert False


def test_download_mitre_groups(bs_self):
	assert False


def test_download_latest_attack(bs_self):
	assert False


def test_git_repo_update(bs_self):
	assert False


def test_git_submodule_pull(bs_self):
	assert False


def test_git_assessalonians_pull(bs_self):
	assert False


def test_get_content(bs_self):
	assert False


def test_get_leader_board(bs_self):
	assert False


def test_get_leader_board_ui(bs_self):
	assert False


def test_edit_file(bs_self):
	assert False


def test_save_file(bs_self):
	assert False


def test_dev_tools(bs_self):
	assert False


def test_get_missing_techniques(bs_self):
	assert False


def test_get_revoked_techniques(bs_self):
	assert False


def test_get_guides_not_referencing(bs_self):
	assert False


def test_validate_folder_naming(bs_self):
	assert False


def test_get_broken(bs_self):
	assert False


def test_get_missing_guide_references(bs_self):
	assert False


def test_get_guides_referencing_technique(bs_self):
	assert False


def test_parse_json_data(bs_self):
	assert False


def test_get_accordion(bs_self):
	assert False


def test_get_urls(bs_self):
	assert False


def test_file_indexer(bs_self):
	assert False
"""
