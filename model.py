from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, Integer, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from setings import DBSettings

if DBSettings.DB_KIND == "sqlite":
    engine = create_async_engine(f"sqlite+aiosqlite:///{DBSettings.DB_NAME}.db", echo=True)
else:
    engine = create_async_engine(DBSettings.uri, echo=True)
# Конфигурация базы данных
#DATABASE_URL = "sqlite+aiosqlite:///crypto_prices.db"
#engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()




# Модель для хранения данных о цене криптовалют
class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    price = Column(Float)
    timestamp = Column(DateTime)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)