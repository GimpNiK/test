# 4. Обновить запись.
# 6. Использовать параметры запроса.
# 10. Использовать SQLAlchemy для одной таблицы.
# 5. Транзакции.
# 9. Асинхронный доступ (databases).


import asyncio
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import declarative_base, query
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


Base = declarative_base()
DATABASE_URL = "sqlite+aiosqlite:///test.db"
engine = create_async_engine(DATABASE_URL, echo=False)

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(Integer)




async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    

            
      
    async with AsyncSession(engine) as session:
        async with session.begin():
            if item := await session.get(Item, 1):
                await session.delete(item)
            session.add(Item(id=1, name="test", value=100))
    

    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(
                select(Item).where(Item.id == 1)
            )
            item = result.scalar_one()
            
            item.name = "updated"
            item.value = 200
    


if __name__ == "__main__":
    asyncio.run(main())
    print("Succesful")