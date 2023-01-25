from bls_bible.lib import verse_of_the_day


def test_update_verses():
    result = verse_of_the_day.update_verses("./")
    assert result


def test_verse_of_the_day():
    result = verse_of_the_day.verse_of_the_day("./")
    assert len(result) > 0
