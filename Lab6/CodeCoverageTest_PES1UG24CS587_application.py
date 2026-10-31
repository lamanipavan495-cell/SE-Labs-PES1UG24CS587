import pytest
from elevator_dispatch import next_direction, door_action, pick_elevator


# ---------- given examples ----------
def test_emergency_holds_doors():
    assert door_action(100, False, True) == "hold_open"

def test_idle_with_no_requests():
    assert next_direction(3, "idle", []) == "idle"


# ---------- next_direction ----------
def test_up_continues_up():
    assert next_direction(3, "up", [5]) == "up"

def test_up_reverses_down():
    assert next_direction(3, "up", [1]) == "down"

def test_up_no_requests_idle():
    assert next_direction(3, "up", []) == "idle"

def test_down_continues_down():
    assert next_direction(3, "down", [1]) == "down"

def test_down_reverses_up():
    assert next_direction(3, "down", [5]) == "up"

def test_down_no_requests_idle():
    assert next_direction(3, "down", []) == "idle"

def test_idle_goes_up():
    assert next_direction(3, "idle", [5]) == "up"

def test_idle_goes_down():
    assert next_direction(3, "idle", [1]) == "down"


# ---------- door_action ----------
def test_overload():
    assert door_action(700, False, False) == "overload"

def test_blocked_reopens():
    assert door_action(100, True, False) == "reopen"

def test_normal_close():
    assert door_action(100, False, False) == "close"


# ---------- pick_elevator ----------
def test_pick_single_busy_car():
    assert pick_elevator([("A", 2, False)], 5) == "A"