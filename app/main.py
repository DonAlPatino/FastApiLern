from fastapi import FastAPI, HTTPException

from app.jsondb import add_student, upd_student, dell_student
from app.students.schemas import SStudent, SUpdateFilter, SStudentUpdate, SDeleteFilter
from app.students.router import router as router_students
from app.majors.router import router as router_majors

app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Привет, Хабр!"}


app.include_router(router_students)
app.include_router(router_majors)


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


# @app.post("/add_student")
# def add_student_handler(student: SStudent):
#     student_dict = student.dict()
#     check = add_student(student_dict)
#     if check:
#         return {"message": "Студент успешно добавлен!"}
#     else:
#         return {"message": "Ошибка при добавлении студента"}
