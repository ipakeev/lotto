from lotto import utils
from lotto.config import TICKET_ROW_N_SYMBOLS
from lotto.config import Text
from lotto.logger import logger
from lotto.ticket import LotteryTicket


class BasePlayer:

    def __init__(self, name: str, ticket: LotteryTicket):
        self.name = name
        self.ticket = ticket
        self._is_lost = False

    @property
    def is_won(self) -> bool:
        return self.ticket.is_winner()

    @property
    def is_lost(self) -> bool:
        return self._is_lost

    def set_lost(self):
        self._is_lost = True

    def __str__(self) -> str:
        name = f"{self.name} (проиграл)" if self.is_lost else self.name
        return name.center(TICKET_ROW_N_SYMBOLS) + "\n" + str(self.ticket)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name}, ticket)"

    def make_decision(self, number: int):
        raise NotImplementedError


class BotPlayer(BasePlayer):

    def make_decision(self, number: int):
        if self.ticket.is_number_exists(number):
            self.ticket.exclude_number(number)


class UserPlayer(BasePlayer):

    def make_decision(self, number: int):
        answer = utils.simple_choice(f"{self.name}, сделайте выбор: ",
                                     [Text.no_such_number, Text.cross_out])

        is_exists = self.ticket.is_number_exists(number)
        if is_exists:
            if answer == Text.cross_out:
                self.ticket.exclude_number(number)
            else:
                self.set_lost()
        else:
            if answer != Text.no_such_number:
                self.set_lost()
        logger.debug(f"{is_exists=}, {answer=}, is_lost={self.is_lost}")
