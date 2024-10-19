from fastapi import FastAPI

from .router import router
from .services import init_db

app = FastAPI()

app.include_router(router)

init_db()
