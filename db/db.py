from tortoise import Tortoise
from db.models import Noun, User
import os
import dotenv

dotenv.load_dotenv()

POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')

db_url = f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'


async def init():
    print("Starting DB init")
    await Tortoise.init(
        db_url=db_url,
        modules={'models': ['db.models']}
    )
    await Tortoise.generate_schemas()
    print('DB inited')

async def get_nouns():
    return await Noun.all().values()

async def get_or_create_user(telegram_id: int, username: str | None, full_name: str | None) -> User:
    user = await User.get_or_none(telegram_id=telegram_id)
    print(user)
    if user is None:
        user = await User.create(
            telegram_id=telegram_id,
            username=username,
            full_name=full_name,
        )
    print(user)
    return user

