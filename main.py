import requests
import asyncio
import os
from fake_useragent import UserAgent
from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from bot import router
from aiogram.fsm.strategy import FSMStrategy
from loader import scheduler
from dotenv import load_dotenv

load_dotenv()


async def starts():

    bot = Bot(os.getenv('TOKEN'))
    dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(starts())