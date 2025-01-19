from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..config.database import SessionLocal
from ..models import containers_model as models
from ..schemas import containers_schema as schemas

router = APIRouter()
templates = Jinja2Templates(directory="templates")


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.get("/containers", response_class=HTMLResponse)
async def containers(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Container))
    containers = result.scalars().all()
    return templates.TemplateResponse(
        "containers.html", {"request": request, "containers": containers}
    )
