from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from ...config.database import SessionLocal
from ...models import containers_model as models
from ...schemas import containers_schema as schemas
from ...utils.telegram_notifier import send_notification
import psutil

router = APIRouter()

templates = Jinja2Templates(directory="templates")


async def get_db():
    async with SessionLocal() as session:
        yield session


## Total running containers
async def get_container_total_running(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Container).where(models.Container.status == "running")
    )

    total = result.scalars().all()
    return len(total)


## Total exited containers
async def get_container_total_exited(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Container).where(models.Container.status != "running")
    )

    total = result.scalars().all()
    return len(total)


@router.post("/status", response_model=schemas.Container)
async def create_or_update_container(
    container: schemas.ContainerCreate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(models.Container).where(
            models.Container.container_id == container.container_id
        )
    )
    db_container = result.scalar_one_or_none()
    if db_container:
        if (
            db_container.status != container.status
            and container.status.lower() != "running"
        ):
            await send_notification(
                f"Container {db_container.name} ({db_container.container_id}) mati."
            )
        db_container.status = container.status
    else:
        new_container = models.Container(
            container_id=container.container_id,
            hostname=container.hostname,
            name=container.name,
            status=container.status,
        )
        db.add(new_container)
    await db.commit()
    await db.refresh(db_container if db_container else new_container)
    return db_container if db_container else new_container


@router.get("/status", response_class=HTMLResponse)
async def get_containers_table(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Container))
    containers = result.scalars().all()
    return templates.TemplateResponse(
        request=request, name="table.html", context={"containers": containers}
    )
