import os


GRADE_BANDS: list[tuple[int, str, float]] = [
    (85, "A", 4.0),
    (80, "A-", 3.7),
    (75, "B+", 3.3),
    (70, "B", 3.0),
    (65, "B-", 2.7),
    (61, "C+", 2.3),
    (58, "C", 2.0),
    (55, "C-", 1.7),
    (50, "D", 1.0),
    (0, "F", 0.0),
]


COURSES: dict[int, list[tuple[str, str, float]]] = {
    1: [
        ("MS-251", "Probability & Statistics", 3.0),
        ("GE-160", "Applications of ICT", 3.0),
        ("GE-169", "Applied Physics", 3.0),
        ("GE-167", "Discrete Structures", 3.0),
        ("HQ-001", "Quran Translation - I", 0.5),
        ("GE-190", "Functional English", 3.0),
    ],
    2: [
        ("CC-112", "Programming Fundamentals", 3.0),
        ("CC-112-L", "Programming Fundamentals Lab", 1.0),
        ("CC-110", "Digital Logic Design", 2.0),
        ("CC-110-L", "Digital Logic Design Lab", 1.0),
        ("MS-252", "Linear Algebra", 3.0),
        ("GE-191", "Expository Writing", 3.0),
        ("GE-163", "Islamic Studies", 2.0),
        ("HQ-002", "Quran Translation - II", 0.5),
    ],
    3: [
        ("CC-211", "Object Oriented Programming", 3.0),
        ("CC-211-L", "Object Oriented Programming Lab", 1.0),
        ("CC-215", "Database Systems", 3.0),
        ("CC-215-L", "Database Systems Lab", 1.0),
        ("CC-210", "Computer Organization & Assembly Language", 3.0),
        ("GE-162", "Calculus & Analytical Geometry", 3.0),
        ("GE-192", "Introduction to Management", 2.0),
        ("HQ-003", "Quran Translation - III", 0.5),
    ],
    4: [
        ("CC-213", "Data Structures", 3.0),
        ("CC-213-L", "Data Structures Lab", 1.0),
        ("CC-312", "Information Security", 3.0),
        ("CC-214", "Computer Networks", 3.0),
        ("CC-212", "Software Engineering", 3.0),
        ("DC-220", "Advanced Database Management Systems", 3.0),
        ("HQ-004", "Quran Translation - IV", 0.5),
    ],
    5: [
        ("CC-313", "Analysis of Algorithms", 3.0),
        ("CC-310", "Artificial Intelligence", 3.0),
        ("DC-320", "Theory of Automata and Formal Languages", 3.0),
        ("DC-321", "Human Computer Interaction", 3.0),
        ("DC-322", "Computer Architecture", 3.0),
        ("EC-330", "Web Technologies / Elective", 3.0),
        ("HQ-005", "Quran Translation - V", 0.5),
    ],
    6: [
        ("CC-311", "Operating Systems", 3.0),
        ("EC-333", "Mobile Application Development / Elective", 3.0),
        ("EC-324", "Software Construction & Development / Elective", 3.0),
        ("EC-335", "Machine Learning / Elective", 3.0),
        ("EC-334", "Game Design and Development / Elective", 3.0),
        ("MS-253", "Multivariable Calculus", 3.0),
        ("HQ-006", "Quran Translation - VI", 0.5),
    ],
    7: [
        ("CC-411", "Final Year Project - I", 2.0),
        ("DC-328", "Parallel & Distributed Computing", 3.0),
        ("EC-345", "Computer Vision / Elective", 3.0),
        ("EC-425", "Software Quality Engineering / Elective", 3.0),
        ("MS-254", "Technical and Business Writing", 3.0),
        ("GE-263", "Entrepreneurship", 2.0),
        ("GE-262", "Professional Practices", 2.0),
        ("HQ-007", "Quran Translation - VII", 0.5),
    ],
    8: [
        ("CC-412", "Final Year Project - II", 4.0),
        ("DC-421", "Compiler Construction", 3.0),
        ("UE-272", "Introduction to Marketing", 3.0),
        ("GE-168", "Ideology and Constitution of Pakistan", 2.0),
        ("GE-363", "Civics and Community Engagement", 2.0),
        ("HQ-008", "Quran Translation - VIII", 0.5),
    ],
}


def _semester_total(semester: int) -> float:
    return sum(ch for _, _, ch in COURSES[semester])


def marks_to_grade_points(marks: int) -> float:
    """Convert a numeric mark (0-100) for a single course into a PUCIT
    grade point, e.g. 85 -> 4.0, 72 -> 3.0.

    Use this the moment the user gives you raw marks for a course (e.g.
    "I got 78 in AI") and you need the grade point before it can be fed
    into calculate_semester_gpa. Call it once per course/mark.

    Returns a plain error string, not an exception, if marks is out of
    the valid 0-100 range.
    """
    if marks < 0 or marks > 100:
        return "Error: marks must be between 0 and 100"
    return next(points for threshold, points in GRADE_BANDS if marks >= threshold)


def calculate_semester_gpa(
    grade_points: list[float], credit_hours: list[float]
) -> float:
    """Calculate a single semester's credit-hour-weighted GPA from a list
    of grade points and the matching list of credit hours, using
    GPA = Σ(grade_point × credit_hours) / Σ(credit_hours).

    Use this once you have a grade point (from marks_to_grade_points, or
    given directly by the user) and the credit hours for every course
    the student took that semester. The two lists must be the same
    length and in the same order (grade_points[i] goes with
    credit_hours[i]). Exclude Math Deficiency courses (MD-001, MD-002)
    entirely — they are pass/fail and never enter a GPA.

    Returns a plain error string if the lists are empty, of different
    lengths, or contain a negative/invalid value.
    """
    if not grade_points or not credit_hours:
        return "Error: grade_points and credit_hours must not be empty"
    if len(grade_points) != len(credit_hours):
        return "Error: grade_points and credit_hours must be the same length"
    if any(gp < 0.0 or gp > 4.0 for gp in grade_points):
        return "Error: grade points must be between 0.0 and 4.0"
    if any(ch <= 0 for ch in credit_hours):
        return "Error: credit hours must be positive"
    total_ch = sum(credit_hours)
    weighted = sum(gp * ch for gp, ch in zip(grade_points, credit_hours))
    return round(weighted / total_ch, 3)


def calculate_new_cgpa(
    current_cgpa: float,
    completed_credit_hours: float,
    semester_gpa: float,
    semester_credit_hours: float,
) -> float:
    """Project a student's new CGPA after adding one more semester, using
    new CGPA = (current_cgpa × completed_ch + semester_gpa × semester_ch)
    / (completed_ch + semester_ch).

    Use this when the user already has a current CGPA and completed
    credit-hour count, and wants to know where a semester GPA (actual or
    hypothetical) would leave their overall CGPA. Never guess any of the
    four inputs — ask for whichever the user hasn't given you, EXCEPT for
    a Semester 1 student: they have no previous record, so pass
    current_cgpa=0.0 and completed_credit_hours=0.0 and do not ask.

    Returns a plain error string for out-of-range GPAs (must be 0.0-4.0)
    or non-positive credit-hour values.
    """
    if not (0.0 <= current_cgpa <= 4.0):
        return "Error: current_cgpa must be between 0.0 and 4.0"
    if not (0.0 <= semester_gpa <= 4.0):
        return "Error: semester_gpa must be between 0.0 and 4.0"
    if completed_credit_hours < 0:
        return "Error: completed_credit_hours cannot be negative"
    if semester_credit_hours <= 0:
        return "Error: semester_credit_hours must be positive"
    new_cgpa = (
        current_cgpa * completed_credit_hours
        + semester_gpa * semester_credit_hours
    ) / (completed_credit_hours + semester_credit_hours)
    return round(new_cgpa, 3)


def required_gpa_for_target(
    target_cgpa: float,
    current_cgpa: float,
    completed_credit_hours: float,
    remaining_credit_hours: float,
) -> float:
    """Calculate the GPA needed over the remaining credit hours to reach
    a target CGPA, using required GPA = (target_cgpa × (completed_ch +
    remaining_ch) − current_cgpa × completed_ch) / remaining_ch.

    Use this when the user states (or has already given you) a target
    CGPA, their current CGPA, completed credit hours, and the number of
    remaining credit hours the target must be reached over. For a
    Semester 1 student pass current_cgpa=0.0 and completed_credit_hours=0.0
    and do not ask for them.

    A result above 4.0 is mathematically correct but impossible: do not
    present it as an answer. Call this tool again with a larger
    remaining_credit_hours (from get_remaining_credit_hours) until the
    result is 4.0 or below.

    Returns a plain error string if remaining_credit_hours is not
    positive or the CGPA values are out of the 0.0-4.0 range.
    """
    if not (0.0 <= target_cgpa <= 4.0):
        return "Error: target_cgpa must be between 0.0 and 4.0"
    if not (0.0 <= current_cgpa <= 4.0):
        return "Error: current_cgpa must be between 0.0 and 4.0"
    if completed_credit_hours < 0:
        return "Error: completed_credit_hours cannot be negative"
    if remaining_credit_hours <= 0:
        return "Error: remaining_credit_hours must be positive"
    total_ch = completed_credit_hours + remaining_credit_hours
    required = (
        target_cgpa * total_ch - current_cgpa * completed_credit_hours
    ) / remaining_credit_hours
    return round(required, 3)


def get_semester_courses(semester: int) -> str:
    """Return the list of graded courses and their credit hours for one
    semester (1-8) of the PUCIT BS(CS) scheme of studies, e.g. for
    checking what a student is/was enrolled in, or getting the credit
    hours needed for calculate_semester_gpa.

    Math Deficiency courses (MD-001, MD-002) are never included — they
    are non-credit, pass/fail, and outside this scheme.

    Returns a plain error string if semester is not between 1 and 8.
    """
    if semester not in COURSES:
        return "Error: semester must be between 1 and 8"
    lines = [f"Semester {semester} courses:"]
    for code, title, ch in COURSES[semester]:
        lines.append(f"  {code} - {title}: {ch} credit hours")
    lines.append(f"  Total: {_semester_total(semester)} credit hours")
    return "\n".join(lines)


def get_remaining_credit_hours(current_semester: int, through_semester: int = 8) -> float:
    """Total the graded credit hours across a range of semesters, from
    current_semester through through_semester inclusive (through_semester
    defaults to 8, the last semester, if you don't pass it).

    Use this to find out how many credit hours a semester (or a run of
    semesters) is worth, WITHOUT doing the addition yourself. This is
    exactly the tool for widening an unreachable target: to
    check "semester 5 only" call get_remaining_credit_hours(5, 5); to
    widen to "semesters 5 through 6" call get_remaining_credit_hours(5, 6);
    then (5, 7); and so on, feeding each result into
    required_gpa_for_target until the required GPA is <= 4.0.

    Returns a plain error string if either semester is outside 1-8, or
    current_semester is greater than through_semester.
    """
    if current_semester not in COURSES or through_semester not in COURSES:
        return "Error: semester must be between 1 and 8"
    if current_semester > through_semester:
        return "Error: current_semester cannot be greater than through_semester"
    total = sum(_semester_total(s) for s in range(current_semester, through_semester + 1))
    return total


def save_report(filename: str, content: str) -> str:
    """Save a text summary (e.g. a semester GPA result, a projected CGPA,
    or a plan for reaching a target) to a file the student can keep.

    Only call this after producing something worth saving, and only when
    the user has actually asked you to save it — never save
    automatically, and never after just a clarifying question or a
    single grade lookup.

    Returns a plain error string if filename is empty or content is
    empty; otherwise returns a confirmation with the saved path.
    """


    name = os.path.basename(filename.strip())
    if not name:
        return "Error: filename must not be empty"
    if not content.strip():
        return "Error: content must not be empty"
    if not name.endswith(".txt"):
        name += ".txt"
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    path = os.path.join(reports_dir, name)
    try:
        os.makedirs(reports_dir, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except (OSError, ValueError) as e:
        return f"Error: could not save the report ({e})"
    return f"Saved report to {path}"


ALL_TOOLS = [
    marks_to_grade_points,
    calculate_semester_gpa,
    calculate_new_cgpa,
    required_gpa_for_target,
    get_semester_courses,
    get_remaining_credit_hours,
    save_report,
]
