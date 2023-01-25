import pytest
from bls_bible.lib.leaderboard import LeaderBoard


class TestLeaderboard:

	def __init__(self):
		self.repo = "blacklanternsecurity/bls-bible"
		self.token = "notarealtoken"


@pytest.fixture
def lb_test():
	return TestLeaderboard()


@pytest.fixture
def lb_board():
	return {}


def test_get_leader_board(lb_test):
	result = LeaderBoard.getLeaderBoard(lb_test)
	assert result is not None


def test_get_leader_board_ui(lb_test, lb_board):
	result = LeaderBoard.getLeaderBoardUI(lb_test, lb_board)
	assert result is not None
