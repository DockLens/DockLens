from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from ..config.database import Base


class Container(Base):
    __tablename__ = "containers"

    id = Column(Integer, primary_key=True, index=True)
    container_id = Column(String, unique=True, index=True, nullable=False)
    hostname = Column(String, nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    notification_sent = Column(Boolean, default=False)
    last_updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
