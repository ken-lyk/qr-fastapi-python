from sqlalchemy import Column, String, Enum, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..utility.enums import UserRoleEnum
from ..config.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, nullable=False, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER, nullable=False)
    disabled = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
