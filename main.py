import os
import random
from sqlite3 import OperationalError

from fastapi import FastAPI
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.responses import FileResponse
from telethon import TelegramClient
from telethon.types import Message

from config import settings
from schemas import PhoneSchema, SendMessageSchema
from services import generate_qr
from users_dao import UsersDao

app = FastAPI()


@app.post("/login/")
async def login(phone: PhoneSchema):
    """Login user by phone number"""
    async with AsyncSession(UsersDao.engine) as session:
        user = await UsersDao.get_user_by_phone_or_create(session, str(phone.phone))

        client = TelegramClient(
            os.path.join("user_sessions", str(phone.phone)),
            settings.API_ID,
            settings.API_HASH,
        )
        try:
            if not client.is_connected():
                await client.connect()
            qr_login = await client.qr_login()

        except OperationalError as ex:
            return {"error": str(ex)}
        finally:
            await client.disconnect()

        qr_id = random.randint(1000, 9999)
        filename = f"media/{qr_id}.png"
        generate_qr(qr_login.url, filename)
        user.status = "waiting_qr_login"
        session.add(user)
        await session.commit()

        return {"qr_link_url": f"{settings.HOST_NAME}/qr/" + str(qr_id)}


@app.get("/check/login/")
async def check_login(phone: int):
    """Check user login status"""
    async with AsyncSession(UsersDao.engine) as session:
        user = await UsersDao.get_user_by_phone(phone)
        if user:
            client = TelegramClient(
                os.path.join("user_sessions", str(phone)),
                settings.API_ID,
                settings.API_HASH,
            )
            if not client.is_connected():
                await client.connect()

            is_authorized = await client.is_user_authorized()
            if not is_authorized:
                status = "waiting_qr_login"
            elif is_authorized:
                status = "logined"
            else:
                status = "error"

            user.status = status
            session.add(user)
            await session.commit()
            client.disconnect()
            return {"status": status}

        return {"error": "User not found"}


@app.get("/qr/{qr_id}/")
async def get_qr(qr_id: int):
    """Returns qr-code as picture"""
    path = f"media/{qr_id}.png"
    return FileResponse(path)


@app.get("/messages/")
async def get_messages(phone: int, uname: str):
    """Get messages of user"""
    async with AsyncSession(UsersDao.engine) as session:
        user = await UsersDao.get_user_by_phone(phone)

        if not user:
            return {"error": "User not found"}

        client = TelegramClient(
            os.path.join("user_sessions", str(phone)),
            settings.API_ID,
            settings.API_HASH,
        )
        if not client.is_connected():
            await client.connect()

        is_authorized = await client.is_user_authorized()

        if not is_authorized:
            return {"error": "User not authorized"}

        messages: list[Message] = await client.get_messages(uname, limit=50)

        messages_data = [{"message_text": message.message} for message in messages]
        client.disconnect()

    return {"messages": messages_data}


@app.post("/messages/")
async def send_message(message_data: SendMessageSchema):
    """Send message to user @username"""

    client = TelegramClient(
        os.path.join("user_sessions", message_data.from_phone),
        settings.API_ID,
        settings.API_HASH,
    )
    if not client.is_connected():
        await client.connect()

    is_authorized = await client.is_user_authorized()

    if not is_authorized:
        return {"error": "User not authorized"}
    try:
        result = await client.send_message(
            message_data.username, message_data.message_text
        )
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "error": str(e)}
    finally:
        client.disconnect()
