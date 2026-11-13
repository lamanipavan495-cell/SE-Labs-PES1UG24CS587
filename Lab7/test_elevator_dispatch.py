
from hypothesis import given, strategies as st

from elevator_dispatch import (
    parse_request,
    total_travel,
    load_percent
)


# Test 1: parse_request
@given(st.text() | st.none())
def test_parse_request_no_crash(s):
    try:
        parse_request(s)
    except Exception as e:
        assert False, f"parse_request crashed with input {s!r}: {e}"


# Test 2: total_travel
@given(st.text() | st.none())
def test_total_travel_no_crash(s):
    try:
        total_travel(s)
    except Exception as e:
        assert False, f"total_travel crashed with input {s!r}: {e}"


# Test 3: load_percent
@given(st.text() | st.none())
def test_load_percent_no_crash(s):
    try:
        load_percent(s)
    except Exception as e:
        assert False, f"load_percent crashed with input {s!r}: {e}"

# Additional correctness tests

# Verify parse_request produces correct results
@given(st.integers(), st.integers())
def test_parse_request_correctness(start, end):
    result = parse_request(f"{start}->{end}")
    assert result == (start, end)


# Verify total_travel calculates the correct distance
@given(st.lists(st.integers(), min_size=1))
def test_total_travel_correctness(floors):
    csv_input = ",".join(map(str, floors))

    expected = sum(
        abs(floors[i + 1] - floors[i])
        for i in range(len(floors) - 1)
    )

    assert total_travel(csv_input) == expected


# Generate valid load and capacity combinations
@st.composite
def valid_load_inputs(draw):
    capacity = draw(st.integers(min_value=1, max_value=1000000))
    load = draw(st.integers(min_value=0, max_value=capacity))
    return load, capacity


# Verify load_percent calculates the correct percentage
@given(valid_load_inputs())
def test_load_percent_correctness(values):
    load, capacity = values

    result = load_percent(f"{load} of {capacity}")

    expected = load * 100 // capacity

    assert result == expected
