import json
import pytest
from bls_bible.lib.utils import utils
from bls_bible.lib.ui import ui


class TestUI:
    def __init__(self):
        self.localPath = "./"
        self.parent = "Data/"
        self.safePath = self.localPath + self.parent
        self.utils = utils(self.localPath)
        self.accordionKey = 1

    def parseJsonData(self, d, t):
        return ui.parseJsonData(self, d, t)


@pytest.fixture
def ui_self():
    return TestUI()


@pytest.fixture
def safe_file():
    return "./Data/Testaments_and_Books/Redvelations/000_Red_Team_Field_Manual_(RTFM).md"


@pytest.fixture
def unsafe_file():
    return "./Data/../../../../../../etc/passwd"


def test_get_theme(ui_self):
    result = ui.get_theme(ui_self)
    assert "css" in result


def test_change_theme(ui_self):
    result = ui.change_theme(ui_self, "cyan")
    assert result


def test_highlight_ttps(ui_self):
    path = "./Data/Testaments_and_Books/Redvelations/Active_Directory/001-5_ADCS_Enumeration.md"
    result = ui.highlight_ttps(ui_self, path)
    assert len(result) > 0


def test_endpoint_blocked(ui_self):
    result = ui.endpoint_blocked(ui_self)
    assert "not available" in result


def test_get_tab_content(ui_self, safe_file):
    result = ui.getTabContent(ui_self, safe_file)
    assert "Active Directory" in result


def test_get_tab_content_lfi(ui_self, unsafe_file):
    result = ui.getTabContent(ui_self, unsafe_file)
    assert "private parts" in result


def test_parse_json_data(ui_self):
    with open("./bls_bible/static/red.json") as i:
        data = json.load(i)
    result = ui.parseJsonData(ui_self, data["children"], "Red")
    assert "ADCS" in result


def test_get_accordion(ui_self):
    result = ui.getAccordion(ui_self, "./bls_bible/static/red.json", "Red")
    assert "ADCS" in result


def test_file_indexer(ui_self):
    result = ui.fileIndexer(ui_self)
    assert "#@T1001" in result
