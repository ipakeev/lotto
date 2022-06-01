import random
from collections.abc import Iterator

from lotto import utils
from lotto.config import MINIMUM_PLAYERS, MAXIMUM_PLAYERS
from lotto.logger import logger
from lotto.players import BasePlayer, BotPlayer, UserPlayer
from lotto.ticket import LotteryTicket


class Lotto:
    players: list[BasePlayer]
    numbers: Iterator[int]

    def __init__(self):
        self.stop_game = False

    def run(self):
        self.stop_game = False
        self.create_players()
        self.init_numbers()

        winners = []
        input("Нажмите Enter, чтобы начать игру: ")
        while self.is_running():
            self.show_all_tickets()
            number = next(self.numbers)
            logger.debug(f"next number: {number}")
            print(f"Следующий боченок: {number}\n")

            for player in self.players:
                if player.is_lost:
                    continue
                player.make_decision(number)
                if player.is_won:
                    winners.append(player)

            if winners:
                break

            answer = utils.simple_choice("Играем дальше?", ["Следующий боченок", "Завершить игру"])
            if answer == "Завершить игру":
                self.stop_game = True

        self.end_game(winners)

    def is_running(self) -> bool:
        if self.stop_game:
            return False
        if all(player.is_lost for player in self.players):
            return False
        return True

    def generate_lottery_ticket(self) -> LotteryTicket:
        ticket = LotteryTicket()
        ticket.generate()
        while any(ticket == player.ticket for player in self.players):
            ticket.generate()
        return ticket

    def create_players(self):
        self.players = []

        n_players = int(utils.simple_choice(
            "Сколько всего будет игроков?",
            [str(i) for i in range(MINIMUM_PLAYERS, MAXIMUM_PLAYERS + 1)],
        ))
        logger.debug(f"n_players: {n_players}")
        n_bots = int(utils.simple_choice(
            "Сколько будет ботов?",
            [str(i) for i in range(0, n_players + 1)],
        ))
        logger.debug(f"n_bots: {n_bots}")
        n_users = n_players - n_bots

        for i in range(n_bots):
            name = f"Бот {i + 1}"
            ticket = self.generate_lottery_ticket()
            bot = BotPlayer(name, ticket)
            self.players.append(bot)
            logger.debug(f"created bot: {bot}")

        for i in range(n_users):
            name = input(f"Введите имя игрока {i + 1}: ")
            name = f"Игрок {i + 1}: {name}"
            ticket = self.generate_lottery_ticket()
            user = UserPlayer(name, ticket)
            self.players.append(user)
            logger.debug(f"created user: {user}")

    def init_numbers(self):
        numbers = list(range(1, 91))
        random.shuffle(numbers)
        self.numbers = iter(numbers)

    def show_all_tickets(self):
        utils.clear_screen()
        for player in self.players:
            print(player)

    def end_game(self, winners: list[BasePlayer]):
        self.show_all_tickets()
        if self.stop_game:
            print(f"Игра остановлена.")
        elif not winners:
            print(f"Победитель не выявлен.")
        else:
            if len(winners) == 1:
                print(f"Поздравляем победителя!")
            else:
                print(f"Поздравляем! Выявлены победители!")
            for player in winners:
                print(f"> {player.name}")
