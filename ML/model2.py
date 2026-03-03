import math

official_student_data={
    2022:905000,
    2023:111300,
    2024:1170000,
    2025:1200000,
}
base_year=2022
growth_rate=0.04
def get_student_count(year: int) -> int:
    """
    Returns student count for given year.
    Uses official data if available,
    otherwise applies growth formula.
    """

    if year in official_student_data:
        return official_student_data[year]

    last_known_year = max(official_student_data.keys())
    last_known_students = official_student_data[last_known_year]

    years_after = year - last_known_year
    estimated = last_known_students * ((1 + growth_rate) ** years_after)

    return int(estimated)
def predict_rank(percentile:float,year:int)->int:
    """
    Advance percentile to rank conversion
    """
    if percentile<0 or percentile>100:
        raise ValueError("percentile must be between 0 and 100")
    total_student=get_student_count(year)
    rank=(100-percentile)*total_student/100
    return math.ceil(rank)

