import requests


def get_students_with_param_mix(course: int, major: str, enrollment_year: int):
    url = f"http://127.0.0.1:8000/students/{course}"
    response = requests.get(url, params={"major": major, "enrollment_year": enrollment_year})
    return response.json()


students = get_students_with_param_mix(2, major=None, enrollment_year=2018)
print(students)