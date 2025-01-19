from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from ..config.database import Base


class Cpu(Base):
    __tablename__ = "Cpus"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String, unique=False, index=False, nullable=False)
    percentage = Column(String, nullable=False)
    notification_sent = Column(Boolean, default=False)
    last_updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
