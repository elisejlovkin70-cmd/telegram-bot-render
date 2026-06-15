# Telegram Bot for Render

Простой асинхронный Telegram-бот на **aiogram 3** + FastAPI, оптимизированный для деплоя на Render.com.

## Как запустить локально

```bash
pip install -r requirements.txt
cp .env.example .env
# Добавь BOT_TOKEN в .env
python bot.py
```

## Деплой на Render

1. Создай **Web Service** → Connect this repo
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `uvicorn bot:app --host 0.0.0.0 --port $PORT`
4. Environment Variables:
   - `BOT_TOKEN` — твой токен от @BotFather
   - `WEBHOOK_URL` — опционально (Render сам даст URL)

Бот поддерживает **webhook** (рекомендуется) и fallback на polling.