from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware


#routers 
from .modules.qr_module.routers import qr_router

app = FastAPI()

origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/check-healthy")
def get():
    return "Hi there"


app.include_router(qr_router.router, tags=['QR module'], prefix="/qr")