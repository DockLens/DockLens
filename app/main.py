from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers.api import containers, hosts
from app.routers.web import dashboard
from app.config.database import init_db
import dotenv

app = FastAPI()

# Load environment variables
dotenv.load_dotenv()

# Read version.txt file
with open("version.txt", "r") as f:
    version = f.read()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# API routes
@app.get("/api")
async def root():
    return {"message": "DockLens API", "version": version}


app.include_router(containers.router, prefix="/api/containers", tags=["Containers"])
app.include_router(hosts.router, prefix="/api/hosts", tags=["containers"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])


@app.on_event("startup")
async def on_startup():
    await init_db()
