from adventure.story import step
import pytest

@pytest.mark.parametrize(
    # fmt: off
    "input_str, expected_output",
    [
        ('Right', 'still'),
        ('right', 'right'),
        ('RIGHT',  'still'),
        ('Left', 'still'),
        ('left', 'left'),
        ('LEFT',  'still'),
    ],
    # fmt: on
)
def test_step(input_str, expected_output):
    result = step(input_str, ["event1", "event2"])
    assert expected_output in result.lower()

