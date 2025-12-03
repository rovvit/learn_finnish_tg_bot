from tortoise import Tortoise
from db.models import Noun, User
from db import DB_URL


async def init():
    print("Starting DB init")
    await Tortoise.init(
        db_url=DB_URL,
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

