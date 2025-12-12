from typing import List, TYPE_CHECKING

from sqlalchemy import String, Integer, Boolean, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from database import Base
from models.base import BaseModelMixin

if TYPE_CHECKING:
    from models.message import Message


class User(BaseModelMixin, Base):
    __tablename__ = 'user'
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    language_code: Mapped[str] = mapped_column(String)
    is_bot: Mapped[bool] = mapped_column(Boolean)
    is_premium: Mapped[bool] = mapped_column(Boolean)

    messages: Mapped[List["Message"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    @classmethod
    async def save_user(cls, user, session):

        stmt = select(cls).where(cls.id == user.id)
        db_user = await session.scalar(stmt)

        if db_user:
            db_user.first_name = user.first_name
            db_user.last_name = user.last_name
            db_user.username = user.username
            db_user.language_code = user.language_code
            db_user.is_premium = user.is_premium
        else:
            db_user = cls(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                language_code=user.language_code,
                is_premium=user.is_premium,
            )
            session.add(db_user)

        await session.commit()
