from fastapi import FastAPI, Depends, HTTPException

from app.jsondb import add_student, upd_student, dell_student
from app.students.schemas import SStudent, SUpdateFilter, SStudentUpdate, SDeleteFilter
from app.students.rb import RBStudent
from app.utils import json_to_dict_list
import os
from typing import Optional, List

# path_to_json = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'students.json')
# Получаем путь к директории текущего скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))

# Переходим на уровень выше
parent_dir = os.path.dirname(script_dir)

# Получаем путь к JSON
path_to_json = os.path.join(parent_dir, 'students.json')

app = FastAPI()

@app.delete("/delete_student")
def delete_student_handler(filter_student: SDeleteFilter):
    check = dell_student(filter_student.key, filter_student.value)
    if check:
        return {"message": "Студент успешно удален!"}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при удалении студента")


@app.put("/update_student")
def update_student_handler(filter_student: SUpdateFilter, new_data: SStudentUpdate):
    check = upd_student(filter_student.dict(), new_data.dict())
    if check:
        return {"message": "Информация о студенте успешно обновлена!"}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при обновлении информации о студенте")


@app.get("/")
def home_page():
    return {"message": "Привет, Хабр!"}

@app.post("/add_student")
def add_student_handler(student: SStudent):
    student_dict = student.dict()
    check = add_student(student_dict)
    if check:
        return {"message": "Студент успешно добавлен!"}
    else:
        return {"message": "Ошибка при добавлении студента"}


@app.get("/students/{course}")
def get_all_students_course(request_body: RBStudent = Depends()) -> List[SStudent]:
    students = json_to_dict_list(path_to_json)
    filtered_students = []
    for student in students:
        if student["course"] == request_body.course:
            filtered_students.append(student)

    if request_body.major:
        filtered_students = [student for student in filtered_students if student['major'].lower() == request_body.major.lower()]

    if request_body.enrollment_year:
        filtered_students = [student for student in filtered_students if student['enrollment_year'] == request_body.enrollment_year]

    return filtered_students

# http://127.0.0.1:8000/students/1?enrollment_year=2019&major=Психология
# @app.get("/students/{course}")
# def get_all_students_course(course: int, major: Optional[str] = None, enrollment_year: Optional[int] = 2018):
#     students = json_to_dict_list(path_to_json)
#     filtered_students = []
#     for student in students:
#         if student["course"] == course:
#             filtered_students.append(student)
#
#     if major:
#         filtered_students = [student for student in filtered_students if student['major'].lower() == major.lower()]
#
#     if enrollment_year:
#         filtered_students = [student for student in filtered_students if student['enrollment_year'] == enrollment_year]
#
#     return filtered_students


@app.get("/student", response_model=SStudent)
def get_student_from_param_id(student_id: int):
    students = json_to_dict_list(path_to_json)
    for student in students:
        if student["student_id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/students")
def get_all_students(course: Optional[int] = None):
    students = json_to_dict_list(path_to_json)
    if course is None:
        return students
    else:
        return_list = []
        for student in students:
            if student["course"] == course:
                return_list.append(student)
        return return_list



# @app.get("/students/{course}")
# def get_all_students_course(course: int):
#     students = json_to_dict_list(path_to_json)
#     return_list = []
#     for student in students:
#         if student["course"] == course:
#             return_list.append(student)
#     return return_list
