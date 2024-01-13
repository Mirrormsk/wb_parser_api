from fastapi import FastAPI

from schemas import PhoneSchema

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/login/")
async def login(phone: PhoneSchema):
    return {"message": f"Hello {phone}"}


@app.get("/check/login")
async def check_login(phone: int):
    return {"status": "waiting_qr_login"}
