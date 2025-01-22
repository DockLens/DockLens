from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from ...config.database import SessionLocal
from ...models import hosts_model as models
from ...schemas import hosts_schema as schemas
from ...utils.telegram_notifier import send_notification
import psutil

router = APIRouter()

templates = Jinja2Templates(directory="templates")


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/cpu", response_model=schemas.Host)
async def create_or_update_host(
    host: schemas.HostCreate, db: AsyncSession = Depends(get_db)
):
    # Coba untuk mendapatkan CPU berdasarkan hostname
    result = await db.execute(
        select(models.Host)
        .where(models.Host.hostname == host.hostname)
        .execution_options(synchronize_session="fetch")
    )
    hosts = result.scalar_one_or_none()

    try:
        host.cpu_usage = float(host.cpu_usage)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid percentage value")

    if hosts:
        if host.cpu_usage > 90:
            if hosts.notification_sent:
                pass
            else:
                await send_notification(f"CPU di {host.hostname} melebihi 90%.")

        elif host.cpu_usage < 90:
            if not hosts.notification_sent:
                await send_notification(
                    f"CPU di {host.hostname} telah turun di bawah 90%. Sekarang: {host.cpu_usage}%"
                )
                hosts.notification_sent = True

        hosts.cpu_usage = host.cpu_usage
        hosts.ram_total = host.ram_total
        hosts.ram_usage = host.ram_usage
        hosts.disk_total = host.disk_total
        hosts.disk_usage = host.disk_usage

    else:
        new_host = models.Host(
            hostname=host.hostname,
            cpu_usage=host.cpu_usage,
            ram_total=host.ram_total,
            ram_usage=host.ram_usage,
            disk_total=host.disk_total,
            disk_usage=host.disk_usage,
            notification_sent=False,
        )
        db.add(new_host)
        hosts = new_host

    await db.commit()
    await db.refresh(hosts)

    print(f"hostname: {host.hostname}, percentage: {host.cpu_usage}")

    return hosts


@router.get("/cpu", response_class=HTMLResponse)
async def get_cpus_table(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Host))
    cpus = result.scalars().all()
    return templates.TemplateResponse(
        request=request,
        name="components/cpu.html",
        context={"cpus": cpus},
    )


@router.get("/agent", response_class=HTMLResponse)
async def get_cpus_table(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Host))
    hosts = result.scalars().all()
    return templates.TemplateResponse(
        request=request,
        name="components/agents/table.html",
        context={"hosts": hosts},
    )


@router.get("/cpu/bar", response_class=HTMLResponse)
async def get_cpus_table(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Host))
    cpus = result.scalars().all()

    percentage = cpus[0].percentage
    return f'<div class="progress-bar bg-info" role="progressbar" style="width: {percentage}%" aria-valuenow="{percentage}" aria-valuemin="0" aria-valuemax="100"></div>'
