from fastapi import APIRouter, Depends
from app.students.dao import StudentDAO
from app.students.rb import RBStudent
from app.students.schemas import SStudent, SStudentAdd

router = APIRouter(prefix='/students', tags=['Работа со студентами'])


@router.get("/", summary="Получить всех студентов")
async def get_all_students(request_body: RBStudent = Depends()) -> list[SStudent]:
    return await StudentDAO.find_all(**request_body.to_dict())


@router.get("/{student_id}", summary="Получить одного студента по id")
async def get_student_by_id(student_id: int) -> SStudent | dict:
    # Поиск без связанной таблицы Major - падает если пытаться подтянуть ее в схему
    # rez = await StudentDAO.find_one_or_none_by_id(student_id)
    rez = await StudentDAO.find_full_data(student_id)
    if rez is None:
        return {'message': f'Студент с ID {student_id} не найден!'}
    # return SStudent.model_validate(rez).model_dump()
    return rez


@router.get("/by_filter", summary="Получить одного студента по фильтру")
async def get_student_by_filter(request_body: RBStudent = Depends()) -> SStudent | dict:
    rez = await StudentDAO.find_one_or_none(**request_body.to_dict())
    if rez is None:
        return {'message': f'Студент с указанными вами параметрами не найден!'}
    return rez


@router.post("/add/")
async def add_student(student: SStudentAdd) -> dict:
    #print(**student.dict())
    check = await StudentDAO.add_student(student.dict())
    if check:
        return {"message": "Студент успешно добавлен!", "student": student}
    else:
        return {"message": "Ошибка при добавлении студента!"}


@router.delete("/dell/{student_id}")
async def dell_student_by_id(student_id: int) -> dict:
    check = await StudentDAO.delete_student_by_id(student_id=student_id)
    if check:
        return {"message": f"Студент с ID {student_id} удален!"}
    else:
        return {"message": "Ошибка при удалении студента!"}
