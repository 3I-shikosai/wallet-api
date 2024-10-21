from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .router import router
from .services import init_db

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


init_db()

app.include_router(router)
