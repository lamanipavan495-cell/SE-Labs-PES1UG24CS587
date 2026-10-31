import pytest
from elevator_dispatch import next_direction, door_action, pick_elevator


# ---------- given examples ----------
def test_emergency_holds_doors():
    assert door_action(100, False, True) == "hold_open"

def test_idle_with_no_requests():
    assert next_direction(3, "idle", []) == "idle"


# ---------- next_direction: every if True and False ----------
@pytest.mark.parametrize("current, direction, requests, expected", [
    (3, "up", [5], "up"),
    (3, "up", [1], "down"),
    (3, "up", [], "idle"),
    (3, "up", [3], "idle"),
    (3, "up", [1, 5], "up"),
    (3, "down", [1], "down"),
    (3, "down", [5], "up"),
    (3, "down", [], "idle"),
    (3, "down", [1, 5], "down"),
    (3, "idle", [5], "up"),
    (3, "idle", [1], "down"),
    (3, "idle", [], "idle"),
    (3, "idle", [1, 5], "up"),
    (3, "sideways", [5], "up"),
])
def test_next_direction(current, direction, requests, expected):
    assert next_direction(current, direction, requests) == expected


# ---------- door_action: every if True and False ----------
@pytest.mark.parametrize("load, blocked, emergency, expected", [
    (100, False, True, "hold_open"),
    (700, False, True, "hold_open"),
    (700, False, False, "overload"),
    (631, False, False, "overload"),
    (630, False, False, "close"),
    (100, True, False, "reopen"),
    (700, True, False, "overload"),
    (100, False, False, "close"),
])
def test_door_action(load, blocked, emergency, expected):
    assert door_action(load, blocked, emergency) == expected


# ---------- pick_elevator: loop and every if True and False ----------
def test_pick_no_cars():
    assert pick_elevator([], 5) is None

def test_pick_single_busy_car():
    assert pick_elevator([("A", 2, False)], 5) == "A"

def test_pick_single_idle_car():
    assert pick_elevator([("A", 2, True)], 5) == "A"

def test_pick_closer_car_wins():
    cars = [("A", 10, True), ("B", 4, True)]
    assert pick_elevator(cars, 5) == "B"

def test_pick_first_car_stays_best():
    cars = [("A", 4, True), ("B", 10, True)]
    assert pick_elevator(cars, 5) == "A"

def test_pick_busy_penalty_loses_to_farther_idle():
    cars = [("A", 5, False), ("B", 8, True)]
    assert pick_elevator(cars, 5) == "B"

def test_pick_tie_keeps_first():
    cars = [("A", 3, True), ("B", 7, True)]
    assert pick_elevator(cars, 5) == "A"