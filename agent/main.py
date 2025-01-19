from fastapi import FastAPI, BackgroundTasks
from .modules.containers import get_containers_info, send_data as send_containers_data
from .modules.hosts import get_cpu_percentage, send_data as send_cpu_data
import time
from .config import INTERVAL
from threading import Thread

app = FastAPI()


# Fungsi background task untuk mengirim data setiap interval
def periodic_task():
    while True:
        containers = get_containers_info()  # Ambil informasi kontainer
        cpu = get_cpu_percentage()  # Ambil persentase CPU
        send_containers_data(containers)
        send_cpu_data(cpu)
        time.sleep(INTERVAL)  # Tunggu sebelum mengirim data lagi


# Endpoint untuk memulai background task pada saat startup
@app.on_event("startup")
async def start_background_task():
    task_thread = Thread(target=periodic_task)
    task_thread.daemon = True  # Menandakan thread ini akan mati bersama aplikasi
    task_thread.start()


@app.get("/")
async def root():
    return {"message": "Docker Monitoring API"}
