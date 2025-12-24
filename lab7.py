# 4. Обновить запись.
# 6. Использовать параметры запроса.
# 10. Использовать SQLAlchemy для одной таблицы.
# 5. Транзакции.
# 9. Асинхронный доступ (databases).


import asyncio
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(Integer)


DATABASE_URL = "sqlite+aiosqlite:///test.db"
engine = create_async_engine(DATABASE_URL, echo=False)

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    

    


if __name__ == "__main__":
    asyncio.run(main())