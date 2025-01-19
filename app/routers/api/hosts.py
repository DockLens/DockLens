from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from ...config.database import SessionLocal
from ...models import cpu_model as models
from ...schemas import cpu_schema as schemas
from ...utils.telegram_notifier import send_notification
import psutil

router = APIRouter()

templates = Jinja2Templates(directory="templates")


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/cpu", response_model=schemas.Cpu)
async def create_or_update_Cpu(
    cpu: schemas.CpuCreate, db: AsyncSession = Depends(get_db)
):
    # Coba untuk mendapatkan CPU berdasarkan hostname
    result = await db.execute(
        select(models.Cpu)
        .where(models.Cpu.hostname == cpu.hostname)
        .execution_options(synchronize_session="fetch")
    )
    db_cpu = result.scalar_one_or_none()

    try:
        cpu.percentage = float(cpu.percentage)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid percentage value")

    if db_cpu:
        # Jika CPU melebihi 90%, kirimkan notifikasi
        if cpu.percentage > 90:
            if db_cpu.notification_sent:
                # Jika notifikasi sudah dikirim, jangan kirim lagi
                pass
            else:
                await send_notification(f"CPU di {db_cpu.hostname} melebihi 90%.")
                db_cpu.notification_sent = True  # Tandai notifikasi sudah dikirim

        # Jika CPU turun di bawah 90%, kirimkan notifikasi sekali
        elif cpu.percentage < 90:
            if not db_cpu.notification_sent:
                await send_notification(
                    f"CPU di {db_cpu.hostname} telah turun di bawah 90%. Sekarang: {cpu.percentage}%"
                )
                db_cpu.notification_sent = True  # Tandai notifikasi sudah dikirim

        db_cpu.percentage = cpu.percentage
    else:
        new_cpu = models.Cpu(
            hostname=cpu.hostname,
            percentage=cpu.percentage,
            notification_sent=False,  # Saat pertama kali, notifikasi belum dikirim
        )
        db.add(new_cpu)
        db_cpu = new_cpu

    await db.commit()
    await db.refresh(db_cpu)

    print(f"hostname: {cpu.hostname}, percentage: {cpu.percentage}")

    return db_cpu


@router.get("/cpu", response_class=HTMLResponse)
async def get_cpus_table(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Cpu))
    cpus = result.scalars().all()  # Perbaikan pada penamaan variabel
    return templates.TemplateResponse(
        request=request,
        name="components/cpu.html",  # Menggunakan 'filename' alih-alih 'name'
        context={"cpus": cpus},
    )


@router.get("/cpu/bar", response_class=HTMLResponse)
async def get_cpus_table(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Cpu))
    cpus = result.scalars().all()  # Perbaikan pada penamaan variabel
    # get cpu percentage
    percentage = cpus[0].percentage
    return f'<div class="progress-bar bg-info" role="progressbar" style="width: {percentage}%" aria-valuenow="{percentage}" aria-valuemin="0" aria-valuemax="100"></div>'
