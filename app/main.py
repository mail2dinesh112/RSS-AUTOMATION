from fastapi import FastAPI
from .database import Base, engine
from .scheduler import start_scheduler, stop_scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RSS Automation Service")

@app.on_event("startup")
def startup_event():
    start_scheduler()

@app.get("/")
def home():
    return {"message": "RSS Automation Service Running"}

@app.on_event("shutdown")
def shutdown_event():
    print("Shutting down RSS Automation Service")
    stop_scheduler()