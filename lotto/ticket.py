from lotto.config import TICKET_N_ROWS, TICKET_N_COLUMNS, TICKET_N_NUMBERS_PER_ROW, TICKET_ROW_N_SYMBOLS
from lotto.utils import sorted_random_subarray


class LotteryTicket:
    """
    Лотерейный билет.
    Для удобства все значения в лотерейном билете представлены в виде строки.
    """

    EMPTY_POSITION = "  "
    EXCLUDED_POSITION = "><"

    all_numbers: list[int]
    matrix: list[list[str]]

    def __str__(self) -> str:
        row_separator = "|" + "+".join("--" for _ in range(TICKET_N_COLUMNS)) + "|\n"

        row_texts = []
        for row in self.matrix:
            row_texts.append("|" + "|".join(row) + "|\n")

        text = ""
        text += "-" * TICKET_ROW_N_SYMBOLS + "\n"
        text += row_separator.join(row_texts)
        text += "-" * TICKET_ROW_N_SYMBOLS + "\n"
        return text

    def __eq__(self, other: "LotteryTicket") -> bool:
        if not isinstance(other, LotteryTicket):
            raise TypeError("Type must by LotteryTicket.")
        return self.all_numbers == other.all_numbers

    def generate(self) -> None:
        # создаем необходимое количество уникальных случайных чисел от 1 до 90
        self.all_numbers = sorted_random_subarray(range(1, 91), TICKET_N_ROWS * TICKET_N_NUMBERS_PER_ROW)

        self.matrix = []
        for row_index in range(TICKET_N_ROWS):
            # создаем случайные индексы для чисел в строке
            indices = sorted_random_subarray(range(TICKET_N_COLUMNS), TICKET_N_NUMBERS_PER_ROW)

            # выбираем числа для строки и создаем итератор
            numbers = iter(self.all_numbers[row_index::TICKET_N_ROWS])

            row = [self.number_as_string(next(numbers)) if i in indices else self.EMPTY_POSITION
                   for i in range(TICKET_N_COLUMNS)]
            self.matrix.append(row)

    @staticmethod
    def number_as_string(number: int) -> str:
        return f"{number:>2}"

    def is_winner(self) -> bool:
        return all(
            value == self.EMPTY_POSITION or value == self.EXCLUDED_POSITION
            for row in self.matrix
            for value in row
        )

    def is_number_exists(self, number: int) -> bool:
        number_as_string = self.number_as_string(number)
        return any(number_as_string in row for row in self.matrix)

    def exclude_number(self, number: int) -> None:
        number_as_string = self.number_as_string(number)
        for row in self.matrix:
            for index in range(len(row)):
                if row[index] == number_as_string:
                    row[index] = self.EXCLUDED_POSITION
                    return
