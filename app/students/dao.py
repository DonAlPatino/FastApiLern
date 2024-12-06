from sqlalchemy import select, insert, update, event, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.majors.models import Major
from app.students.models import Student


@event.listens_for(Student, 'after_insert')
def receive_after_insert(mapper, connection, target):
    major_id = target.major_id
    connection.execute(
        update(Major)
        .where(Major.id == major_id)
        .values(count_students=Major.count_students + 1)
    )


@event.listens_for(Student, 'after_delete')
def receive_after_delete(mapper, connection, target):
    major_id = target.major_id
    connection.execute(
        update(Major)
        .where(Major.id == major_id)
        .values(count_students=Major.count_students - 1)
    )


class StudentDAO(BaseDAO):
    model = Student

    @classmethod
    async def find_full_data(cls, student_id: int):
        async with async_session_maker() as session:
            # Запрос для получения информации о студенте вместе с информацией о факультете
            query = select(cls.model).options(joinedload(cls.model.major)).filter_by(id=student_id)
            result = await session.execute(query)
            student_info = result.scalar_one_or_none()

            # Если студент не найден, возвращаем None
            if not student_info:
                return None

            student_data = student_info.to_dict()
            student_data['major'] = student_info.major.major_name
            return student_data

    # Связь двух таблиц через 2 отдельных запроса
    # @classmethod
    # async def find_full_data(cls, student_id: int):
    #     async with async_session_maker() as session:
    #         # Первый запрос для получения информации о студенте
    #         query_student = select(cls.model).filter_by(id=student_id)
    #         result_student = await session.execute(query_student)
    #         student_info = result_student.scalar_one_or_none()
    #
    #         # Если студент не найден, возвращаем None
    #         if not student_info:
    #             return None
    #
    #         # Второй запрос для получения информации о специальности
    #         query_major = select(Major).filter_by(id=student_info.major_id)
    #         result_major = await session.execute(query_major)
    #         major_info = result_major.scalar_one()
    #
    #         student_data = student_info.to_dict()
    #         student_data['major'] = major_info.major_name
    #
    #         return student_data

    @classmethod
    async def add_student(cls, student_data: dict):
        async with async_session_maker() as session:
            async with session.begin():
                # # Вставка нового студента
                # stmt = insert(cls.model).values(**student_data).returning(cls.model.id, cls.model.major_id)
                # result = await session.execute(stmt)
                # new_student_id, major_id = result.fetchone()
                #
                # # # Увеличение счетчика студентов в таблице Major
                # # update_major = (
                # #     update(Major)
                # #     .where(Major.id == major_id)
                # #     .values(count_students=Major.count_students + 1)
                # # )
                # # await session.execute(update_major)
                #
                # try:
                #     await session.commit()
                # except SQLAlchemyError as e:
                #     await session.rollback()
                #     raise e

                new_student = cls.model(**student_data)
                print(new_student)
                session.add(new_student)
                await session.flush()
                new_student_id = new_student.id
                await session.commit()

                return new_student_id

    @classmethod
    async def delete_student_by_id(cls, student_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                query = select(cls.model).filter_by(id=student_id)
                result = await session.execute(query)
                student_to_delete = result.scalar_one_or_none()

                if not student_to_delete:
                    return None

                # Удаляем студента
                await session.execute(
                    delete(cls.model).filter_by(id=student_id)
                )

                await session.commit()
                return student_id

