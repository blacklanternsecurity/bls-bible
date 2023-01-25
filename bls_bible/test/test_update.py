import pytest
from bls_bible.lib.update import update
from bls_bible.lib.update import mitre_update
from bls_bible.lib.update import git_update
from bls_bible.lib.utils import utils


class TestUpdate:
    def __init__(self):
        self.source = "local"
        self.redParent = "Data/Testaments_and_Books/Redvelations/"
        self.blueParent = "Data/Testaments_and_Books/Blue_Testament/"
        self.purpleParent = "Data/Testaments_and_Books/Purplippians/"
        self.apocryphaParent = "Data/Testaments_and_Books/Apocrypha/"
        self.assessmentParent = "Data/Testaments_and_Books/Assessalonians/"
        self.localPath = "./"
        self.ttpParent = "Data/TTP/"
        self.localDeployment = "True"
        self.parent = "Data/"
        self.safePath = "./Data/"
        self.utils = utils(self.localPath)


class TestMitreUpdate:
    def __init__(self):
        self.localPath = "./"

    def crawlGroups(self):
        return mitre_update.crawlGroups(self)

    def crawlJsonForDownload(self, id):
        return mitre_update.crawlJsonForDownload(self, id)


class TestGitUpdate:
    def __init__(self):
        self.localPath = "./"


@pytest.fixture
def test_git_update():
    return TestGitUpdate()


@pytest.fixture
def test_update():
    return TestUpdate()


@pytest.fixture
def test_mitre_update():
    return TestMitreUpdate()


def test_update_json_file(test_update):
    result = update.update_json_file(test_update)
    assert result


def test_get_reverse_references(test_update):
    result = update.get_reverse_references(test_update)
    assert result


def test_get_apts(test_mitre_update):
    result = mitre_update.get_apts(test_mitre_update)
    assert "G0018" in result


def test_crawl_groups(test_mitre_update):
    result = mitre_update.crawlGroups(test_mitre_update)
    assert "G0018" in result


def test_crawl_json(test_mitre_update):
    result = mitre_update.crawlJson(test_mitre_update, "G0018")
    assert "T1059" in result


def test_download_mitre_groups(test_mitre_update):
    result = mitre_update.downloadMitreGroups(test_mitre_update)
    assert "G0018" in result


def test_crawl_json_for_download(test_mitre_update):
    result = mitre_update.crawlJsonForDownload(test_mitre_update, "G0018")
    assert len(result["techniques"]) > 0


def test_download_latest_attack(test_mitre_update):
    result = mitre_update.downloadLatestAttack(test_mitre_update)
    assert "T1059" in result


def test_git_submodule_pull(test_git_update):
    result = git_update.git_submodule_pull(test_git_update)
    assert len(result) >= 0


def test_git_repo_update(test_git_update):
    result = git_update.git_repo_update(test_git_update)
    assert result is None
