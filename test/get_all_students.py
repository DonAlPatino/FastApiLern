import requests


def get_all_students():
    url = "http://127.0.0.1:8000/students"
    response = requests.get(url)
    return response.json()


students = get_all_students()
for i in students:
    print(i)