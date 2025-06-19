from fastapi import FastAPI
from contextlib import asynccontextmanager

from Routers.loan_predict import router as loan_predict_router
from Routers.price_predict import router as house_predict_router
from database.config import connect_db, disconnect_db  

from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await disconnect_db()

app = FastAPI(lifespan=lifespan)




origins = [
    "http://localhost:3000",
    "http://127.0.0.1:5500",
    # "http://192.168.X.X:3001", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(loan_predict_router)
app.include_router(house_predict_router)

if __name__ == "__main__":
    port = int(8000)  # default to 8000 locally
    uvicorn.run("app:app", host="0.0.0.0", port=port)
