from fastapi import FastAPI
from .views import router as fastapi_app

app = FastAPI()
app.include_router(fastapi_app)