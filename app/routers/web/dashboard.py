from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ...config.database import SessionLocal
from ...models import containers_model as models
from ...schemas import containers_schema as schemas
from ...routers.api.containers import (
    get_container_total_running,
    get_container_total_exited,
)
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Container))
    containers = result.scalars().all()
    containers_running = await get_container_total_running(db)
    containers_exited = await get_container_total_exited(db)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "containers": containers,
            "containers_running": containers_running,
            "containers_exited": containers_exited,
        },
    )


@router.get("/containers", response_class=HTMLResponse)
async def containers(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Container))
    containers = result.scalars().all()
    return templates.TemplateResponse(
        "containers.html", {"request": request, "containers": containers}
    )
