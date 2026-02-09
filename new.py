from datetime import date
from typing import Optional
from sqlalchemy import create_engine, String, Text, select, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass
