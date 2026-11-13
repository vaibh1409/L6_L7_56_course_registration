import re


def format_course_code(code):
    """
    Formats 'cs 301' as 'CS301'.
    Returns None if the input is not a string of exactly two words:
    letters (department) followed by digits (number).
    """
    if not isinstance(code, str):
        return None
    parts = code.split()
    if len(parts) != 2:
        return None
    dept, number = parts
    if not re.fullmatch(r"[A-Za-z]+", dept) or not re.fullmatch(r"[0-9]+", number):
        return None
    return dept.upper() + number


def total_credits(text):
    """
    Adds up comma-separated course credits.
    Returns None if the input is not a string, or if any value is empty,
    negative, or not a whole number.
    """
    if not isinstance(text, str):
        return None
    total = 0
    for credit in text.split(','):
        credit = credit.strip()
        if not re.fullmatch(r"[0-9]+", credit):
            return None
        try:
            total += int(credit)
        except ValueError:  # e.g. absurdly long digit strings
            return None
    return total


def parse_student_record(line):
    """
    Parses 'SRN|name|status' into a dictionary.
    Returns None if the input is not a string or does not have exactly
    three non-empty fields.
    """
    if not isinstance(line, str):
        return None
    parts = [p.strip() for p in line.split('|')]
    if len(parts) != 3 or not all(parts):
        return None
    return {"srn": parts[0].upper(),
            "name": parts[1],
            "status": parts[2].lower()}


def main():
    print("==== Running format_course_code ====")
    value = input("Enter a course code as DEPT NUMBER (e.g. cs 301): ")
    result = format_course_code(value)
    print("Formatted course code:", result if result is not None else "Invalid input")

    print("\n==== Running total_credits ====")
    value = input("Enter course credits separated by commas (e.g. 4,3,4): ")
    result = total_credits(value)
    print("Total credits:", result if result is not None else "Invalid input")

    print("\n==== Running parse_student_record ====")
    value = input("Enter a student record as SRN|name|status (e.g. pes1ug23cs001|Asha|regular): ")
    result = parse_student_record(value)
    print("Student record:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
