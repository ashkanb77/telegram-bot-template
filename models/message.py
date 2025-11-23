from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, DateTime, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from .base import BaseModelMixin

if TYPE_CHECKING:
    from models.user import User


class Message(BaseModelMixin, Base):
    __tablename__ = "message"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    user: Mapped["User"] = relationship(back_populates="messages")

    content: Mapped[str] = mapped_column(String, nullable=False)

    answer: Mapped[str] = mapped_column(String, nullable=True)
    answered_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())
