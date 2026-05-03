from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from db.database import engine, Base
from api.websocket import router as ws_router
from api.rest import router as rest_router
import os

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Real-Time Face Detection")

app.include_router(ws_router)
app.include_router(rest_router, prefix="/api")

# We make sure the static directory exists
os.makedirs("static", exist_ok=True)

# Mount frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def get_root():
    return RedirectResponse(url="/static/index.html")
