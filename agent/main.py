from fastapi import FastAPI, BackgroundTasks
from .modules.containers import get_containers_info, send_data as send_containers_data
from .modules.hosts import get_system_info, send_data as send_host_data
import time
from .config import INTERVAL
from threading import Thread

app = FastAPI()

# read file version.txt
with open("version.txt", "r") as f:
    version = f.read()


def periodic_task():
    while True:
        containers = get_containers_info()
        hosts = get_system_info()
        send_containers_data(containers)
        send_host_data(hosts)
        time.sleep(INTERVAL)


@app.on_event("startup")
async def start_background_task():
    task_thread = Thread(target=periodic_task)
    task_thread.daemon = True
    task_thread.start()


@app.get("/")
async def root():
    return {"message": "Agent Docker Monitoring API", "version": version}
