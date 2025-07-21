# main.py
import asyncio
from create_bot import bot, dp
from handlers.clock_handler import clock_router
from handlers.nouns_handler import nouns_router
from handlers.start import start_router
from handlers.numbers_handler import numbers_router
from handlers.colors_handler import colors_router
from handlers.verbs_handler import verbs_router
from handlers.weather_handler import weather_router
from db.db import init


async def main():
    await init()
    dp.include_router(start_router)
    dp.include_router(numbers_router)
    dp.include_router(colors_router)
    dp.include_router(verbs_router)
    dp.include_router(weather_router)
    dp.include_router(nouns_router)
    dp.include_router(clock_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())