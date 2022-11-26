from aiogram import Bot, Dispatcher, types
from config  import TOKEN_BOT
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from src.database.db import Database
import logging


bot = Bot(token=TOKEN_BOT)
logging.basicConfig(level=logging.INFO)
dp= Dispatcher(bot, storage=MemoryStorage())
html= types.ParseMode.HTML
db= Database('src/database/database.db')

class Data(StatesGroup):
    Q1 = State()
    date = State()
    time= State()
    remind= State()