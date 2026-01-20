from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.src.core.database import get_db_base , get_db , engine
from backend.src.api.v1 import assets , chat

Base = get_db_base()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="THE Ledger API")

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router= assets.router , prefix="/assets", tags=["Assets"])
app.include_router(router=chat.router, prefix="/agent" , tags=["Agent"])


@app.get("/health")
def health_check():
    return {"status" : "It's working broski dw"}

@app.get("/")
def main():
    return {"status" : "up and running twin"}