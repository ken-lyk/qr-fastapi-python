from sqlalchemy import Column, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..config.database import Base
 
class QR(Base):
    __tablename__ = "qr"
    id = Column(String, primary_key=True, nullable=False, unique=True)
    path = Column(Text, nullable=False, default='')
    data = Column(Text, nullable=False)
    source = Column(String, nullable=False)
    disabled = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    user_id = Column(String, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User")
