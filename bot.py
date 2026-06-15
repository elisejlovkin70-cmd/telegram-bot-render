import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from fastapi import FastAPI
from contextlib import asynccontextmanager

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_BASE_URL = os.getenv("WEBHOOK_BASE_URL", "")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# FastAPI app for Render
app = FastAPI()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот, запущенный на Render 🚀")

@dp.message(F.text)
async def echo(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    webhook_url = f"{WEBHOOK_BASE_URL.rstrip('/')}/webhook" if WEBHOOK_BASE_URL else None
    if webhook_url:
        await bot.set_webhook(webhook_url)
        logging.info(f"Webhook set to {webhook_url}")
    else:
        await bot.delete_webhook()
        logging.info("Using polling (fallback)")
    yield
    # On shutdown
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def webhook(request: types.Update):
    await dp.feed_update(bot, request)

if __name__ == "__main__":
    import uvicorn
    logging.basicConfig(level=logging.INFO)
    uvicorn.run("bot:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
