import pytest
from yamconwaylib import YamConway


@pytest.fixture
def yamconway_default():
    yc = YamConway()
    yield yc
    print("Finished fixture.")


def test_yamconway_boards_exit(yamconway_default):
    assert yamconway_default.board1
    assert yamconway_default.board2


def test_yamconway_boards_size(yamconway_default):
    assert len(yamconway_default.board1) == 20
    assert len(yamconway_default.board1) == 20


def test_yamconway_stats_zero(yamconway_default):
    assert yamconway_default.stats.births == 0
    assert yamconway_default.stats.deaths == 0
