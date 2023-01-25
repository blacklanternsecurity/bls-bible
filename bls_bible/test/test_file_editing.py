import pytest
from bls_bible.lib.file_editing import file_editing
from datetime import datetime


class TestFileEditing:
    def __init__(self):
        self.localPath = "./bls_bible/test"
        self.localDeployment = "True"
        self.parent = "/"
        self.safePath = self.localPath + self.parent


@pytest.fixture
def file_edit():
    return TestFileEditing()


@pytest.fixture()
def good_path():
    return "./bls_bible/test/test_page.md"


@pytest.fixture()
def lfi_path():
    return "./../../../../../../../etc/passwd"


@pytest.fixture()
def file_content():
    return str(datetime.utcnow().timestamp())


def test_edit_file(file_edit, good_path):
    out = file_editing.edit_file(file_edit, good_path)
    assert "private parts" not in out


def test_edit_file_lfi(file_edit, lfi_path):
    out = file_editing.edit_file(file_edit, lfi_path)
    assert "private parts" in out


def test_save_file(file_edit, good_path, file_content):
    out = file_editing.save_file(file_edit, good_path, file_content)
    with open(good_path) as f:
        saved_content = f.read()
    assert out and file_content in saved_content


def test_save_file_lfi(file_edit, lfi_path, file_content):
    out = file_editing.save_file(file_edit, lfi_path, file_content)
    assert not out
