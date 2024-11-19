import requests


def get_students_with_param_path(course: int):
    url = f"http://127.0.0.1:8000/students/{course}"
    response = requests.get(url)
    return response.json()


students = get_students_with_param_path(2)
for student in students:
    print(student)