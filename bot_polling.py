from loader import dp
from aiogram import executor
from aiogram.types import BotCommand
from src.handlers import main
from notification import notify
import asyncio

async def check():
    while True:
        await notify()
        await asyncio.sleep(1)
    

async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        BotCommand("start", "restart bot")
    ])
    asyncio.create_task(check())


executor.start_polling(dp, skip_updates=False, on_startup=set_default_commands)