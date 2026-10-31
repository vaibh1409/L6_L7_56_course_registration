import pytest
from course_registration import can_register, waitlist_position, late_fee


# ---------- can_register ----------
def test_registered():
    assert can_register("regular", 20, 4, True) == "registered"

@pytest.mark.parametrize("status,limit", [("regular", 24), ("probation", 16), ("honors", 28)])
def test_registered_exactly_at_limit(status, limit):
    # boundary: current + course == max  -> NOT exceeded
    assert can_register(status, limit - 3, 3, True) == "registered"

def test_unknown_status():
    with pytest.raises(ValueError, match="unknown status"):
        can_register("alumni", 10, 4, True)

def test_invalid_course_credits_zero():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, 0, True)

def test_invalid_course_credits_negative():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, -2, True)

def test_prerequisites_missing():
    assert can_register("regular", 10, 4, False) == "prerequisites missing"

def test_credit_limit_exceeded_by_one():
    assert can_register("honors", 26, 3, True) == "credit limit exceeded"

def test_probation_limit_exceeded():
    assert can_register("probation", 14, 4, True) == "credit limit exceeded"


# ---------- waitlist_position ----------
def test_seat_available():
    assert waitlist_position(30, 40, 0) == 0

def test_invalid_capacity_zero():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(0, 0, 0)

def test_invalid_capacity_negative():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(5, -1, 0)

def test_last_seat_available():
    assert waitlist_position(39, 40, 0) == 0

def test_class_exactly_full_empty_waitlist():
    assert waitlist_position(40, 40, 0) == 1

def test_waitlist_one_below_limit():
    assert waitlist_position(40, 40, 9) == 10

def test_waitlist_exactly_full():
    assert waitlist_position(40, 40, 10) == -1

def test_waitlist_over_full():
    assert waitlist_position(45, 40, 15) == -1


# ---------- late_fee ----------
def test_zero_days_late():
    assert late_fee(0, 15, False) == 0

def test_negative_days_late():
    assert late_fee(-3, 15, False) == 0

def test_waiver_applied():
    assert late_fee(5, 15, True) == 0

def test_one_day_late():
    assert late_fee(1, 15, False) == 500

def test_exactly_seven_days_late():
    assert late_fee(7, 15, False) == 500

def test_eight_days_late():
    assert late_fee(8, 15, False) == 600

def test_credits_exactly_20_no_surcharge():
    assert late_fee(5, 20, False) == 500

def test_credits_21_surcharge():
    assert late_fee(5, 21, False) == 750

def test_fee_exactly_2000_not_capped():
    assert late_fee(22, 20, False) == 2000

def test_fee_just_over_2000_capped():
    assert late_fee(23, 20, False) == 2000

def test_fee_capped_with_surcharge():
    assert late_fee(40, 25, False) == 2000
