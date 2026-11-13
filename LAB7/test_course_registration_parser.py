from hypothesis import given, strategies as st
from course_registration_parser import format_course_code, total_credits, parse_student_record


@given(st.text() | st.none())
def test_format_course_code_no_crash(s):
    try:
        format_course_code(s)
    except Exception as e:
        assert False, f"format_course_code crashed with: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_total_credits_no_crash(s):
    try:
        total_credits(s)
    except Exception as e:
        assert False, f"total_credits crashed with: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_parse_student_record_no_crash(s):
    try:
        parse_student_record(s)
    except Exception as e:
        assert False, f"parse_student_record crashed with: {type(e).__name__}: {e}"


# ---- extra: fuzz with other input types, and check valid input still works ----
@given(st.one_of(st.integers(), st.floats(), st.lists(st.integers()), st.binary(), st.booleans()))
def test_all_functions_non_string_no_crash(x):
    for f in (format_course_code, total_credits, parse_student_record):
        try:
            f(x)
        except Exception as e:
            assert False, f"{f.__name__} crashed on {x!r} with: {type(e).__name__}: {e}"


def test_valid_inputs_still_work():
    assert format_course_code("cs 301") == "CS301"
    assert total_credits("4,3,4") == 11
    assert parse_student_record("pes1ug23cs001|Asha|Regular") == {
        "srn": "PES1UG23CS001", "name": "Asha", "status": "regular"}
