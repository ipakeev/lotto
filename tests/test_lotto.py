from unittest import mock

import pytest

from lotto import utils
from lotto.lotto import Lotto
from lotto.players import BotPlayer, UserPlayer


@pytest.fixture
def game():
    return Lotto()


class TestLotto:

    def test_create_players(self, game):
        utils.simple_choice = mock.Mock(side_effect=[4, 3])
        with mock.patch("builtins.input"):
            game.create_players()
        assert utils.simple_choice.call_count == 2
        assert len(game.players) == 4
        assert sum(isinstance(i, BotPlayer) for i in game.players) == 3
        assert sum(isinstance(i, UserPlayer) for i in game.players) == 1

    def test_is_running(self, game):
        utils.simple_choice = mock.Mock(side_effect=[4, 3])
        with mock.patch("builtins.input"):
            game.create_players()

        assert game.is_running()

        game.stop_game = True
        assert not game.is_running()

        game.stop_game = False
        for i in range(len(game.players) - 1):
            game.players[i].set_lost()
            assert game.is_running()
        game.players[-1].set_lost()
        assert not game.is_running()
