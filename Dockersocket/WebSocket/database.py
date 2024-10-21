from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


engine = create_async_engine("sqlite+aiosqlite:///./data/site.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class TaskModel(Model):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    complete: Mapped[bool]
