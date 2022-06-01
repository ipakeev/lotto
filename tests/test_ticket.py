import pytest

from lotto import config
from lotto.ticket import LotteryTicket


@pytest.fixture
def ticket():
    ticket = LotteryTicket()
    ticket.generate()
    return ticket


class TestTicket:

    def test_all_numbers(self, ticket):
        expected_n_numbers = config.TICKET_N_ROWS * config.TICKET_N_NUMBERS_PER_ROW
        assert len(ticket.all_numbers) == expected_n_numbers
        assert len(set(ticket.all_numbers)) == expected_n_numbers

    def test_matrix_size(self, ticket):
        assert len(ticket.matrix) == config.TICKET_N_ROWS
        for row in ticket.matrix:
            assert len(row) == config.TICKET_N_COLUMNS

    def test_matrix_numbers(self, ticket):
        all_numbers = []
        for row in ticket.matrix:
            numbers = [int(i) for i in row if i not in [
                ticket.EMPTY_POSITION, ticket.EXCLUDED_POSITION
            ]]
            assert len(numbers) == config.TICKET_N_NUMBERS_PER_ROW
            all_numbers.extend(numbers)

        expected_n_numbers = config.TICKET_N_ROWS * config.TICKET_N_NUMBERS_PER_ROW
        assert len(all_numbers) == expected_n_numbers
        assert len(set(all_numbers)) == expected_n_numbers

    def test_equality(self, ticket):
        other_ticket = LotteryTicket()
        other_ticket.generate()
        assert ticket != other_ticket

        other_ticket.all_numbers = ticket.all_numbers[:]
        assert ticket == other_ticket

        with pytest.raises(TypeError):
            _ = ticket != 1

    @pytest.mark.parametrize("number, string", [
        (1, " 1"),
        (10, "10"),
        (90, "90"),
    ])
    def test_number_as_string(self, number, string):
        assert LotteryTicket.number_as_string(number) == string

    def test_is_winner(self, ticket):
        def mark_excluded(row):
            for i in range(config.TICKET_N_COLUMNS):
                if row[i] == ticket.EMPTY_POSITION or row[i] == ticket.EXCLUDED_POSITION:
                    continue
                row[i] = ticket.EXCLUDED_POSITION

        assert not ticket.is_winner()

        mark_excluded(ticket.matrix[0])
        assert not ticket.is_winner()

        for row_index in range(1, config.TICKET_N_ROWS):
            mark_excluded(ticket.matrix[row_index])
        assert ticket.is_winner()

    def test_is_number_exists(self, ticket):
        for number in range(1, 91):
            if number in ticket.all_numbers:
                assert ticket.is_number_exists(number)
            else:
                assert not ticket.is_number_exists(number)

    def test_exclude_number(self, ticket):
        for row_index in range(config.TICKET_N_ROWS):
            for column_index in range(config.TICKET_N_COLUMNS):
                value = ticket.matrix[row_index][column_index]
                if value == ticket.EMPTY_POSITION:
                    continue
                assert value != ticket.EXCLUDED_POSITION
                ticket.exclude_number(int(value))
                assert ticket.matrix[row_index][column_index] == ticket.EXCLUDED_POSITION
