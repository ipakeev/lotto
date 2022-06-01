import random
from unittest import mock

import pytest

from lotto import utils
from lotto.config import Text
from lotto.players import BotPlayer, UserPlayer
from lotto.ticket import LotteryTicket


@pytest.fixture
def ticket():
    random.seed(0)
    ticket = LotteryTicket()
    ticket.generate()
    return ticket


@pytest.fixture
def bot(ticket):
    return BotPlayer("bot", ticket)


@pytest.fixture
def user(ticket):
    return UserPlayer("user", ticket)


def test_is_lost(bot):
    assert not bot.is_lost
    bot.set_lost()
    assert bot.is_lost


def test_bot_decision(bot):
    assert not bot.is_won
    for number in range(1, 91):
        bot.make_decision(number)
        string = bot.ticket.number_as_string(number)
        assert all([string not in row for row in bot.ticket.matrix])
        assert not bot.is_lost
    assert bot.is_won


@pytest.mark.parametrize("number", list(range(1, 91)))
def test_user_decision_correct(user, number):
    string = user.ticket.number_as_string(number)
    if user.ticket.is_number_exists(number):
        utils.simple_choice = mock.Mock(return_value=Text.cross_out)
        user.make_decision(number)
        utils.simple_choice.assert_called_once()
        assert all([string not in row for row in user.ticket.matrix])
        assert not user.is_lost
    else:
        utils.simple_choice = mock.Mock(return_value=Text.no_such_number)
        user.make_decision(number)
        utils.simple_choice.assert_called_once()
        assert not user.is_lost


@pytest.mark.parametrize("number", list(range(1, 91)))
def test_user_decision_fail(user, number):
    string = user.ticket.number_as_string(number)
    if user.ticket.is_number_exists(number):
        utils.simple_choice = mock.Mock(return_value=Text.no_such_number)
        user.make_decision(number)
        utils.simple_choice.assert_called_once()
        assert any([string in row for row in user.ticket.matrix])
        assert user.is_lost
    else:
        utils.simple_choice = mock.Mock(return_value=Text.cross_out)
        user.make_decision(number)
        utils.simple_choice.assert_called_once()
        assert user.is_lost
