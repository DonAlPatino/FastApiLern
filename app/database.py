from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


# from app.config import get_db_url

DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'fast_api'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


# DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)





