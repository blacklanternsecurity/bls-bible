import pytest
from bls_bible.lib.utils import utils


class TestUtils:
    def __init__(self):
        self.localPath = "./"
        self.safePath = self.localPath + "Data/"
        self.localDeployment = False
        self.parent = "Data/Testaments_and_Books/Redvelations/"

    def parse_dir_local(self, parent):
        return utils.parse_dir_local(self, parent)

    def getUrls(self, data, urls):
        return utils.getUrls(self, data, urls)


@pytest.fixture
def test_utils():
    return TestUtils()


def test_parse_dir_local(test_utils):
    result = utils.parse_dir_local(
        test_utils, test_utils.localPath + "Data/Testaments_and_Books/Redvelations/"
    )
    assert "Active Directory" in result


def test_get_ttp_content(test_utils):
    result = utils.get_ttp_content(test_utils, "T1001_Data_Obfuscation.md")
    assert len(result["phases"]) > 0


def test_get_urls(test_utils):
    data = {
        "children": [
            {
                "name": "as400.txt",
                "type": "url",
                "url": "getContent('./Data/Testaments_and_Books/Redvelations/Accounts/Default_Credentials/as400.txt')",
            }
        ],
        "name": "Default Credentials",
        "type": "folder",
    }
    urls = []
    result = utils.getUrls(test_utils, data, urls)
    assert len(result) > 0


def test_get_content(test_utils):
    path = "./Data/Testaments_and_Books/Redvelations/Accounts/Default_Credentials/as400.txt"
    result = utils.get_content(
        test_utils,
        path,
        test_utils.safePath,
        test_utils.localDeployment,
        test_utils.parent,
    )
    assert "private parts" not in result


def test_get_content_lfi(test_utils):
    path = "./Data/Testaments_and_Books/../../../../../../../etc/passwd"
    result = utils.get_content(
        test_utils,
        path,
        test_utils.safePath,
        test_utils.localDeployment,
        test_utils.parent,
    )
    assert "private parts" in result


def test_get_guides_referencing_technique(test_utils):
    tech = "T1595"
    result = utils.get_guides_referencing_technique(test_utils, tech)
    assert len(result) > 0
