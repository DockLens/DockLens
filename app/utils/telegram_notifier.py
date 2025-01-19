import os
import dotenv
from telegram import Bot

dotenv.load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)


async def send_notification(message: str):
    await bot.send_message(chat_id=CHAT_ID, text=message)
