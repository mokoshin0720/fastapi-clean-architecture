from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKeyConstraint, PrimaryKeyConstraint, String, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Todo(Base):
    __tablename__ = 'todos'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='todos_pkey'),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    todo_detail: Mapped['TodoDetail'] = relationship('TodoDetail', uselist=False, back_populates='todo')


class TodoDetail(Base):
    __tablename__ = 'todo_details'
    __table_args__ = (
        ForeignKeyConstraint(['todo_id'], ['todos.id'], ondelete='CASCADE', name='fk_todo_details_todo_id'),
        PrimaryKeyConstraint('todo_id', name='todo_details_pkey')
    )

    todo_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    completed: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    todo: Mapped['Todo'] = relationship('Todo', back_populates='todo_detail')
