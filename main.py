# main.py
import asyncio
from create_bot import bot, dp
from handlers.start import start_router
from handlers.numbers_handler import numbers_router

async def main():
    dp.include_router(start_router)
    dp.include_router(numbers_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())