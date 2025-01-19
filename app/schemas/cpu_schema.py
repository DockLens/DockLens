from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CpuBase(BaseModel):
    hostname: str
    percentage: str
    notification_sent: Optional[bool] = False


class CpuCreate(CpuBase):
    pass


class CpuUpdate(CpuBase):
    pass


class Cpu(CpuBase):
    id: int
    last_updated: datetime

    class Config:
        orm_mode = True
