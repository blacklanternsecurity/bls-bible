import pytest

from bls_bible.lib.devtools import developer_tools
from bls_bible.lib.utils import utils


class TestDeveloperTools:
    def __init__(self):
        self.localPath = "./"
        self.utils = utils(self.localPath)
        self.parent = 'Data/'


@pytest.fixture
def dev_tool():
    return TestDeveloperTools()


def test_dev_tools(dev_tool):
    out = developer_tools.devTools(dev_tool)
    assert "<html>" in out and "</html>" in out


def test_get_missing_techniques(dev_tool):
    out = developer_tools.get_missing_techniques(dev_tool)
    assert "<html>" in out and "</html>" in out


def test_get_revoked_techniques(dev_tool):
    out = developer_tools.get_revoked_techniques(dev_tool)
    assert "<html>" in out and "</html>" in out


def test_get_guides_not_referencing(dev_tool):
    out = developer_tools.get_guides_not_referencing(dev_tool)
    assert "<html>" in out and "</html>" in out


def test_validate_folder_naming(dev_tool):
    out = developer_tools.validate_folder_naming(dev_tool)
    assert "<html>" in out and "</html>" in out


def test_get_broken(dev_tool):
    out = developer_tools.getBroken(dev_tool)
    assert "<html>" in out


def test_get_missing_guide_references(dev_tool):
    out = developer_tools.get_missing_guide_references(dev_tool)
    assert "<html>" in out and "</html>" in out
