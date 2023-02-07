import pytest

from bls_bible.lib.search import search as s
from bls_bible.lib.search import search_filter as sf


class TestSearch:
    def __init__(self):
        self.source = "local"
        self.localPath = "./"


class TestSearchFilter:
    def __init__(self):
        self.localPath = "./"


@pytest.fixture
def search_filter():
    return TestSearchFilter()


@pytest.fixture
def search():
    return TestSearch()


def test_search_advanced(search):
    context = 0
    regex = "ADCS"
    result = s.search_advanced(search, regex, context)
    assert len(result) > 0


def test_search_local(search):
    osTags = "WINDOWS"
    onpremTags = "ACTIVEDIRECTORY"
    cloudTags = "AZURE"
    applicationTags = "WEB"
    specialTags = "OFFICE"
    guideTtpTags = "GUIDE"
    aptTags = "G0018"
    term = "AD"
    result = s.search_local(
        search,
        term,
        osTags,
        onpremTags,
        cloudTags,
        applicationTags,
        specialTags,
        guideTtpTags,
        aptTags,
    )
    assert "</ul>" in result


def test_filter_apts(search_filter):
    apt = "G0018"
    result = sf.filter_apts(search_filter, apt)
    assert len(result) > 0
