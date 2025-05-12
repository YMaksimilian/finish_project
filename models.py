from sqlalchemy.orm import Mapped, mapped_column
from db import engine, Base
from datetime import datetime
from sqlalchemy import Date, func



class Expenses(Base):
    __tablename__ = "expenses" # назначаем имя таблицы
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime]
    sum: Mapped[float]
    source: Mapped[str] = mapped_column(nullable=True)
    creation_time: Mapped[Date] = mapped_column(Date, server_default=func.now())

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)