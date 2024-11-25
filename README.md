"# FastApiLern" 

https://habr.com/ru/companies/amvera/articles/826196/

uvicorn app.main:app --reload

ge и le в Pydantic
gt, ge, lt, le: Ограничения для числовых значений (больше, больше или равно, меньше, меньше или равно).

====================
Игры с sys.path чтобы срабатывал import от корневого каталога

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
print(sys.path)
# sys.path[0] += '\\..'

from app.database import DATABASE_URL, Base
from app.students.models import Student, Major

===============

alembic revision --autogenerate -m "Initial revision"
