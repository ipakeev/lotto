import pytest

from lotto.utils import sorted_random_subarray


@pytest.fixture
def array():
    return list(range(10))


@pytest.mark.parametrize("length", [
    *list(range(11))
])
def test_sorted_random_subarray(array, length: int):
    subarray = sorted_random_subarray(array, length)
    assert len(subarray) == length
    assert len(set(subarray)) == length


def test_sorted_random_subarray_raises(array):
    with pytest.raises(AssertionError):
        sorted_random_subarray(array, -1)
    with pytest.raises(AssertionError):
        sorted_random_subarray(array, 11)
