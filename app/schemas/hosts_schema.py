from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class HostBase(BaseModel):
    hostname: str
    cpu_usage: str
    ram_total: str
    ram_usage: str
    disk_total: str
    disk_usage: str
    notification_sent: Optional[bool] = False


class HostCreate(HostBase):
    pass


class HostUpdate(HostBase):
    pass


class Host(HostBase):
    id: int
    last_updated: datetime

    class Config:
        orm_mode = True
