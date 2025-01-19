from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ContainerBase(BaseModel):
    container_id: str
    hostname: str
    name: str
    status: str


class ContainerCreate(ContainerBase):
    pass


class ContainerUpdate(ContainerBase):
    pass


class Container(ContainerBase):
    id: int
    last_updated: datetime

    class Config:
        orm_mode = True
