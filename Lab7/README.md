# Lab 7 – Fuzz Testing: Elevator Dispatch

## Objective
To identify and fix input validation bugs in the elevator dispatch application using property-based fuzz testing with the Hypothesis library.

## Technologies Used
- Python 3.13
- Hypothesis
- Pytest

## Project Files

| File | Description |
|---|---|
| elevator_dispatch.py | Elevator dispatch application |
| test_elevator_dispatch.py | Hypothesis fuzz and correctness tests |
| screenshots/ | Screenshots of execution and testing |

## Functions Tested

1. `parse_request(text)` – Parses elevator floor requests.
2. `total_travel(floors_csv)` – Calculates total travel distance.
3. `load_percent(text)` – Calculates elevator load percentage.

## Bugs Identified

Fuzz testing identified:
- Invalid and missing elevator request values.
- Empty and malformed floor lists.
- Invalid load and capacity values.
- Unexpected `None` inputs.
- Division by zero and invalid load ranges.

## Fixes Implemented

- Added input type validation.
- Added format and empty-value checks.
- Added integer conversion error handling.
- Added capacity and load range validation.
- Invalid inputs return `None` instead of crashing.

## Testing

Six Hypothesis tests were executed:
- Three no-crash tests.
- Three correctness tests.

### Final Test Results

**6 passed in 1.47 seconds.**

## Conclusion

Hypothesis successfully identified edge-case input validation bugs in the original elevator dispatch application. Defensive validation was implemented, and the corrected application passed all six automated tests.